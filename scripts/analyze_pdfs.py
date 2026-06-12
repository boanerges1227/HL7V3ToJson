#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract detailed XML examples from PDF documents and generate comprehensive JSON examples.
"""

import PyPDF2
import re
import json
import os

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text

def extract_xml_sections(text):
    """Extract XML sections from PDF text."""
    xml_sections = []
    
    # Look for XML code blocks
    # Pattern 1: Between ```xml and ```
    pattern1 = r'```xml\s*(.*?)\s*```'
    matches1 = re.findall(pattern1, text, re.DOTALL)
    xml_sections.extend(matches1)
    
    # Pattern 2: Look for HL7-like XML structures
    pattern2 = r'<(?:ClinicalDocument|POOR|QUMT|MCCI|PRPA|POLB|SUBMIT|RETRIEVE).*?>.*?</(?:ClinicalDocument|POOR|QUMT|MCCI|PRPA|POLB|SUBMIT|RETRIEVE)[^>]*>'
    matches2 = re.findall(pattern2, text, re.DOTALL | re.IGNORECASE)
    xml_sections.extend(matches2)
    
    return xml_sections

def find_all_interactions(text):
    """Find all message interaction identifiers."""
    interactions = set()
    
    # Common interaction patterns
    patterns = [
        r'(POOR_IN\d+[A-Z]*\d*)',
        r'(QUMT_IN\d+[A-Z]*\d*)',
        r'(MCCI_IN\d+[A-Z]*\d*)',
        r'(PRPA_IN\d+[A-Z]*\d*)',
        r'(POLB_IN\d+[A-Z]*\d*)',
        r'(SUBMIT_IN\d+[A-Z]*\d*)',
        r'(RETRIEVE_IN\d+[A-Z]*\d*)',
        r'(QUQI_IN\d+[A-Z]*\d*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        interactions.update(matches)
    
    return sorted(interactions)

def extract_service_sections(text):
    """Extract service section headers and content."""
    sections = {}
    
    # Find section headers like "5.2.1 预约申请请求"
    pattern = r'(\d+\.\d+\.\d+)\s+([\u4e00-\u9fa5]+(?:请求|应答|消息))'
    matches = re.finditer(pattern, text)
    
    for match in matches:
        section_num = match.group(1)
        section_name = match.group(2)
        sections[section_name] = section_num
    
    return sections

def main():
    base_dir = "/Users/panzhuang/开发/JHIPV7/trunk-doc"
    
    pdf_files = {
        "part10": os.path.join(base_dir, "医院信息平台交互标准\u2002第10部分预约信息交互服务.pdf"),
        "part11": os.path.join(base_dir, "医院信息平台交互标准\u2002第11部分状态信息交互服务.pdf")
    }
    
    output_info = {}
    
    for part_key, pdf_path in pdf_files.items():
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing: {part_key}")
        print(f"{'='*60}")
        
        text = extract_text_from_pdf(pdf_path)
        
        # Find all interactions
        interactions = find_all_interactions(text)
        print(f"\nAll interactions found: {interactions}")
        
        # Find service sections
        sections = extract_service_sections(text)
        print(f"\nService sections found: {sections}")
        
        # Extract XML sections
        xml_sections = extract_xml_sections(text)
        print(f"\nXML sections found: {len(xml_sections)}")
        
        # Store info
        output_info[part_key] = {
            "interactions": interactions,
            "sections": sections,
            "xml_count": len(xml_sections)
        }
        
        # Print first few XML sections if any
        for i, xml in enumerate(xml_sections[:3]):
            print(f"\nXML Section {i+1} (first 500 chars):")
            print(xml[:500])
            print("...")
    
    # Save analysis results
    analysis_file = os.path.join(base_dir, "scripts", "pdf_analysis.json")
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(output_info, f, ensure_ascii=False, indent=2)
    
    print(f"\n\nAnalysis saved to: {analysis_file}")

if __name__ == "__main__":
    main()
