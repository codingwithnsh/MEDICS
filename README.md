
# Medics Software

## Table of Contents
1. [Introduction](#1-introduction)
2. [Features](#2-features)
3. [System Requirements](#3-system-requirements)
4. [Installation Guide](#4-installation-guide)
5. [Usage Instructions](#5-usage-instructions)
6. [Screenshots](#6-screenshots)
7. [API Reference](#7-api-reference)
8. [Troubleshooting](#8-troubleshooting)
9. [Testing](#9-testing)
10. [Deployment](#10-deployment)
11. [Roadmap](#11-roadmap)
12. [License](#12-license)
13. [Contact](#13-contact)
14. [Contribution Guide](#14-contribution-guide)
15. [FAQs](#15-faqs)

## 1. Introduction
The Medics software is a medical management system designed to help patients and doctors manage medical information effectively. It allows patients to enter their diagnoses, schedule appointments, and provides doctors with an overview of their patients.

## 2. Features
- Patient login and registration
- Doctor login and management
- Diagnosis submission
- Appointment scheduling
- Data stored in Excel format
- User-friendly interface

## 3. System Requirements
- Python 3.7 or higher
- pandas library
- openpyxl library
- Excel installed (for viewing Excel files)

## 4. Installation Guide
Follow these steps to install and run the Medics software on your local machine.

### 4.1 Clone the Repository
First, clone the repository to your local machine using the following command:
```bash
git clone https://github.com/username/medics.git
```

### 4.2 Install Dependencies
Navigate into the project directory and install the required Python packages:
```bash
cd medics
pip install -r requirements.txt
```
Alternatively, you can manually install dependencies:
```bash
pip install pandas openpyxl
```

### 4.3 Database Setup
Ensure that you have the necessary Excel files (patients.xlsx and doctors.xlsx) in the root directory. If not, create them manually or run the following script to generate template files:
```bash
python setup_database.py
```

## 5. Usage Instructions
To start the application, run the following command in your terminal:
```bash
python main.py
```

Follow the prompts to log in or register as a patient or doctor. Patients can submit their diagnoses and schedule appointments, while doctors can view patient information.

## 6. Screenshots
![Login Screen](Images/login%20screen.png)
![Patient Dashboard](Images/patient%20dashboard.png)
![Doctor Dashboard](Images/doctor%20dashboard.png)

## 7. API Reference
### Authentication API
- **Endpoint:** `/api/auth`
- **Methods:** `POST`
- **Request Body:** `{ "username": "user", "password": "pass" }`

### Diagnosis Submission API
- **Endpoint:** `/api/diagnosis`
- **Methods:** `POST`
- **Request Body:** `{ "diagnosis": "diagnosis details", "patient_id": "id" }`

## 8. Troubleshooting
If you encounter issues, try the following steps:
- Ensure all dependencies are installed correctly.
- Check the Excel file paths in the configuration.
- Review the logs for error messages.

## 9. Testing
To run the tests for the Medics software, use the following command:
```bash
pytest
```

Ensure that you have pytest installed:
```bash
pip install pytest
```

## 10. Deployment
To deploy the Medics software, ensure the necessary dependencies are installed and follow the setup instructions for your environment.

## 11. Roadmap
- [ ] Add mobile compatibility
- [ ] Improve user interface
- [ ] Implement cloud storage for data

## 12. License
This project is licensed. See the [LICENSE](LICENSE.md) file for more details.

## 13. Contact
For any inquiries, please contact:
- Email: your_email@example.com

## 14. Contribution Guide
We welcome contributions to the **Medics** project! If you’d like to contribute, please follow these steps:

1. **Fork the Repository**: Click on the "Fork" button on the top right of the repository page.
2. **Clone Your Fork**: Use the following command to clone your forked repository to your local machine:
   ```bash
   git clone https://github.com/your-username/medics.git
   ```
3. **Create a Branch**: Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-branch-name
   ```
4. **Make Changes**: Implement your feature or bug fix.
5. **Commit Changes**: Commit your changes with a descriptive message:
   ```bash
   git commit -m "Add feature/bug fix description"
   ```
6. **Push Changes**: Push your changes to your forked repository:
   ```bash
   git push origin feature-branch-name
   ```
7. **Create a Pull Request**: Go to the original repository and create a pull request.

## 15. FAQs
**Q1: How do I reset my password?**  
A1: Currently, the system does not support password recovery. Please contact your doctor or system administrator to reset your password.

**Q2: Can I run this software on any operating system?**  
A2: Yes, the Medics software is compatible with Windows, macOS, and Linux.

**Q3: How is my data stored?**  
A3: All patient and doctor data are stored in Excel files. Ensure these files are backed up regularly to prevent data loss.

**Q4: Is there a mobile version of the application?**  
A4: Currently, the Medics software is desktop-based. Future updates may include mobile compatibility.
