# JSON示例文件目录

基于 **WS/T 846-2024** 医院信息平台交互标准的JSON示例文件。

## 目录结构

```
json-examples/
├── README.md                              # 本文件
├── 字段说明.md                            # 完整字段说明（Markdown格式）
│
├── 第2部分_个人信息/                       # 个人信息注册、查询服务
│   ├── 注册请求.json                      # PRPA_IN201311UV02
│   ├── 注册应答成功.json                   # MCCI_IN000002UV01
│   ├── 注册应答异常.json                   # MCCI_IN000002UV01
│   ├── 更新请求.json                       # PRPA_IN201314UV02
│   ├── 查询请求.json                       # PRPA_IN201305UV02
│   ├── 查询应答成功.json                   # PRPA_IN201306UV02
│   ├── 查询应答异常.json                   # PRPA_IN201306UV02
│   ├── 合并请求.json                       # PRPA_IN201304UV02
│   └── 字段说明.json                       # 字段定义
│
├── 第3部分_医疗机构/                       # 医疗卫生机构注册、查询服务
│   ├── 注册请求.json                       # PRPM_IN401030UV01
│   ├── 更新请求.json                       # PRPM_IN403010UV01
│   ├── 查询请求.json                       # PRPM_IN406010UV01
│   ├── 查询应答.json                       # PRPM_IN406110UV01
│   ├── 通用应答.json                       # MCCI_IN000002UV01
│   ├── 字段说明.json
│   └── schema.json                         # JSON Schema定义
│
├── 第4部分_医护人员/                       # 医疗卫生人员注册、查询服务
│   ├── 注册请求.json                       # PRPM_IN301010UV01
│   ├── 更新请求.json                       # PRPM_IN303010UV01
│   ├── 查询请求.json                       # PRPM_IN306010UV01
│   ├── 查询应答.json                       # PRPM_IN306011UV01
│   ├── 通用应答.json                       # MCCI_IN000002UV01
│   └── 字段说明.json
│
├── 第5部分_术语/                           # 术语注册、查询服务
│   ├── 注册请求.json                       # PRVS_IN000001UV01
│   ├── 更新请求.json                       # PRVS_IN000002UV01
│   ├── 查询请求.json                       # PRVS_IN000003UV01
│   ├── 查询应答.json                       # PRVS_IN000004UV01
│   ├── 通用应答.json                       # MCCI_IN000002UV01
│   └── 字段说明.json
│
├── 第6部分_文档/                           # 文档注册、查询服务
│   ├── 注册请求.json                       # RCMR_IN000002UV02
│   ├── 查询请求.json                       # RCMR_IN000031UV01
│   ├── 查询应答.json                       # RCMR_IN000032UV01
│   ├── 通用应答.json                       # MCCI_IN000002UV01
│   └── 字段说明.json
│
├── 第7部分_就诊信息/                       # 就诊信息交互服务
│   ├── 就诊卡新增请求.json
│   ├── 就诊卡更新请求.json
│   ├── 就诊卡查询请求.json
│   ├── 就诊卡查询应答.json
│   ├── 门诊挂号新增请求.json
│   ├── 门诊挂号更新请求.json
│   ├── 门诊挂号查询请求.json
│   ├── 门诊挂号查询应答.json
│   ├── 住院登记请求.json
│   ├── 住院更新请求.json
│   ├── 住院查询请求.json
│   ├── 住院查询应答.json
│   ├── 住院转科新增请求.json
│   ├── 住院转科更新请求.json
│   ├── 住院转科查询请求.json
│   ├── 住院转科查询应答.json
│   ├── 出院登记新增请求.json
│   ├── 出院登记更新请求.json
│   ├── 出院信息查询请求.json
│   ├── 出院信息查询应答.json
│   └── 字段说明.json
│
├── 第8部分_医嘱/                           # 医嘱信息交互服务
│   ├── 开立请求.json                       # POOR_IN200901UV
│   ├── 查询请求.json                       # QUMT_IN020030UV01
│   ├── 查询应答.json                       # QUMT_IN020040UV01
│   ├── 通用应答.json                       # MCCI_IN000002UV01
│   ├── 字段说明.json
│   └── schema.json                         # JSON Schema定义
│
├── 第10部分_预约/                          # 预约信息交互服务
│   ├── 申请请求.json                       # POOR_IN200910UV
│   ├── 申请应答.json                       # MCCI_IN000002UV01
│   ├── 取消请求.json                       # POOR_IN200911UV
│   ├── 取消应答.json                       # MCCI_IN000002UV01
│   ├── 查询请求.json                       # QUMT_IN020050UV01
│   ├── 查询应答.json                       # QUMT_IN020060UV01
│   └── 字段说明.json
│
└── 第11部分_状态/                          # 状态信息交互服务
    ├── 更新请求.json                       # POOR_IN200920UV
    ├── 更新应答.json                       # MCCI_IN000002UV01
    ├── 查询请求.json                       # QUMT_IN020070UV01
    ├── 查询应答.json                       # QUMT_IN020080UV01
    └── 字段说明.json
```

