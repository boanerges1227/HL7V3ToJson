#!/usr/bin/env python3
"""
根据WS/T 846-2024标准，为测试数据文件添加完整的示例值
"""

import json
import os
import glob
import re

# 标准OID定义
OID_MAP = {
    "2.16.156.10011.2.5.1.1": "消息流水号",
    "2.16.156.10011.2.5.1.2": "消息服务标识",
    "2.16.156.10011.2.5.1.3": "系统标识",
    "2.16.156.10011.2.5.1.4": "患者编号",
    "2.16.156.10011.2.5.1.5": "域ID",
    "2.16.156.10011.2.5.1.6": "就诊卡号",
    "2.16.156.10011.2.5.1.8": "就诊次数",
    "2.16.156.10011.2.5.1.9": "就诊流水号",
    "2.16.156.10011.2.5.1.14": "药物编码",
    "2.16.156.10011.1.3": "身份证件号码",
    "2.16.156.10011.1.4": "医护人员工号",
    "2.16.156.10011.1.5": "医院编码",
    "2.16.156.10011.1.10": "门急诊号",
    "2.16.156.10011.1.12": "住院号",
    "2.16.156.10011.1.19": "居民健康卡号",
    "2.16.156.10011.1.21": "病房号",
    "2.16.156.10011.1.22": "病床号",
    "2.16.156.10011.1.26": "科室编码",
    "2.16.156.10011.1.27": "病区编码",
    "2.16.156.10011.1.28": "医嘱编码",
}

# 示例数据
SAMPLE_VALUES = {
    # 患者信息
    "patient_name": "张三",
    "patient_id": "PAT-2024-100001",
    "id_card": "110101199001011234",
    "phone": "13800138000",
    "birth_date": "19900101",
    "gender_code": "M",
    "gender_name": "男性",
    "health_card": "HC-2024-888888",
    
    # 医师信息
    "doctor_id": "DOC001",
    "doctor_name": "张三",
    "doctor2_id": "DOC002",
    "doctor2_name": "李四",
    "nurse_id": "NURSE001",
    "nurse_name": "王护士",
    
    # 科室信息
    "dept_id": "DEPT-CARDIO-001",
    "dept_name": "心血管内科",
    "dept2_id": "DEPT-RESP-001",
    "dept2_name": "呼吸内科",
    "dept3_id": "DEPT-PHARMACY-001",
    "dept3_name": "药剂科",
    
    # 医院信息
    "hospital_id": "HOSP-001",
    "hospital_name": "北京协和医院",
    
    # 系统信息
    "sender_system": "SYS-EMR-001",
    "receiver_system": "SYS-HIS-001",
    
    # 消息信息
    "msg_id": "MSG-20241010-00001",
    "timestamp": "20241010110000",
    
    # 就诊信息
    "encounter_id": "ENC-20241010-001",
    "visit_number": "1",
    "outpatient_no": "M20241010-0001",
    "inpatient_no": "I20241010-0001",
    
    # 医嘱信息
    "order_id": "ORD-20241010-001",
    "order_content": "阿莫西林胶囊 0.5g×24粒 口服 每日三次",
    "medicine_name": "阿莫西林胶囊",
    "medicine_code": "AMX-001",
    
    # 预约信息
    "appointment_id": "APT-20241010-001",
    "appointment_time": "20241015090000",
    
    # 病床信息
    "bed_id": "BED-001",
    "bed_name": "1床",
    "ward_id": "WARD-001",
    "ward_name": "205室",
    "ward_area_id": "WARD-AREA-001",
    "ward_area_name": "心血管病区",
    
    # 出院信息
    "discharge_id": "DCG-20241010-001",
    "discharge_time": "20241015153045",
    
    # 转科信息
    "transfer_id": "TRF-20241010-001",
    
    # 术语信息
    "terminology_id": "TERM-001",
    "terminology_name": "上呼吸道感染",
    
    # 文档信息
    "document_id": "DOC-20241010-001",
    "document_title": "入院记录",
    
    # 状态信息
    "status_code": "active",
    "status_name": "有效",
    
    # 诊断信息
    "diagnosis_name": "上呼吸道感染",
    "diagnosis_code": "J06.9",
}


def get_oid_description(root_value):
    """根据OID获取描述"""
    return OID_MAP.get(root_value, "未知标识")


