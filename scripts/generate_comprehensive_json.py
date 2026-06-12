#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive JSON examples based on actual XML content from PDFs.
"""

import PyPDF2
import re
import json
import os
from xml.etree import ElementTree as ET

# Common message header fields based on the XML examples
MESSAGE_HEADER = {
    "_description": "消息头信息，所有消息类型的公共部分",
    "id": {
        "_description": "消息流水号，唯一标识本条消息",
        "_cardinality": "1..1",
        "_required": True,
        "_format": "字符串，最大长度50",
        "_example": "22a0f9e0-4454-11dc-a6be-3603d6866807",
        "root": {
            "_description": "固定值，标识ID类型为消息流水号",
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
        "_format": "yyyyMMddHHmmss",
        "_example": "20070803130624"
    },
    "interactionId": {
        "_description": "消息服务标识，标识本消息对应哪个服务接口",
        "_cardinality": "1..1",
        "_required": True,
        "root": {
            "_description": "固定值，标识ID类型为消息服务标识",
            "_value": "2.16.156.10011.2.5.1.2"
        },
        "extension": {
            "_description": "服务标识代码"
        }
    },
    "processingCode": {
        "_description": "处理代码，标识此消息属于哪种系统环境",
        "_cardinality": "1..1",
        "_required": True,
        "_allowedValues": {
            "D": "调试系统（Debug）",
            "P": "产品系统（Production）",
            "T": "训练系统（Training）"
        }
    },
    "processingModeCode": {
        "_description": "处理模式代码"
    },
    "acceptAckCode": {
        "_description": "消息应答控制码，标识接收方是否需要返回应答",
        "_cardinality": "1..1",
        "_required": True,
        "_allowedValues": {
            "AL": "总是返回应答（Always）",
            "ER": "仅在错误时返回应答（Error/reject only）",
            "NE": "从不返回应答（Never）"
        }
    },
    "receiver": {
        "_description": "接收者信息，标识消息的目标系统",
        "_cardinality": "1..1",
        "_required": True,
        "_attributes": {
            "typeCode": "RCV"
        },
        "device": {
            "_description": "接收设备/系统信息",
            "id": {
                "_description": "接收系统标识",
                "item": {
                    "_description": "系统标识信息",
                    "root": {
                        "_description": "固定值，标识ID类型为系统标识",
                        "_value": "2.16.156.10011.2.5.1.3"
                    },
                    "extension": {
                        "_description": "接收系统的唯一标识编码"
                    }
                }
            },
            "telecom": {
                "_description": "接收系统通信地址"
            }
        }
    },
    "sender": {
        "_description": "发送者信息，标识消息的来源系统",
        "_cardinality": "1..1",
        "_required": True,
        "_attributes": {
            "typeCode": "SND"
        },
        "device": {
            "_description": "发送设备/系统信息",
            "id": {
                "_description": "发送系统标识",
                "item": {
                    "_description": "系统标识信息",
                    "root": {
                        "_description": "固定值，标识ID类型为系统标识",
                        "_value": "2.16.156.10011.2.5.1.3"
                    },
                    "extension": {
                        "_description": "发送系统的唯一标识编码"
                    }
                }
            },
            "telecom": {
                "_description": "发送系统通信地址"
            }
        }
    }
}

# Part 10: Appointment Information Interaction Service
PART10_SERVICES = {
    "预约申请请求": {
        "interaction_id": "POOR_IN200910UV",
        "description": "预约申请请求消息，用于向医院信息平台提交预约申请",
        "main_element": "appointment",
        "fields": {
            "_description": "预约申请信息主体",
            "id": {
                "_description": "预约流水号，由申请方生成",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "字符串，最大长度50",
                "_dataElement": "预约流水号",
                "root": {
                    "_value": "2.16.156.10011.1.30"
                },
                "extension": {
                    "_description": "预约流水号的具体值"
                }
            },
            "statusCode": {
                "_description": "预约状态码",
                "_cardinality": "1..1",
                "_required": True,
                "_allowedValues": {
                    "active": "有效",
                    "completed": "已完成",
                    "cancelled": "已取消"
                }
            },
            "effectiveTime": {
                "_description": "预约有效时间",
                "_cardinality": "0..1",
                "_required": False,
                "low": {
                    "_description": "预约开始时间"
                },
                "high": {
                    "_description": "预约结束时间"
                }
            },
            "appointmentReasonCode": {
                "_description": "预约原因编码",
                "_cardinality": "0..1",
                "_required": False,
                "codeSystem": {
                    "_value": "2.16.156.10011.2.3.1.268"
                },
                "displayName": {
                    "_description": "预约原因名称"
                }
            },
            "patient": {
                "_description": "患者信息",
                "_cardinality": "1..1",
                "_required": True,
                "id": {
                    "_description": "患者标识列表",
                    "_cardinality": "1..*",
                    "_required": True,
                    "item": [
                        {
                            "_description": "患者编号（必填）",
                            "root": {"_value": "2.16.156.10011.2.5.1.4"},
                            "extension": {"_description": "患者编号值"}
                        },
                        {
                            "_description": "门（急）诊号",
                            "root": {"_value": "2.16.156.10011.1.10"},
                            "extension": {"_description": "门（急）诊号值"}
                        }
                    ]
                },
                "person": {
                    "_description": "患者个人信息",
                    "name": {
                        "_description": "患者姓名",
                        "_dataElement": "DE02.01.039.01"
                    },
                    "gender": {
                        "_description": "患者性别",
                        "_dataElement": "DE02.01.040.00",
                        "_codeSystem": "2.16.156.10011.2.3.3.4"
                    },
                    "birthTime": {
                        "_description": "患者出生日期",
                        "_dataElement": "DE02.01.005.00",
                        "_format": "yyyyMMdd"
                    }
                },
                "telecom": {
                    "_description": "患者联系电话",
                    "_dataElement": "DE02.01.010.05"
                }
            },
            "service": {
                "_description": "预约服务信息",
                "_cardinality": "1..1",
                "_required": True,
                "code": {
                    "_description": "预约服务类型编码",
                    "codeSystem": {
                        "_value": "2.16.156.10011.2.3.1.268"
                    },
                    "displayName": {
                        "_description": "预约服务类型名称，如：门诊预约、检查预约等"
                    }
                },
                "provider": {
                    "_description": "服务提供方信息",
                    "organization": {
                        "_description": "医疗机构信息",
                        "id": {
                            "_description": "医疗机构编码",
                            "item": {
                                "root": {"_value": "2.16.156.10011.1.19"},
                                "extension": {"_description": "医疗机构编码值"}
                            }
                        },
                        "name": {
                            "_description": "医疗机构名称"
                        }
                    },
                    "serviceLocation": {
                        "_description": "服务地点信息",
                        "id": {
                            "_description": "科室编码",
                            "item": {
                                "root": {"_value": "2.16.156.10011.1.26"},
                                "extension": {"_description": "科室编码值"}
                            }
                        },
                        "name": {
                            "_description": "科室名称"
                        }
                    },
                    "serviceProvider": {
                        "_description": "服务提供者（医生）信息",
                        "id": {
                            "_description": "医生工号",
                            "item": {
                                "root": {"_value": "2.16.156.10011.1.4"},
                                "extension": {"_description": "医生工号值"}
                            }
                        },
                        "person": {
                            "_description": "医生个人信息",
                            "name": {
                                "_description": "医生姓名"
                            }
                        }
                    }
                }
            },
            "slot": {
                "_description": "预约时间段信息",
                "_cardinality": "1..1",
                "_required": True,
                "id": {
                    "_description": "时间段标识"
                },
                "statusCode": {
                    "_description": "时间段状态"
                },
                "effectiveTime": {
                    "_description": "预约时间",
                    "_cardinality": "1..1",
                    "_required": True,
                    "low": {
                        "_description": "预约开始时间"
                    },
                    "high": {
                        "_description": "预约结束时间"
                    }
                }
            },
            "annotation": {
                "_description": "预约备注信息",
                "_cardinality": "0..1",
                "_required": False,
                "text": {
                    "_description": "备注内容"
                }
            }
        }
    },
    "预约申请应答": {
        "interaction_id": "MCCI_IN000002UV01",
        "description": "预约申请应答消息，用于返回预约申请的处理结果",
        "main_element": "acknowledgment",
        "fields": {
            "_description": "应答信息主体",
            "queryAck": {
                "_description": "应答确认信息",
                "_cardinality": "1..1",
                "_required": True,
                "queryId": {
                    "_description": "原请求消息流水号",
                    "root": {"_value": "2.16.156.10011.2.5.1.1"},
                    "extension": {"_description": "原请求消息流水号值"}
                },
                "statusCode": {
                    "_description": "应答状态码",
                    "_allowedValues": {
                        "delivered": "已交付",
                        "processing": "处理中",
                        "error": "错误",
                        "pending": "待处理"
                    }
                },
                "queryNameCode": {
                    "_description": "查询名称代码"
                },
                "resultTotalQuantity": {
                    "_description": "结果总数"
                },
                "resultCurrentQuantity": {
                    "_description": "当前结果数"
                },
                "resultRemainingQuantity": {
                    "_description": "剩余结果数"
                }
            },
            "acknowledgmentDetail": {
                "_description": "应答详情",
                "_cardinality": "0..*",
                "_required": False,
                "typeCode": {
                    "_description": "应答类型代码"
                },
                "targetMessage": {
                    "_description": "目标消息信息"
                },
                "statusCode": {
                    "_description": "状态码"
                },
                "text": {
                    "_description": "应答文本信息"
                }
            }
        }
    },
    "预约查询请求": {
        "interaction_id": "QUMT_IN020050UV01",
        "description": "预约查询请求消息，用于查询预约信息",
        "main_element": "query",
        "fields": {
            "_description": "查询参数信息",
            "queryByParameter": {
                "_description": "查询参数",
                "_cardinality": "1..1",
                "_required": True,
                "statusCode": {
                    "_description": "查询状态",
                    "_fixedValue": "new"
                },
                "parameters": {
                    "_description": "查询条件参数",
                    "appointmentId": {
                        "_description": "预约编号查询条件",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "预约编号",
                            "extension": {"_description": "预约编号值"},
                            "root": {"_value": "2.16.156.10011.1.30"}
                        }
                    },
                    "patientId": {
                        "_description": "患者编号查询条件",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "患者编号",
                            "extension": {"_description": "患者编号值"},
                            "root": {"_value": "2.16.156.10011.2.5.1.4"}
                        }
                    },
                    "serviceDate": {
                        "_description": "预约日期查询条件",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "日期范围",
                            "low": {"_description": "开始日期"},
                            "high": {"_description": "结束日期"}
                        },
                        "semanticsText": {"_description": "预约日期"}
                    },
                    "serviceProviderId": {
                        "_description": "服务提供者编号查询条件",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "服务提供者编号",
                            "extension": {"_description": "服务提供者编号值"},
                            "root": {"_value": "2.16.156.10011.1.4"}
                        }
                    }
                }
            }
        }
    },
    "预约查询应答": {
        "interaction_id": "QUMT_IN020060UV01",
        "description": "预约查询应答消息，用于返回预约查询结果",
        "main_element": "queryResponse",
        "fields": {
            "_description": "查询应答信息主体",
            "queryAck": {
                "_description": "应答确认信息",
                "_cardinality": "1..1",
                "_required": True,
                "queryId": {
                    "_description": "原请求消息流水号",
                    "root": {"_value": "2.16.156.10011.2.5.1.1"},
                    "extension": {"_description": "原请求消息流水号值"}
                },
                "statusCode": {
                    "_description": "应答状态码"
                },
                "resultTotalQuantity": {
                    "_description": "结果总数"
                }
            },
            "appointmentList": {
                "_description": "预约信息列表",
                "_cardinality": "0..*",
                "_required": False,
                "appointment": {
                    "_description": "预约信息",
                    "id": {
                        "_description": "预约流水号"
                    },
                    "statusCode": {
                        "_description": "预约状态"
                    },
                    "effectiveTime": {
                        "_description": "预约时间"
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
            }
        }
    },
    "预约取消请求": {
        "interaction_id": "POOR_IN200911UV",
        "description": "预约取消请求消息，用于取消已有的预约",
        "main_element": "cancelAppointment",
        "fields": {
            "_description": "预约取消信息主体",
            "id": {
                "_description": "预约流水号",
                "_cardinality": "1..1",
                "_required": True,
                "root": {"_value": "2.16.156.10011.1.30"},
                "extension": {"_description": "预约流水号值"}
            },
            "statusCode": {
                "_description": "取消后状态",
                "_fixedValue": "cancelled"
            },
            "cancelReasonCode": {
                "_description": "取消原因编码",
                "_cardinality": "0..1",
                "_required": False,
                "codeSystem": {
                    "_value": "2.16.156.10011.2.3.1.268"
                },
                "displayName": {
                    "_description": "取消原因名称"
                }
            },
            "effectiveTime": {
                "_description": "取消时间"
            },
            "patient": {
                "_description": "患者信息",
                "_cardinality": "1..1",
                "_required": True,
                "id": {
                    "_description": "患者编号",
                    "root": {"_value": "2.16.156.10011.2.5.1.4"},
                    "extension": {"_description": "患者编号值"}
                }
            },
            "annotation": {
                "_description": "取消备注信息",
                "_cardinality": "0..1",
                "_required": False,
                "text": {
                    "_description": "备注内容"
                }
            }
        }
    },
    "预约取消应答": {
        "interaction_id": "MCCI_IN000002UV01",
        "description": "预约取消应答消息，用于返回预约取消的处理结果",
        "main_element": "acknowledgment",
        "fields": {
            "_description": "应答信息主体",
            "queryAck": {
                "_description": "应答确认信息",
                "_cardinality": "1..1",
                "_required": True,
                "queryId": {
                    "_description": "原请求消息流水号"
                },
                "statusCode": {
                    "_description": "应答状态码"
                }
            }
        }
    }
}

# Part 11: Status Information Interaction Service
PART11_SERVICES = {
    "状态更新请求": {
        "interaction_id": "POOR_IN200920UV",
        "description": "状态更新请求消息，用于更新业务对象的状态信息",
        "main_element": "statusUpdate",
        "fields": {
            "_description": "状态更新信息主体",
            "id": {
                "_description": "更新请求流水号",
                "_cardinality": "1..1",
                "_required": True,
                "root": {"_value": "2.16.156.10011.2.5.1.1"},
                "extension": {"_description": "更新请求流水号值"}
            },
            "statusCode": {
                "_description": "目标状态码",
                "_cardinality": "1..1",
                "_required": True
            },
            "target": {
                "_description": "目标对象信息",
                "_cardinality": "1..1",
                "_required": True,
                "id": {
                    "_description": "目标对象标识",
                    "_cardinality": "1..1",
                    "_required": True,
                    "root": {"_description": "目标对象标识类型"},
                    "extension": {"_description": "目标对象标识值"}
                },
                "typeCode": {
                    "_description": "目标对象类型代码"
                }
            },
            "effectiveTime": {
                "_description": "生效时间",
                "_cardinality": "0..1",
                "_required": False
            },
            "actor": {
                "_description": "操作者信息",
                "_cardinality": "0..1",
                "_required": False,
                "id": {
                    "_description": "操作者标识",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.4"},
                        "extension": {"_description": "操作者工号"}
                    }
                },
                "person": {
                    "_description": "操作者个人信息",
                    "name": {
                        "_description": "操作者姓名"
                    }
                }
            },
            "annotation": {
                "_description": "备注信息",
                "_cardinality": "0..1",
                "_required": False,
                "text": {
                    "_description": "备注内容"
                }
            }
        }
    },
    "状态更新应答": {
        "interaction_id": "MCCI_IN000002UV01",
        "description": "状态更新应答消息，用于返回状态更新的处理结果",
        "main_element": "acknowledgment",
        "fields": {
            "_description": "应答信息主体",
            "queryAck": {
                "_description": "应答确认信息",
                "_cardinality": "1..1",
                "_required": True,
                "queryId": {
                    "_description": "原请求消息流水号"
                },
                "statusCode": {
                    "_description": "应答状态码"
                }
            }
        }
    },
    "状态查询请求": {
        "interaction_id": "QUMT_IN020070UV01",
        "description": "状态查询请求消息，用于查询业务对象的状态信息",
        "main_element": "query",
        "fields": {
            "_description": "查询参数信息",
            "queryByParameter": {
                "_description": "查询参数",
                "_cardinality": "1..1",
                "_required": True,
                "statusCode": {
                    "_description": "查询状态",
                    "_fixedValue": "new"
                },
                "parameters": {
                    "_description": "查询条件参数",
                    "targetId": {
                        "_description": "目标对象标识查询条件",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "目标对象标识",
                            "extension": {"_description": "目标对象标识值"}
                        }
                    },
                    "targetType": {
                        "_description": "目标对象类型查询条件",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "目标对象类型代码"
                        }
                    },
                    "statusTime": {
                        "_description": "状态时间查询条件",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "时间范围",
                            "low": {"_description": "开始时间"},
                            "high": {"_description": "结束时间"}
                        },
                        "semanticsText": {"_description": "状态时间"}
                    }
                }
            }
        }
    },
    "状态查询应答": {
        "interaction_id": "QUMT_IN020080UV01",
        "description": "状态查询应答消息，用于返回状态查询结果",
        "main_element": "queryResponse",
        "fields": {
            "_description": "查询应答信息主体",
            "queryAck": {
                "_description": "应答确认信息",
                "_cardinality": "1..1",
                "_required": True,
                "queryId": {
                    "_description": "原请求消息流水号"
                },
                "statusCode": {
                    "_description": "应答状态码"
                },
                "resultTotalQuantity": {
                    "_description": "结果总数"
                }
            },
            "statusList": {
                "_description": "状态信息列表",
                "_cardinality": "0..*",
                "_required": False,
                "statusInfo": {
                    "_description": "状态信息",
                    "id": {
                        "_description": "目标对象标识"
                    },
                    "statusCode": {
                        "_description": "当前状态码"
                    },
                    "effectiveTime": {
                        "_description": "状态生效时间"
                    },
                    "previousStatus": {
                        "_description": "前一状态"
                    },
                    "actor": {
                        "_description": "操作者信息"
                    }
                }
            }
        }
    }
}

def generate_clean_test_data(json_data):
    """Generate clean test data without _description and other metadata."""
    def clean_value(key, value, parent_key=None):
        if key.startswith('_'):
            return None
        
        if isinstance(value, dict):
            cleaned = {}
            for k, v in value.items():
                result = clean_value(k, v, key)
                if result is not None:
                    cleaned[k] = result
            return cleaned if cleaned else {}
        elif isinstance(value, list):
            cleaned_list = []
            for item in value:
                if isinstance(item, dict):
                    cleaned_item = {}
                    for k, v in item.items():
                        result = clean_value(k, v, parent_key)
                        if result is not None:
                            cleaned_item[k] = result
                    cleaned_list.append(cleaned_item)
                else:
                    cleaned_list.append(item)
            return cleaned_list
        else:
            return value
    
    result = {}
    for key, value in json_data.items():
        cleaned = clean_value(key, value)
        if cleaned is not None:
            result[key] = cleaned
    
    return result

def generate_sample_values(json_data, service_name):
    """Generate sample values for test data."""
    def add_sample_values(obj, path=""):
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                if key.startswith('_'):
                    result[key] = value
                    continue
                
                new_path = f"{path}.{key}" if path else key
                
                if isinstance(value, dict):
                    # Add sample values based on field name
                    if key == "extension" and "_description" in value:
                        if "流水号" in value.get("_description", "") or "编号" in value.get("_description", ""):
                            result[key] = "SAMPLE-001"
                        elif "工号" in value.get("_description", ""):
                            result[key] = "DOC001"
                        elif "编码" in value.get("_description", ""):
                            result[key] = "CODE001"
                        else:
                            result[key] = "SAMPLE-VALUE"
                    elif key == "root" and "_value" in value:
                        result[key] = value
                    elif key == "value":
                        result[key] = add_sample_values(value, new_path)
                    else:
                        result[key] = add_sample_values(value, new_path)
                elif isinstance(value, list):
                    result[key] = [add_sample_values(item, new_path) if isinstance(item, dict) else item for item in value]
                else:
                    result[key] = value
            
            return result
        return obj
    
    return add_sample_values(json_data)

def main():
    base_dir = "/Users/panzhuang/开发/JHIPV7/trunk-doc"
    json_examples_dir = os.path.join(base_dir, "json-examples")
    test_data_dir = os.path.join(base_dir, "test-data")
    
    os.makedirs(json_examples_dir, exist_ok=True)
    os.makedirs(test_data_dir, exist_ok=True)
    
    # Generate Part 10 files
    print("\n" + "="*60)
    print("Generating Part 10 - Appointment Information Interaction Service")
    print("="*60)
    
    for service_name, service_info in PART10_SERVICES.items():
        # Create JSON example
        json_example = {
            "messageHeader": MESSAGE_HEADER.copy()
        }
        json_example["messageHeader"]["interactionId"]["extension"]["_fixedValue"] = service_info["interaction_id"]
        json_example["messageHeader"]["interactionId"]["extension"]["_description"] = f"固定值 {service_info['interaction_id']} 表示{service_info['description']}"
        json_example[service_info["main_element"]] = service_info["fields"]
        
        # Save JSON example
        json_file = os.path.join(json_examples_dir, f"第10部分_{service_name}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_example, f, ensure_ascii=False, indent=2)
        print(f"Generated: {json_file}")
        
        # Generate clean test data
        clean_data = generate_clean_test_data(json_example)
        sample_data = generate_sample_values(clean_data, service_name)
        
        test_file = os.path.join(test_data_dir, f"clean_第10部分_{service_name}.json")
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        print(f"Generated: {test_file}")
    
    # Generate Part 11 files
    print("\n" + "="*60)
    print("Generating Part 11 - Status Information Interaction Service")
    print("="*60)
    
    for service_name, service_info in PART11_SERVICES.items():
        # Create JSON example
        json_example = {
            "messageHeader": MESSAGE_HEADER.copy()
        }
        json_example["messageHeader"]["interactionId"]["extension"]["_fixedValue"] = service_info["interaction_id"]
        json_example["messageHeader"]["interactionId"]["extension"]["_description"] = f"固定值 {service_info['interaction_id']} 表示{service_info['description']}"
        json_example[service_info["main_element"]] = service_info["fields"]
        
        # Save JSON example
        json_file = os.path.join(json_examples_dir, f"第11部分_{service_name}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_example, f, ensure_ascii=False, indent=2)
        print(f"Generated: {json_file}")
        
        # Generate clean test data
        clean_data = generate_clean_test_data(json_example)
        sample_data = generate_sample_values(clean_data, service_name)
        
        test_file = os.path.join(test_data_dir, f"clean_第11部分_{service_name}.json")
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
        print(f"Generated: {test_file}")
    
    print("\n" + "="*60)
    print("All files generated successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
