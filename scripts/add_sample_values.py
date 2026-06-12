#!/usr/bin/env python3
"""
为测试数据文件添加完整的示例值
"""

import json
import os
import glob
import copy

# 常用示例值
SAMPLE_DATA = {
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
    
    # 科室信息
    "dept_id": "DEPT-CARDIO-001",
    "dept_name": "心血管内科",
    "dept2_id": "DEPT-RESP-001",
    "dept2_name": "呼吸内科",
    
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
}


def add_values_to_json(obj, path=""):
    """递归为JSON对象添加示例值"""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            
            if isinstance(value, dict):
                result[key] = add_values_to_json(value, new_path)
            elif isinstance(value, list):
                result[key] = [add_values_to_json(item, new_path) for item in value]
            elif value is None or value == "" or value == {}:
                # 根据路径和key名添加示例值
                result[key] = get_sample_value(key, new_path)
            else:
                result[key] = value
        return result
    elif isinstance(obj, list):
        return [add_values_to_json(item, path) for item in obj]
    else:
        return obj


def get_sample_value(key, path):
    """根据key和路径返回合适的示例值"""
    key_lower = key.lower()
    path_lower = path.lower()
    
    # ID相关
    if key == "extension" or key == "id":
        if "msg" in path_lower or "message" in path_lower:
            return SAMPLE_DATA["msg_id"]
        elif "patient" in path_lower:
            return SAMPLE_DATA["patient_id"]
        elif "doctor" in path_lower or "person" in path_lower:
            return SAMPLE_DATA["doctor_id"]
        elif "dept" in path_lower or "organization" in path_lower:
            return SAMPLE_DATA["dept_id"]
        elif "hospital" in path_lower:
            return SAMPLE_DATA["hospital_id"]
        elif "encounter" in path_lower:
            return SAMPLE_DATA["encounter_id"]
        elif "order" in path_lower:
            return SAMPLE_DATA["order_id"]
        elif "appointment" in path_lower:
            return SAMPLE_DATA["appointment_id"]
        elif "system" in path_lower or "device" in path_lower:
            return SAMPLE_DATA["sender_system"]
        elif "bed" in path_lower:
            return SAMPLE_DATA["bed_id"]
        elif "ward" in path_lower:
            return SAMPLE_DATA["ward_id"]
        else:
            return "ID-001"
    
    # root OID
    if key == "root":
        if "1.1" in path:
            return "2.16.156.10011.2.5.1.1"
        elif "1.2" in path:
            return "2.16.156.10011.2.5.1.2"
        elif "1.3" in path:
            return "2.16.156.10011.2.5.1.3"
        elif "1.4" in path:
            return "2.16.156.10011.2.5.1.4"
        elif "1.1.3" in path:
            return "2.16.156.10011.1.3"
        elif "1.1.4" in path:
            return "2.16.156.10011.1.4"
        elif "1.1.5" in path:
            return "2.16.156.10011.1.5"
        elif "1.1.10" in path:
            return "2.16.156.10011.1.10"
        elif "1.1.12" in path:
            return "2.16.156.10011.1.12"
        elif "1.1.19" in path:
            return "2.16.156.10011.1.19"
        elif "1.1.21" in path:
            return "2.16.156.10011.1.21"
        elif "1.1.22" in path:
            return "2.16.156.10011.1.22"
        elif "1.1.26" in path:
            return "2.16.156.10011.1.26"
        elif "1.1.27" in path:
            return "2.16.156.10011.1.27"
        elif "1.1.28" in path:
            return "2.16.156.10011.1.28"
        else:
            return "2.16.156.10011.2.5.1.1"
    
    # 时间相关
    if key == "value" and ("time" in path_lower or "date" in path_lower):
        return SAMPLE_DATA["timestamp"]
    if key == "creationTime":
        return SAMPLE_DATA["timestamp"]
    
    # 名称相关
    if key == "value" and "name" in path_lower:
        if "patient" in path_lower:
            return SAMPLE_DATA["patient_name"]
        elif "doctor" in path_lower or "person" in path_lower:
            return SAMPLE_DATA["doctor_name"]
        elif "dept" in path_lower:
            return SAMPLE_DATA["dept_name"]
        elif "hospital" in path_lower:
            return SAMPLE_DATA["hospital_name"]
        elif "medicine" in path_lower or "drug" in path_lower:
            return SAMPLE_DATA["medicine_name"]
        else:
            return "示例名称"
    
    # 文本内容
    if key == "text" or key == "value":
        if "order" in path_lower:
            return SAMPLE_DATA["order_content"]
        elif "note" in path_lower or "remark" in path_lower:
            return "请注意观察患者反应，如有不适及时处理"
        elif "result" in path_lower:
            return "查询成功，找到相关记录"
        elif "description" in path_lower:
            return "示例描述内容"
        else:
            return "示例值"
    
    # 状态码
    if key == "code":
        if "status" in path_lower:
            return "active"
        elif "gender" in path_lower:
            return SAMPLE_DATA["gender_code"]
        else:
            return "01"
    
    # 显示名称
    if key == "displayName":
        return "示例显示名称"
    
    # 电话
    if "telecom" in path_lower or "phone" in path_lower:
        return SAMPLE_DATA["phone"]
    
    # 性别
    if "gender" in path_lower:
        return SAMPLE_DATA["gender_name"]
    
    # 出生日期
    if "birth" in path_lower:
        return SAMPLE_DATA["birth_date"]
    
    # 身份证
    if "idcard" in path_lower or "identity" in path_lower:
        return SAMPLE_DATA["id_card"]
    
    # 默认值
    return "示例值"


def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 添加示例值
        updated_data = add_values_to_json(data)
        
        # 写回文件
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"  错误: {e}")
        return False


def main():
    # 获取所有测试数据文件
    test_files = sorted(glob.glob("test-data/clean_*.json"))
    
    print(f"找到 {len(test_files)} 个测试数据文件")
    print()
    
    success_count = 0
    fail_count = 0
    
    for filepath in test_files:
        filename = os.path.basename(filepath)
        
        # 检查当前value数量
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            old_count = content.count('"value"')
        
        # 处理文件
        if process_file(filepath):
            # 检查更新后的value数量
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                new_count = content.count('"value"')
            
            print(f"✓ {filename}: {old_count} -> {new_count} 个value")
            success_count += 1
        else:
            print(f"✗ {filename}: 处理失败")
            fail_count += 1
    
    print()
    print(f"处理完成: 成功 {success_count} 个, 失败 {fail_count} 个")


if __name__ == '__main__':
    main()