def infer_value_from_context(key, path, parent_key=""):
    """根据上下文推断应该使用的值"""
    path_lower = path.lower()
    key_lower = key.lower()
    
    # 根据root OID推断值
    if key_lower == "root":
        if "1.1.3" in path or "idcard" in path_lower:
            return SAMPLE_VALUES["id_card"]
        elif "1.1.4" in path and ("doctor" in path_lower or "person" in path_lower):
            return SAMPLE_VALUES["doctor_id"]
        elif "1.1.5" in path:
            return SAMPLE_VALUES["hospital_id"]
        elif "1.1.10" in path:
            return SAMPLE_VALUES["outpatient_no"]
        elif "1.1.12" in path:
            return SAMPLE_VALUES["inpatient_no"]
        elif "1.1.19" in path:
            return SAMPLE_VALUES["health_card"]
        elif "1.1.21" in path:
            return SAMPLE_VALUES["ward_id"]
        elif "1.1.22" in path:
            return SAMPLE_VALUES["bed_id"]
        elif "1.1.26" in path:
            return SAMPLE_VALUES["dept_id"]
        elif "1.1.27" in path:
            return SAMPLE_VALUES["ward_area_id"]
        elif "1.1.28" in path:
            return SAMPLE_VALUES["order_id"]
        elif "2.5.1.1" in path:
            return SAMPLE_VALUES["msg_id"]
        elif "2.5.1.3" in path:
            return SAMPLE_VALUES["sender_system"]
        elif "2.5.1.4" in path:
            return SAMPLE_VALUES["patient_id"]
        elif "2.5.1.5" in path:
            return "01"
        elif "2.5.1.6" in path:
            return "CARD-001"
        elif "2.5.1.8" in path:
            return SAMPLE_VALUES["visit_number"]
        elif "2.5.1.9" in path:
            return SAMPLE_VALUES["encounter_id"]
        else:
            return "2.16.156.10011.2.5.1.1"
    
    # 根据extension推断值
    if key_lower == "extension":
        if "msg" in path_lower or "message" in path_lower:
            return SAMPLE_VALUES["msg_id"]
        elif "patient" in path_lower:
            return SAMPLE_VALUES["patient_id"]
        elif "doctor" in path_lower or "person" in path_lower:
            return SAMPLE_VALUES["doctor_id"]
        elif "dept" in path_lower or "organization" in path_lower:
            return SAMPLE_VALUES["dept_id"]
        elif "hospital" in path_lower:
            return SAMPLE_VALUES["hospital_id"]
        elif "encounter" in path_lower:
            return SAMPLE_VALUES["encounter_id"]
        elif "order" in path_lower:
            return SAMPLE_VALUES["order_id"]
        elif "appointment" in path_lower:
            return SAMPLE_VALUES["appointment_id"]
        elif "system" in path_lower or "device" in path_lower:
            return SAMPLE_VALUES["sender_system"]
        elif "bed" in path_lower:
            return SAMPLE_VALUES["bed_id"]
        elif "ward" in path_lower:
            return SAMPLE_VALUES["ward_id"]
        elif "discharge" in path_lower:
            return SAMPLE_VALUES["discharge_id"]
        elif "transfer" in path_lower:
            return SAMPLE_VALUES["transfer_id"]
        elif "terminology" in path_lower or "term" in path_lower:
            return SAMPLE_VALUES["terminology_id"]
        elif "document" in path_lower or "doc" in path_lower:
            return SAMPLE_VALUES["document_id"]
        elif "outpatient" in path_lower:
            return SAMPLE_VALUES["outpatient_no"]
        elif "inpatient" in path_lower:
            return SAMPLE_VALUES["inpatient_no"]
        elif "health" in path_lower:
            return SAMPLE_VALUES["health_card"]
        else:
            return "ID-001"
    
    # 根据value上下文推断
    if key_lower == "value":
        if "name" in path_lower:
            if "patient" in path_lower:
                return SAMPLE_VALUES["patient_name"]
            elif "doctor" in path_lower or "person" in path_lower:
                return SAMPLE_VALUES["doctor_name"]
            elif "dept" in path_lower:
                return SAMPLE_VALUES["dept_name"]
            elif "hospital" in path_lower:
                return SAMPLE_VALUES["hospital_name"]
            elif "medicine" in path_lower or "drug" in path_lower:
                return SAMPLE_VALUES["medicine_name"]
            elif "diagnosis" in path_lower:
                return SAMPLE_VALUES["diagnosis_name"]
            elif "document" in path_lower:
                return SAMPLE_VALUES["document_title"]
            elif "terminology" in path_lower:
                return SAMPLE_VALUES["terminology_name"]
            else:
                return "示例名称"
        elif "time" in path_lower or "date" in path_lower:
            if "birth" in path_lower:
                return SAMPLE_VALUES["birth_date"]
            elif "discharge" in path_lower:
                return SAMPLE_VALUES["discharge_time"]
            elif "appointment" in path_lower:
                return SAMPLE_VALUES["appointment_time"]
            else:
                return SAMPLE_VALUES["timestamp"]
        elif "text" in path_lower:
            if "order" in path_lower:
                return SAMPLE_VALUES["order_content"]
            elif "note" in path_lower or "remark" in path_lower:
                return "请注意观察患者反应，如有不适及时处理"
            elif "result" in path_lower:
                return "查询成功，找到相关记录"
            elif "diagnosis" in path_lower:
                return "患者主诉咳嗽、流涕3天，伴发热1天"
            else:
                return "示例文本内容"
        elif "code" in path_lower:
            if "gender" in path_lower:
                return SAMPLE_VALUES["gender_code"]
            elif "status" in path_lower:
                return SAMPLE_VALUES["status_code"]
            elif "diagnosis" in path_lower:
                return SAMPLE_VALUES["diagnosis_code"]
            else:
                return "01"
        elif "phone" in path_lower or "telecom" in path_lower:
            return SAMPLE_VALUES["phone"]
        elif "gender" in path_lower:
            return SAMPLE_VALUES["gender_name"]
        elif "birth" in path_lower:
            return SAMPLE_VALUES["birth_date"]
        elif "quantity" in path_lower:
            return "1"
        else:
            return "示例值"
    
    # 根据key名称推断
    if key_lower == "code":
        if "status" in path_lower:
            return SAMPLE_VALUES["status_code"]
        elif "gender" in path_lower:
            return SAMPLE_VALUES["gender_code"]
        elif "diagnosis" in path_lower:
            return SAMPLE_VALUES["diagnosis_code"]
        else:
            return "01"
    
    if key_lower == "displayname":
        if "gender" in path_lower:
            return SAMPLE_VALUES["gender_name"]
        elif "status" in path_lower:
            return SAMPLE_VALUES["status_name"]
        elif "dept" in path_lower:
            return SAMPLE_VALUES["dept_name"]
        elif "diagnosis" in path_lower:
            return SAMPLE_VALUES["diagnosis_name"]
        else:
            return "示例显示名称"
    
    if key_lower == "text":
        if "order" in path_lower:
            return SAMPLE_VALUES["order_content"]
        elif "note" in path_lower or "remark" in path_lower:
            return "请注意观察患者反应，如有不适及时处理"
        elif "result" in path_lower:
            return "查询成功，找到相关记录"
        elif "diagnosis" in path_lower:
            return "患者主诉咳嗽、流涕3天，伴发热1天"
        else:
            return "示例文本内容"
    
    if key_lower == "telecom" or "phone" in key_lower:
        return SAMPLE_VALUES["phone"]
    
    if key_lower == "birthtime":
        return SAMPLE_VALUES["birth_date"]
    
    # 默认值
    return "示例值"


