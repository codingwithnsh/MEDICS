import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
import textwrap

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load Excel database
users_df = pd.read_excel(os.path.join(script_dir, 'database.xlsx'), sheet_name='users')
filtered_specializations = set()

# Ensure proper column types
users_df['Symptoms'] = users_df['Symptoms'].astype(str)
if 'Appointment Slot' not in users_df.columns:
    users_df['Appointment Slot'] = ''
if 'Preferred Doctor' not in users_df.columns:
    users_df['Preferred Doctor'] = ''

# Main root window
root = tk.Tk()
root.title('MEDICS: MEDICAL EXAMINATION AND DIAGNOSIS INFORMATION CARE SYSTEM')
root.geometry('800x600')

# Global variable for the currently logged-in user
current_user = None

# Global variable for results_frame
results_frame = None

# Global variable for confirm button
confirm_btn = None

def show_view(view, matched_specialization=None):
    for widget in root.winfo_children():
        widget.destroy()

    if view == 'login':
        show_login()
    elif view == 'signup':
        show_signup()
    elif view == 'patient':
        show_patient_dashboard()
    elif view == 'doctor':
        show_doctor_dashboard()
    elif view == 'select_doctor':
        show_select_doctor(matched_specialization)

def show_login():
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill='both', expand=True)

    # Load and display image
    img = Image.open(os.path.join(script_dir, 'login_image.png'))
    img = img.resize((400, 399), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = ttk.Label(frame, image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack(pady=10)

    ttk.Label(frame, text='Username').pack(pady=5)
    username_entry = ttk.Entry(frame)
    username_entry.pack(pady=5)

    ttk.Label(frame, text='Password').pack(pady=5)
    password_entry = ttk.Entry(frame, show='*')
    password_entry.pack(pady=5)

    login_btn = ttk.Button(frame, text='Login', command=lambda: authenticate_user(username_entry, password_entry))
    login_btn.pack(pady=10)

    signup_btn = ttk.Button(frame, text='Sign Up', command=lambda: show_view('signup'))
    signup_btn.pack(pady=10)

def show_signup():
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill='both', expand=True)

    ttk.Label(frame, text='Name').pack(pady=5)
    name_entry = ttk.Entry(frame)
    name_entry.pack(pady=5)

    ttk.Label(frame, text='Username').pack(pady=5)
    username_entry = ttk.Entry(frame)
    username_entry.pack(pady=5)

    ttk.Label(frame, text='Password').pack(pady=5)
    password_entry = ttk.Entry(frame, show='*')
    password_entry.pack(pady=5)

    ttk.Label(frame, text='City').pack(pady=5)
    city_entry = ttk.Entry(frame)
    city_entry.pack(pady=5)

    ttk.Label(frame, text='Address').pack(pady=5)
    address_entry = ttk.Entry(frame)
    address_entry.pack(pady=5)

    ttk.Label(frame, text='Specialization (if Doctor)').pack(pady=5)
    specialization_entry = ttk.Entry(frame)
    specialization_entry.pack(pady=5)

    signup_btn = ttk.Button(frame, text='Sign Up', command=lambda: register_user(name_entry, username_entry, password_entry, city_entry, address_entry, specialization_entry))
    signup_btn.pack(pady=10)

    login_btn = ttk.Button(frame, text='Back to Login', command=lambda: show_view('login'))
    login_btn.pack(pady=10)

def register_user(name_entry, username_entry, password_entry, city_entry, address_entry, specialization_entry):
    global users_df

    name = name_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    city = city_entry.get()
    address = address_entry.get()
    user_type = 'Doctor' if specialization_entry.get() else 'Patient'
    specialization = specialization_entry.get() if user_type == 'Doctor' else ''

    if not name or not username or not password or not city or not address or (user_type == 'Doctor' and not specialization):
        messagebox.showerror('Error', 'All fields are required.')
        return

    if username in users_df['Username'].values:
        messagebox.showerror('Error', 'Username already exists.')
        return

    new_user = pd.DataFrame([[name, username, password, address, city, '', '', '', user_type, specialization, '', '']],
                            columns=['Name', 'Username', 'Password', 'Address', 'City', 'Diagnosis', 'Appointment Slot', 'Preferred Doctor', 'User Type', 'Specialization', 'Assigned Patients', 'Doctor ID'])
    users_df = pd.concat([users_df, new_user], ignore_index=True)

    save_data()
    messagebox.showinfo('Success', 'User registered successfully.')
    show_view('login')

def authenticate_user(username_entry, password_entry):
    global current_user
    current_user = None  # Reset current_user on each login attempt

    username = username_entry.get()
    password = password_entry.get()

    user = users_df[(users_df['Username'] == username) & (users_df['Password'] == password)]
    if not user.empty:
        current_user = username
        user_type = user['User Type'].values[0]
        if user_type == 'Patient':
            show_view('patient')
        elif user_type == 'Doctor':
            show_view('doctor')
    else:
        messagebox.showerror('Error', 'Invalid username or password.')

def show_patient_dashboard():
    global results_frame
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill='both', expand=True)

    # Load and display image
    img = Image.open(os.path.join(script_dir, 'patient_dashboard_image.png'))
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = ttk.Label(frame, image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack(pady=10)

    ttk.Label(frame, text='Enter Symptoms (comma-separated):').pack(pady=5)
    diagnosis_entry = ttk.Entry(frame)
    diagnosis_entry.pack(pady=5)

    submit_btn = ttk.Button(frame, text='Submit Symptoms', command=lambda: submit_symptoms(diagnosis_entry))
    submit_btn.pack(pady=10, anchor='s')  # Anchor the button to the bottom

    results_frame = ttk.Frame(frame)
    results_frame.pack(pady=10, fill='both', expand=True)

def submit_symptoms(diagnosis_entry):
    symptoms = diagnosis_entry.get().strip().lower()
    users_df.loc[users_df['Username'] == current_user, 'Symptoms'] = symptoms
    save_data()

    # Map symptoms to specializations
    specialization_map = {
        # General Medicine
        'fever': 'The Department of General Medicine',
        'cough': 'The Department of General Medicine',
        'cold': 'The Department of General Medicine',
        'nausea': 'The Department of General Medicine',
        'headache': 'The Department of General Medicine',
        'fatigue': 'The Department of General Medicine',
        'body ache': 'The Department of General Medicine',
        'vomiting': 'The Department of General Medicine',
        'sore throat': 'The Department of General Medicine',
        'dizziness': 'The Department of General Medicine',
        'loss of appetite': 'The Department of General Medicine',
        'weakness': 'The Department of General Medicine',
        'chills': 'The Department of General Medicine',
        'high fever': 'The Department of General Medicine',

        # Urology
        'urine': 'The Department of Urology',
        'urine problems': 'The Department of Urology',
        'kidney pain': 'The Department of Urology',
        'bladder issues': 'The Department of Urology',
        'frequent urination': 'The Department of Urology',
        'painful urination': 'The Department of Urology',
        'blood in urine': 'The Department of Urology',
        'urinary incontinence': 'The Department of Urology',
        'prostate issues': 'The Department of Urology',
        'pelvic pain': 'The Department of Urology',
        'reduced urine output': 'The Department of Urology',

        # Cardiology
        'chest pain': 'The Department of Cardiology',
        'shortness of breath': 'The Department of Cardiology',
        'irregular heartbeat': 'The Department of Cardiology',
        'high blood pressure': 'The Department of Cardiology',
        'low blood pressure': 'The Department of Cardiology',
        'heart palpitations': 'The Department of Cardiology',
        'swelling in legs': 'The Department of Cardiology',
        'dizziness with chest pain': 'The Department of Cardiology',
        'cyanosis': 'The Department of Cardiology',

        # Endocrinology
        'diabetes': 'The Department of Endocrinology',
        'thyroid issues': 'The Department of Endocrinology',
        'obesity': 'The Department of Endocrinology',
        'hormonal imbalance': 'The Department of Endocrinology',
        'growth problems': 'The Department of Endocrinology',
        'adrenal gland issues': 'The Department of Endocrinology',
        'hyperthyroidism': 'The Department of Endocrinology',
        'hypothyroidism': 'The Department of Endocrinology',

        # Dermatology
        'skin rash': 'The Department of Dermatology',
        'acne': 'The Department of Dermatology',
        'eczema': 'The Department of Dermatology',
        'psoriasis': 'The Department of Dermatology',
        'hair loss': 'The Department of Dermatology',
        'skin infection': 'The Department of Dermatology',
        'allergic rash': 'The Department of Dermatology',
        'dry skin': 'The Department of Dermatology',
        'dark spots': 'The Department of Dermatology',

        # Hematology
        'anemia': 'The Department of Hematology',
        'blood disorders': 'The Department of Hematology',
        'leukemia': 'The Department of Hematology',
        'clotting problems': 'The Department of Hematology',
        'low platelet count': 'The Department of Hematology',
        'iron deficiency': 'The Department of Hematology',
        'abnormal bleeding': 'The Department of Hematology',
        'excessive bruising': 'The Department of Hematology',

        # Orthopedics
        'back pain': 'The Department of Orthopedics',
        'joint pain': 'The Department of Orthopedics',
        'bone fracture': 'The Department of Orthopedics',
        'arthritis': 'The Department of Orthopedics',
        'muscle strain': 'The Department of Orthopedics',
        'neck pain': 'The Department of Orthopedics',
        'knee pain': 'The Department of Orthopedics',
        'spinal problems': 'The Department of Orthopedics',
        'frozen shoulder': 'The Department of Orthopedics',
        'osteoporosis': 'The Department of Orthopedics',

        # Ophthalmology
        'vision loss': 'The Department of Ophthalmology',
        'red eyes': 'The Department of Ophthalmology',
        'blurred vision': 'The Department of Ophthalmology',
        'cataract': 'The Department of Ophthalmology',
        'glaucoma': 'The Department of Ophthalmology',
        'watery eyes': 'The Department of Ophthalmology',
        'eye pain': 'The Department of Ophthalmology',
        'itchy eyes': 'The Department of Ophthalmology',
        'light sensitivity': 'The Department of Ophthalmology',

        # ENT
        'earache': 'The Department of ENT',
        'hearing loss': 'The Department of ENT',
        'nosebleed': 'The Department of ENT',
        'sinusitis': 'The Department of ENT',
        'tonsillitis': 'The Department of ENT',
        'blocked ears': 'The Department of ENT',
        'throat pain': 'The Department of ENT',
        'ear discharge': 'The Department of ENT',

        # Gastroenterology
        'stomach pain': 'The Department of Gastroenterology',
        'acid reflux': 'The Department of Gastroenterology',
        'constipation': 'The Department of Gastroenterology',
        'diarrhea': 'The Department of Gastroenterology',
        'liver disease': 'The Department of Gastroenterology',
        'abdominal bloating': 'The Department of Gastroenterology',
        'vomiting blood': 'The Department of Gastroenterology',
        'jaundice': 'The Department of Gastroenterology',
        'indigestion': 'The Department of Gastroenterology',
        'intestinal blockage': 'The Department of Gastroenterology',
    }

    # Find matching specialization based on symptoms
    matched_specialization = None
    for symptom, specialization in specialization_map.items():
        if symptom in symptoms:
            matched_specialization = specialization
            break

    if matched_specialization:
        messagebox.showinfo('Specialization Matched', f"Please select a doctor from the {matched_specialization} department.")
        show_view('select_doctor', matched_specialization)
    else:
        messagebox.showerror('Error', 'No matching specialization found. Please check your symptoms.')

def save_data():
    try:
        with pd.ExcelWriter(os.path.join(script_dir, 'database.xlsx'), engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            users_df.to_excel(writer, sheet_name='users', index=False)
    except FileNotFoundError:
        messagebox.showerror('Error', 'Database file not found. Please check the file path.')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def save_patient_data():
    try:
        with pd.ExcelWriter(os.path.join(script_dir, 'database.xlsx'), engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            users_df.to_excel(writer, sheet_name='users', index=False)
    except FileNotFoundError:
        messagebox.showerror('Error', 'Database file not found. Please check the file path.')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def show_select_doctor(matched_specialization=None):
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill='both', expand=True)

    ttk.Label(frame, text='Select Preferred Doctor:').pack(pady=10)

    # Get the city of the current patient
    patient_city = users_df.loc[users_df['Username'] == current_user, 'City'].values[0]

    columns = ('Name', 'Specialization', 'Address')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, anchor='w')
        tree.column(col, width=300, anchor='w')

    # Filter doctors based on the patient's city and specialization
    doctor_filter = users_df[(users_df['City'] == patient_city) & (users_df['User Type'] == 'Doctor')]

    if matched_specialization:
        doctor_filter = doctor_filter[doctor_filter['Specialization'] == matched_specialization]

    for _, row in doctor_filter.iterrows():
        name = row['Name']
        specialization = textwrap.fill(str(row['Specialization']), width=90)
        address = textwrap.fill(str(row['Address']), width=50)
        tree.insert('', 'end', values=(name, specialization, address))

    tree.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    # Adjust row height based on content
    style = ttk.Style()
    style.configure('Treeview', rowheight=40)  # Default row height
    for item in tree.get_children():
        values = tree.item(item, 'values')
        max_lines = max(len(values[1].split('\n')), len(values[2].split('\n')))
        style.configure('Treeview', rowheight=max_lines * 20)  # Adjust the multiplier as needed

    ttk.Label(frame, text='Select Preferred Time Slot:').pack(pady=10)

    slots = ['10:00 AM - 11:00 AM', '11:00 AM - 12:00 PM', '01:00 PM - 02:00 PM', '02:00 PM - 03:00 PM']
    slot_var = tk.StringVar(value=slots[0])

    for slot in slots:
        ttk.Radiobutton(frame, text=slot, variable=slot_var, value=slot).pack(pady=5)

    schedule_btn = ttk.Button(frame, text='Book Appointment', command=lambda: schedule_appointment(tree, slot_var))
    schedule_btn.pack(pady=10)

def schedule_appointment(tree, slot_var):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a doctor.')
        return

    selected_doctor = tree.item(selected_item[0], 'values')[0]
    selected_slot = slot_var.get()

    # Check if the selected doctor exists in the DataFrame
    doctor_row = users_df[(users_df['Name'] == selected_doctor) & (users_df['User Type'] == 'Doctor')]
    if doctor_row.empty:
        messagebox.showerror('Error', 'Selected doctor not found.')
        return

    doctor_id = doctor_row['Username'].values[0]
    users_df.loc[users_df['Username'] == current_user, 'Appointment Slot'] = str(selected_slot)
    users_df.loc[users_df['Username'] == current_user, 'Preferred Doctor'] = doctor_id

    assigned_patients = doctor_row['Assigned Patients'].values[0]
    if pd.isnull(assigned_patients):
        assigned_patients = []
    else:
        assigned_patients = assigned_patients.split(', ')

    assigned_patients.append(current_user)
    users_df.loc[users_df['Username'] == doctor_id, 'Assigned Patients'] = ', '.join(assigned_patients)

    save_data()
    messagebox.showinfo('Appointment', f'Appointment scheduled with {selected_doctor} at {selected_slot}')

    # Reset the form elements
    for widget in root.winfo_children():
        widget.destroy()

    # Redirect to login view
    show_view('login')

def show_doctor_dashboard():
    global action_frame
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill='both', expand=True)

    ttk.Label(frame, text='Doctor Dashboard').pack(pady=10)
    load_patient_data(current_user, frame)

    # Create a frame for action buttons
    action_frame = ttk.Frame(frame, padding="20")
    action_frame.pack(pady=10, fill='both', expand=True)

    back_btn = ttk.Button(frame, text='Back', command=lambda: show_view('login'))
    back_btn.pack(pady=10)

