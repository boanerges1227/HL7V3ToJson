#!/usr/bin/env python3
"""
Generate JSON examples from Part 7 (就诊信息交互服务) PDF document.
Extracts XML examples and converts to JSON format matching existing patterns.
"""

import re
import json
import os
import uuid
from datetime import datetime

# Service mapping: section_id -> (service_name, message_type, service_code)
SECTION_MAPPING = {
    'A.1.1': ('就诊卡信息新增请求', 'PRPA_IN201311UV02', 'EncounterCardInfoAdd'),
    'A.1.2': ('就诊卡信息新增应答_成功', 'MCCI_IN000002UV01', 'EncounterCardInfoAdd'),
    'A.1.3': ('就诊卡信息新增应答_异常', 'MCCI_IN000002UV01', 'EncounterCardInfoAdd'),
    'A.2.1': ('就诊卡信息更新请求', 'PRPA_IN201314UV02', 'EncounterCardInfoUpdate'),
    'A.2.2': ('就诊卡信息更新应答_成功', 'MCCI_IN000002UV01', 'EncounterCardInfoUpdate'),
    'A.2.3': ('就诊卡信息更新应答_异常', 'MCCI_IN000002UV01', 'EncounterCardInfoUpdate'),
    'A.3.1': ('就诊卡信息查询请求', 'PRPA_IN201305UV02', 'EncounterCardInfoQuery'),
    'A.3.2': ('就诊卡信息查询应答_成功', 'PRPA_IN201306UV02', 'EncounterCardInfoQuery'),
    'A.3.3': ('就诊卡信息查询应答_异常', 'PRPA_IN201306UV02', 'EncounterCardInfoQuery'),
    'A.4.1': ('门诊挂号信息新增请求', 'PRPA_IN400001UV', 'OutpatientRegistrationAdd'),
    'A.4.2': ('门诊挂号信息新增应答_成功', 'MCCI_IN000002UV01', 'OutpatientRegistrationAdd'),
    'A.4.3': ('门诊挂号信息新增应答_异常', 'MCCI_IN000002UV01', 'OutpatientRegistrationAdd'),
    'A.5.1': ('门诊挂号信息更新请求', 'PRPA_IN400002UV', 'OutpatientRegistrationUpdate'),
    'A.5.2': ('门诊挂号信息更新应答_成功', 'MCCI_IN000002UV01', 'OutpatientRegistrationUpdate'),
    'A.5.3': ('门诊挂号信息更新应答_异常', 'MCCI_IN000002UV01', 'OutpatientRegistrationUpdate'),
    'A.6.1': ('门诊挂号信息查询请求', 'PRPA_IN900300UV', 'OutpatientRegistrationQuery'),
    'A.6.2': ('门诊挂号信息查询应答_成功', 'PRPA_IN900350UV', 'OutpatientRegistrationQuery'),
    'A.6.3': ('门诊挂号信息查询应答_异常', 'PRPA_IN900350UV', 'OutpatientRegistrationQuery'),
    'A.7.1': ('住院就诊信息登记请求', 'PRPA_IN400001UV', 'InpatientEncounterRegister'),
    'A.7.2': ('住院就诊信息登记应答_成功', 'MCCI_IN000002UV01', 'InpatientEncounterRegister'),
    'A.7.3': ('住院就诊信息登记应答_异常', 'MCCI_IN000002UV01', 'InpatientEncounterRegister'),
    'A.8.1': ('住院就诊信息更新请求', 'PRPA_IN400002UV', 'InpatientEncounterUpdate'),
    'A.8.2': ('住院就诊信息更新应答_成功', 'MCCI_IN000002UV01', 'InpatientEncounterUpdate'),
    'A.8.3': ('住院就诊信息更新应答_异常', 'MCCI_IN000002UV01', 'InpatientEncounterUpdate'),
    'A.9.1': ('住院就诊信息查询请求', 'PRPA_IN900300UV', 'InpatientEncounterQuery'),
    'A.9.2': ('住院就诊信息查询应答_成功', 'PRPA_IN900350UV', 'InpatientEncounterQuery'),
    'A.9.3': ('住院就诊信息查询应答_异常', 'PRPA_IN900350UV', 'InpatientEncounterQuery'),
    'A.10.1': ('住院转科信息新增请求', 'PRPA_IN302011UV', 'InpatientTransferAdd'),
    'A.10.2': ('住院转科信息新增应答_成功', 'MCCI_IN000002UV01', 'InpatientTransferAdd'),
    'A.10.3': ('住院转科信息新增应答_异常', 'MCCI_IN000002UV01', 'InpatientTransferAdd'),
    'A.11.1': ('住院转科信息更新请求', 'PRPA_IN302012UV', 'InpatientTransferUpdate'),
    'A.11.2': ('住院转科信息更新应答_成功', 'MCCI_IN000002UV01', 'InpatientTransferUpdate'),
    'A.11.3': ('住院转科信息更新应答_异常', 'MCCI_IN000002UV01', 'InpatientTransferUpdate'),
    'A.12.1': ('住院转科信息查询请求', 'PRPA_IN900300UV', 'InpatientTransferQuery'),
    'A.12.2': ('住院转科信息查询应答_成功', 'PRPA_IN900350UV', 'InpatientTransferQuery'),
    'A.12.3': ('住院转科信息查询应答_异常', 'PRPA_IN900350UV', 'InpatientTransferQuery'),
    'A.13.1': ('出院登记信息新增请求', 'PRPA_IN400003UV01', 'DischargeRegisterAdd'),
    'A.13.2': ('出院登记信息新增应答_成功', 'MCCI_IN000002UV01', 'DischargeRegisterAdd'),
    'A.13.3': ('出院登记信息新增应答_异常', 'MCCI_IN000002UV01', 'DischargeRegisterAdd'),
    'A.14.1': ('出院登记信息更新请求', 'PRPA_IN400002UV', 'DischargeRegisterUpdate'),
    'A.14.2': ('出院登记信息更新应答_成功', 'MCCI_IN000002UV01', 'DischargeRegisterUpdate'),
    'A.14.3': ('出院登记信息更新应答_异常', 'MCCI_IN000002UV01', 'DischargeRegisterUpdate'),
    'A.15.1': ('出院信息查询请求', 'PRPA_IN900300UV', 'DischargeQuery'),
    'A.15.2': ('出院信息查询应答_成功', 'PRPA_IN900350UV', 'DischargeQuery'),
    'A.15.3': ('出院信息查询应答_异常', 'PRPA_IN900350UV', 'DischargeQuery'),
}

