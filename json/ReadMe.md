# ReadMe

## Endpoint Security Minimum Data Standards Cross Reference Detailed Implementation Guidance

### Purpose:

In support of the Department of Defense (DoD) Chief Information Officer (CIO) and United States Cyber Command, DISA Program Executive Office (PEO) Cyber has developed the worksheets contained in this Excel spreadsheet.  The worksheets extend guidance provided in Tab B to the DoD Chief Information Security Officer memorandum, “Endpoint Security Minimum Data Standards and Endpoint Security Criteria,” released on 9 July 2023. The primary objective of this release is to ensure that critical endpoint, device, and compliance data can be consistently represented, cross-referenced, and exchanged, enabling robust asset management and compliance tracking within complex enterprise environments.

Guidance is provided in six Excel worksheets.

The first worksheet, the Master Device Endpoint Record (MDER) Metadata Name Assignment and Formatting worksheet, catalogs over 700 unique data elements across seven primary categories—including network, hardware, software, operational context, user data, security products, and vulnerability/compliance information. The worksheet specifies the data labels and their intended mappings to the Tab B described data requirements.

The second resource is a set of four sample XML-based asset inventory worksheets demonstrating a minimum of one, each, of the data constructs described in MDER worksheets.  The worksheets contain real-world representative device, configuration, compliance, and vulnerability data using the DOD Assessment Results Format (ARF) XML structure. This file is designed to demonstrate how diverse cybersecurity data types, ranging from device hardware and software inventory to patch status and open ports, can be encoded into ARF documents that will successfully process into the existing Continuous Monitoring and Risk Scoring (CMRS) system.

"Report Header Data" is not specifically addressed in the Metadata Name Assignment and Formatting worksheet, but is required for successful processing of data in CMRS.  Parties that are planning to send data to CMRS are requested to coordinate with the CMRS team to register their product as a known "Sensor Type" and to implement appropriate processing logic based on the expected publishing implementation.

## Metadata Name Assignment and Formatting Guide Document Structure

The spreadsheet contains two main sheets:

### Sheet 1: "MDER Endpoint Data" (733 records, 15 columns)

The MDER Endpoint Data worksheet is the primary data specification with columns for ID tracking, data categorization, ARF object mapping, and implementation guidance

Key columns: ID, Data Category, Data Set, MDER Data Element, ARF Class/Object, Object Property, Example Entry, BBD Reference, Guidance

### Data Categories (7 Primary Categories)

#### 1. Network Configuration (99 records)

Network Interfaces, Fully Qualified Domain Name (FQDN), Network Functions, Listening Ports

#### 2. Hardware Configuration (108 records)

Motherboard, CPU, BIOS, Memory, Physical/Logical Disks, Trusted Platform Module

Operating System,

Virtualization Status, USB Devices, Device Inventory Status

USCYBERCOM Category, Up Time

#### 3. Software Configuration (134 records)

Applications (Extended & Basic Reporting)

Patches

Security Configuration Data for Microsoft Exchange, Web Servers

#### 4. Operational Context (45 records)

Cyber Operational Attribute Management (COAMS) Tags

#### 5. User Data (6 records)

User and account specific data elements

#### 6. Security Product Configuration (317 records - largest category)

Management Agent

Anti-Malware

Host Firewall

Host Behavioral IPS

Logical USB Port Control

Application Whitelisting

Software/Patch Inventory and Deployment

Compliance Assessment

STIG and other Benchmark Compliance , Vulnerability Scanning

PKI Trust Roots, Local Administrator Password

#### 7. Vulnerability and Compliance (24 records)

Vulnerability Results, General Compliance Results

## XML Encoding Tabs

The worksheets with the "XML_" prefix  demonstrate the encoding of data elements defined in the MDER Metadata Name Assignment and Formatting Guide document into XML-valid data structures that can be ingested into the existing CMRS system.

### Sheet Breakdown:

#### 1. Device Sheet (617 rows)

