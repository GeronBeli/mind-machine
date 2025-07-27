# 1. Project Description: MindMachine - Project of HTW Berlin

## Vision

The **MindMachine** offers a powerful web application for secure document access, intelligent search functions, and efficient file management.

The vision of the MindMachine project is to create an intuitive and robust browser application that enables HTW users to efficiently manage their files and extract relevant information from documents using AI-powered search queries. The main goal is to develop a user-friendly platform that can be seamlessly integrated into the daily workflow of HTW users.



## Goals

The main goals of the project are:

1. **User-Friendliness:** The application should provide an easy-to-understand user interface that enables intuitive navigation and interaction. Both HTW users and administrators should be able to navigate the platform effortlessly.

2. **Efficient File Management:** HTW users should be able to efficiently open, upload, delete, and rename files in their private directory using the application. The file directory view should be individually tailored to the logged-in user.

3. **AI-Powered Search Queries:** The application should allow HTW users to ask questions in the form of text or voice prompts. The AI processes these queries, generates search requests, and displays relevant results directly in the user interface.

4. **Security and Data Protection:** The platform must comply with general security standards, especially regarding authentication via HTW logins, secure login and logout processes, and the protection of user privacy.

5. **Search and Interaction History:** The application should provide a search history for HTW users to track previous queries. The ability to navigate directly to the results of past searches contributes to efficiency and user-friendliness.

Achieving these goals will help improve the workflow of HTW users, increase efficiency in file management, and facilitate access to relevant information through AI-powered search queries.

## Contributors and Project Background

The **MindMachine** project was a collaborative effort by students of the Master's program "Computer Science in Engineering" at the University of Applied Sciences (HTW) Berlin. It was developed during the winter semester 2023/24 as part of the practice-oriented module "M4.1 Advanced Software Engineering". The aim was to enhance students' advanced computer science knowledge, deepen their software development skills, and apply modern software engineering processes in a self-managed project.

Students took on various roles within the agile process and used modern tools for requirements management, configuration management, automated testing, and project management. Special emphasis was placed on fostering teamwork in joint projects to optimally prepare students for their future careers.

The close collaboration between HTW Berlin and the students in developing **MindMachine** highlights the cooperative nature of the module. The goal was to develop innovative solutions for challenges in engineering sciences and ensure that students are well prepared for their professional future.


I served as the software architect and backend developer. After the course, I independently rewrote the entire backend (except utils package) to improve structure, maintainability, and scalability.
This rewritten backend is my own work and is suitable for production-grade applications.

# 2. Installation

**Note:** To use this application, an active internet connection and a valid HTW Berlin account are required. Manual registration is not supported, as authentication is handled via the HTW LDAP server.

The application is containerized using Docker. To get started, ensure you have Docker installed and launch the system using `docker-compose`. 
Make sure the required LDAP credentials for the HTW server are provided in the `.env` file, as these are necessary for authentication.

If you are not connected to the local HTW network, access to the LDAP server requires a VPN connection. Instructions for setting up VPN access to the HTW network can be found here:
https://rz.htw-berlin.de/anleitungen/vpn/


# 3. Acknowledgements

I would like to express my sincere gratitude to **Prof. Dr. Erik Rodner** for his invaluable guidance, support, and encouragement throughout the development of the MindMachine project.

Special thanks also go to my dedicated teammates for their collaboration and commitment.

Their teamwork and expertise were essential to the success of this project.


# 4. Licence and Copyright


```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```