# Common message header fields with descriptions
MESSAGE_HEADER_TEMPLATE = {
    "_description": "消息头信息，所有消息类型的公共部分",
    "id": {
        "_description": "消息流水号，唯一标识本条消息",
        "_cardinality": "1..1",
        "_required": True,
        "_format": "字符串，最大长度50",
        "_dataElement": "消息流水号",
        "root": {
            "_description": "固定值，标识ID类型为消息流水号",
            "_value": "2.16.156.10011.2.5.1.1"
        },
        "extension": {
            "_description": "消息流水号的具体值，由发送方生成的唯一标识",
            "_example": "22a0f9e0-4454-11dc-a6be-3603d6866807"
        }
    },
    "creationTime": {
        "_description": "消息创建时间，标识消息何时生成",
        "_cardinality": "1..1",
        "_required": True,
        "_format": "日期时间格式，yyyyMMddHHmmss（DT15）",
        "_example": "20241010110000"
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
            "_description": "服务标识代码",
            "_allowedValues": [
                "PRPA_IN201311UV02 - 就诊卡信息新增请求",
                "PRPA_IN201314UV02 - 就诊卡信息更新请求",
                "PRPA_IN201305UV02 - 就诊卡信息查询请求",
                "PRPA_IN201306UV02 - 就诊卡信息查询应答",
                "PRPA_IN400001UV - 门诊挂号/住院就诊信息新增请求",
                "PRPA_IN400002UV - 门诊挂号/住院就诊信息更新请求",
                "PRPA_IN400003UV01 - 出院登记信息新增请求",
                "PRPA_IN900300UV - 信息查询请求",
                "PRPA_IN900350UV - 信息查询应答",
                "PRPA_IN302011UV - 住院转科信息新增请求",
                "PRPA_IN302012UV - 住院转科信息更新请求",
                "MCCI_IN000002UV01 - 通用应答消息"
            ]
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
            }
        }
    },
    "sender": {
        "_description": "发送者信息，标识消息的来源系统",
        "_cardinality": "1..1",
        "_required": True,
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
            }
        }
    }
}


def extract_xml_blocks(text):
    """Extract XML blocks from the PDF text."""
    appendix_start = text.find('附录A')
    if appendix_start == -1:
        appendix_start = 0
    appendix_text = text[appendix_start:]
    
    # Find all section markers
    section_pattern = r'A\.(\d+)\.(\d+)\s+([^\n]+)'
    sections = [(m.start(), m.group(0)) for m in re.finditer(section_pattern, appendix_text)]
    
    xml_blocks = []
    for i, (start_pos, section_header) in enumerate(sections):
        # Get section ID
        section_match = re.match(r'A\.(\d+)\.(\d+)', section_header)
        if not section_match:
            continue
        section_id = f"A.{section_match.group(1)}.{section_match.group(2)}"
        
        # Get content until next section
        if i + 1 < len(sections):
            end_pos = sections[i + 1][0]
        else:
            end_pos = len(appendix_text)
        
        section_content = appendix_text[start_pos:end_pos]
        
        # Find XML content
        xml_match = re.search(r'<(PRPA_[^>\s]+|MCCI_[^>\s]+)', section_content)
        if xml_match:
            msg_type = xml_match.group(1)
            # Get the XML content (simplified - just the structure)
            xml_blocks.append({
                'section_id': section_id,
                'section_name': section_header.split(section_id)[-1].strip().lstrip(':： '),
                'message_type': msg_type,
                'content': section_content
            })
    
    return xml_blocks


