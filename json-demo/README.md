# 测试数据目录

基于 **WS/T 846-2024** 医院信息平台交互标准的测试数据文件。

## 目录结构

```
test-data/
├── 第2部分_个人信息/           # 个人信息注册、查询服务
│   ├── 注册请求.json
│   ├── 注册应答成功.json
│   ├── 注册应答异常.json
│   ├── 更新请求.json
│   ├── 查询请求.json
│   ├── 查询应答成功.json
│   ├── 查询应答异常.json
│   └── 合并请求.json
│
├── 第3部分_医疗机构/           # 医疗卫生机构注册、查询服务
│   ├── 注册请求.json
│   ├── 更新请求.json
│   ├── 查询请求.json
│   ├── 查询应答.json
│   └── 通用应答.json
│
├── 第4部分_医护人员/           # 医疗卫生人员注册、查询服务
│   ├── 注册请求.json
│   ├── 更新请求.json
│   ├── 查询请求.json
│   ├── 查询应答.json
│   └── 通用应答.json
│
├── 第5部分_术语/               # 术语注册、查询服务
│   ├── 注册请求.json
│   ├── 更新请求.json
│   ├── 查询请求.json
│   ├── 查询应答.json
│   └── 通用应答.json
│
├── 第6部分_文档/               # 文档注册、查询服务
│   ├── 注册请求.json
│   ├── 查询请求.json
│   ├── 查询应答.json
│   └── 通用应答.json
│
├── 第7部分_就诊信息/           # 就诊信息交互服务
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
│   └── 出院信息查询应答.json
│
├── 第8部分_医嘱/               # 医嘱信息交互服务
│   ├── 开立请求.json
│   ├── 查询请求.json
│   ├── 查询应答.json
│   └── 通用应答.json
│
├── 第10部分_预约/              # 预约信息交互服务
│   ├── 申请请求.json
│   ├── 申请应答.json
│   ├── 取消请求.json
│   ├── 取消应答.json
│   ├── 查询请求.json
│   └── 查询应答.json
│
├── 第11部分_状态/              # 状态信息交互服务
│   ├── 更新请求.json
│   ├── 更新应答.json
│   ├── 查询请求.json
│   └── 查询应答.json
│
└── *.json                     # 旧格式文件（保留）
```

## 使用说明

### 1. 按部分使用

```bash
# 使用第8部分医嘱开立请求进行测试
curl -X POST http://your-api/order/create \
  -H "Content-Type: application/json" \
  -d @test-data/第8部分_医嘱/开立请求.json

# 使用第2部分个人信息注册请求进行测试
curl -X POST http://your-api/patient/register \
  -H "Content-Type: application/json" \
  -d @test-data/第2部分_个人信息/注册请求.json
```

### 2. 批量测试

```bash
# 测试第8部分所有接口
for f in test-data/第8部分_医嘱/*.json; do
    echo "Testing: $f"
    curl -X POST http://your-api/test \
      -H "Content-Type: application/json" \
      -d @"$f"
done
```

## 文件命名规则

- `注册请求.json` - 新增数据的请求消息
- `注册应答成功.json` - 注册成功时的应答
- `注册应答异常.json` - 注册失败时的应答
- `更新请求.json` - 更新数据的请求消息
- `查询请求.json` - 查询数据的请求消息
- `查询应答.json` - 查询成功的应答
- `通用应答.json` - 操作成功/失败的通用应答

## 消息类型标识符

| 部分 | 服务 | 请求标识符 | 应答标识符 |
|------|------|-----------|-----------|
| 第2部分 | 个人信息注册 | PRPA_IN201311UV02 | MCCI_IN000002UV01 |
| 第2部分 | 个人信息查询 | PRPA_IN201305UV02 | PRPA_IN201306UV02 |
| 第3部分 | 机构注册 | PRPM_IN401030UV01 | MCCI_IN000002UV01 |
| 第3部分 | 机构查询 | PRPM_IN406010UV01 | PRPM_IN406110UV01 |
| 第4部分 | 人员注册 | PRPM_IN301010UV01 | MCCI_IN000002UV01 |
| 第4部分 | 人员查询 | PRPM_IN306010UV01 | PRPM_IN306011UV01 |
| 第5部分 | 术语注册 | PRVS_IN000001UV01 | MCCI_IN000002UV01 |
| 第5部分 | 术语查询 | PRVS_IN000003UV01 | PRVS_IN000004UV01 |
| 第6部分 | 文档注册 | RCMR_IN000002UV02 | MCCI_IN000002UV01 |
| 第6部分 | 文档查询 | RCMR_IN000031UV01 | RCMR_IN000032UV01 |
| 第7部分 | 门诊挂号 | PRPA_IN400001UV | MCCI_IN000002UV01 |
| 第7部分 | 住院登记 | PRPA_IN400001UV | MCCI_IN000002UV01 |
| 第7部分 | 出院登记 | PRPA_IN400003UV01 | MCCI_IN000002UV01 |
| 第8部分 | 医嘱开立 | POOR_IN200901UV | MCCI_IN000002UV01 |
| 第8部分 | 医嘱查询 | QUMT_IN020030UV01 | QUMT_IN020040UV01 |
| 第10部分 | 预约申请 | POOR_IN200910UV | MCCI_IN000002UV01 |
| 第10部分 | 预约查询 | QUMT_IN020050UV01 | QUMT_IN020060UV01 |
| 第11部分 | 状态更新 | POOR_IN200920UV | MCCI_IN000002UV01 |
| 第11部分 | 状态查询 | QUMT_IN020070UV01 | QUMT_IN020080UV01 |
