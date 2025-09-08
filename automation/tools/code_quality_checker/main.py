#!/usr/bin/env python3
"""
Code Quality Checker
Comprehensive tool for checking and improving code quality across the personal system.
"""

import os
import ast
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeQualityChecker:
    """Check and improve code quality across the system."""
    
    def __init__(self, config_path: str = "automation/tools/code_quality_checker/code_quality_config.yaml"):
        """Initialize the code quality checker."""
        self.config_path = config_path
        self.config = self._load_config()
        self.issues = {
            'missing_type_hints': [],
            'missing_docstrings': [],
            'missing_logging': [],
            'generic_exceptions': [],
            'missing_error_handling': []
        }
    
    def _load_config(self) -> Dict:
        """Load quality check configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            return self._get_default_config()
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'type_hints': {
                'required': True,
                'exclude_patterns': ['test_', '__init__']
            },
            'docstrings': {
                'required': True,
                'exclude_patterns': ['test_']
            },
            'logging': {
                'required': True,
                'exclude_patterns': ['test_']
            },
            'error_handling': {
                'required': True,
                'exclude_generic_exceptions': True
            }
        }
    
    def check_file(self, file_path: Path) -> Dict[str, List]:
        """Check a single Python file for quality issues."""
        file_issues = {
            'missing_type_hints': [],
            'missing_docstrings': [],
            'missing_logging': [],
            'generic_exceptions': [],
            'missing_error_handling': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Check for type hints
            if self.config.get('type_hints', {}).get('required', True):
                file_issues['missing_type_hints'] = self._check_type_hints(tree, file_path)
            
            # Check for docstrings
            if self.config.get('docstrings', {}).get('required', True):
                file_issues['missing_docstrings'] = self._check_docstrings(tree, file_path)
            
            # Check for logging
            if self.config.get('logging', {}).get('required', True):
                file_issues['missing_logging'] = self._check_logging(content, file_path)
            
            # Check error handling
            if self.config.get('error_handling', {}).get('required', True):
                file_issues['generic_exceptions'] = self._check_generic_exceptions(tree, file_path)
                file_issues['missing_error_handling'] = self._check_error_handling(tree, file_path)
            
        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")
        
        return file_issues
    
    def _check_type_hints(self, tree: ast.AST, file_path: Path) -> List[str]:
        """Check for missing type hints in functions."""
        issues = []
        exclude_patterns = self.config.get('type_hints', {}).get('exclude_patterns', [])
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Skip excluded patterns
                if any(pattern in node.name for pattern in exclude_patterns):
                    continue
                
                # Check if function has return type annotation
                if node.returns is None and not node.name.startswith('_'):
                    issues.append(f"Function '{node.name}' missing return type hint")
                
                # Check if parameters have type hints
                for arg in node.args.args:
                    if arg.annotation is None and not arg.arg.startswith('_'):
                        issues.append(f"Parameter '{arg.arg}' in function '{node.name}' missing type hint")
        
        return issues
    
    def _check_docstrings(self, tree: ast.AST, file_path: Path) -> List[str]:
        """Check for missing docstrings."""
        issues = []
        exclude_patterns = self.config.get('docstrings', {}).get('exclude_patterns', [])
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # Skip excluded patterns
                if any(pattern in node.name for pattern in exclude_patterns):
                    continue
                
                # Check if function/class has docstring
                if not ast.get_docstring(node) and not node.name.startswith('_'):
                    issues.append(f"{type(node).__name__} '{node.name}' missing docstring")
        
        return issues
    
    def _check_logging(self, content: str, file_path: Path) -> List[str]:
        """Check for proper logging usage."""
        issues = []
        exclude_patterns = self.config.get('logging', {}).get('exclude_patterns', [])
        
        # Skip excluded patterns
        if any(pattern in file_path.name for pattern in exclude_patterns):
            return issues
        
        # Check if file imports logging
        if 'import logging' not in content and 'from logging' not in content:
            issues.append("File missing logging import")
        
        # Check if file has logger setup
        if 'logger = logging.getLogger' not in content and 'logging.getLogger' not in content:
            issues.append("File missing logger setup")
        
        return issues
    
    def _check_generic_exceptions(self, tree: ast.AST, file_path: Path) -> List[str]:
        """Check for generic exception handling."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None or (isinstance(node.type, ast.Name) and node.type.id == 'Exception'):
                    issues.append(f"Generic exception handling at line {node.lineno}")
        
        return issues
    
    def _check_error_handling(self, tree: ast.AST, file_path: Path) -> List[str]:
        """Check for missing error handling in critical functions."""
        issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if function has try-except blocks
                has_try_except = any(isinstance(child, ast.Try) for child in ast.walk(node))
                
                # Check if function makes external calls that might need error handling
                has_external_calls = any(
                    isinstance(child, ast.Call) and 
                    isinstance(child.func, ast.Attribute) and
                    child.func.attr in ['open', 'request', 'get', 'post', 'put', 'delete']
                    for child in ast.walk(node)
                )
                
                if has_external_calls and not has_try_except and not node.name.startswith('_'):
                    issues.append(f"Function '{node.name}' makes external calls without error handling")
        
        return issues
    
    def check_directory(self, directory: Path) -> Dict[str, List]:
        """Check all Python files in a directory."""
        all_issues = {
            'missing_type_hints': [],
            'missing_docstrings': [],
            'missing_logging': [],
            'generic_exceptions': [],
            'missing_error_handling': []
        }
        
        for py_file in directory.rglob("*.py"):
            if py_file.name.startswith('.') or '__pycache__' in str(py_file):
                continue
            
            file_issues = self.check_file(py_file)
            for issue_type, issues in file_issues.items():
                for issue in issues:
                    all_issues[issue_type].append(f"{py_file}: {issue}")
        
        return all_issues
    
    def generate_report(self, issues: Dict[str, List]) -> str:
        """Generate a quality report."""
        report = ["# Code Quality Report\n"]
        
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        report.append(f"**Total Issues Found: {total_issues}**\n")
        
        for issue_type, issue_list in issues.items():
            if issue_list:
                report.append(f"## {issue_type.replace('_', ' ').title()}")
                report.append(f"**Count: {len(issue_list)}**\n")
                for issue in issue_list:
                    report.append(f"- {issue}")
                report.append("")
        
        return "\n".join(report)
    
    def save_report(self, report: str, output_path: str = "automation/outputs/code_quality_report.md"):
        """Save the quality report."""
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            f.write(report)
        
        logger.info(f"Quality report saved to {output_path}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Check code quality across the system")
    parser.add_argument("--path", default="automation/", help="Path to check")
    parser.add_argument("--check-all", action="store_true", help="Check all Python files")
    parser.add_argument("--check-type-hints", action="store_true", help="Check type hints only")
    parser.add_argument("--check-docstrings", action="store_true", help="Check docstrings only")
    parser.add_argument("--check-logging", action="store_true", help="Check logging only")
    parser.add_argument("--fix", action="store_true", help="Attempt to fix common issues")
    parser.add_argument("--output", default="automation/outputs/code_quality_report.md", help="Output file path")
    
    args = parser.parse_args()
    
    checker = CodeQualityChecker()
    
    if args.check_all:
        path = Path(".")
    else:
        path = Path(args.path)
    
    if not path.exists():
        logger.error(f"Path does not exist: {path}")
        return
    
    logger.info(f"Checking code quality in: {path}")
    
    if path.is_file():
        issues = checker.check_file(path)
    else:
        issues = checker.check_directory(path)
    
    report = checker.generate_report(issues)
    checker.save_report(report, args.output)
    
    # Print summary
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    logger.info(f"Quality check complete. Found {total_issues} issues.")
    
    if total_issues > 0:
        logger.info("See the report for details on how to fix issues.")

if __name__ == "__main__":
    main()