def generate_encounter_card_add_json():
    """Generate JSON for 就诊卡信息新增请求 (PRPA_IN201311UV02)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "encounterCard": {
            "_description": "就诊卡信息主体，包含就诊卡的完整内容",
            "patient": {
                "_description": "患者信息，包含就诊卡持有者的详细信息",
                "id": {
                    "_description": "就诊卡标识",
                    "_cardinality": "1..1",
                    "_required": True,
                    "_format": "字符串，最大长度50",
                    "item": {
                        "_description": "就诊卡标识信息",
                        "root": {
                            "_description": "固定值，标识ID类型为就诊卡标识",
                            "_value": "2.16.156.10011.2.5.1.6"
                        },
                        "extension": {
                            "_description": "就诊卡标识的具体值",
                            "_example": "就诊卡ID"
                        }
                    }
                },
                "statusCode": {
                    "_description": "就诊卡状态",
                    "_cardinality": "1..1",
                    "_required": True,
                    "_allowedValues": {
                        "active": "激活",
                        "disable": "作废",
                        "retired": "退卡"
                    }
                },
                "effectiveTime": {
                    "_description": "建卡日期时间",
                    "_cardinality": "1..1",
                    "_required": True,
                    "_format": "日期时间格式，yyyyMMddHHmmss（DT15）",
                    "low": {
                        "_description": "建卡开始时间",
                        "_example": "20241010110000"
                    }
                },
                "patientPerson": {
                    "_description": "患者个人信息",
                    "id": {
                        "_description": "身份证件号码",
                        "_cardinality": "1..1",
                        "_required": True,
                        "_dataElement": "DE02.01.030.00",
                        "item": {
                            "_description": "身份证件标识",
                            "root": {
                                "_description": "固定值，标识ID类型为身份证件号码",
                                "_value": "2.16.156.10011.1.3"
                            },
                            "extension": {
                                "_description": "身份证件号码的具体值",
                                "_example": "120109197706015516"
                            }
                        }
                    },
                    "name": {
                        "_description": "患者姓名",
                        "_cardinality": "1..1",
                        "_required": True,
                        "_dataElement": "DE02.01.039.00",
                        "item": {
                            "_description": "姓名信息",
                            "part": {
                                "_description": "姓名部分",
                                "_example": "刘永好"
                            }
                        }
                    },
                    "telecom": {
                        "_description": "患者联系电话号码",
                        "_cardinality": "0..1",
                        "_required": False,
                        "_dataElement": "DE02.01.010.00",
                        "item": {
                            "_description": "联系电话",
                            "_example": "028-2222444"
                        }
                    },
                    "administrativeGenderCode": {
                        "_description": "患者性别信息",
                        "_cardinality": "1..1",
                        "_required": True,
                        "_dataElement": "DE02.01.040.00",
                        "codeSystem": {
                            "_description": "固定值，性别代码表",
                            "_value": "2.16.156.10011.2.3.3.4"
                        },
                        "codeSystemName": {
                            "_description": "固定值，性别代码表名称",
                            "_value": "生理性别代码表(GB/T2261.1)"
                        },
                        "code": {
                            "_description": "性别代码",
                            "_allowedValues": {
                                "1": "男性",
                                "2": "女性",
                                "9": "未说明的性别",
                                "0": "未知的性别"
                            }
                        },
                        "displayName": {
                            "_description": "性别名称",
                            "_example": "男性"
                        }
                    },
                    "birthTime": {
                        "_description": "患者出生日期",
                        "_cardinality": "0..1",
                        "_required": False,
                        "_dataElement": "DE02.01.005.00",
                        "_format": "日期格式，yyyyMMdd",
                        "_example": "19570323"
                    },
                    "addr": {
                        "_description": "患者联系地址",
                        "_cardinality": "0..1",
                        "_required": False,
                        "item": {
                            "_description": "地址信息",
                            "part": [
                                {
                                    "_description": "非结构化地址（完整地址描述）",
                                    "type": {"_value": "SAL"},
                                    "value": {"_description": "完整地址", "_example": "四川省成都市双流县红沙村"}
                                },
                                {
                                    "_description": "地址-省（自治区、直辖市）",
                                    "type": {"_value": "STA"},
                                    "value": {"_description": "省份", "_dataElement": "DE02.01.091.00"}
                                },
                                {
                                    "_description": "地址-市（地区）",
                                    "type": {"_value": "CTY"},
                                    "value": {"_description": "城市", "_dataElement": "DE02.01.092.00"}
                                },
                                {
                                    "_description": "地址-县（区）",
                                    "type": {"_value": "CNT"},
                                    "value": {"_description": "区县", "_dataElement": "DE02.01.093.00"}
                                },
                                {
                                    "_description": "地址-乡（镇、街道办事处）",
                                    "type": {"_value": "STB"},
                                    "value": {"_description": "乡镇", "_dataElement": "DE02.01.094.00"}
                                },
                                {
                                    "_description": "地址-村（街、路、弄等）",
                                    "type": {"_value": "STR"},
                                    "value": {"_description": "街道", "_dataElement": "DE02.01.095.00"}
                                },
                                {
                                    "_description": "地址-门牌号码",
                                    "type": {"_value": "BNR"},
                                    "value": {"_description": "门牌号", "_dataElement": "DE02.01.096.00"}
                                },
                                {
                                    "_description": "邮政编码",
                                    "type": {"_value": "ZIP"},
                                    "value": {"_description": "邮编", "_dataElement": "DE02.01.047.00"}
                                }
                            ]
                        }
                    },
                    "maritalStatusCode": {
                        "_description": "婚姻状况信息",
                        "_cardinality": "0..1",
                        "_required": False,
                        "_dataElement": "DE02.01.018.00",
                        "codeSystem": {
                            "_description": "固定值，婚姻状况代码表",
                            "_value": "2.16.156.10011.2.3.3.5"
                        },
                        "codeSystemName": {
                            "_description": "固定值，婚姻状况代码表名称",
                            "_value": "婚姻状况代码表(GB/T2261.2)"
                        },
                        "code": {
                            "_description": "婚姻状况代码",
                            "_allowedValues": {
                                "10": "未婚",
                                "20": "已婚",
                                "21": "初婚",
                                "22": "再婚",
                                "23": "复婚",
                                "30": "丧偶",
                                "40": "离婚",
                                "90": "其他"
                            }
                        },
                        "displayName": {
                            "_description": "婚姻状况名称",
                            "_example": "未婚"
                        }
                    },
                    "ethnicGroupCode": {
                        "_description": "民族信息",
                        "_cardinality": "0..1",
                        "_required": False,
                        "_dataElement": "DE02.01.025.00",
                        "item": {
                            "_description": "民族信息",
                            "codeSystem": {
                                "_description": "固定值，民族代码表",
                                "_value": "2.16.156.10011.2.3.3.3"
                            },
                            "codeSystemName": {
                                "_description": "固定值，民族代码表名称",
                                "_value": "民族类别代码表(GB3304)"
                            },
                            "code": {
                                "_description": "民族代码",
                                "_example": "01"
                            },
                            "displayName": {
                                "_description": "民族名称",
                                "_example": "汉族"
                            }
                        }
                    },
                    "asEmployee": {
                        "_description": "职业信息",
                        "_cardinality": "0..1",
                        "_required": False,
                        "occupationCode": {
                            "_description": "职业类别代码",
                            "_dataElement": "DE02.01.042.00",
                            "codeSystem": {
                                "_description": "固定值，职业代码表",
                                "_value": "2.16.156.10011.2.3.3.7"
                            },
                            "codeSystemName": {
                                "_description": "固定值，职业代码表名称",
                                "_value": "职业类别代码表(GB/T6565)"
                            },
                            "code": {
                                "_description": "职业代码",
                                "_example": "13"
                            },
                            "displayName": {
                                "_description": "职业名称",
                                "_example": "专业技术人员"
                            }
                        }
                    }
                }
            }
        }
    }


def generate_encounter_card_update_json():
    """Generate JSON for 就诊卡信息更新请求 (PRPA_IN201314UV02)."""
    base = generate_encounter_card_add_json()
    base["messageHeader"]["interactionId"]["extension"]["_description"] = "服务标识代码，PRPA_IN201314UV02 - 就诊卡信息更新请求"
    return base


def generate_encounter_card_query_request_json():
    """Generate JSON for 就诊卡信息查询请求 (PRPA_IN201305UV02)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "query": {
            "_description": "查询参数信息",
            "queryByParameter": {
                "_description": "查询参数",
                "parameterList": {
                    "_description": "查询参数列表",
                    "patientId": {
                        "_description": "患者编号查询参数",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "患者编号值",
                            "item": {
                                "root": {
                                    "_description": "固定值，标识ID类型为患者编号",
                                    "_value": "2.16.156.10011.2.5.1.4"
                                },
                                "extension": {
                                    "_description": "患者编号的具体值"
                                }
                            }
                        }
                    },
                    "cardId": {
                        "_description": "就诊卡号查询参数",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "就诊卡号值",
                            "item": {
                                "root": {
                                    "_description": "固定值，标识ID类型为就诊卡号",
                                    "_value": "2.16.156.10011.2.5.1.6"
                                },
                                "extension": {
                                    "_description": "就诊卡号的具体值"
                                }
                            }
                        }
                    },
                    "certificateId": {
                        "_description": "身份证件号码查询参数",
                        "_cardinality": "0..1",
                        "_required": False,
                        "value": {
                            "_description": "身份证件号码值",
                            "item": {
                                "root": {
                                    "_description": "固定值，标识ID类型为身份证件号码",
                                    "_value": "2.16.156.10011.1.3"
                                },
                                "extension": {
                                    "_description": "身份证件号码的具体值"
                                }
                            }
                        }
                    }
                }
            }
        }
    }


