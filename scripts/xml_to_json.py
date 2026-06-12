#!/usr/bin/env python3
"""
医院信息平台交互标准 XML-to-JSON 转换脚本
基于 WS/T 846-2024 标准

用法:
    python xml_to_json.py input.xml output.json
    python xml_to_json.py --batch input_dir output_dir
"""

import sys
import os
import json
import re
import xml.etree.ElementTree as ET
from collections import OrderedDict
from typing import Any, Dict, List, Optional


class HL7XmlToJsonConverter:
    """HL7 CDA XML to JSON 转换器"""
    
    # ID根标识符的中文映射
    ID_ROOT_MAP = {
        "2.16.156.10011.2.5.1.1": "消息流水号",
        "2.16.156.10011.2.5.1.2": "消息服务标识",
        "2.16.156.10011.2.5.1.3": "系统标识",
        "2.16.156.10011.2.5.1.4": "患者编号",
        "2.16.156.10011.2.5.1.5": "域ID",
        "2.16.156.10011.2.5.1.8": "就诊次数",
        "2.16.156.10011.2.5.1.9": "就诊流水号",
        "2.16.156.10011.2.5.1.14": "药物编码体系",
        "2.16.156.10011.2.5.1.20": "资源流水号",
        "2.16.156.10011.2.5.1.29": "预约流水号",
        "2.16.156.10011.1.3": "身份证件号码",
        "2.16.156.10011.1.4": "医护人员工号",
        "2.16.156.10011.1.5": "医院编码",
        "2.16.156.10011.1.10": "门（急）诊号",
        "2.16.156.10011.1.12": "住院号",
        "2.16.156.10011.1.19": "居民健康卡号",
        "2.16.156.10011.1.21": "病房号",
        "2.16.156.10011.1.22": "病床号",
        "2.16.156.10011.1.26": "科室编码",
        "2.16.156.10011.1.27": "病区编码",
        "2.16.156.10011.1.28": "医嘱编码",
    }
    
    def convert_file(self, input_path: str, output_path: str) -> bool:
        """转换单个XML文件"""
        try:
            # 预处理XML（修复常见问题）
            xml_content = self._preprocess_xml(input_path)
            
            # 解析XML
            root = ET.fromstring(xml_content)
            
            # 转换为JSON
            json_data = self._convert_element(root)
            
            # 写入JSON文件
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 转换成功: {input_path} -> {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ 转换失败: {input_path} - {e}")
            return False
    
    def _preprocess_xml(self, file_path: str) -> str:
        """预处理XML，修复PDF提取导致的格式问题"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复属性之间缺少空格的问题
        # 例如: <idroot="..." 变为 <id root="..."
        content = re.sub(r'(<\w+)([A-Z]\w*=")', r'\1 \2', content)
        
        # 修复自闭合标签
        content = re.sub(r'/>\s*<', '/>\n<', content)
        
        # 确保有XML声明
        if not content.startswith('<?xml'):
            content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
        
        return content
    
    def _convert_element(self, elem: ET.Element) -> Any:
        """递归转换XML元素为JSON"""
        result = OrderedDict()
        
        # 处理属性
        if elem.attrib:
            for attr_name, attr_value in elem.attrib.items():
                # 转换xsi:type等特殊属性
                if attr_name.startswith('{'):
                    attr_name = attr_name.split('}')[-1]
                result[attr_name] = attr_value
        
        # 处理子元素
        children = list(elem)
        if not children:
            # 叶子节点
            if elem.text and elem.text.strip():
                if len(result) == 0:
                    return elem.text.strip()
                else:
                    result['value'] = elem.text.strip()
            elif len(result) == 1 and 'value' not in result:
                return list(result.values())[0]
            return result if result else None
        
        # 按标签名分组子元素
        grouped = OrderedDict()
        for child in children:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            child_data = self._convert_element(child)
            
            if tag in grouped:
                # 如果已存在，转换为数组
                if not isinstance(grouped[tag], list):
                    grouped[tag] = [grouped[tag]]
                grouped[tag].append(child_data)
            else:
                grouped[tag] = child_data
        
        result.update(grouped)
        return result
    
    def convert_batch(self, input_dir: str, output_dir: str):
        """批量转换目录中的所有XML文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        success_count = 0
        fail_count = 0
        
        for filename in os.listdir(input_dir):
            if filename.endswith('.xml'):
                input_path = os.path.join(input_dir, filename)
                output_filename = filename.replace('.xml', '.json')
                output_path = os.path.join(output_dir, output_filename)
                
                if self.convert_file(input_path, output_path):
                    success_count += 1
                else:
                    fail_count += 1
        
        print(f"\n批量转换完成: 成功 {success_count} 个, 失败 {fail_count} 个")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    converter = HL7XmlToJsonConverter()
    
    if sys.argv[1] == '--batch':
        # 批量转换模式
        if len(sys.argv) != 4:
            print("用法: python xml_to_json.py --batch input_dir output_dir")
            sys.exit(1)
        converter.convert_batch(sys.argv[2], sys.argv[3])
    else:
        # 单文件转换模式
        if len(sys.argv) != 3:
            print("用法: python xml_to_json.py input.xml output.json")
            sys.exit(1)
        converter.convert_file(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