## 文件说明

### JSON示例文件（含字段说明）

每个部分的JSON示例文件包含完整的字段说明（以 `_` 开头的字段）：

| 字段 | 说明 |
|------|------|
| `_description` | 字段含义说明 |
| `_cardinality` | 基数（1..1必须唯一，0..1可选） |
| `_required` | 是否必填 |
| `_format` | 数据格式要求 |
| `_dataElement` | 对应的数据元标识符 |
| `_allowedValues` | 允许的取值及含义 |
| `_fixedValue` | 固定值 |

### 字段说明文件

每个部分都有一个 `字段说明.json` 文件，包含：
- 部分名称和标准编号
- 每个服务的消息类型标识符
- 所有字段的完整定义

### Schema文件

部分目录包含 `schema.json` 文件，用于验证JSON数据格式。

## 使用说明

### 1. 查看字段说明

```bash
# 查看第8部分医嘱的字段说明
cat json-examples/第8部分_医嘱/字段说明.json | jq .
```

### 2. 使用JSON示例

```bash
# 查看医嘱开立请求示例
cat json-examples/第8部分_医嘱/开立请求.json | jq .
```

### 3. 移除字段说明（用于测试）

```bash
# 使用Python移除_开头的字段
python3 -c "
import json, sys
data = json.load(open('json-examples/第8部分_医嘱/开立请求.json'))
def clean(obj):
    if isinstance(obj, dict):
        return {k: clean(v) for k, v in obj.items() if not k.startswith('_')}
    elif isinstance(obj, list):
        return [clean(i) for i in obj]
    return obj
json.dump(clean(data), sys.stdout, ensure_ascii=False, indent=2)
" > clean_request.json
```

## 消息类型标识符汇总

| 部分 | 服务 | 请求标识符 | 应答标识符 |
|------|------|-----------|-----------|
| 第2部分 | 个人信息注册 | PRPA_IN201311UV02 | MCCI_IN000002UV01 |
| 第2部分 | 个人信息查询 | PRPA_IN201305UV02 | PRPA_IN201306UV02 |
| 第2部分 | 个人信息更新 | PRPA_IN201314UV02 | MCCI_IN000002UV01 |
| 第2部分 | 个人信息合并 | PRPA_IN201304UV02 | MCCI_IN000002UV01 |
| 第3部分 | 机构注册 | PRPM_IN401030UV01 | MCCI_IN000002UV01 |
| 第3部分 | 机构更新 | PRPM_IN403010UV01 | MCCI_IN000002UV01 |
| 第3部分 | 机构查询 | PRPM_IN406010UV01 | PRPM_IN406110UV01 |
| 第4部分 | 人员注册 | PRPM_IN301010UV01 | MCCI_IN000002UV01 |
| 第4部分 | 人员更新 | PRPM_IN303010UV01 | MCCI_IN000002UV01 |
| 第4部分 | 人员查询 | PRPM_IN306010UV01 | PRPM_IN306011UV01 |
| 第5部分 | 术语注册 | PRVS_IN000001UV01 | MCCI_IN000002UV01 |
| 第5部分 | 术语更新 | PRVS_IN000002UV01 | MCCI_IN000002UV01 |
| 第5部分 | 术语查询 | PRVS_IN000003UV01 | PRVS_IN000004UV01 |
| 第6部分 | 文档注册 | RCMR_IN000002UV02 | MCCI_IN000002UV01 |
| 第6部分 | 文档查询 | RCMR_IN000031UV01 | RCMR_IN000032UV01 |
| 第7部分 | 门诊挂号 | PRPA_IN400001UV | MCCI_IN000002UV01 |
| 第7部分 | 住院登记 | PRPA_IN400001UV | MCCI_IN000002UV01 |
| 第7部分 | 出院登记 | PRPA_IN400003UV01 | MCCI_IN000002UV01 |
| 第8部分 | 医嘱开立 | POOR_IN200901UV | MCCI_IN000002UV01 |
| 第8部分 | 医嘱更新 | POOR_IN200902UV | MCCI_IN000002UV01 |
| 第8部分 | 医嘱查询 | QUMT_IN020030UV01 | QUMT_IN020040UV01 |
| 第10部分 | 预约申请 | POOR_IN200910UV | MCCI_IN000002UV01 |
| 第10部分 | 预约取消 | POOR_IN200911UV | MCCI_IN000002UV01 |
| 第10部分 | 预约查询 | QUMT_IN020050UV01 | QUMT_IN020060UV01 |
| 第11部分 | 状态更新 | POOR_IN200920UV | MCCI_IN000002UV01 |
| 第11部分 | 状态查询 | QUMT_IN020070UV01 | QUMT_IN020080UV01 |