def generate_encounter_card_query_response_json():
    """Generate JSON for 就诊卡信息查询应答 (PRPA_IN201306UV02)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "queryAck": {
            "_description": "查询应答信息",
            "queryId": {
                "_description": "查询标识",
                "_cardinality": "1..1",
                "_required": True,
                "root": {
                    "_description": "固定值",
                    "_value": "2.16.156.10011.2.5.1.1"
                },
                "extension": {
                    "_description": "查询标识值"
                }
            },
            "statusCode": {
                "_description": "查询状态码"
            },
            "queryResponseCode": {
                "_description": "查询响应代码",
                "_allowedValues": {
                    "OK": "找到数据",
                    "NF": "未找到数据",
                    "QE": "查询参数错误",
                    "AE": "系统错误"
                }
            },
            "resultTotalQuantity": {
                "_description": "查询结果总数"
            }
        },
        "encounterCard": {
            "_description": "就诊卡信息列表",
            "_cardinality": "0..*",
            "_required": False,
            "patient": generate_encounter_card_add_json()["encounterCard"]["patient"]
        }
    }


def generate_ack_json(is_success=True):
    """Generate JSON for 通用应答 (MCCI_IN000002UV01)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "acknowledgement": {
            "_description": "应答信息",
            "typeCode": {
                "_description": "处理结果类型码",
                "_cardinality": "1..1",
                "_required": True,
                "_allowedValues": {
                    "AA": "接受成功（Accept Acknowledgement）",
                    "AE": "接受失败（Application Error）",
                    "AR": "拒绝（Application Reject）"
                }
            },
            "targetMessage": {
                "_description": "原始消息引用",
                "_cardinality": "1..1",
                "_required": True,
                "id": {
                    "_description": "原始消息流水号",
                    "root": {
                        "_description": "固定值",
                        "_value": "2.16.156.10011.2.5.1.1"
                    },
                    "extension": {
                        "_description": "原始消息流水号的具体值"
                    }
                }
            },
            "detail": {
                "_description": "处理结果详情",
                "text": {
                    "_description": "处理结果说明",
                    "_cardinality": "1..1",
                    "_required": True,
                    "_format": "字符串，最大长度200"
                }
            }
        }
    }