Purpose: Show encoding of MDER-defined data elements into an ARF XML document that can be ingested into the existing CMRS system

Content: Production-representative sample data from multiple vendor products encoded into schema-valid ARF XML data structures

Topic: A single asset baseline document containing at least one, each, of the distinct encoding samples for MDER data elements and attributes appropriate for a “managed asset” ARF XML document

#### 2. OSStig Sheet (45 rows)

Purpose: Demonstrate encoding of Operating System Security Technical Implementation Guide (STIG) compliance data

Content: Security Technical Implementation Guide assessment results

Focus: OS-level security configuration compliance as an example of how to encode STIG and other common benchmark results into a Benchmark ARF XML document

#### 3. PatchComp Sheet (46 rows)

Purpose: Demonstrate encoding of Patch compliance and vulnerability assessment results

Content: Software patch compliance results

Focus: Example of how to encode patch compliance data into a Benchmark ARF XML document

#### 4. OpenPorts Sheet (39 rows)

Purpose: Demonstrate encoding of discovered exposed network ports, listening services, and source executables as a benchmark-encoded inventory

Content: Open port discovery, network service enumeration, and source executables encoded as an “informational” benchmark ARF XML document

Focus: Example of how to encode listening service data into an informational benchmark document in ARF XML

### XML Namespace Structure:

The XML documents is composed of multiple sub-schemas, from the OASIS Web Service Notification schema and from the “NetD” schemas developed by the NSA as chartered by the DOD CND Architect:

<Notify xmlns:xsd="http://www.w3.org/2001/XMLSchema"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xmlns="http://docs.oasis-open.org/wsn/b-2"

xmlns:device="http://metadata.dod.mil/mdr/ns/netops/shared_data/device/0.41"

xmlns:ar="http://metadata.dod.mil/mdr/ns/netops/shared_data/assessment_report/0.41"

xmlns:cpe="http://scap.nist.gov/schema/cpe-record/0.1"

xmlns:tagged_value="http://metadata.dod.mil/mdr/ns/netops/shared_data/tagged_value/0.41"

xmlns:cndc="http://metadata.dod.mil/mdr/ns/netops/net_defense/cnd-core/0.41">

### Key Cybersecurity Frameworks Identified:

OASIS Web Services Notification (WSN): Event notification framework (docs.oasis-open.org/wsn/b-2)

DoD Metadata Standards: Military network operations data structures (metadata.dod.mil/mdr/ns/netops/)

SCAP (Security Content Automation Protocol): NIST vulnerability assessment framework (scap.nist.gov)

CPE (Common Platform Enumeration): Standardized platform identification (cpe.mitre.org)

OVAL: Vulnerability assessment language (oval.mitre.org)

XCCDF: Security configuration checklists (checklists.nist.gov/xccdf)

### Data Structure Pattern:

Each sheet follows a consistent 4-column structure:

#### 1. Row Number - Sequential identifier

#### 2. Comments - Human-readable annotations (as required)

#### 3. DD Ref - Reference numbers to source rows in the MDER Metadata Name Assignment and Formatting Guide

#### 4. XML - Structured cybersecurity data in ARF XML format.  The XML column is created with the intent that it can be copied and pasted into a text document, saved with a .xml extension, and can be ingested into the current CMRS system without error.  When testing, note the "device" level timestamps must be within the last 30 days for CMRS to process an XML document.  Also, when ingesting a document containing a new device, the Pre-Ingest Correlation Engine (PICE) application must be manually run for the new device to show in the user interface.

### Approved for Public Release; Distribution Unlimited. Public Release Case Number 25-2707

© 2025 The MITRE Corporation.

### This technical data deliverable was developed using contract funds under Basic Contract No. W56KGU-18-D-0004.

### Acknowledgements

The authors would like to acknowledge the contributions of Joe Wolfkiel, Endpoint SCM Engineering Lead, DISA. Joe will serve as the primary point of contact for all matters related to this product.

