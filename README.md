# disa-endpoint-data-interoperability
Endpoint Security Minimum Data Standards Technical Guide

In support of the Department of Defense (DoD) Chief Information Officer (CIO) and United States Cyber Command, DISA Program Executive Office (PEO) Cyber has developed the worksheets contained in this Excel spreadsheet.  The worksheets extend guidance provided in Tab B to the DoD Chief Information Security Officer memorandum, “Endpoint Security Minimum Data Standards and Endpoint Security Criteria,” released on 9 July 2023. The primary objective of this release is to ensure that critical endpoint, device, and compliance data can be consistently represented, cross-referenced, and exchanged, enabling robust asset management and compliance tracking within complex enterprise environments.

Guidance is provided in six Excel worksheets.

The first worksheet, the Master Device Endpoint Record (MDER) Metadata Name Assignment and Formatting worksheet, catalogs over 700 unique data elements across seven primary categories—including network, hardware, software, operational context, user data, security products, and vulnerability/compliance information. The worksheet specifies the data labels and their intended mappings to the Tab B described data requirements.

The second resource is a set of four sample XML-based asset inventory worksheets demonstrating a minimum of one, each, of the data constructs described in MDER worksheets.  The worksheets contain real-world representative device, configuration, compliance, and vulnerability data using the DOD Assessment Results Format (ARF) XML structure. This file is designed to demonstrate how diverse cybersecurity data types, ranging from device hardware and software inventory to patch status and open ports, can be encoded into ARF documents that will successfully process into the existing Continuous Monitoring and Risk Scoring (CMRS) system.

"Report Header Data" is not specifically addressed in the Metadata Name Assignment and Formatting worksheet, but is required for successful processing of data in CMRS.  Parties that are planning to send data to CMRS are requested to coordinate with the CMRS team to register their product as a known "Sensor Type" and to implement appropriate processing logic based on the expected publishing implementation.