def generate_outpatient_registration_add_json():
    """Generate JSON for 门诊挂号信息新增请求 (PRPA_IN400001UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "registration": {
            "_description": "门诊挂号信息主体",
            "id": {
                "_description": "挂号流水号",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "字符串，最大长度50",
                "item": {
                    "_description": "挂号流水号标识",
                    "root": {
                        "_description": "固定值",
                        "_value": "2.16.156.10011.2.5.1.20"
                    },
                    "extension": {
                        "_description": "挂号流水号的具体值"
                    }
                }
            },
            "statusCode": {
                "_description": "挂号状态",
                "_allowedValues": {
                    "active": "有效",
                    "completed": "已完成",
                    "cancelled": "已取消"
                }
            },
            "effectiveTime": {
                "_description": "挂号时间",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "日期时间格式，yyyyMMddHHmmss（DT15）"
            },
            "patient": {
                "_description": "患者信息",
                "id": {
                    "_description": "患者标识",
                    "_cardinality": "1..1",
                    "_required": True,
                    "item": {
                        "_description": "患者标识信息",
                        "root": {
                            "_description": "固定值",
                            "_value": "2.16.156.10011.2.5.1.4"
                        },
                        "extension": {
                            "_description": "患者编号的具体值"
                        }
                    }
                },
                "name": {
                    "_description": "患者姓名",
                    "_dataElement": "DE02.01.039.00"
                },
                "gender": {
                    "_description": "患者性别",
                    "_dataElement": "DE02.01.040.00"
                },
                "birthTime": {
                    "_description": "患者出生日期",
                    "_dataElement": "DE02.01.005.00"
                }
            },
            "appointment": {
                "_description": "预约信息",
                "id": {
                    "_description": "预约流水号",
                    "item": {
                        "root": {
                            "_description": "固定值",
                            "_value": "2.16.156.10011.2.5.1.29"
                        },
                        "extension": {
                            "_description": "预约流水号的具体值"
                        }
                    }
                },
                "statusCode": {
                    "_description": "预约状态"
                },
                "requestedAct": {
                    "_description": "预约就诊信息",
                    "code": {
                        "_description": "就诊类型代码",
                        "displayName": {
                            "_description": "就诊类型名称",
                            "_allowedValues": {
                                "1": "普通门诊",
                                "2": "急诊",
                                "3": "专家门诊",
                                "4": "特需门诊"
                            }
                        }
                    },
                    "slot": {
                        "_description": "时间段信息",
                        "startTime": {
                            "_description": "开始时间"
                        },
                        "endTime": {
                            "_description": "结束时间"
                        }
                    }
                }
            },
            "department": {
                "_description": "就诊科室信息",
                "id": {
                    "_description": "科室编码",
                    "_dataElement": "DE08.10.025.00",
                    "item": {
                        "root": {
                            "_value": "2.16.156.10011.1.26"
                        },
                        "extension": {
                            "_description": "科室编码的具体值"
                        }
                    }
                },
                "name": {
                    "_description": "科室名称",
                    "_dataElement": "DE08.10.026.00"
                }
            },
            "doctor": {
                "_description": "接诊医生信息",
                "id": {
                    "_description": "医生工号",
                    "item": {
                        "root": {
                            "_value": "2.16.156.10011.1.4"
                        },
                        "extension": {
                            "_description": "医生工号的具体值"
                        }
                    }
                },
                "name": {
                    "_description": "医生姓名",
                    "_dataElement": "DE02.01.039.00"
                }
            }
        }
    }


def generate_outpatient_registration_update_json():
    """Generate JSON for 门诊挂号信息更新请求 (PRPA_IN400002UV)."""
    base = generate_outpatient_registration_add_json()
    base["messageHeader"]["interactionId"]["extension"]["_description"] = "服务标识代码，PRPA_IN400002UV - 门诊挂号信息更新请求"
    return base


def generate_outpatient_registration_query_request_json():
    """Generate JSON for 门诊挂号信息查询请求 (PRPA_IN900300UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "query": {
            "_description": "查询参数信息",
            "queryByParameter": {
                "_description": "查询参数",
                "parameterList": {
                    "_description": "查询参数列表",
                    "patientId": {
                        "_description": "患者编号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.4"},
                                "extension": {"_description": "患者编号的具体值"}
                            }
                        }
                    },
                    "registrationId": {
                        "_description": "挂号流水号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.20"},
                                "extension": {"_description": "挂号流水号的具体值"}
                            }
                        }
                    },
                    "departmentId": {
                        "_description": "科室编码查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.1.26"},
                                "extension": {"_description": "科室编码的具体值"}
                            }
                        }
                    },
                    "doctorId": {
                        "_description": "医生工号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.1.4"},
                                "extension": {"_description": "医生工号的具体值"}
                            }
                        }
                    },
                    "registrationTime": {
                        "_description": "挂号时间查询参数",
                        "value": {
                            "_description": "时间范围",
                            "low": {"_description": "开始时间"},
                            "high": {"_description": "结束时间"}
                        }
                    }
                }
            }
        }
    }


def generate_outpatient_registration_query_response_json():
    """Generate JSON for 门诊挂号信息查询应答 (PRPA_IN900350UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "queryAck": {
            "_description": "查询应答信息",
            "queryId": {
                "_description": "查询标识",
                "root": {"_value": "2.16.156.10011.2.5.1.1"},
                "extension": {"_description": "查询标识值"}
            },
            "statusCode": {"_description": "查询状态码"},
            "queryResponseCode": {
                "_description": "查询响应代码",
                "_allowedValues": {
                    "OK": "找到数据",
                    "NF": "未找到数据",
                    "QE": "查询参数错误",
                    "AE": "系统错误"
                }
            },
            "resultTotalQuantity": {"_description": "查询结果总数"}
        },
        "registration": {
            "_description": "门诊挂号信息列表",
            "_cardinality": "0..*",
            "item": generate_outpatient_registration_add_json()["registration"]
        }
    }


def generate_inpatient_encounter_register_json():
    """Generate JSON for 住院就诊信息登记请求 (PRPA_IN400001UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "encounter": {
            "_description": "住院就诊信息主体",
            "id": {
                "_description": "就诊流水号",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "字符串，最大长度50",
                "item": {
                    "_description": "就诊流水号标识",
                    "root": {
                        "_description": "固定值",
                        "_value": "2.16.156.10011.2.5.1.9"
                    },
                    "extension": {
                        "_description": "就诊流水号的具体值"
                    }
                }
            },
            "statusCode": {
                "_description": "就诊状态",
                "_allowedValues": {
                    "active": "就诊中",
                    "completed": "已完成",
                    "cancelled": "已取消"
                }
            },
            "effectiveTime": {
                "_description": "入院时间",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "日期时间格式，yyyyMMddHHmmss（DT15）"
            },
            "patient": {
                "_description": "患者信息",
                "id": {
                    "_description": "患者标识",
                    "_cardinality": "1..*",
                    "_required": True,
                    "_itemDescription": {
                        "2.16.156.10011.2.5.1.4": "患者编号（必填）",
                        "2.16.156.10011.1.12": "住院号"
                    }
                },
                "name": {
                    "_description": "患者姓名",
                    "_dataElement": "DE02.01.039.00"
                },
                "gender": {
                    "_description": "患者性别",
                    "_dataElement": "DE02.01.040.00"
                },
                "birthTime": {
                    "_description": "患者出生日期",
                    "_dataElement": "DE02.01.005.00"
                }
            },
            "admissionDepartment": {
                "_description": "入院科室信息",
                "id": {
                    "_description": "科室编码",
                    "_dataElement": "DE08.10.025.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.26"},
                        "extension": {"_description": "科室编码的具体值"}
                    }
                },
                "name": {
                    "_description": "科室名称",
                    "_dataElement": "DE08.10.026.00"
                }
            },
            "admissionWard": {
                "_description": "入院病区信息",
                "id": {
                    "_description": "病区编码",
                    "_dataElement": "DE08.10.054.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.27"},
                        "extension": {"_description": "病区编码的具体值"}
                    }
                },
                "name": {
                    "_description": "病区名称",
                    "_dataElement": "DE08.10.054.00"
                }
            },
            "bed": {
                "_description": "床位信息",
                "id": {
                    "_description": "床位号",
                    "_dataElement": "DE01.00.026.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.22"},
                        "extension": {"_description": "床位号的具体值"}
                    }
                },
                "name": {
                    "_description": "床位名称"
                }
            },
            "admittingDoctor": {
                "_description": "主治医师信息",
                "id": {
                    "_description": "医师工号",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.4"},
                        "extension": {"_description": "医师工号的具体值"}
                    }
                },
                "name": {
                    "_description": "医师姓名",
                    "_dataElement": "DE02.01.039.00"
                }
            },
            "patientType": {
                "_description": "患者类型",
                "_dataElement": "DE02.01.060.00",
                "code": {
                    "_description": "患者类型代码",
                    "_codeSystem": "2.16.156.10011.2.3.1.271"
                },
                "displayName": {
                    "_description": "患者类型名称",
                    "_allowedValues": {
                        "1": "自费",
                        "2": "医保",
                        "3": "公费"
                    }
                }
            },
            "diagnosis": {
                "_description": "入院诊断信息",
                "_cardinality": "0..*",
                "_required": False,
                "code": {
                    "_description": "诊断编码",
                    "_dataElement": "DE05.01.025.00"
                },
                "displayName": {
                    "_description": "诊断名称",
                    "_dataElement": "DE05.01.025.00"
                }
            }
        }
    }


