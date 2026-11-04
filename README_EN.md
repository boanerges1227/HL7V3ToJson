# HL7V3ToJson - Hospital Information Platform Interchange Standard (V3)

Converts HL7 V3 messages from XML format into a more concise, user-friendly JSON format based on the **WS/T 846-2024** national health industry standard, facilitating system integration and API testing in hospital information platforms.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Directory Structure](#directory-structure)
- [File Statistics](#file-statistics)
- [Message Type Summary](#message-type-summary)
- [Common Field Description](#common-field-description)
- [OID Identifier Reference](#oid-identifier-reference)
- [Usage Guide](#usage-guide)
- [Version Information](#version-information)

---

## Project Overview

This project converts XML message formats defined in the "Hospital Information Platform Interchange Standard" (WS/T 846-2024) series PDF documents into structured JSON format, providing two categories of data:

- **json-examples/**: JSON examples with field annotations, for understanding and learning message structures
- **json-demo/**: Clean test data, ready for API development and automated testing

Also includes a Java-based JSON/XML conversion tool and Python data generation scripts.

### Standard Documents

> **Note**: The WS/T 846 series consists of 11 parts. Part 1 is the general introduction, and Part 9 (Fee Information Interchange Service) has not yet been published. This project covers the remaining 9 parts.

| Part | Standard No. | Name | Pages |
|------|-------------|------|-------|
| Part 2 | WS/T 846.2-2024 | Personal Information Registration & Query Service | 38 |
| Part 3 | WS/T 846.3-2024 | Healthcare Institution Registration & Query Service | 21 |
| Part 4 | WS/T 846.4-2024 | Healthcare Personnel Registration & Query Service | 24 |
| Part 5 | WS/T 846.5-2024 | Terminology Registration & Query Service | 18 |
| Part 6 | WS/T 846.6-2024 | Document Registration & Query Service | 27 |
| Part 7 | WS/T 846.7-2024 | Visit Information Interchange Service | 128 |
| Part 8 | WS/T 846.8-2024 | Medical Order Interchange Service | 44 |
| Part 10 | WS/T 846.10-2024 | Appointment Interchange Service | 66 |
| Part 11 | WS/T 846.11-2024 | Status Information Interchange Service | 91 |

---

## Prerequisites

### JSON Data Usage

No dependencies required — directly parse JSON files with any HTTP client or programming language.

### Java Converter

| Dependency | Version | Description |
|------------|---------|-------------|
| JDK | 11+ | Compile and run Java programs |
| org.json | 20231013+ | JSON parsing library (only required by `HospitalXmlJsonConverter`) |

> `HospitalConverter` and `SimpleConverter` require no external dependencies, using only JDK built-in libraries.

```bash
# Download org.json dependency (only needed to compile HospitalXmlJsonConverter)
curl -L -o json.jar 'https://repo1.maven.org/maven2/org/json/json/20231013/json-20231013.jar'

# Compile all classes
javac -cp json.jar -d out/ src/main/java/com/hospital/converter/*.java

# Run
java -cp out:json.jar com.hospital.converter.HospitalXmlJsonConverter json2xml input.json output.xml
```

### Python Scripts

| Dependency | Version | Description |
|------------|---------|-------------|
| Python | 3.8+ | Run data generation scripts |

```bash
python3 scripts/generate_test_data.py
```

---

## Directory Structure

```
HL7V3ToJson/
├── README.md                              # Project documentation (Chinese)
├── README_EN.md                           # Project documentation (English)
│
├── json-examples/                         # JSON example files (with field descriptions)
│   ├── README.md                          # Directory description
│   ├── 字段说明.md                        # Complete field description document
│   ├── 第2部分_个人信息/                   # Personal Info Service (10 files)
│   │   ├── 注册请求.json
│   │   ├── 注册应答成功.json
│   │   ├── 注册应答异常.json
│   │   ├── 更新请求.json
│   │   ├── 查询请求.json
│   │   ├── 查询应答成功.json
│   │   ├── 查询应答异常.json
│   │   ├── 合并请求.json
│   │   ├── 字段说明.json
│   │   └── 字段说明.md
│   ├── 第3部分_医疗机构/                   # Healthcare Institution Service (8 files)
│   │   ├── 注册请求.json
│   │   ├── 更新请求.json
│   │   ├── 查询请求.json
│   │   ├── 查询应答.json
│   │   ├── 通用应答.json
│   │   ├── 字段说明.json
│   │   ├── 字段说明.md
│   │   └── schema.json
│   ├── 第4部分_医护人员/                   # Healthcare Personnel Service (7 files)
│   │   ├── 注册请求.json
│   │   ├── 更新请求.json
│   │   ├── 查询请求.json
│   │   ├── 查询应答.json
│   │   ├── 通用应答.json
│   │   ├── 字段说明.json
│   │   └── 字段说明.md
│   ├── 第5部分_术语/                       # Terminology Service (7 files)
│   │   ├── 注册请求.json
│   │   ├── 更新请求.json
│   │   ├── 查询请求.json
│   │   ├── 查询应答.json
│   │   ├── 通用应答.json
│   │   ├── 字段说明.json
│   │   └── 字段说明.md
│   ├── 第6部分_文档/                       # Document Service (6 files)
│   │   ├── 注册请求.json
│   │   ├── 查询请求.json
│   │   ├── 查询应答.json
│   │   ├── 通用应答.json
│   │   ├── 字段说明.json
│   │   └── 字段说明.md
│   ├── 第7部分_就诊信息/                   # Visit Information Service (22 files)
│   │   ├── 就诊卡新增请求.json
│   │   ├── 就诊卡更新请求.json
│   │   ├── 就诊卡查询请求.json
│   │   ├── 就诊卡查询应答.json
│   │   ├── 门诊挂号新增请求.json
│   │   ├── 门诊挂号更新请求.json
│   │   ├── 门诊挂号查询请求.json
│   │   ├── 门诊挂号查询应答.json
│   │   ├── 住院登记请求.json
│   │   ├── 住院更新请求.json
│   │   ├── 住院查询请求.json
│   │   ├── 住院查询应答.json
│   │   ├── 住院转科新增请求.json
│   │   ├── 住院转科更新请求.json
│   │   ├── 住院转科查询请求.json
│   │   ├── 住院转科查询应答.json
│   │   ├── 出院登记新增请求.json
│   │   ├── 出院登记更新请求.json
│   │   ├── 出院信息查询请求.json
│   │   ├── 出院信息查询应答.json
│   │   ├── 字段说明.json
│   │   └── 字段说明.md
│   ├── 第8部分_医嘱/                       # Medical Order Service (7 files)
│   │   ├── 开立请求.json
│   │   ├── 查询请求.json
│   │   ├── 查询应答.json
│   │   ├── 通用应答.json
│   │   ├── 字段说明.json
│   │   ├── 字段说明.md
│   │   └── schema.json
│   ├── 第10部分_预约/                      # Appointment Service (8 files)
│   │   ├── 申请请求.json
│   │   ├── 申请应答.json
│   │   ├── 取消请求.json
│   │   ├── 取消应答.json
│   │   ├── 查询请求.json
│   │   ├── 查询应答.json
│   │   ├── 字段说明.json
│   │   └── 字段说明.md
│   └── 第11部分_状态/                      # Status Service (6 files)
│       ├── 更新请求.json
│       ├── 更新应答.json
│       ├── 查询请求.json
│       ├── 查询应答.json
│       ├── 字段说明.json
│       └── 字段说明.md
│
├── json-demo/                             # Clean test data (for API testing)
│   ├── README.md
│   ├── 字段说明.md
│   ├── 第2部分_个人信息/                   # 8 JSON files
│   ├── 第3部分_医疗机构/                   # 5 JSON files
│   ├── 第4部分_医护人员/                   # 5 JSON files
│   ├── 第5部分_术语/                       # 5 JSON files
│   ├── 第6部分_文档/                       # 4 JSON files
│   ├── 第7部分_就诊信息/                   # 20 JSON files
│   ├── 第8部分_医嘱/                       # 4 JSON files
│   ├── 第10部分_预约/                      # 6 JSON files
│   └── 第11部分_状态/                      # 4 JSON files
│
├── java-converter/                        # Java JSON/XML conversion tool
│   ├── README.md
│   ├── converter.sh
│   └── src/main/java/com/hospital/converter/
│       ├── HospitalConverter.java         # Basic converter (no external deps)
│       ├── SimpleConverter.java           # Simplified converter
│       └── HospitalXmlJsonConverter.java  # Full converter (requires org.json)
│
└── scripts/                               # Utility scripts
    ├── xml_to_json.py                     # XML to JSON script
    ├── generate_test_data.py              # Test data generator
    ├── fill_values.py                     # Field value filler
    ├── generate_comprehensive_json.py     # Comprehensive JSON generator
    ├── generate_part7_json.py             # Part 7 dedicated generator
    ├── extract_and_generate.py            # PDF extraction & generation
    ├── analyze_pdfs.py                    # PDF analyzer
    └── add_sample_values.py               # Sample value filler
```

---

## File Statistics

| Directory | JSON Files | MD Files | Description |
|-----------|-----------|----------|-------------|
| json-examples/ | 72 | 11 | JSON examples with field descriptions |
| json-demo/ | 61 | 11 | Clean test data |
| **Total** | **133** | **22** | |

---

## Message Type Summary

### Part 2: Personal Information Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Personal Info Registration | PRPA_IN201311UV02 | New patient info registration |
| Personal Info Update | PRPA_IN201314UV02 | Patient info update |
| Personal Info Query | PRPA_IN201305UV02 | Patient info query |
| Personal Info Merge | PRPA_IN201304UV02 | Duplicate record merge |

### Part 3: Healthcare Institution Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Institution Registration | PRPM_IN401030UV01 | New institution info registration |
| Institution Update | PRPM_IN403010UV01 | Institution info update |
| Institution Query | PRPM_IN406010UV01 | Institution info query |

### Part 4: Healthcare Personnel Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Personnel Registration | PRPM_IN301010UV01 | New personnel info registration |
| Personnel Update | PRPM_IN303010UV01 | Personnel info update |
| Personnel Query | PRPM_IN306010UV01 | Personnel info query |

### Part 5: Terminology Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Terminology Registration | PRVS_IN000001UV01 | New terminology registration |
| Terminology Update | PRVS_IN000002UV01 | Terminology info update |
| Terminology Query | PRVS_IN000003UV01 | Terminology info query |

### Part 6: Document Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Document Registration | RCMR_IN000002UV02 | Medical document registration |
| Document Query | RCMR_IN000031UV01 | Medical document query |

### Part 7: Visit Information Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Visit Card Info Add | PRPA_IN201311UV02 | Visit card info registration |
| Visit Card Info Update | PRPA_IN201314UV02 | Visit card info update |
| Visit Card Info Query | PRPA_IN201305UV02 | Visit card info query |
| Outpatient Registration Add | PRPA_IN400001UV | Outpatient registration |
| Outpatient Registration Update | PRPA_IN400002UV | Outpatient registration update |
| Outpatient Registration Query | PRPA_IN900300UV | Outpatient registration query |
| Inpatient Visit Registration | PRPA_IN400001UV | Inpatient admission registration |
| Inpatient Visit Update | PRPA_IN400002UV | Inpatient info update |
| Inpatient Visit Query | PRPA_IN900300UV | Inpatient info query |
| Inpatient Transfer Add | PRPA_IN302011UV | Inpatient transfer registration |
| Inpatient Transfer Update | PRPA_IN302012UV | Inpatient transfer update |
| Inpatient Transfer Query | PRPA_IN900300UV | Inpatient transfer query |
| Discharge Registration Add | PRPA_IN400003UV01 | Discharge registration |
| Discharge Registration Update | PRPA_IN400002UV | Discharge info update |
| Discharge Registration Query | PRPA_IN900300UV | Discharge info query |

### Part 8: Medical Order Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Order Create | POOR_IN200901UV | Order info creation |
| Order Update | POOR_IN200902UV | Order info update |
| Order Query | QUMT_IN020030UV01 | Order info query |

### Part 10: Appointment Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Appointment Request | POOR_IN200910UV | Appointment registration request |
| Appointment Cancel | POOR_IN200911UV | Appointment cancellation |
| Appointment Query | QUMT_IN020050UV01 | Appointment info query |

### Part 11: Status Service

| Service | Interaction ID | Description |
|---------|---------------|-------------|
| Status Update | POOR_IN200920UV | Business status update |
| Status Query | QUMT_IN020070UV01 | Business status query |

---

## Common Field Description

### Message Header (messageHeader)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id.root | string | Yes | Fixed value: 2.16.156.10011.2.5.1.1 |
| id.extension | string | Yes | Message serial number |
| creationTime | datetime | Yes | Format: yyyyMMddHHmmss |
| interactionId.extension | string | Yes | Service code identifier |
| processingCode | string | Yes | D-Debug / P-Production / T-Training |
| acceptAckCode | string | Yes | AL-Always / ER-Error only / NE-Never |

### Acknowledgement (acknowledgement)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| typeCode | string | Yes | AA-Success / AE-Failure / AR-Reject |
| targetMessage.id.extension | string | Yes | Request message serial number |
| acknowledgementDetail.text | string | Yes | Processing result description |

---

## OID Identifier Reference

| OID | Description |
|-----|-------------|
| 2.16.156.10011.2.5.1.1 | Message serial number |
| 2.16.156.10011.2.5.1.2 | Message service identifier |
| 2.16.156.10011.2.5.1.3 | System identifier |
| 2.16.156.10011.2.5.1.4 | Patient number |
| 2.16.156.10011.1.3 | ID card number |
| 2.16.156.10011.1.4 | Healthcare personnel ID |
| 2.16.156.10011.1.5 | Hospital code |
| 2.16.156.10011.1.10 | Outpatient/Emergency visit number |
| 2.16.156.10011.1.12 | Inpatient number |
| 2.16.156.10011.1.19 | Resident health card number |
| 2.16.156.10011.1.26 | Department code |
| 2.16.156.10011.1.27 | Ward code |
| 2.16.156.10011.1.28 | Medical order code |

---

## Usage Guide

### 1. View JSON Examples

```bash
# View medical order create request example (with field descriptions)
cat json-examples/第8部分_医嘱/开立请求.json

# View clean test data
cat json-demo/第8部分_医嘱/开立请求.json
```

### 2. API Testing with Test Data

```bash
# Test API with curl
curl -X POST http://your-api/order/create \
  -H "Content-Type: application/json" \
  -d @json-demo/第8部分_医嘱/开立请求.json
```

### 3. Using Java Converter

```bash
cd java-converter/src/main/java

# Compile (no external dependencies required)
javac com/hospital/converter/HospitalConverter.java

# JSON to XML
java com.hospital.converter.HospitalConverter json2xml input.json output.xml

# XML to JSON
java com.hospital.converter.HospitalConverter xml2json input.xml output.json
```

### 4. Using Python Scripts

```bash
# Generate test data
python3 scripts/generate_test_data.py
```

---

## Version Information

- **Standard Version**: WS/T 846-2024
- **Release Date**: 2024-10-28
- **Effective Date**: 2025-04-01
- **Project Status**: Completed