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
 * 医院信息平台 JSON/XML 互转工具
 * 基于 WS/T 846-2024 标准
 */
public class HospitalConverter {

    private static final List<String> SKIPPED_KEYS = Arrays.asList("_description", "_cardinality", "_required", 
        "_format", "_dataElement", "_allowedValues", "_fixedValue", "_type", "_itemDescription");

    /**
     * JSON字符串解析为Map
     */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> parseJson(String json) {
        json = json.trim();
        if (json.startsWith("{") && json.endsWith("}")) {
            json = json.substring(1, json.length() - 1);
        }
        return parseJsonObject(json);
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> parseJsonObject(String json) {
        Map<String, Object> map = new LinkedHashMap<>();
        List<String> pairs = splitJsonPairs(json);
        
        for (String pair : pairs) {
            int colonIdx = findColon(pair);
            if (colonIdx == -1) continue;
            
            String key = pair.substring(0, colonIdx).trim().replace("\"", "");
            String value = pair.substring(colonIdx + 1).trim();
            
            if (shouldSkip(key)) continue;
            
            map.put(key, parseJsonValue(value));
        }
        return map;
    }

    private static Object parseJsonValue(String value) {
        value = value.trim();
        
        if (value.equals("null")) return null;
        if (value.equals("true")) return true;
        if (value.equals("false")) return false;
        
        if (value.startsWith("\"") && value.endsWith("\"")) {
            return value.substring(1, value.length() - 1);
        }
        
        if (value.startsWith("{")) {
            return parseJsonObject(extractBraces(value));
        }
        
        if (value.startsWith("[")) {
            return parseJsonArray(value);
        }
        
        try {
            if (value.contains(".")) return Double.parseDouble(value);
            return Long.parseLong(value);
        } catch (NumberFormatException e) {
            return value;
        }
    }

    @SuppressWarnings("unchecked")
    private static List<Object> parseJsonArray(String array) {
        List<Object> list = new ArrayList<>();
        array = array.trim();
        if (array.startsWith("[") && array.endsWith("]")) {
            array = array.substring(1, array.length() - 1).trim();
        }
        if (array.isEmpty()) return list;
        
        List<String> items = splitArrayItems(array);
        for (String item : items) {
            list.add(parseJsonValue(item.trim()));
        }
        return list;
    }

    private static List<String> splitJsonPairs(String json) {
        List<String> pairs = new ArrayList<>();
        boolean inQuotes = false;
        boolean inBraces = false;
        int braceCount = 0;
        StringBuilder current = new StringBuilder();
        
        for (int i = 0; i < json.length(); i++) {
            char c = json.charAt(i);
            
            if (c == '"') {
                inQuotes = !inQuotes;
                current.append(c);
            } else if (!inQuotes) {
                if (c == '{') {
                    inBraces = true;
                    braceCount++;
                    current.append(c);
                } else if (c == '}') {
                    braceCount--;
                    if (braceCount == 0) inBraces = false;
                    current.append(c);
                } else if (c == ',' && !inBraces && braceCount == 0) {
                    pairs.add(current.toString());
                    current = new StringBuilder();
                } else {
                    current.append(c);
                }
            } else {
                current.append(c);
            }
        }
        if (current.length() > 0) {
            pairs.add(current.toString());
        }
        return pairs;
    }

    private static List<String> splitArrayItems(String array) {
        List<String> items = new ArrayList<>();
        boolean inQuotes = false;
        boolean inBraces = false;
        int braceCount = 0;
        StringBuilder current = new StringBuilder();
        
        for (int i = 0; i < array.length(); i++) {
            char c = array.charAt(i);
            
            if (c == '"') {
                inQuotes = !inQuotes;
                current.append(c);
            } else if (!inQuotes) {
                if (c == '{') {
                    inBraces = true;
                    braceCount++;
                    current.append(c);
                } else if (c == '}') {
                    braceCount--;
                    if (braceCount == 0) inBraces = false;
                    current.append(c);
                } else if (c == ',' && !inBraces && braceCount == 0) {
                    items.add(current.toString());
                    current = new StringBuilder();
                } else {
                    current.append(c);
                }
            } else {
                current.append(c);
            }
        }
        if (current.length() > 0) {
            items.add(current.toString());
        }
        return items;
    }

    private static String extractBraces(String s) {
        int start = s.indexOf('{');
        int end = findMatchingBrace(s, start);
        return s.substring(start + 1, end);
    }

    private static int findMatchingBrace(String s, int start) {
        int count = 0;
        for (int i = start; i < s.length(); i++) {
            if (s.charAt(i) == '{') count++;
            if (s.charAt(i) == '}') {
                count--;
                if (count == 0) return i;
            }
        }
        return s.length() - 1;
    }

    private static int findColon(String s) {
        boolean inQuotes = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '"') inQuotes = !inQuotes;
            if (c == ':' && !inQuotes) return i;
        }
        return -1;
    }

    private static boolean shouldSkip(String key) {
        return SKIPPED_KEYS.contains(key);
    }

    /**
     * Map转XML
     */
    public static String mapToXml(Map<String, Object> map, String rootElement) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.newDocument();
        
        Element root = doc.createElement(rootElement);
        doc.appendChild(root);
        
        mapToXmlElement(map, root, doc);
        
        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer transformer = transformerFactory.newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        transformer.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
        
        StringWriter writer = new StringWriter();
        transformer.transform(new DOMSource(doc), new StreamResult(writer));
        
        return writer.toString();
    }

    @SuppressWarnings("unchecked")
    private static void mapToXmlElement(Map<String, Object> map, Element parent, Document doc) {
        for (Map.Entry<String, Object> entry : map.entrySet()) {
            String key = entry.getKey();
            Object value = entry.getValue();
            
            if (value instanceof Map) {
                Element element = doc.createElement(key);
                parent.appendChild(element);
                mapToXmlElement((Map<String, Object>) value, element, doc);
            } else if (value instanceof List) {
                List<Object> list = (List<Object>) value;
                for (Object item : list) {
                    Element element = doc.createElement(key);
                    parent.appendChild(element);
                    if (item instanceof Map) {
                        mapToXmlElement((Map<String, Object>) item, element, doc);
                    } else {
                        element.setTextContent(item != null ? item.toString() : "");
                    }
                }
            } else {
                Element element = doc.createElement(key);
                parent.appendChild(element);
                element.setTextContent(value != null ? value.toString() : "");
            }
        }
    }

    /**
     * XML转Map
     */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> xmlToMap(String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xml)));
        
        Element root = doc.getDocumentElement();
        return elementToMap(root);
    }

    @SuppressWarnings("unchecked")
    private static Map<String, Object> elementToMap(Element element) {
        Map<String, Object> map = new LinkedHashMap<>();
        
        NodeList children = element.getChildNodes();
        List<Element> childElements = new ArrayList<>();
        
        for (int i = 0; i < children.getLength(); i++) {
            if (children.item(i).getNodeType() == Node.ELEMENT_NODE) {
                childElements.add((Element) children.item(i));
            }
        }
        
        if (childElements.isEmpty()) {
            String text = element.getTextContent().trim();
            if (!text.isEmpty()) {
                map.put("value", text);
            }
        } else {
            Map<String, List<Object>> childMap = new LinkedHashMap<>();
            
            for (Element child : childElements) {
                String childName = child.getNodeName();
                Object childValue;
                
                if (child.getChildNodes().getLength() == 1 && 
                    child.getChildNodes().item(0).getNodeType() == Node.TEXT_NODE) {
                    String text = child.getTextContent().trim();
                    childValue = text.isEmpty() ? elementToMap(child) : text;
                } else {
                    childValue = elementToMap(child);
                }
                
                childMap.computeIfAbsent(childName, k -> new ArrayList<>()).add(childValue);
            }
            
            for (Map.Entry<String, List<Object>> entry : childMap.entrySet()) {
                if (entry.getValue().size() == 1) {
                    map.put(entry.getKey(), entry.getValue().get(0));
                } else {
                    map.put(entry.getKey(), entry.getValue());
                }
            }
        }
        
        return map;
    }

    /**
     * Map转JSON字符串
     */
    @SuppressWarnings("unchecked")
    public static String mapToJson(Map<String, Object> map, int indent) {
        StringBuilder sb = new StringBuilder();
        sb.append("{\n");
        
        List<Map.Entry<String, Object>> entries = new ArrayList<>(map.entrySet());
        for (int i = 0; i < entries.size(); i++) {
            Map.Entry<String, Object> entry = entries.get(i);
            sb.append("  ".repeat(indent));
            sb.append("\"").append(entry.getKey()).append("\": ");
            sb.append(valueToJson(entry.getValue(), indent));
            if (i < entries.size() - 1) sb.append(",");
            sb.append("\n");
        }
        
        sb.append("  ".repeat(indent - 1));
        sb.append("}");
        return sb.toString();
    }

    @SuppressWarnings("unchecked")
    private static String valueToJson(Object value, int indent) {
        if (value == null) return "null";
        if (value instanceof Boolean) return value.toString();
        if (value instanceof Number) return value.toString();
        if (value instanceof String) return "\"" + escapeJson((String) value) + "\"";
        if (value instanceof Map) return mapToJson((Map<String, Object>) value, indent + 1);
        if (value instanceof List) {
            List<Object> list = (List<Object>) value;
            StringBuilder sb = new StringBuilder("[");
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) sb.append(", ");
                sb.append(valueToJson(list.get(i), indent));
            }
            sb.append("]");
            return sb.toString();
        }
        return "\"" + escapeJson(value.toString()) + "\"";
    }

    private static String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"")
                .replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t");
    }

    /**
     * JSON转XML
     */
    public static String jsonToXml(String json, String rootElement) throws Exception {
        Map<String, Object> map = parseJson(json);
        return mapToXml(map, rootElement);
    }

    /**
     * XML转JSON
     */
    public static String xmlToJson(String xml) throws Exception {
        Map<String, Object> map = xmlToMap(xml);
        return mapToJson(map, 1);
    }

    /**
     * 批量转换
     */
    public static void batchConvert(String inputDir, String outputDir, boolean jsonToXml) throws Exception {
        File dir = new File(inputDir);
        File outDir = new File(outputDir);
        outDir.mkdirs();
        
        String[] extensions = jsonToXml ? new String[]{".json"} : new String[]{".xml"};
        
        File[] files = dir.listFiles();
        if (files == null) return;
        
        for (File file : files) {
            if (file.isFile()) {
                String name = file.getName().toLowerCase();
                boolean matches = false;
                for (String ext : extensions) {
                    if (name.endsWith(ext)) {
                        matches = true;
                        break;
                    }
                }
                
                if (matches) {
                    try {
                        String content = new String(Files.readAllBytes(file.toPath()), "UTF-8");
                        String result;
                        String outputName;
                        
                        if (jsonToXml) {
                            result = jsonToXml(content, "root");
                            outputName = file.getName().replace(".json", ".xml");
                        } else {
                            result = xmlToJson(content);
                            outputName = file.getName().replace(".xml", ".json");
                        }
                        
                        File outputFile = new File(outDir, outputName);
                        Files.write(outputFile.toPath(), result.getBytes("UTF-8"));
                        System.out.println("✓ " + file.getName() + " -> " + outputName);
                    } catch (Exception e) {
                        System.out.println("✗ " + file.getName() + ": " + e.getMessage());
                    }
                }
            }
        }
    }

    /**
     * 主方法
     */
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("医院信息平台 JSON/XML 互转工具");
            System.out.println("用法:");
            System.out.println("  java HospitalConverter json2xml input.json output.xml [rootElement]");
            System.out.println("  java HospitalConverter xml2json input.xml output.json");
            System.out.println("  java HospitalConverter batch inputDir outputDir [json2xml|xml2json]");
            return;
        }
        
        try {
            String command = args[0];
            
            switch (command) {
                case "json2xml":
                    if (args.length < 3) {
                        System.out.println("参数不足: json2xml input.json output.xml [rootElement]");
                        return;
                    }
                    String jsonContent = new String(Files.readAllBytes(Paths.get(args[1])), "UTF-8");
                    String rootElement = args.length > 3 ? args[3] : "root";
                    String xmlResult = jsonToXml(jsonContent, rootElement);
                    Files.write(Paths.get(args[2]), xmlResult.getBytes("UTF-8"));
                    System.out.println("✓ JSON转XML完成: " + args[2]);
                    break;
                    
                case "xml2json":
                    if (args.length < 3) {
                        System.out.println("参数不足: xml2json input.xml output.json");
                        return;
                    }
                    String xmlContent = new String(Files.readAllBytes(Paths.get(args[1])), "UTF-8");
                    String jsonResult = xmlToJson(xmlContent);
                    Files.write(Paths.get(args[2]), jsonResult.getBytes("UTF-8"));
                    System.out.println("✓ XML转JSON完成: " + args[2]);
                    break;
                    
                case "batch":
                    if (args.length < 3) {
                        System.out.println("参数不足: batch inputDir outputDir [json2xml|xml2json]");
                        return;
                    }
                    boolean toJson = args.length > 3 && args[3].equals("xml2json");
                    batchConvert(args[1], args[2], !toJson);
                    break;
                    
                default:
                    System.out.println("未知命令: " + command);
            }
        } catch (Exception e) {
            System.err.println("转换失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