def generate_inpatient_encounter_update_json():
    """Generate JSON for 住院就诊信息更新请求 (PRPA_IN400002UV)."""
    base = generate_inpatient_encounter_register_json()
    base["messageHeader"]["interactionId"]["extension"]["_description"] = "服务标识代码，PRPA_IN400002UV - 住院就诊信息更新请求"
    return base


def generate_inpatient_encounter_query_request_json():
    """Generate JSON for 住院就诊信息查询请求 (PRPA_IN900300UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "query": {
            "_description": "查询参数信息",
            "queryByParameter": {
                "_description": "查询参数",
                "parameterList": {
                    "_description": "查询参数列表",
                    "patientId": {
                        "_description": "患者编号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.4"},
                                "extension": {"_description": "患者编号的具体值"}
                            }
                        }
                    },
                    "encounterId": {
                        "_description": "就诊流水号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.9"},
                                "extension": {"_description": "就诊流水号的具体值"}
                            }
                        }
                    },
                    "inpatientId": {
                        "_description": "住院号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.1.12"},
                                "extension": {"_description": "住院号的具体值"}
                            }
                        }
                    },
                    "departmentId": {
                        "_description": "科室编码查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.1.26"},
                                "extension": {"_description": "科室编码的具体值"}
                            }
                        }
                    },
                    "admissionTime": {
                        "_description": "入院时间查询参数",
                        "value": {
                            "_description": "时间范围",
                            "low": {"_description": "开始时间"},
                            "high": {"_description": "结束时间"}
                        }
                    }
                }
            }
        }
    }


def generate_inpatient_encounter_query_response_json():
    """Generate JSON for 住院就诊信息查询应答 (PRPA_IN900350UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "queryAck": {
            "_description": "查询应答信息",
            "queryId": {
                "_description": "查询标识",
                "root": {"_value": "2.16.156.10011.2.5.1.1"},
                "extension": {"_description": "查询标识值"}
            },
            "statusCode": {"_description": "查询状态码"},
            "queryResponseCode": {
                "_description": "查询响应代码",
                "_allowedValues": {
                    "OK": "找到数据",
                    "NF": "未找到数据",
                    "QE": "查询参数错误",
                    "AE": "系统错误"
                }
            },
            "resultTotalQuantity": {"_description": "查询结果总数"}
        },
        "encounter": {
            "_description": "住院就诊信息列表",
            "_cardinality": "0..*",
            "item": generate_inpatient_encounter_register_json()["encounter"]
        }
    }


def generate_inpatient_transfer_add_json():
    """Generate JSON for 住院转科信息新增请求 (PRPA_IN302011UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "transfer": {
            "_description": "住院转科信息主体",
            "id": {
                "_description": "转科流水号",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "字符串，最大长度50",
                "item": {
                    "_description": "转科流水号标识",
                    "root": {
                        "_description": "固定值",
                        "_value": "2.16.156.10011.2.5.1.20"
                    },
                    "extension": {
                        "_description": "转科流水号的具体值"
                    }
                }
            },
            "statusCode": {
                "_description": "转科状态",
                "_allowedValues": {
                    "active": "有效",
                    "completed": "已完成",
                    "cancelled": "已取消"
                }
            },
            "effectiveTime": {
                "_description": "转科时间",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "日期时间格式，yyyyMMddHHmmss（DT15）"
            },
            "encounter": {
                "_description": "就诊信息",
                "id": {
                    "_description": "就诊流水号",
                    "item": {
                        "root": {"_value": "2.16.156.10011.2.5.1.9"},
                        "extension": {"_description": "就诊流水号的具体值"}
                    }
                }
            },
            "patient": {
                "_description": "患者信息",
                "id": {
                    "_description": "患者标识",
                    "item": {
                        "root": {"_value": "2.16.156.10011.2.5.1.4"},
                        "extension": {"_description": "患者编号的具体值"}
                    }
                },
                "name": {
                    "_description": "患者姓名",
                    "_dataElement": "DE02.01.039.00"
                }
            },
            "sourceDepartment": {
                "_description": "转出科室信息",
                "id": {
                    "_description": "科室编码",
                    "_dataElement": "DE08.10.025.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.26"},
                        "extension": {"_description": "科室编码的具体值"}
                    }
                },
                "name": {
                    "_description": "科室名称",
                    "_dataElement": "DE08.10.026.00"
                }
            },
            "targetDepartment": {
                "_description": "转入科室信息",
                "id": {
                    "_description": "科室编码",
                    "_dataElement": "DE08.10.025.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.26"},
                        "extension": {"_description": "科室编码的具体值"}
                    }
                },
                "name": {
                    "_description": "科室名称",
                    "_dataElement": "DE08.10.026.00"
                }
            },
            "sourceWard": {
                "_description": "转出病区信息",
                "id": {
                    "_description": "病区编码",
                    "_dataElement": "DE08.10.054.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.27"},
                        "extension": {"_description": "病区编码的具体值"}
                    }
                },
                "name": {
                    "_description": "病区名称",
                    "_dataElement": "DE08.10.054.00"
                }
            },
            "targetWard": {
                "_description": "转入病区信息",
                "id": {
                    "_description": "病区编码",
                    "_dataElement": "DE08.10.054.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.27"},
                        "extension": {"_description": "病区编码的具体值"}
                    }
                },
                "name": {
                    "_description": "病区名称",
                    "_dataElement": "DE08.10.054.00"
                }
            },
            "transferDoctor": {
                "_description": "转科医师信息",
                "id": {
                    "_description": "医师工号",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.4"},
                        "extension": {"_description": "医师工号的具体值"}
                    }
                },
                "name": {
                    "_description": "医师姓名",
                    "_dataElement": "DE02.01.039.00"
                }
            },
            "transferReason": {
                "_description": "转科原因",
                "_cardinality": "0..1",
                "_required": False,
                "_format": "字符串，最大长度200"
            }
        }
    }


def generate_inpatient_transfer_update_json():
    """Generate JSON for 住院转科信息更新请求 (PRPA_IN302012UV)."""
    base = generate_inpatient_transfer_add_json()
    base["messageHeader"]["interactionId"]["extension"]["_description"] = "服务标识代码，PRPA_IN302012UV - 住院转科信息更新请求"
    return base


def generate_inpatient_transfer_query_request_json():
    """Generate JSON for 住院转科信息查询请求 (PRPA_IN900300UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "query": {
            "_description": "查询参数信息",
            "queryByParameter": {
                "_description": "查询参数",
                "parameterList": {
                    "_description": "查询参数列表",
                    "patientId": {
                        "_description": "患者编号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.4"},
                                "extension": {"_description": "患者编号的具体值"}
                            }
                        }
                    },
                    "encounterId": {
                        "_description": "就诊流水号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.9"},
                                "extension": {"_description": "就诊流水号的具体值"}
                            }
                        }
                    },
                    "transferId": {
                        "_description": "转科流水号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.20"},
                                "extension": {"_description": "转科流水号的具体值"}
                            }
                        }
                    },
                    "transferTime": {
                        "_description": "转科时间查询参数",
                        "value": {
                            "_description": "时间范围",
                            "low": {"_description": "开始时间"},
                            "high": {"_description": "结束时间"}
                        }
                    }
                }
            }
        }
    }


