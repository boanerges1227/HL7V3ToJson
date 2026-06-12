#!/usr/bin/env python3
"""
从文档版JSON生成纯净测试版JSON
去除所有 _ 开头的说明字段，保留实际数据结构
"""

import json
import os


def clean_json(obj):
    """递归去除所有 _ 开头的字段"""
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items() if not k.startswith('_')}
    elif isinstance(obj, list):
        return [clean_json(item) for item in obj]
    else:
        return obj


def generate_test_data():
    """生成带有示例数据的测试JSON"""
    
    # 医嘱开立请求 - 完整测试数据
    order_create_request = {
        "messageHeader": {
            "id": {
                "root": "2.16.156.10011.2.5.1.1",
                "extension": "TEST-ORDER-001"
            },
            "creationTime": "20241010110000",
            "interactionId": {
                "root": "2.16.156.10011.2.5.1.2",
                "extension": "POOR_IN200901UV"
            },
            "processingCode": "P",
            "acceptAckCode": "AL",
            "receiver": {
                "device": {
                    "id": {
                        "item": {
                            "root": "2.16.156.10011.2.5.1.3",
                            "extension": "SYS-HIS-001"
                        }
                    }
                }
            },
            "sender": {
                "device": {
                    "id": {
                        "item": {
                            "root": "2.16.156.10011.2.5.1.3",
                            "extension": "SYS-EMR-001"
                        }
                    }
                }
            }
        },
        "order": {
            "author": {
                "time": "20241010100303",
                "signatureCode": "S",
                "signatureText": "张三",
                "assignedEntity": {
                    "id": {
                        "item": {
                            "root": "2.16.156.10011.1.4",
                            "extension": "DOC001"
                        }
                    },
                    "person": {
                        "name": ["张三"]
                    },
                    "organization": {
                        "id": {
                            "item": {
                                "root": "2.16.156.10011.1.26",
                                "extension": "DEPT-001"
                            }
                        },
                        "name": ["心内科"]
                    }
                }
            },
            "verifier": {
                "time": "20241010100500",
                "signatureCode": "S",
                "signatureText": "李四",
                "assignedEntity": {
                    "id": {
                        "item": {
                            "root": "2.16.156.10011.1.4",
                            "extension": "DOC002"
                        }
                    },
                    "person": {
                        "name": ["李四"]
                    }
                }
            },
            "components": [
                {
                    "sequenceNumber": "1",
                    "substanceAdministration": {
                        "id": {
                            "item": {
                                "root": "2.16.156.10011.1.28",
                                "extension": "ORD-20241010-001"
                            }
                        },
                        "code": {
                            "codeSystem": "2.16.156.10011.2.3.1.268",
                            "codeSystemName": "医嘱项目类型代码表",
                            "displayName": "药品类医嘱"
                        },
                        "text": "阿莫西林胶囊 0.5g*24粒",
                        "statusCode": "active",
                        "effectiveTime": {
                            "validTimeLow": "20241010100000",
                            "validTimeHigh": "20241017100000",
                            "code": {
                                "codeSystem": "2.16.156.10011.2.5.1.13",
                                "codeSystemName": "药物使用频次代码表",
                                "code": "tid",
                                "displayName": "每日三次"
                            }
                        },
                        "routeCode": {
                            "codeSystem": "2.16.156.10011.2.3.1.158",
                            "codeSystemName": "用药途径代码表",
                            "displayName": "口服"
                        },
                        "doseQuantity": {
                            "value": "0.5",
                            "unit": "g"
                        },
                        "doseCheckQuantity": [
                            {
                                "numerator": {"value": "1.5", "unit": "g"},
                                "denominator": {"value": "1", "unit": "d"}
                            }
                        ],
                        "administrationUnitCode": {
                            "codeSystem": "2.16.156.10011.2.3.1.211",
                            "codeSystemName": "药物剂型代码表",
                            "displayName": "胶囊剂"
                        },
                        "consumable2": {
                            "manufacturedProduct1": {
                                "id": {"extension": "PKG-001"},
                                "manufacturedProduct": {
                                    "code": {
                                        "code": "AMX-001",
                                        "codeSystem": "2.16.156.10011.2.5.1.14"
                                    },
                                    "name": ["阿莫西林胶囊"],
                                    "asContent": {
                                        "containerPackagedProduct": {
                                            "capacityQuantity": {"value": "0.5", "unit": "g/粒"}
                                        }
                                    }
                                },
                                "subjectOf3": {
                                    "policy": {
                                        "code": {
                                            "code": "01",
                                            "displayName": "甲类"
                                        }
                                    }
                                }
                            }
                        },
                        "location": {
                            "serviceDeliveryLocation": {
                                "location": {
                                    "id": {
                                        "item": {
                                            "root": "2.16.156.10011.1.26",
                                            "extension": "PHARMACY-001"
                                        }
                                    },
                                    "name": ["门诊药房"]
                                }
                            }
                        },
                        "pertinentInformation": {
                            "observation": {
                                "value": {
                                    "code": "2",
                                    "codeSystem": "2.16.156.10011.2.3.2.58",
                                    "displayName": "临时医嘱"
                                }
                            }
                        },
                        "component2": {
                            "supplyRequest": {
                                "statusCode": "active",
                                "quantity": {"value": "24", "unit": "粒"}
                            }
                        },
                        "subjectOf6": {
                            "annotation": {
                                "text": "饭后服用，如有不适及时就诊"
                            }
                        }
                    }
                }
            ],
            "encounter": {
                "id": [
                    {"extension": "1", "root": "2.16.156.10011.2.5.1.8"},
                    {"extension": "ENC-20241010-001", "root": "2.16.156.10011.2.5.1.9"}
                ],
                "code": {
                    "codeSystem": "2.16.156.10011.2.3.1.271",
                    "code": "01",
                    "displayName": "门诊"
                },
                "statusCode": "active",
                "subject": {
                    "patient": {
                        "id": [
                            {"root": "2.16.156.10011.2.5.1.4", "extension": "PAT-2024001"},
                            {"root": "2.16.156.10011.1.10", "extension": "M20241010001"}
                        ],
                        "telecom": {"item": {"value": "13800138000"}},
                        "statusCode": "active",
                        "patientPerson": {
                            "id": [
                                {"root": "2.16.156.10011.1.3", "extension": "110101199001011234"}
                            ],
                            "name": {"item": {"part": {"value": "王五"}}},
                            "administrativeGenderCode": {
                                "codeSystem": "2.16.156.10011.2.3.3.4",
                                "code": "M",
                                "displayName": "男性"
                            },
                            "birthTime": {"value": "19900101"},
                            "asOtherIDs": {
                                "id": [
                                    {"root": "2.16.156.10011.1.19", "extension": "HC-2024001"}
                                ]
                            }
                        }
                    }
                },
                "location": {
                    "serviceDeliveryLocation": {
                        "location": {
                            "id": {
                                "item": {"root": "2.16.156.10011.1.26", "extension": "DEPT-001"}
                            },
                            "name": {"item": {"part": {"value": "心内科"}}},
                            "serviceProviderOrganization": {
                                "asOrganizationPartOf": {
                                    "wholeOrganization": {
                                        "id": {"item": {"root": "2.16.156.10011.1.27", "extension": "WARD-001"}},
                                        "name": {"item": {"part": {"value": "心血管病区"}}}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    # 通用应答 - 成功
    ack_success = {
        "messageHeader": {
            "id": {
                "root": "2.16.156.10011.2.5.1.1",
                "extension": "TEST-ACK-001"
            },
            "creationTime": "20241010110030",
            "interactionId": {
                "root": "2.16.156.10011.2.5.1.2",
                "extension": "MCCI_IN000002UV01"
            },
            "processingCode": "P",
            "acceptAckCode": "AL",
            "receiver": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-EMR-001"}}
                }
            },
            "sender": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-HIS-001"}}
                }
            }
        },
        "acknowledgement": {
            "typeCode": "AA",
            "targetMessage": {
                "id": {
                    "root": "2.16.156.10011.2.5.1.1",
                    "extension": "TEST-ORDER-001"
                }
            },
            "acknowledgementDetail": {
                "text": "医嘱新增成功"
            }
        }
    }
    
    # 通用应答 - 失败
    ack_fail = {
        "messageHeader": {
            "id": {
                "root": "2.16.156.10011.2.5.1.1",
                "extension": "TEST-ACK-002"
            },
            "creationTime": "20241010110030",
            "interactionId": {
                "root": "2.16.156.10011.2.5.1.2",
                "extension": "MCCI_IN000002UV01"
            },
            "processingCode": "P",
            "acceptAckCode": "AL",
            "receiver": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-EMR-001"}}
                }
            },
            "sender": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-HIS-001"}}
                }
            }
        },
        "acknowledgement": {
            "typeCode": "AE",
            "targetMessage": {
                "id": {
                    "root": "2.16.156.10011.2.5.1.1",
                    "extension": "TEST-ORDER-001"
                }
            },
            "acknowledgementDetail": {
                "text": "医嘱新增失败：患者编号不存在"
            }
        }
    }
    
    # 查询请求
    query_request = {
        "messageHeader": {
            "id": {
                "root": "2.16.156.10011.2.5.1.1",
                "extension": "TEST-QUERY-001"
            },
            "creationTime": "20241010111000",
            "interactionId": {
                "root": "2.16.156.10011.2.5.1.2",
                "extension": "QUMT_IN020030UV01"
            },
            "processingCode": "P",
            "acceptAckCode": "AL",
            "receiver": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-HIS-001"}}
                }
            },
            "sender": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-EMR-001"}}
                }
            }
        },
        "queryByParameter": {
            "statusCode": {"code": "new"},
            "queryByParameterPayload": {
                "statusCode": {"code": "new"},
                "actId": {
                    "value": [
                        {"extension": "ORD-20241010-001", "root": "2.16.156.10011.1.28"}
                    ]
                },
                "patientId": {
                    "value": [
                        {"extension": "PAT-2024001", "root": "2.16.156.10011.2.5.1.4"}
                    ]
                }
            }
        }
    }
    
    # 查询应答
    query_response = {
        "messageHeader": {
            "id": {
                "root": "2.16.156.10011.2.5.1.1",
                "extension": "TEST-QUERY-ACK-001"
            },
            "creationTime": "20241010111001",
            "interactionId": {
                "root": "2.16.156.10011.2.5.1.2",
                "extension": "QUMT_IN020040UV01"
            },
            "processingCode": "P",
            "processingModeCode": {"code": "I"},
            "acceptAckCode": "AL",
            "receiver": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-EMR-001"}}
                }
            },
            "sender": {
                "device": {
                    "id": {"item": {"root": "2.16.156.10011.2.5.1.3", "extension": "SYS-HIS-001"}}
                }
            }
        },
        "acknowledgement": {
            "typeCode": "AA",
            "targetMessage": {
                "id": {
                    "root": "2.16.156.10011.2.5.1.1",
                    "extension": "TEST-QUERY-001"
                }
            },
            "acknowledgementDetail": {
                "text": "查询成功"
            }
        },
        "queryAck": {
            "queryId": {"extension": "TEST-QUERY-001"},
            "queryResponseCode": {"code": "OK"},
            "resultTotalQuantity": {"value": "1"}
        },
        "controlActProcess": {
            "subject": {
                "placerGroup": {
                    "author": {
                        "time": {"value": "20241010100303"},
                        "signatureCode": {"code": "S"},
                        "signatureText": {"value": "张三"},
                        "assignedEntity": {
                            "id": {"item": {"root": "2.16.156.10011.1.4", "extension": "DOC001"}},
                            "assignedPerson": {
                                "name": {"item": {"part": {"value": "张三"}}}
                            }
                        }
                    },
                    "component2": {
                        "sequenceNumber": {"value": "1"},
                        "substanceAdministrationRequest": {
                            "id": {"root": "2.16.156.10011.1.28", "extension": "ORD-20241010-001"},
                            "code": {"displayName": {"value": "药品类医嘱"}},
                            "text": {"value": "阿莫西林胶囊 0.5g*24粒"},
                            "statusCode": {"code": "active"},
                            "routeCode": {"displayName": {"value": "口服"}},
                            "doseQuantity": {"value": "0.5", "unit": "g"}
                        }
                    },
                    "componentOf1": {
                        "encounter": {
                            "id": {"item": {"extension": "ENC-20241010-001", "root": "2.16.156.10011.2.5.1.9"}},
                            "subject": {
                                "patient": {
                                    "id": {"item": {"root": "2.16.156.10011.2.5.1.4", "extension": "PAT-2024001"}},
                                    "patientPerson": {
                                        "name": {"item": {"part": {"value": "王五"}}}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    return {
        "order_create_request": order_create_request,
        "ack_success": ack_success,
        "ack_fail": ack_fail,
        "query_request": query_request,
        "query_response": query_response
    }


def main():
    # 创建测试版目录
    test_dir = "test-data"
    os.makedirs(test_dir, exist_ok=True)
    
    # 生成测试数据
    test_data = generate_test_data()
    
    # 写入测试数据文件
    for name, data in test_data.items():
        filepath = os.path.join(test_dir, f"{name}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ 生成: {filepath}")
    
    # 同时生成从文档版去除说明字段的纯净版
    doc_files = [
        "医嘱开立请求_POOR_IN200901UV.json",
        "医嘱应答_MCCI_IN000002UV01.json",
        "医嘱查询请求_QUMT_IN020030UV01.json",
        "医嘱查询应答_QUMT_IN020040UV01.json"
    ]
    
    doc_dir = "json-examples"
    print("\n从文档版生成纯净版:")
    for filename in doc_files:
        src = os.path.join(doc_dir, filename)
        if os.path.exists(src):
            with open(src, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cleaned = clean_json(data)
            dst = os.path.join(test_dir, f"clean_{filename}")
            with open(dst, 'w', encoding='utf-8') as f:
                json.dump(cleaned, f, ensure_ascii=False, indent=2)
            print(f"✓ 生成: {dst}")
    
    print(f"\n测试数据已生成到 {test_dir}/ 目录")


if __name__ == '__main__':
    main()
