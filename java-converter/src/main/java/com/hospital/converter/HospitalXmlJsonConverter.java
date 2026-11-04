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
import org.json.*;

/**
 * 医院信息平台 JSON/XML 互转工具
 * 基于 WS/T 846-2024 标准
 */
public class HospitalXmlJsonConverter {

    /**
     * JSON转XML
     */
    public static String jsonToXml(String jsonStr, String rootElement) throws Exception {
        JSONObject json = new JSONObject(jsonStr);
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.newDocument();
        
        Element root = doc.createElement(rootElement);
        doc.appendChild(root);
        
        jsonToXmlElement(json, root, doc);
        
        TransformerFactory transformerFactory = TransformerFactory.newInstance();
        Transformer transformer = transformerFactory.newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        transformer.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
        
        StringWriter writer = new StringWriter();
        transformer.transform(new DOMSource(doc), new StreamResult(writer));
        
        return writer.toString();
    }

    private static void jsonToXmlElement(JSONObject json, Element parent, Document doc) {
        Iterator<String> keys = json.keys();
        while (keys.hasNext()) {
            String key = keys.next();
            Object value = json.get(key);
            
            if (value instanceof JSONObject) {
                Element element = doc.createElement(key);
                parent.appendChild(element);
                jsonToXmlElement((JSONObject) value, element, doc);
            } else if (value instanceof JSONArray) {
                JSONArray array = (JSONArray) value;
                for (int i = 0; i < array.length(); i++) {
                    Element element = doc.createElement(key);
                    parent.appendChild(element);
                    Object item = array.get(i);
                    if (item instanceof JSONObject) {
                        jsonToXmlElement((JSONObject) item, element, doc);
                    } else {
                        element.setTextContent(item.toString());
                    }
                }
            } else if (value != null) {
                Element element = doc.createElement(key);
                parent.appendChild(element);
                element.setTextContent(value.toString());
            }
        }
    }

    /**
     * XML转JSON
     */
    public static String xmlToJson(String xmlStr) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new InputSource(new StringReader(xmlStr)));
        
        Element root = doc.getDocumentElement();
        JSONObject json = xmlElementToJson(root);
        
        return json.toString(2);
    }

    private static JSONObject xmlElementToJson(Element element) {
        JSONObject json = new JSONObject();
        
        // 处理属性
        NamedNodeMap attributes = element.getAttributes();
        for (int i = 0; i < attributes.getLength(); i++) {
            Node attr = attributes.item(i);
            json.put("@" + attr.getNodeName(), attr.getNodeValue());
        }
        
        // 处理子元素
        NodeList children = element.getChildNodes();
        Map<String, List<Object>> childMap = new LinkedHashMap<>();
        
        for (int i = 0; i < children.getLength(); i++) {
            Node child = children.item(i);
            if (child.getNodeType() == Node.ELEMENT_NODE) {
                String childName = child.getNodeName();
                Object childValue;
                
                if (child.hasChildNodes() && child.getChildNodes().getLength() == 1 
                    && child.getChildNodes().item(0).getNodeType() == Node.TEXT_NODE) {
                    String text = child.getTextContent().trim();
                    if (text.isEmpty()) {
                        childValue = xmlElementToJson((Element) child);
                    } else {
                        childValue = text;
                    }
                } else if (child instanceof Element) {
                    childValue = xmlElementToJson((Element) child);
                } else {
                    childValue = child.getTextContent();
                }
                
                childMap.computeIfAbsent(childName, k -> new ArrayList<>()).add(childValue);
            }
        }
        
        for (Map.Entry<String, List<Object>> entry : childMap.entrySet()) {
            if (entry.getValue().size() == 1) {
                json.put(entry.getKey(), entry.getValue().get(0));
            } else {
                json.put(entry.getKey(), new JSONArray(entry.getValue()));
            }
        }
        
        // 如果只有文本内容，直接返回文本
        if (json.length() == 0 && element.getTextContent() != null) {
            return new JSONObject().put("value", element.getTextContent().trim());
        }
        
        return json;
    }

    /**
     * 批量转换目录中的文件
     */
    public static void batchConvert(String inputDir, String outputDir, boolean jsonToXml) throws Exception {
        File dir = new File(inputDir);
        File outDir = new File(outputDir);
        outDir.mkdirs();
        
        String[] extensions = jsonToXml ? new String[]{".json"} : new String[]{".xml"};
        
        for (File file : dir.listFiles()) {
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
                        System.out.println("✓ 转换成功: " + file.getName() + " -> " + outputName);
                    } catch (Exception e) {
                        System.out.println("✗ 转换失败: " + file.getName() + " - " + e.getMessage());
                    }
                }
            }
        }
    }

    /**
     * 主方法
     */
    public static void main(String[] args) {
        if (args.length < 3) {
            System.out.println("用法:");
            System.out.println("  JSON转XML: java HospitalXmlJsonConverter json2xml input.json output.xml");
            System.out.println("  XML转JSON: java HospitalXmlJsonConverter xml2json input.xml output.json");
            System.out.println("  批量转换: java HospitalXmlJsonConverter batch inputDir outputDir [json2xml|xml2json]");
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