def generate_inpatient_transfer_query_response_json():
    """Generate JSON for 住院转科信息查询应答 (PRPA_IN900350UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "queryAck": {
            "_description": "查询应答信息",
            "queryId": {
                "_description": "查询标识",
                "root": {"_value": "2.16.156.10011.2.5.1.1"},
                "extension": {"_description": "查询标识值"}
            },
            "statusCode": {"_description": "查询状态码"},
            "queryResponseCode": {
                "_description": "查询响应代码",
                "_allowedValues": {
                    "OK": "找到数据",
                    "NF": "未找到数据",
                    "QE": "查询参数错误",
                    "AE": "系统错误"
                }
            },
            "resultTotalQuantity": {"_description": "查询结果总数"}
        },
        "transfer": {
            "_description": "住院转科信息列表",
            "_cardinality": "0..*",
            "item": generate_inpatient_transfer_add_json()["transfer"]
        }
    }


def generate_discharge_register_add_json():
    """Generate JSON for 出院登记信息新增请求 (PRPA_IN400003UV01)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "discharge": {
            "_description": "出院登记信息主体",
            "id": {
                "_description": "出院登记流水号",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "字符串，最大长度50",
                "item": {
                    "_description": "出院登记流水号标识",
                    "root": {
                        "_description": "固定值",
                        "_value": "2.16.156.10011.2.5.1.20"
                    },
                    "extension": {
                        "_description": "出院登记流水号的具体值"
                    }
                }
            },
            "statusCode": {
                "_description": "出院登记状态",
                "_allowedValues": {
                    "active": "有效",
                    "completed": "已完成",
                    "cancelled": "已取消"
                }
            },
            "effectiveTime": {
                "_description": "出院时间",
                "_cardinality": "1..1",
                "_required": True,
                "_format": "日期时间格式，yyyyMMddHHmmss（DT15）"
            },
            "encounter": {
                "_description": "就诊信息",
                "id": {
                    "_description": "就诊流水号",
                    "item": {
                        "root": {"_value": "2.16.156.10011.2.5.1.9"},
                        "extension": {"_description": "就诊流水号的具体值"}
                    }
                }
            },
            "patient": {
                "_description": "患者信息",
                "id": {
                    "_description": "患者标识",
                    "item": {
                        "root": {"_value": "2.16.156.10011.2.5.1.4"},
                        "extension": {"_description": "患者编号的具体值"}
                    }
                },
                "name": {
                    "_description": "患者姓名",
                    "_dataElement": "DE02.01.039.00"
                }
            },
            "dischargeDepartment": {
                "_description": "出院科室信息",
                "id": {
                    "_description": "科室编码",
                    "_dataElement": "DE08.10.025.00",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.26"},
                        "extension": {"_description": "科室编码的具体值"}
                    }
                },
                "name": {
                    "_description": "科室名称",
                    "_dataElement": "DE08.10.026.00"
                }
            },
            "dischargeDiagnosis": {
                "_description": "出院诊断信息",
                "_cardinality": "1..*",
                "_required": True,
                "code": {
                    "_description": "诊断编码",
                    "_dataElement": "DE05.01.025.00"
                },
                "displayName": {
                    "_description": "诊断名称",
                    "_dataElement": "DE05.01.025.00"
                },
                "isPrincipal": {
                    "_description": "是否主诊断",
                    "_allowedValues": {
                        "Y": "是",
                        "N": "否"
                    }
                }
            },
            "dischargingDoctor": {
                "_description": "出院医师信息",
                "id": {
                    "_description": "医师工号",
                    "item": {
                        "root": {"_value": "2.16.156.10011.1.4"},
                        "extension": {"_description": "医师工号的具体值"}
                    }
                },
                "name": {
                    "_description": "医师姓名",
                    "_dataElement": "DE02.01.039.00"
                }
            },
            "dischargeDisposition": {
                "_description": "出院方式",
                "_allowedValues": {
                    "1": "医嘱离院",
                    "2": "医嘱转院",
                    "3": "医嘱转社区卫生服务机构/乡镇卫生院",
                    "4": "非医嘱离院",
                    "5": "死亡"
                }
            },
            "hospitalDays": {
                "_description": "住院天数",
                "_format": "数值型"
            }
        }
    }