def load_patient_data(username, frame):
    doc_info = users_df[(users_df['Username'] == username) & (users_df['User Type'] == 'Doctor')]
    if doc_info.empty:
        messagebox.showerror('Error', 'No doctor data found for the username.')
        return

    doc_info = doc_info.iloc[0]
    assigned_patients = doc_info['Assigned Patients']
    if isinstance(assigned_patients, str):
        assigned_patients = assigned_patients.split(', ')
    else:
        assigned_patients = []

    if not assigned_patients:
        ttk.Label(frame, text='No assigned patients found.').pack(pady=10)
        return

    columns = ('Name', 'Symptoms', 'Appointment Slot', 'Preferred Doctor ID')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for patient in assigned_patients:
        patient_data = users_df[users_df['Username'] == patient]
        if not patient_data.empty:
            tree.insert('', 'end', values=(patient_data['Name'].values[0], patient_data['Symptoms'].values[0], patient_data['Appointment Slot'].values[0], patient_data['Preferred Doctor'].values[0]))

    tree.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    tree.bind('<<TreeviewSelect>>', lambda event: show_action_buttons(event, tree, username, assigned_patients))

def show_action_buttons(event, tree, username, assigned_patients):
    global action_frame
    selected_item = tree.selection()
    if selected_item:
        patient_name = tree.item(selected_item[0], 'values')[0]
        patient_username = users_df[users_df['Name'] == patient_name]['Username'].values[0]

        # Remove existing buttons if any
        for widget in action_frame.winfo_children():
            widget.destroy()

        btn_done = ttk.Button(action_frame, text='Done', command=lambda p=patient_username: mark_done(p, username, assigned_patients))
        btn_done.pack(pady=5)

        btn_progress = ttk.Button(action_frame, text='In Progress', command=lambda p=patient_username: mark_in_progress(p, assigned_patients))
        btn_progress.pack(pady=5)

def mark_done(patient_username, username, assigned_patients):
    if patient_username in assigned_patients:
        assigned_patients.remove(patient_username)
        users_df.loc[users_df['Username'] == username, 'Assigned Patients'] = ', '.join(assigned_patients)
        users_df.loc[users_df['Username'] == patient_username, 'Preferred Doctor'] = ''
        save_data()
        show_view('doctor')
    else:
        messagebox.showerror('Error', 'Patient not found in the assigned list.')

def mark_in_progress(patient_username, assigned_patients):
    next_patient = assigned_patients[0] if assigned_patients else None
    if next_patient:
        next_patient_name = users_df[users_df['Username'] == next_patient]['Name'].values[0]
        messagebox.showinfo('Next Patient', f'Next patient: {next_patient_name}')
    else:
        messagebox.showinfo('Next Patient', 'No more patients in the schedule.')

# Show login view initially
show_view('login')

root.mainloop()