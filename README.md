# Endpoint Security Minimum Data Standards Technical Guide

In support of the Department of Defense (DoD) Chief Information Officer (CIO) and United States Cyber Command, DISA Program Executive Office (PEO) Cyber has developed the worksheets contained in this Excel spreadsheet.  The worksheets extend guidance provided in Tab B to the DoD Chief Information Security Officer memorandum, “Endpoint Security Minimum Data Standards and Endpoint Security Criteria,” released on 9 July 2023. The primary objective of this release is to ensure that critical endpoint, device, and compliance data can be consistently represented, cross-referenced, and exchanged, enabling robust asset management and compliance tracking within complex enterprise environments.

## Endpoint Security Minimum Data Standards Technical Implementation Guide v1.0

Guidance is provided in six Excel worksheets within the official ["single workbook"](/Endpoint%20Security%20Minimum%20Data%20Standards%20Technical%20Implementation%20Guide%20v1.0.xlsx).

The first worksheet, the Master Device Endpoint Record (MDER) Metadata Name Assignment and Formatting worksheet, catalogs over 700 unique data elements across seven primary categories—including network, hardware, software, operational context, user data, security products, and vulnerability/compliance information. The worksheet specifies the data labels and their intended mappings to the Tab B described data requirements.

The second resource is a set of four sample XML-based asset inventory worksheets demonstrating a minimum of one, each, of the data constructs described in MDER worksheets.  The worksheets contain real-world representative device, configuration, compliance, and vulnerability data using the DOD Assessment Results Format (ARF) XML structure. This file is designed to demonstrate how diverse cybersecurity data types, ranging from device hardware and software inventory to patch status and open ports, can be encoded into ARF documents that will successfully process into the existing Continuous Monitoring and Risk Scoring (CMRS) system.

"Report Header Data" is not specifically addressed in the Metadata Name Assignment and Formatting worksheet, but is required for successful processing of data in CMRS.  Parties that are planning to send data to CMRS are requested to coordinate with the CMRS team to register their product as a known "Sensor Type" and to implement appropriate processing logic based on the expected publishing implementation.

## XLS - Extractor

A Python CLI tool for intelligently extracting Excel sheets to JSON and Markdown formats is included in this repo. 

## Extracted Convience JSON & MarkDown Files

The XLS sheets have been extracted into [./json](./json) folders using the xls-extractor tool. Each worksheet has been converted into a corresponding JSON file to facilitate easier integration and processing in various systems. The JSON files maintain the structure and data elements of the original Excel worksheets, ensuring that all critical endpoint, device, and compliance data can be programmatically accessed and utilized in automated workflows.

``` 
$> pip install -e .
[...]
$> ./bin/xls-extractor Endpoint\ Security\ Minimum\ Data\ Standards\ Technical\ Implementation\ Guide\ v1.0.xlsx
# Alternative - Include hidden columns in extraction, and formulas into a custom output directory
$> ./bin/xls-extractor input.xlsx --include-hidden --extract-mode formulas -o ./my-output-dir/
```

The cover sheet ["README"](./json/ReadMe.md) provides additional context and instructions for using the data contained within the JSON files. 

The ["MDER"](./json/MDER.json) has been converted into JSON file that includes the *values* of the data elements as specified in the original Excel worksheet, as well as excluding the hidden columns. The JSON representation allows for seamless integration with asset management systems, enabling efficient tracking and reporting of endpoint security data across the DoD enterprise.

```json
{
  "MDER": [
    {
      "ID": "1.1.1",
      "Data_Category": "Network Configuration",
      "Data_Set": "Network Interfaces",
      "MDER_Data_Element": "Interface identifier",
      "ARF_Class/Object": "CPE Record",
      "Object_Property": "CPE String",
      "Property_Component": "Version",
      "Component_Value": "OS-assigned identifier (eth01, etc.)",
      "Example_Entry": "Ethernet_4",
      "BBD_Ref": "44",
      "Guidance": "- Use CPE encoding with preserved capitalization"
    },
    {
      "ID": "1.1.2",
      "Data_Category": "Network Configuration",
      "Data_Set": "Network Interfaces",
      "MDER_Data_Element": "MAC Address",
      "ARF_Class/Object": "CPE Record",
      "Object_Property": "Tagged String",
      "Property_Component": "Name",
      "Component_Value": "MacAddress-#",
      "Example_Entry": "MacAddress-0",
      "BBD_Ref": "46",
      "Guidance": "- Increment is a one-digit integer (0-9) \n- Increment indicates which interface configuration this item aligns to.  \n- Interfaces are numbered sequentially.  \n- Only populated if the interface has this information."
    },
    {
    ...
    },
  ]
}
```
