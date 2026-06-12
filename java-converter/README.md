# 医院信息平台 JSON/XML 互转工具

基于 **WS/T 846-2024** 标准，实现 JSON 和 XML 格式的互相转换。

## 功能特性

- JSON 转 XML
- XML 转 JSON
- 批量转换目录中的文件
- 支持 HL7/CDA 消息格式
- 自动跳过元数据字段（以 `_` 开头的字段）

## 文件说明

| 文件 | 说明 |
|------|------|
| `HospitalConverter.java` | 主转换器（推荐使用） |
| `SimpleConverter.java` | 简化版转换器 |
| `converter.sh` | Shell 脚本封装 |

## 编译和运行

### 编译

```bash
cd java-converter/src/main/java
javac com/hospital/converter/HospitalConverter.java
```

### JSON转XML

```bash
java com.hospital.converter.HospitalConverter json2xml input.json output.xml [rootElement]
```

### XML转JSON

```bash
java com.hospital.converter.HospitalConverter xml2json input.xml output.json
```

### 批量转换

```bash
# JSON转XML
java com.hospital.converter.HospitalConverter batch test-data xml-output json2xml

# XML转JSON
java com.hospital.converter.HospitalConverter batch xml-output json-output xml2json
```

## 使用示例

### 单文件转换

```bash
cd java-converter/src/main/java

# JSON转XML
java com.hospital.converter.HospitalConverter json2xml \
  ../../../../test-data/clean_医嘱开立请求_POOR_IN200901UV.json \
  /tmp/output.xml

# XML转JSON
java com.hospital.converter.HospitalConverter xml2json \
  /tmp/output.xml \
  /tmp/output.json
```

### 批量转换测试数据

```bash
cd java-converter/src/main/java

# 将 test-data 目录下所有 JSON 文件转换为 XML
mkdir -p ../../../../xml-output
java com.hospital.converter.HospitalConverter batch \
  ../../../../test-data \
  ../../../../xml-output \
  json2xml

# 将 xml-output 目录下所有 XML 文件转换为 JSON
mkdir -p ../../../../json-output
java com.hospital.converter.HospitalConverter batch \
  ../../../../xml-output \
  ../../../../json-output \
  xml2json
```

## 转换示例

### 输入 JSON

```json
{
  "messageHeader": {
    "id": {
      "root": "2.16.156.10011.2.5.1.1",
      "extension": "MSG-001"
    },
    "creationTime": "20241010110000"
  },
  "patient": {
    "name": "张三",
    "gender": "M"
  }
}
```

### 输出 XML

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<root>
  <messageHeader>
    <id>
      <root>2.16.156.10011.2.5.1.1</root>
      <extension>MSG-001</extension>
    </id>
    <creationTime>20241010110000</creationTime>
  </messageHeader>
  <patient>
    <name>张三</name>
    <gender>M</gender>
  </patient>
</root>
```

## 支持的特性

- 嵌套对象
- 数组/列表
- 文本值
- 空元素处理
- 元数据字段自动跳过（`_description`, `_cardinality` 等）

## 注意事项

1. JSON 中以 `_` 开头的字段会被忽略
2. XML 中的属性在转换时会丢失（当前版本不支持属性）
3. 数组在 XML 中会重复同名元素
4. 空值会被忽略

## 测试

使用 `test-data/` 目录下的测试文件进行转换测试：

```bash
cd java-converter/src/main/java

# 测试单个文件
java com.hospital.converter.HospitalConverter json2xml \
  ../../../../test-data/clean_医嘱开立请求_POOR_IN200901UV.json \
  /tmp/test.xml

# 验证转换结果
cat /tmp/test.xml
```
