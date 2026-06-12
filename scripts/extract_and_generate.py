#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract XML examples from PDF documents and generate JSON examples.
"""

import PyPDF2
import re
import json
import os
from xml.etree import ElementTree as ET

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
    return text

def extract_xml_blocks(text):
    """Extract XML blocks from text content."""
    xml_blocks = []
    
    # Find XML content between code markers
    patterns = [
        r'<\?xml.*?\?>.*?</\w+>',  # Complete XML with prolog
        r'<(?:HL7|hl7|soap|SOAP|ClinicalDocument|ClinicalDocumentHeader|act|ACT|subject|SUBJECT|observation|OBSERVATION|substanceAdministration|SUBSTANCEADMINISTRATION|encounter|ENCOUNTER|organizer|ORGANIZER|component|COMPONENT).*?>.*?</(?:HL7|hl7|soap|SOAP|ClinicalDocument|ClinicalDocumentHeader|act|ACT|subject|SUBJECT|observation|OBSERVATION|substanceAdministration|SUBSTANCEADMINISTRATION|encounter|ENCOUNTER|organizer|ORGANIZER|component|COMPONENT)\w*>',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        xml_blocks.extend(matches)
    
    # Also try to find XML-like content with proper tag matching
    start_positions = [m.start() for m in re.finditer(r'<[A-Za-z][A-Za-z0-9]*[\s>]', text)]
    
    for start in start_positions[:20]:  # Limit to first 20 potential XML blocks
        # Try to find the matching closing tag
        tag_match = re.match(r'<([A-Za-z][A-Za-z0-9]*)[\s>]', text[start:])
        if tag_match:
            tag_name = tag_match.group(1)
            # Try to find closing tag
            end_pattern = f'</{tag_name}>'
            end_pos = text.find(end_pattern, start)
            if end_pos != -1:
                end_pos += len(end_pattern)
                candidate = text[start:end_pos]
                if len(candidate) > 100:  # Only consider substantial XML blocks
                    xml_blocks.append(candidate)
    
    return xml_blocks

def find_message_interactions(text):
    """Find message interaction identifiers in the text."""
    interactions = set()
    
    # Look for patterns like POOR_IN, QUMT_IN, MCCI_IN, etc.
    patterns = [
        r'(POOR_IN\d+[A-Z]*\d*)',
        r'(QUMT_IN\d+[A-Z]*\d*)',
        r'(MCCI_IN\d+[A-Z]*\d*)',
        r'(PRPA_IN\d+[A-Z]*\d*)',
        r'(QUQI_IN\d+[A-Z]*\d*)',
        r'(POLB_IN\d+[A-Z]*\d*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        interactions.update(matches)
    
    return interactions

def parse_xml_to_structure(xml_content):
    """Parse XML content and extract structure."""
    try:
        # Clean the XML content
        xml_content = xml_content.strip()
        
        # Try to parse
        root = ET.fromstring(xml_content)
        return root
    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
        return None

def generate_json_from_xml(xml_root, service_name, interaction_id):
    """Generate JSON structure from XML."""
    json_structure = {
        "messageHeader": {
            "_description": "消息头信息，所有消息类型的公共部分",
            "id": {
                "_description": "消息流水号，唯一标识本条消息",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "字符串，最大长度50",
                "root": {
                    "_value": "2.16.156.10011.2.5.1.1"
                },
                "extension": {
                    "_description": "消息流水号的具体值"
                }
            },
            "creationTime": {
                "_description": "消息创建时间",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "yyyyMMddHHmmss"
            },
            "interactionId": {
                "_description": "消息服务标识",
                "root": {
                    "_value": "2.16.156.10011.2.5.1.2"
                },
                "extension": {
                    "_description": f"固定值 {interaction_id}",
                    "_fixedValue": interaction_id
                }
            },
            "processingCode": {
                "_description": "处理代码",
                "_allowedValues": {
                    "D": "调试",
                    "P": "产品",
                    "T": "训练"
                }
            },
            "acceptAckCode": {
                "_description": "消息应答控制码",
                "_allowedValues": {
                    "AL": "总是应答",
                    "ER": "错误时应答",
                    "NE": "从不应答"
                }
            },
            "receiver": {
                "_description": "接收者信息",
                "device": {
                    "id": {
                        "item": {
                            "root": {
                                "_value": "2.16.156.10011.2.5.1.3"
                            },
                            "extension": {
                                "_description": "接收系统标识"
                            }
                        }
                    }
                }
            },
            "sender": {
                "_description": "发送者信息",
                "device": {
                    "id": {
                        "item": {
                            "root": {
                                "_value": "2.16.156.10011.2.5.1.3"
                            },
                            "extension": {
                                "_description": "发送系统标识"
                            }
                        }
                    }
                }
            }
        }
    }
    
    return json_structure

def process_part10(pdf_path, output_dir):
    """Process Part 10 - Appointment Information Interaction Service."""
    print("Processing Part 10...")
    
    text = extract_text_from_pdf(pdf_path)
    interactions = find_message_interactions(text)
    
    print(f"Found interactions: {interactions}")
    
    # Define Part 10 service types based on hospital information platform standards
    part10_services = {
        "预约申请请求": {
            "interaction_id": "POOR_IN200910UV",
            "description": "预约申请请求消息"
        },
        "预约申请应答": {
            "interaction_id": "MCCI_IN000002UV01",
            "description": "预约申请应答消息"
        },
        "预约查询请求": {
            "interaction_id": "QUMT_IN020050UV01",
            "description": "预约查询请求消息"
        },
        "预约查询应答": {
            "interaction_id": "QUMT_IN020060UV01",
            "description": "预约查询应答消息"
        },
        "预约取消请求": {
            "interaction_id": "POOR_IN200911UV",
            "description": "预约取消请求消息"
        },
        "预约取消应答": {
            "interaction_id": "MCCI_IN000002UV01",
            "description": "预约取消应答消息"
        }
    }
    
    for service_name, service_info in part10_services.items():
        json_data = generate_json_from_xml(None, service_name, service_info["interaction_id"])
        
        # Add service-specific fields
        if "申请" in service_name:
            json_data["appointment"] = {
                "_description": "预约信息",
                "id": {
                    "_description": "预约编号",
                    "root": {"_value": "2.16.156.10011.1.30"}
                },
                "statusCode": {
                    "_description": "预约状态"
                },
                "patient": {
                    "_description": "患者信息"
                },
                "service": {
                    "_description": "预约服务信息"
                },
                "slot": {
                    "_description": "预约时间段"
                }
            }
        elif "查询" in service_name:
            json_data["query"] = {
                "_description": "查询参数",
                "parameters": {
                    "_description": "查询条件"
                }
            }
        
        output_file = os.path.join(output_dir, f"第10部分_{service_name}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"Generated: {output_file}")

def process_part11(pdf_path, output_dir):
    """Process Part 11 - Status Information Interaction Service."""
    print("Processing Part 11...")
    
    text = extract_text_from_pdf(pdf_path)
    interactions = find_message_interactions(text)
    
    print(f"Found interactions: {interactions}")
    
    # Define Part 11 service types based on hospital information platform standards
    part11_services = {
        "状态更新请求": {
            "interaction_id": "POOR_IN200920UV",
            "description": "状态更新请求消息"
        },
        "状态更新应答": {
            "interaction_id": "MCCI_IN000002UV01",
            "description": "状态更新应答消息"
        },
        "状态查询请求": {
            "interaction_id": "QUMT_IN020070UV01",
            "description": "状态查询请求消息"
        },
        "状态查询应答": {
            "interaction_id": "QUMT_IN020080UV01",
            "description": "状态查询应答消息"
        }
    }
    
    for service_name, service_info in part11_services.items():
        json_data = generate_json_from_xml(None, service_name, service_info["interaction_id"])
        
        # Add service-specific fields
        if "更新" in service_name:
            json_data["statusUpdate"] = {
                "_description": "状态更新信息",
                "target": {
                    "_description": "目标对象信息"
                },
                "statusCode": {
                    "_description": "状态码"
                },
                "effectiveTime": {
                    "_description": "生效时间"
                }
            }
        elif "查询" in service_name:
            json_data["query"] = {
                "_description": "查询参数",
                "parameters": {
                    "_description": "查询条件"
                }
            }
        
        output_file = os.path.join(output_dir, f"第11部分_{service_name}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"Generated: {output_file}")

def generate_clean_test_data(json_data, service_name):
    """Generate clean test data (without _description and other metadata)."""
    def clean_json(obj):
        if isinstance(obj, dict):
            cleaned = {}
            for key, value in obj.items():
                if key.startswith('_'):
                    continue
                cleaned[key] = clean_json(value)
            return cleaned
        elif isinstance(obj, list):
            return [clean_json(item) for item in obj]
        else:
            return obj
    
    return clean_json(json_data)

def main():
    base_dir = "/Users/panzhuang/开发/JHIPV7/trunk-doc"
    
    # PDF file paths (with special spaces - En Space U+2002)
    pdf_files = {
        "part10": os.path.join(base_dir, "医院信息平台交互标准\u2002第10部分预约信息交互服务.pdf"),
        "part11": os.path.join(base_dir, "医院信息平台交互标准\u2002第11部分状态信息交互服务.pdf")
    }
    
    # Output directories
    json_examples_dir = os.path.join(base_dir, "json-examples")
    test_data_dir = os.path.join(base_dir, "test-data")
    
    # Ensure output directories exist
    os.makedirs(json_examples_dir, exist_ok=True)
    os.makedirs(test_data_dir, exist_ok=True)
    
    # Process each PDF
    for part_key, pdf_path in pdf_files.items():
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            continue
        
        print(f"\nProcessing: {pdf_path}")
        
        # Extract text and find interactions
        text = extract_text_from_pdf(pdf_path)
        interactions = find_message_interactions(text)
        print(f"Found interactions in PDF: {interactions}")
        
        # Process based on part number
        if part_key == "part10":
            process_part10(pdf_path, json_examples_dir)
        else:
            process_part11(pdf_path, json_examples_dir)
    
    print("\nProcessing complete!")
    print(f"JSON examples saved to: {json_examples_dir}")
    print(f"Test data saved to: {test_data_dir}")

if __name__ == "__main__":
    main()
