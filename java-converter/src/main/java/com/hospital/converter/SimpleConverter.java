package com.hospital.converter;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import javax.xml.parsers.*;
import javax.xml.transform.*;
import javax.xml.transform.dom.*;
import javax.xml.transform.stream.*;
import org.w3c.dom.*;
import org.xml.sax.InputSource;

/**
 * 医院信息平台 JSON/XML 互转工具（简化版）
 * 不依赖外部库，仅使用JDK内置类
 */
public class SimpleConverter {

    /**
     * JSON转XML
     */
    public static String jsonToXml(String json) throws Exception {
        StringBuilder xml = new StringBuilder();
        xml.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
        
        // 移除JSON外层大括号
        json = json.trim();
        if (json.startsWith("{") && json.endsWith("}")) {
            json = json.substring(1, json.length() - 1).trim();
        }
        
        parseJsonToXml(json, xml, 0);
        return xml.toString();
    }

    private static void parseJsonToXml(String json, StringBuilder xml, int indent) {
        String indentStr = "  ".repeat(indent);
        String[] lines = json.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");
        
        for (String line : lines) {
            line = line.trim();
            if (line.isEmpty()) continue;
            
            int colonIndex = findColonIndex(line);
            if (colonIndex == -1) continue;
            
            String key = line.substring(0, colonIndex).trim().replace("\"", "");
            String value = line.substring(colonIndex + 1).trim();
            
            // 跳过元数据字段
            if (key.startsWith("_")) continue;
            
            if (value.startsWith("{")) {
                // 对象
                xml.append(indentStr).append("<").append(key).append(">\n");
                String inner = extractObject(value);
                parseJsonToXml(inner, xml, indent + 1);
                xml.append(indentStr).append("</").append(key).append(">\n");
            } else if (value.startsWith("[")) {
                // 数组
                String[] items = extractArrayItems(value);
                for (String item : items) {
                    xml.append(indentStr).append("<").append(key).append(">\n");
                    if (item.trim().startsWith("{")) {
                        String inner = extractObject(item);
                        parseJsonToXml(inner, xml, indent + 1);
                    } else {
                        xml.append(indentStr).append("  ").append(escapeXml(item.trim().replace("\"", ""))).append("\n");
                    }
                    xml.append(indentStr).append("</").append(key).append(">\n");
                }
            } else {
                // 值
                String cleanValue = value.replace("\"", "").replace("null", "");
                if (!cleanValue.isEmpty()) {
                    xml.append(indentStr).append("<").append(key).append(">").append(escapeXml(cleanValue)).append("</").append(key).append(">\n");
                }
            }
        }
    }

    private static int findColonIndex(String s) {
        boolean inQuotes = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') inQuotes = !inQuotes;
            if (c == ':' && !inQuotes) return i;
        }
        return -1;
    }

    private static String extractObject(String s) {
        int start = s.indexOf('{');
        int end = s.lastIndexOf('}');
        if (start >= 0 && end > start) {
            return s.substring(start + 1, end);
        }
        return s;
    }

    private static String[] extractArrayItems(String s) {
        int start = s.indexOf('[');
        int end = s.lastIndexOf(']');
        if (start >= 0 && end > start) {
            String content = s.substring(start + 1, end).trim();
            if (content.isEmpty()) return new String[0];
            return splitArrayItems(content);
        }
        return new String[]{s};
    }

    private static String[] splitArrayItems(String s) {
        List<String> items = new ArrayList<>();
        boolean inQuotes = false;
        int depth = 0;
        StringBuilder current = new StringBuilder();
        
        for (char c : s.toCharArray()) {
            if (c == '"') inQuotes = !inQuotes;
            if (!inQuotes) {
                if (c == '{' || c == '[') depth++;
                if (c == '}' || c == ']') depth--;
            }
            
            if (c == ',' && !inQuotes && depth == 0) {
                items.add(current.toString());
                current = new StringBuilder();
            } else {
                current.append(c);
            }
        }
        if (current.length() > 0) {
            items.add(current.toString());
        }
        
        return items.toArray(new String[0]);
    }

    /**
     * XML转JSON
     */
    public static String xmlToJson(String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xml)));
        
        StringBuilder json = new StringBuilder();
        json.append("{\n");
        
        Element root = doc.getDocumentElement();
        elementToJson(root, json, 1);
        
        json.append("}\n");
        return json.toString();
    }

    private static void elementToJson(Element element, StringBuilder json, int indent) {
        String indentStr = "  ".repeat(indent);
        String childIndentStr = "  ".repeat(indent + 1);
        
        // 处理属性
        NamedNodeMap attributes = element.getAttributes();
        for (int i = 0; i < attributes.getLength(); i++) {
            Node attr = attributes.item(i);
            json.append(childIndentStr).append("\"@").append(attr.getNodeName()).append("\": \"").append(escapeJson(attr.getNodeValue())).append("\",\n");
        }
        
        // 处理子元素
        NodeList children = element.getChildNodes();
        List<Element> childElements = new ArrayList<>();
        
        for (int i = 0; i < children.getLength(); i++) {
            if (children.item(i).getNodeType() == Node.ELEMENT_NODE) {
                childElements.add((Element) children.item(i));
            }
        }
        
        if (childElements.isEmpty()) {
            // 叶子节点
            String text = element.getTextContent().trim();
            if (!text.isEmpty()) {
                json.append(indentStr).append("\"").append(element.getNodeName()).append("\": \"").append(escapeJson(text)).append("\"\n");
            }
        } else {
            // 有子元素
            json.append(indentStr).append("\"").append(element.getNodeName()).append("\": {\n");
            
            for (int i = 0; i < childElements.size(); i++) {
                Element child = childElements.get(i);
                elementToJson(child, json, indent + 1);
                if (i < childElements.size() - 1) {
                    json.append(",\n");
                } else {
                    json.append("\n");
                }
            }
            
            json.append(indentStr).append("}");
        }
    }

    private static String escapeXml(String s) {
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;");
    }

    private static String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t");
    }

    /**
     * 主方法
     */
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("用法:");
            System.out.println("  JSON转XML: java SimpleConverter json2xml input.json output.xml");
            System.out.println("  XML转JSON: java SimpleConverter xml2json input.xml output.json");
            return;
        }
        
        try {
            String command = args[0];
            String inputFile = args[1];
            String outputFile = args.length > 2 ? args[2] : null;
            
            String content = new String(Files.readAllBytes(Paths.get(inputFile)), "UTF-8");
            String result;
            
            switch (command) {
                case "json2xml":
                    result = jsonToXml(content);
                    if (outputFile == null) {
                        outputFile = inputFile.replace(".json", ".xml");
                    }
                    break;
                case "xml2json":
                    result = xmlToJson(content);
                    if (outputFile == null) {
                        outputFile = inputFile.replace(".xml", ".json");
                    }
                    break;
                default:
                    System.out.println("未知命令: " + command);
                    return;
            }
            
            Files.write(Paths.get(outputFile), result.getBytes("UTF-8"));
            System.out.println("✓ 转换完成: " + outputFile);
            
        } catch (Exception e) {
            System.err.println("转换失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