def add_values_recursive(obj, path="", parent_key=""):
    """递归为JSON对象添加示例值"""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                if not value:  # 空字典
                    result[key] = infer_value_from_context(key, new_path, parent_key)
                else:
                    result[key] = add_values_recursive(value, new_path, key)
            elif isinstance(value, list):
                if not value:  # 空列表
                    result[key] = []
                else:
                    result[key] = [add_values_recursive(item, new_path, key) for item in value]
            elif value is None:
                result[key] = infer_value_from_context(key, new_path, parent_key)
            elif value == "":
                result[key] = infer_value_from_context(key, new_path, parent_key)
            else:
                result[key] = value
        return result
    elif isinstance(obj, list):
        if not obj:
            return obj
        return [add_values_recursive(item, path, parent_key) for item in obj]
    else:
        return obj


def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 计算原始value数量
        original_content = json.dumps(data, ensure_ascii=False)
        original_count = original_content.count('"value"')
        
        # 添加示例值
        updated_data = add_values_recursive(data)
        
        # 计算更新后value数量
        updated_content = json.dumps(updated_data, ensure_ascii=False)
        updated_count = updated_content.count('"value"')
        
        # 写回文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        
        return original_count, updated_count
    except Exception as e:
        print(f"  错误: {e}")
        return None, None


def main():
    # 获取所有测试数据文件
    test_files = sorted(glob.glob("test-data/clean_*.json"))
    
    print(f"找到 {len(test_files)} 个测试数据文件")
    print()
    
    total_original = 0
    total_updated = 0
    updated_files = 0
    
    for filepath in test_files:
        filename = os.path.basename(filepath)
        original_count, updated_count = process_file(filepath)
        
        if original_count is not None:
            total_original += original_count
            total_updated += updated_count
            if updated_count > original_count:
                updated_files += 1
                print(f"✓ {filename}: {original_count} -> {updated_count} 个value (+{updated_count - original_count})")
            else:
                print(f"  {filename}: {original_count} 个value (无变化)")
        else:
            print(f"✗ {filename}: 处理失败")
    
    print()
    print(f"处理完成:")
    print(f"  - 更新文件: {updated_files} 个")
    print(f"  - value总数: {total_original} -> {total_updated} (+{total_updated - total_original})")


if __name__ == '__main__':
    main()
