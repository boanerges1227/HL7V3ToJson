#!/bin/bash

# 医院信息平台 JSON/XML 互转工具

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JAVA_DIR="$SCRIPT_DIR/src/main/java/com/hospital/converter"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 使用说明
usage() {
    echo -e "${YELLOW}医院信息平台 JSON/XML 互转工具${NC}"
    echo ""
    echo "用法:"
    echo "  $0 json2xml <input.json> [output.xml]"
    echo "  $0 xml2json <input.xml> [output.json]"
    echo "  $0 batch <inputDir> <outputDir> [json2xml|xml2json]"
    echo ""
    echo "示例:"
    echo "  $0 json2xml test-data/order_create_request.json output.xml"
    echo "  $0 xml2json test-data/sample.xml output.json"
    echo "  $0 batch test-data xml-output json2xml"
    echo ""
}

# 检查Java是否安装
check_java() {
    if ! command -v java &> /dev/null; then
        echo -e "${RED}错误: 未找到 Java，请先安装 Java${NC}"
        exit 1
    fi
}

# 编译
compile() {
    echo -e "${YELLOW}编译转换器...${NC}"
    cd "$JAVA_DIR"
    javac SimpleConverter.java 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 编译成功${NC}"
    else
        echo -e "${RED}✗ 编译失败${NC}"
        exit 1
    fi
}

# JSON转XML
json2xml() {
    local input="$1"
    local output="$2"
    
    if [ ! -f "$input" ]; then
        echo -e "${RED}错误: 输入文件不存在: $input${NC}"
        exit 1
    fi
    
    if [ -z "$output" ]; then
        output="${input%.json}.xml"
    fi
    
    cd "$JAVA_DIR"
    java SimpleConverter json2xml "$input" "$output"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 转换完成: $output${NC}"
    else
        echo -e "${RED}✗ 转换失败${NC}"
        exit 1
    fi
}

# XML转JSON
xml2json() {
    local input="$1"
    local output="$2"
    
    if [ ! -f "$input" ]; then
        echo -e "${RED}错误: 输入文件不存在: $input${NC}"
        exit 1
    fi
    
    if [ -z "$output" ]; then
        output="${input%.xml}.json"
    fi
    
    cd "$JAVA_DIR"
    java SimpleConverter xml2json "$input" "$output"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 转换完成: $output${NC}"
    else
        echo -e "${RED}✗ 转换失败${NC}"
        exit 1
    fi
}

# 批量转换
batch() {
    local input_dir="$1"
    local output_dir="$2"
    local direction="$3"
    
    if [ ! -d "$input_dir" ]; then
        echo -e "${RED}错误: 输入目录不存在: $input_dir${NC}"
        exit 1
    fi
    
    mkdir -p "$output_dir"
    
    cd "$JAVA_DIR"
    java SimpleConverter batch "$input_dir" "$output_dir" "$direction"
}

# 主函数
main() {
    check_java
    
    if [ $# -lt 1 ]; then
        usage
        exit 1
    fi
    
    local command="$1"
    shift
    
    case "$command" in
        json2xml)
            compile
            json2xml "$@"
            ;;
        xml2json)
            compile
            xml2json "$@"
            ;;
        batch)
            compile
            batch "$@"
            ;;
        *)
            echo -e "${RED}未知命令: $command${NC}"
            usage
            exit 1
            ;;
    esac
}

main "$@"
