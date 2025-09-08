#!/usr/bin/env python3
"""
Lab Results Analyzer
Extracts and analyzes lab results from PDF files
"""

import PyPDF2
import os
import re
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def analyze_lab_results(text, filename):
    """Analyze lab results text for key information"""
    analysis = {
        'filename': filename,
        'test_date': None,
        'lab_name': None,
        'test_type': None,
        'results': [],
        'abnormal_values': [],
        'summary': ""
    }
    
    # Extract test date
    date_patterns = [
        r'(\d{1,2}/\d{1,2}/\d{4})',
        r'(\d{4}-\d{2}-\d{2})',
        r'(\w+ \d{1,2},? \d{4})'
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            analysis['test_date'] = match.group(1)
            break
    
    # Extract lab name
    lab_patterns = [
        r'(LabCorp|Quest|LabCorp|Mayo|Cleveland|Stanford)',
        r'(Laboratory|Lab|Medical Center)',
        r'(CLIA|CAP|Accredited)'
    ]
    
    for pattern in lab_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            analysis['lab_name'] = match.group(1)
            break
    
    # Extract test results (looking for common lab result patterns)
    result_patterns = [
        r'([A-Za-z\s]+)\s*([0-9.]+)\s*([A-Za-z/%]+)\s*([0-9.]+)\s*-\s*([0-9.]+)',  # Standard lab result format
        r'([A-Za-z\s]+)\s*([0-9.]+)\s*([A-Za-z/%]+)',  # Simple result format
        r'([A-Za-z\s]+)\s*([0-9.]+)',  # Basic result format
    ]
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if len(line) > 10:  # Skip very short lines
            for pattern in result_patterns:
                match = re.search(pattern, line)
                if match:
                    test_name = match.group(1).strip()
                    if len(test_name) > 2 and len(test_name) < 50:  # Reasonable test name length
                        result = {
                            'test_name': test_name,
                            'value': match.group(2),
                            'unit': match.group(3) if len(match.groups()) > 2 else '',
                            'reference_range': f"{match.group(4)}-{match.group(5)}" if len(match.groups()) > 4 else ''
                        }
                        analysis['results'].append(result)
                        break
    
    # Look for abnormal indicators
    abnormal_indicators = ['HIGH', 'LOW', 'ABNORMAL', 'POSITIVE', 'NEGATIVE', 'CRITICAL']
    for line in lines:
        for indicator in abnormal_indicators:
            if indicator in line.upper():
                analysis['abnormal_values'].append(line.strip())
                break
    
    # Generate summary
    if analysis['results']:
        analysis['summary'] = f"Found {len(analysis['results'])} test results"
        if analysis['abnormal_values']:
            analysis['summary'] += f" with {len(analysis['abnormal_values'])} abnormal indicators"
    else:
        analysis['summary'] = "No structured test results found"
    
    return analysis

def main():
    """Main function to analyze all lab result PDFs"""
    lab_results_dir = Path("domains/health/medical/lab_results")
    pdf_files = list(lab_results_dir.glob("*.pdf"))
    
    print("🔬 Lab Results Analysis Report")
    print("=" * 50)
    print()
    
    if not pdf_files:
        print("No PDF files found in lab results directory")
        return
    
    all_analyses = []
    
    for pdf_file in pdf_files:
        print(f"📄 Analyzing: {pdf_file.name}")
        print("-" * 30)
        
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        
        # Analyze results
        analysis = analyze_lab_results(text, pdf_file.name)
        all_analyses.append(analysis)
        
        # Display analysis
        print(f"Test Date: {analysis['test_date'] or 'Not found'}")
        print(f"Lab Name: {analysis['lab_name'] or 'Not found'}")
        print(f"Results Found: {len(analysis['results'])}")
        print(f"Abnormal Indicators: {len(analysis['abnormal_values'])}")
        print(f"Summary: {analysis['summary']}")
        
        if analysis['results']:
            print("\nSample Results:")
            for i, result in enumerate(analysis['results'][:5]):  # Show first 5 results
                print(f"  {i+1}. {result['test_name']}: {result['value']} {result['unit']}")
            if len(analysis['results']) > 5:
                print(f"  ... and {len(analysis['results']) - 5} more results")
        
        if analysis['abnormal_values']:
            print("\nAbnormal Indicators Found:")
            for abnormal in analysis['abnormal_values'][:3]:  # Show first 3
                print(f"  - {abnormal}")
            if len(analysis['abnormal_values']) > 3:
                print(f"  ... and {len(analysis['abnormal_values']) - 3} more")
        
        print("\n" + "=" * 50 + "\n")
    
    # Overall summary
    print("📊 OVERALL SUMMARY")
    print("=" * 50)
    total_results = sum(len(analysis['results']) for analysis in all_analyses)
    total_abnormal = sum(len(analysis['abnormal_values']) for analysis in all_analyses)
    
    print(f"Total PDFs Analyzed: {len(all_analyses)}")
    print(f"Total Test Results Found: {total_results}")
    print(f"Total Abnormal Indicators: {total_abnormal}")
    print(f"Files with Results: {sum(1 for a in all_analyses if a['results'])}")
    print(f"Files with Abnormal Values: {sum(1 for a in all_analyses if a['abnormal_values'])}")

if __name__ == "__main__":
    main()

