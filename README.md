
# Medics: A Medical Information and Appointment System

**Medics** is a comprehensive medical software built in Python that helps patients input diagnoses, retrieve medical information, and schedule appointments with doctors. The system also provides a doctor portal to view patient details and manage appointments. All data is stored in an Excel-based database for easy integration and portability.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [System Requirements](#system-requirements)
5. [Installation Guide](#installation-guide)
   1. [Clone the Repository](#clone-the-repository)
   2. [Install Dependencies](#install-dependencies)
   3. [Database Setup](#database-setup)
6. [Usage](#usage)
   1. [Running the Application](#running-the-application)
   2. [Patient Login](#patient-login)
   3. [Doctor Login](#doctor-login)
   4. [Diagnosis Submission](#diagnosis-submission)
   5. [Appointment Scheduling](#appointment-scheduling)
7. [Excel Database Structure](#excel-database-structure)
   1. [Patient Sheet](#patient-sheet)
   2. [Doctor Sheet](#doctor-sheet)
8. [Code Breakdown](#code-breakdown)
   1. [Patient Class](#patient-class)
   2. [Doctor Class](#doctor-class)
   3. [Appointment Management](#appointment-management)
9. [Error Handling and Debugging](#error-handling-and-debugging)
10. [Development Guidelines](#development-guidelines)
11. [Unit Testing](#unit-testing)
12. [Continuous Integration (CI)](#continuous-integration-ci)
13. [Known Issues](#known-issues)
14. [Contribution Guide](#contribution-guide)
15. [FAQs](#faqs)
16. [License](#license)

---

<a name="introduction"></a>

## 1. Introduction

Welcome to the **Medics** repository. This software is designed for medical professionals and patients, making it easier to diagnose conditions, view medical records, and schedule appointments. The system is built using Python, with data stored in Excel files for portability and ease of use. Whether you're a patient seeking medical information or a doctor managing appointments, **Medics** is here to simplify the process.

### Use Cases:
- Patients can log in, enter diagnoses, view medical information, and book appointments.
- Doctors can view their patients' details and manage appointments efficiently.
- Hospitals can use this system as a lightweight alternative for managing patient records.

---

<a name="features"></a>

## 2. Features

- **Patient Login and Registration**: Secure login system for patients to access their dashboard.
- **Doctor Login**: Doctors have their portal to view assigned patients and manage schedules.
- **Diagnosis Management**: Patients can enter symptoms and receive feedback on their condition.
- **Appointment Booking**: Patients can book appointments with available doctors.
- **Doctor Dashboard**: Doctors can view patient records, including their diagnoses and appointment details.
- **Excel Integration**: All data is stored in local Excel files for easy data management.
- **Error Handling**: The system includes comprehensive error handling for smoother user experience.
- **User-friendly UI**: Simple UI that caters to both patients and doctors.

---

<a name="technology-stack"></a>

## 3. Technology Stack

- **Programming Language**: Python 3.x
- **Database**: Excel (via pandas and openpyxl libraries)
- **Libraries**:
  - `pandas`: For data manipulation and Excel file interaction.
  - `openpyxl`: For Excel file handling.
  - `tkinter`: For user interface design.
- **IDE**: Compatible with all major Python IDEs (PyCharm, VSCode, etc.)

---

<a name="system-requirements"></a>

## 4. System Requirements

- **Python**: Version 3.7 or above.
- **Pandas Library**: Version 1.3.0 or above.
- **openpyxl**: Version 3.0.7 or above.
- **Operating System**: Compatible with Windows, macOS, and Linux.
- **Memory**: Minimum 512MB RAM for light usage, 1GB or more recommended.

---

<a name="installation-guide"></a>

## 5. Installation Guide

Follow these steps to install and run the Medics software on your local machine.

### 5.1 Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone https://github.com/username/medics.git
```

### 5.2 Install Dependencies

Navigate into the project directory and install the required Python packages:

```bash
cd medics
pip install -r requirements.txt
```

Alternatively, you can manually install dependencies:

```bash
pip install pandas openpyxl
```

### 5.3 Database Setup

Ensure that you have the necessary Excel files (patients.xlsx and doctors.xlsx) in the root directory. If not, create them manually or run the following script to generate template files:

```bash
python setup_database.py
```

---

<a name="usage"></a>

## 6. Usage

### 6.1 Running the Application

Once you have installed all dependencies, run the following command to start the application:

```bash
python medics.py
```

### 6.2 Patient Login

- Upon running the program, the user will be prompted to enter their username and password.
- Once authenticated, patients can access their medical dashboard.

### 6.3 Doctor Login

- Doctors use a separate login page to access their dashboard, where they can manage patients and appointments.

### 6.4 Diagnosis Submission

- Patients can input their symptoms or diagnoses in the input fields.
- After submission, the system will retrieve related medical information from the database.

### 6.5 Appointment Scheduling

- Patients can view available doctors and schedule appointments directly from their dashboard.
- Appointments are stored in the Excel database for both patients and doctors.

---

<a name="excel-database-structure"></a>

## 7. Excel Database Structure

The Excel files are critical to how Medics stores and manages data. Below is the structure for both files:

### 7.1 Patient Sheet

| Column Name      | Data Type  | Description                                      |
|------------------|------------|--------------------------------------------------|
| Patient Name     | String     | The full name of the patient.                    |
| Username         | String     | The patient's username for login.                |
| Password         | String     | The patient's password (encrypted).              |
| Diagnosis        | String     | The diagnosis or symptoms entered by the patient.|
| Appointment Date | DateTime   | The date and time of the scheduled appointment.  |
| Doctor Assigned  | String     | The doctor assigned to the patient.              |

### 7.2 Doctor Sheet

| Column Name       | Data Type  | Description                                      |
|-------------------|------------|--------------------------------------------------|
| Doctor Name       | String     | The full name of the doctor.                     |
| Username          | String     | The doctor's username for login.                 |
| Password          | String     | The doctor's password (encrypted).               |
| Assigned Patients | List       | A list of patients assigned to the doctor.       |

---

<a name="code-breakdown"></a>

## 8. Code Breakdown

Here is an overview of the important code components in the Medics system.

### 8.1 Patient Class

```python
class Patient:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Fetch patient details from Excel file.
        self.patient_data = self.load_patient_data()

    def load_patient_data(self):
        # Logic to load patient data from patients.xlsx
        pass

    def submit_diagnosis(self, diagnosis):
        # Logic to update diagnosis in the Excel file.
        pass

    def schedule_appointment(self, doctor, date):
        # Logic to schedule an appointment in the Excel file.
        pass
```

### 8.2 Doctor Class

```python
class Doctor:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        # Fetch doctor details from Excel file.
        self.doctor_data = self.load_doctor_data()

    def load_doctor_data(self):
        # Logic to load doctor data from doctors.xlsx
        pass

    def view_patients(self):
        # Logic to view all assigned patients.
        pass
```

### 8.3 Appointment Management

```python
def assign_patient_to_doctor(patient, doctor):
    # Logic to assign a patient to a specific doctor in the Excel sheet.
    pass
```

---

<a name="error-handling-and-debugging"></a>

## 9. Error Handling and Debugging

To ensure smooth operation, the following error handling mechanisms are implemented:

- **Invalid Login**: If a patient or doctor enters incorrect login credentials, the system will prompt an error message.
- **Empty Diagnosis**: The system will not allow a patient to submit an empty diagnosis field.
- **Excel File Access**: If the Excel files are inaccessible or corrupted, the system will prompt the user to restore the files. 


