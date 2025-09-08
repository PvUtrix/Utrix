# Development Standards

## Code Quality & Style

### Python Standards
- **PEP 8 compliance**: Follow Python style guidelines
- **Type hints**: Use type annotations for function parameters and return values
- **Docstrings**: Include comprehensive docstrings for all functions and classes
- **Error handling**: Implement proper exception handling with specific error types
- **Logging**: Use structured logging with appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)

### Code Organization
- **Single responsibility**: Each function/class should have one clear purpose
- **DRY principle**: Don't repeat yourself - extract common functionality
- **Meaningful names**: Use descriptive variable and function names
- **Consistent formatting**: Use consistent indentation and spacing
- **Comments**: Explain complex logic and business rules

### File Structure Template
```python
#!/usr/bin/env python3
"""
Module docstring describing the purpose and usage.
"""

import logging
from typing import Dict, List, Optional

# Constants
DEFAULT_CONFIG = "config.yaml"

# Logging setup
logger = logging.getLogger(__name__)

class ExampleClass:
    """Class docstring explaining purpose and usage."""
    
    def __init__(self, config: Dict[str, str]) -> None:
        """Initialize with configuration dictionary."""
        self.config = config
        logger.info("Initialized ExampleClass")
    
    def process_data(self, data: List[str]) -> Optional[Dict[str, int]]:
        """
        Process input data and return results.
        
        Args:
            data: List of strings to process
            
        Returns:
            Dictionary with processed results or None if error
            
        Raises:
            ValueError: If data is empty or invalid
        """
        if not data:
            raise ValueError("Data cannot be empty")
        
        try:
            # Processing logic here
            result = {}
            for item in data:
                result[item] = len(item)
            
            logger.info(f"Processed {len(data)} items")
            return result
            
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return None

def main() -> None:
    """Main entry point for the script."""
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Main logic here
        pass
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise

if __name__ == "__main__":
    main()
```

## Testing Standards

### Unit Testing
- **Test coverage**: Aim for >80% code coverage
- **Test structure**: Use Arrange-Act-Assert pattern
- **Test naming**: Use descriptive test names that explain the scenario
- **Mocking**: Mock external dependencies and APIs
- **Edge cases**: Test boundary conditions and error cases

### Test Organization
```python
import unittest
from unittest.mock import Mock, patch
from your_module import ExampleClass

class TestExampleClass(unittest.TestCase):
    """Test cases for ExampleClass."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = {"key": "value"}
        self.instance = ExampleClass(self.config)
    
    def test_process_data_with_valid_input(self) -> None:
        """Test processing with valid input data."""
        # Arrange
        test_data = ["hello", "world"]
        expected = {"hello": 5, "world": 5}
        
        # Act
        result = self.instance.process_data(test_data)
        
        # Assert
        self.assertEqual(result, expected)
    
    def test_process_data_with_empty_input(self) -> None:
        """Test processing with empty input raises ValueError."""
        # Arrange
        test_data = []
        
        # Act & Assert
        with self.assertRaises(ValueError):
            self.instance.process_data(test_data)
```

## Error Handling & Resilience

### Exception Handling
- **Specific exceptions**: Catch specific exception types, not generic Exception
- **Error logging**: Log errors with context and stack traces
- **Graceful degradation**: Provide fallback behavior when possible
- **User-friendly messages**: Provide clear error messages for users
- **Recovery mechanisms**: Implement retry logic for transient failures

### Retry Patterns
```python
import time
import random
from functools import wraps
from typing import Callable, Type, Tuple

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Decorator for retrying functions with exponential backoff."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise
                    
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    time.sleep(delay)
                    delay = min(delay * 2, max_delay)
                    delay += random.uniform(0, 1)  # Add jitter
            
        return wrapper
    return decorator
```

## Performance Optimization

### Code Performance
- **Efficient algorithms**: Choose appropriate data structures and algorithms
- **Lazy loading**: Load data only when needed
- **Caching**: Implement caching for expensive operations
- **Batch processing**: Process data in batches when possible
- **Memory management**: Be mindful of memory usage and cleanup

## Security Best Practices

### Input Validation
- **Sanitize inputs**: Validate and sanitize all user inputs
- **Type checking**: Use type hints and runtime type checking
- **Length limits**: Implement reasonable limits on input sizes
- **Format validation**: Validate data formats (email, URL, etc.)
- **SQL injection prevention**: Use parameterized queries

### Secure Coding
```python
import re
import html
from typing import Any, Dict

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent XSS."""
    return html.escape(user_input.strip())
```

## Configuration Management

### Environment Variables
- **Use .env files**: Store environment-specific configuration
- **Type conversion**: Convert string env vars to appropriate types
- **Default values**: Provide sensible defaults
- **Validation**: Validate configuration on startup
- **Documentation**: Document all configuration options

### Configuration Patterns
```python
import os
from typing import Optional, Union
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration."""
    database_url: str
    api_key: str
    debug: bool = False
    max_retries: int = 3
    timeout: float = 30.0
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables."""
        return cls(
            database_url=os.getenv('DATABASE_URL', 'sqlite:///default.db'),
            api_key=os.getenv('API_KEY', ''),
            debug=os.getenv('DEBUG', 'false').lower() == 'true',
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            timeout=float(os.getenv('TIMEOUT', '30.0'))
        )
    
    def validate(self) -> None:
        """Validate configuration values."""
        if not self.api_key:
            raise ValueError("API_KEY is required")
        if self.max_retries < 0:
            raise ValueError("MAX_RETRIES must be non-negative")
        if self.timeout <= 0:
            raise ValueError("TIMEOUT must be positive")
```

## Version Control Best Practices

### Git Workflow
- **Meaningful commits**: Write clear, descriptive commit messages
- **Atomic commits**: Each commit should represent a single logical change
- **Branch naming**: Use descriptive branch names (feature/, bugfix/, hotfix/)
- **Pull requests**: Use PRs for code review and discussion
- **Clean history**: Keep commit history clean and organized

### Commit Message Format
```
type(scope): brief description

Detailed explanation of the change, including:
- What was changed and why
- Any breaking changes
- Related issues or tickets

Closes #123
```

Types: feat, fix, docs, style, refactor, test, chore
Scopes: automation, config, docs, scripts, tools, etc.

## Code Review Guidelines

### Review Checklist
- **Functionality**: Does the code work as intended?
- **Code quality**: Is the code clean, readable, and maintainable?
- **Testing**: Are there adequate tests for the changes?
- **Documentation**: Is the code properly documented?
- **Security**: Are there any security vulnerabilities?
- **Performance**: Are there any performance concerns?
- **Standards**: Does the code follow project standards?
