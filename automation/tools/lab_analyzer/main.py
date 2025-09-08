#!/usr/bin/env python3
"""
Advanced Lab Results Analyzer
Better PDF text extraction and analysis for lab results
"""

import PyPDF2
import re
from pathlib import Path
from datetime import datetime

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file with better error handling"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"--- PAGE {page_num + 1} ---\n{page_text}\n"
            return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def clean_text(text):
    """Clean and normalize extracted text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove page markers
    text = re.sub(r'--- PAGE \d+ ---', '', text)
    # Normalize line breaks
    text = text.replace('\n', ' ').replace('\r', ' ')
    return text.strip()

def extract_dates(text):
    """Extract various date formats from text"""
    date_patterns = [
        (r'(\d{1,2}/\d{1,2}/\d{4})', '%m/%d/%Y'),
        (r'(\d{4}-\d{2}-\d{2})', '%Y-%m-%d'),
        (r'(\d{1,2}-\d{1,2}-\d{4})', '%m-%d-%Y'),
        (r'(\w+ \d{1,2},? \d{4})', '%B %d, %Y'),
        (r'(\d{1,2}\.\d{1,2}\.\d{4})', '%d.%m.%Y'),
    ]
    
    dates = []
    for pattern, date_format in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                if date_format == '%B %d, %Y':
                    # Handle month names
                    parsed_date = datetime.strptime(match, date_format)
                else:
                    parsed_date = datetime.strptime(match, date_format)
                dates.append((match, parsed_date))
            except ValueError:
                continue
    
    # Return the most recent date if multiple found
    if dates:
        dates.sort(key=lambda x: x[1], reverse=True)
        return dates[0][0]
    return None

def extract_lab_info(text):
    """Extract laboratory information"""
    lab_patterns = [
        r'(LabCorp|Quest Diagnostics|Mayo Clinic|Cleveland Clinic|Stanford Health)',
        r'(Gemotest|Gemotest\.ru)',
        r'(Cobas|Roche)',
        r'(CLIA|CAP|Accredited|Laboratory|Lab)',
        r'(www\.gemotest\.ru)',
    ]
    
    for pattern in lab_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def extract_test_results(text):
    """Extract test results with better pattern matching"""
    # Split into lines and clean
    lines = [line.strip() for line in text.split(' ') if line.strip()]
    
    results = []
    current_result = {}
    
    # Look for test result patterns
    for i, line in enumerate(lines):
        # Skip very short lines
        if len(line) < 3:
            continue
            
        # Look for test names (usually longer text)
        if len(line) > 5 and not re.match(r'^\d+\.?\d*$', line):
            # Check if next few lines contain values
            test_name = line
            value = None
            unit = None
            
            # Look ahead for values
            for j in range(i+1, min(i+5, len(lines))):
                next_line = lines[j]
                # Check if it's a number
                if re.match(r'^\d+\.?\d*$', next_line):
                    value = next_line
                    # Look for units
                    if j+1 < len(lines):
                        potential_unit = lines[j+1]
                        if re.match(r'^[A-Za-z/%]+$', potential_unit):
                            unit = potential_unit
                    break
            
            if value:
                result = {
                    'test_name': test_name,
                    'value': value,
                    'unit': unit or '',
                    'status': 'Normal'  # Default status
                }
                results.append(result)
    
    return results

def analyze_pdf_content(pdf_path):
    """Comprehensive analysis of a single PDF"""
    print(f"\n🔍 Detailed Analysis: {pdf_path.name}")
    print("=" * 60)
    
    # Extract text
    raw_text = extract_text_from_pdf(pdf_path)
    if raw_text.startswith("Error"):
        print(f"❌ {raw_text}")
        return None
    
    # Clean text
    cleaned_text = clean_text(raw_text)
    
    # Extract information
    test_date = extract_dates(cleaned_text)
    lab_name = extract_lab_info(cleaned_text)
    test_results = extract_test_results(cleaned_text)
    
    # Display results
    print(f"📅 Test Date: {test_date or 'Not detected'}")
    print(f"🏥 Laboratory: {lab_name or 'Not detected'}")
    print(f"🔬 Test Results Found: {len(test_results)}")
    
    if test_results:
        print("\n📊 Test Results:")
        for i, result in enumerate(test_results, 1):
            status_icon = "✅" if result['status'] == 'Normal' else "⚠️"
            print(f"  {i}. {status_icon} {result['test_name']}: {result['value']} {result['unit']}")
    
    # Look for specific test types
    test_types = []
    if 'HIV' in cleaned_text.upper():
        test_types.append('HIV Testing')
    if 'HERPES' in cleaned_text.upper():
        test_types.append('Herpes Simplex Virus Testing')
    if 'COBAS' in cleaned_text.upper():
        test_types.append('Roche Cobas Testing')
    if 'GEMOTEST' in cleaned_text.upper():
        test_types.append('Gemotest Laboratory')
    
    if test_types:
        print(f"\n🧪 Test Types Detected: {', '.join(test_types)}")
    
    # Look for any abnormal indicators
    abnormal_indicators = ['HIGH', 'LOW', 'ABNORMAL', 'POSITIVE', 'NEGATIVE', 'CRITICAL', 'ELEVATED', 'DECREASED']
    abnormal_found = []
    for indicator in abnormal_indicators:
        if indicator in cleaned_text.upper():
            abnormal_found.append(indicator)
    
    if abnormal_found:
        print(f"\n⚠️ Abnormal Indicators: {', '.join(abnormal_found)}")
    else:
        print("\n✅ No abnormal indicators detected")
    
    return {
        'date': test_date,
        'lab': lab_name,
        'results': test_results,
        'test_types': test_types,
        'abnormal': abnormal_found
    }

def main():
    """Main analysis function"""
    print("🔬 ADVANCED LAB RESULTS ANALYSIS")
    print("=" * 60)
    
    lab_results_dir = Path("domains/health/medical/lab_results")
    pdf_files = list(lab_results_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in lab results directory")
        return
    
    print(f"📁 Found {len(pdf_files)} lab result PDFs")
    print()
    
    all_analyses = []
    
    for pdf_file in pdf_files:
        analysis = analyze_pdf_content(pdf_file)
        if analysis:
            all_analyses.append(analysis)
    
    # Generate comprehensive summary
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE SUMMARY")
    print("=" * 60)
    
    total_results = sum(len(a['results']) for a in all_analyses if a['results'])
    total_abnormal = sum(len(a['abnormal']) for a in all_analyses if a['abnormal'])
    
    print(f"📄 Total PDFs Analyzed: {len(all_analyses)}")
    print(f"🔬 Total Test Results: {total_results}")
    print(f"⚠️ Total Abnormal Indicators: {total_abnormal}")
    
    # Date range
    dates = [a['date'] for a in all_analyses if a['date']]
    if dates:
        print(f"📅 Date Range: {min(dates)} to {max(dates)}")
    
    # Lab information
    labs = [a['lab'] for a in all_analyses if a['lab']]
    if labs:
        unique_labs = list(set(labs))
        print(f"🏥 Laboratories: {', '.join(unique_labs)}")
    
    # Test types
    all_test_types = []
    for a in all_analyses:
        all_test_types.extend(a['test_types'])
    if all_test_types:
        unique_test_types = list(set(all_test_types))
        print(f"🧪 Test Categories: {', '.join(unique_test_types)}")
    
    print("\n💡 Recommendations:")
    if total_abnormal > 0:
        print("  • Review abnormal results with healthcare provider")
        print("  • Consider follow-up testing if recommended")
    else:
        print("  • All results appear within normal ranges")
        print("  • Continue regular health monitoring")
    
    print("  • Store results in appropriate health tracking systems")
    print("  • Schedule follow-up appointments as needed")

if __name__ == "__main__":
    main()