def generate_discharge_register_update_json():
    """Generate JSON for 出院登记信息更新请求 (PRPA_IN400002UV)."""
    base = generate_discharge_register_add_json()
    base["messageHeader"]["interactionId"]["extension"]["_description"] = "服务标识代码，PRPA_IN400002UV - 出院登记信息更新请求"
    return base


def generate_discharge_query_request_json():
    """Generate JSON for 出院信息查询请求 (PRPA_IN900300UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "query": {
            "_description": "查询参数信息",
            "queryByParameter": {
                "_description": "查询参数",
                "parameterList": {
                    "_description": "查询参数列表",
                    "patientId": {
                        "_description": "患者编号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.4"},
                                "extension": {"_description": "患者编号的具体值"}
                            }
                        }
                    },
                    "encounterId": {
                        "_description": "就诊流水号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.9"},
                                "extension": {"_description": "就诊流水号的具体值"}
                            }
                        }
                    },
                    "dischargeId": {
                        "_description": "出院登记流水号查询参数",
                        "value": {
                            "item": {
                                "root": {"_value": "2.16.156.10011.2.5.1.20"},
                                "extension": {"_description": "出院登记流水号的具体值"}
                            }
                        }
                    },
                    "dischargeTime": {
                        "_description": "出院时间查询参数",
                        "value": {
                            "_description": "时间范围",
                            "low": {"_description": "开始时间"},
                            "high": {"_description": "结束时间"}
                        }
                    }
                }
            }
        }
    }


def generate_discharge_query_response_json():
    """Generate JSON for 出院信息查询应答 (PRPA_IN900350UV)."""
    return {
        "messageHeader": MESSAGE_HEADER_TEMPLATE.copy(),
        "queryAck": {
            "_description": "查询应答信息",
            "queryId": {
                "_description": "查询标识",
                "root": {"_value": "2.16.156.10011.2.5.1.1"},
                "extension": {"_description": "查询标识值"}
            },
            "statusCode": {"_description": "查询状态码"},
            "queryResponseCode": {
                "_description": "查询响应代码",
                "_allowedValues": {
                    "OK": "找到数据",
                    "NF": "未找到数据",
                    "QE": "查询参数错误",
                    "AE": "系统错误"
                }
            },
            "resultTotalQuantity": {"_description": "查询结果总数"}
        },
        "discharge": {
            "_description": "出院信息列表",
            "_cardinality": "0..*",
            "item": generate_discharge_register_add_json()["discharge"]
        }
    }


def generate_clean_json(data, remove_descriptions=True):
    """Generate clean JSON by removing description fields."""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            if key.startswith('_'):
                if not remove_descriptions:
                    result[key] = value
            else:
                result[key] = generate_clean_json(value, remove_descriptions)
        return result
    elif isinstance(data, list):
        return [generate_clean_json(item, remove_descriptions) for item in data]
    else:
        return data


def main():
    # Define all JSON generators
    generators = {
        '就诊卡信息新增请求_PRPA_IN201311UV02': generate_encounter_card_add_json,
        '就诊卡信息更新请求_PRPA_IN201314UV02': generate_encounter_card_update_json,
        '就诊卡信息查询请求_PRPA_IN201305UV02': generate_encounter_card_query_request_json,
        '就诊卡信息查询应答_PRPA_IN201306UV02': generate_encounter_card_query_response_json,
        '通用应答_MCCI_IN000002UV01': generate_ack_json,
        '门诊挂号信息新增请求_PRPA_IN400001UV': generate_outpatient_registration_add_json,
        '门诊挂号信息更新请求_PRPA_IN400002UV': generate_outpatient_registration_update_json,
        '门诊挂号信息查询请求_PRPA_IN900300UV': generate_outpatient_registration_query_request_json,
        '门诊挂号信息查询应答_PRPA_IN900350UV': generate_outpatient_registration_query_response_json,
        '住院就诊信息登记请求_PRPA_IN400001UV': generate_inpatient_encounter_register_json,
        '住院就诊信息更新请求_PRPA_IN400002UV': generate_inpatient_encounter_update_json,
        '住院就诊信息查询请求_PRPA_IN900300UV': generate_inpatient_encounter_query_request_json,
        '住院就诊信息查询应答_PRPA_IN900350UV': generate_inpatient_encounter_query_response_json,
        '住院转科信息新增请求_PRPA_IN302011UV': generate_inpatient_transfer_add_json,
        '住院转科信息更新请求_PRPA_IN302012UV': generate_inpatient_transfer_update_json,
        '住院转科信息查询请求_PRPA_IN900300UV': generate_inpatient_transfer_query_request_json,
        '住院转科信息查询应答_PRPA_IN900350UV': generate_inpatient_transfer_query_response_json,
        '出院登记信息新增请求_PRPA_IN400003UV01': generate_discharge_register_add_json,
        '出院登记信息更新请求_PRPA_IN400002UV': generate_discharge_register_update_json,
        '出院信息查询请求_PRPA_IN900300UV': generate_discharge_query_request_json,
        '出院信息查询应答_PRPA_IN900350UV': generate_discharge_query_response_json,
    }
    
    # Ensure directories exist
    os.makedirs('json-examples', exist_ok=True)
    os.makedirs('test-data', exist_ok=True)
    
    # Generate files
    generated_files = []
    for filename, generator in generators.items():
        # Generate JSON with descriptions
        json_data = generator()
        json_path = f'json-examples/{filename}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        generated_files.append(json_path)
        
        # Generate clean test data
        clean_data = generate_clean_json(json_data)
        clean_path = f'test-data/clean_{filename}.json'
        with open(clean_path, 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, ensure_ascii=False, indent=2)
        generated_files.append(clean_path)
    
    print(f"Generated {len(generated_files)} files")
    return generated_files


if __name__ == '__main__':
    files = main()
    for f in files:
        print(f)
