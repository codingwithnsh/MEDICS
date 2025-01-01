import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
import textwrap

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load Excel database
disease_df = pd.read_excel(os.path.join(script_dir, 'diseases.xlsx'), sheet_name='Disease')
users_df = pd.read_excel(os.path.join(script_dir, 'database.xlsx'), sheet_name='users')

# Ensure proper column types
users_df['Diagnosis'] = users_df['Diagnosis'].astype(str)
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

def show_view(view):
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
        show_select_doctor()

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
    ttk.Label(frame, text=f'Welcome, {current_user}').pack(pady=10)
    patient_info = users_df[users_df['Username'] == current_user].iloc[0]
    ttk.Label(frame, text=f'Name: {patient_info["Name"]}').pack(pady=5)

    # Load and display image
    img = Image.open(os.path.join(script_dir, 'patient_dashboard_image.png'))
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = ttk.Label(frame, image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack(pady=10)

    ttk.Label(frame, text='Enter Diagnoses (comma-separated):').pack(pady=5)
    diagnosis_entry = ttk.Entry(frame)
    diagnosis_entry.pack(pady=5)

    submit_btn = ttk.Button(frame, text='Submit Diagnosis', command=lambda: submit_diagnosis(diagnosis_entry))
    submit_btn.pack(pady=10, anchor='s')  # Anchor the button to the bottom

    results_frame = ttk.Frame(frame)
    results_frame.pack(pady=10, fill='both', expand=True)

def submit_diagnosis(diagnosis_entry):
    symptoms = [s.strip().lower() for s in diagnosis_entry.get().split(',')]
    disease_df['Symptoms'] = disease_df['Symptoms'].str.strip().str.lower()

    results = []
    for symptom in symptoms:
        result = disease_df[disease_df['Symptoms'].str.contains(symptom, case=False, na=False)]
        if not result.empty:
            results.append(result)

    update_table(results)
    save_patient_data()

def update_table(results):
    global results_frame
    global confirm_btn
    for widget in results_frame.winfo_children():
        widget.destroy()

    columns = ('Disease', 'Symptoms', 'Severity', 'Initial Treatment')
    tree = ttk.Treeview(results_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    for result in results:
        for _, row in result.iterrows():
            tree.insert('', 'end', values=(row['Disease'], row['Symptoms'], row['Severity'], row['Initial Treatment']))
    tree.pack(side='left', fill='both', expand=True)

    scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    # Create and display the Confirm Selection button
    if confirm_btn:
        confirm_btn.destroy()
    confirm_btn = ttk.Button(results_frame, text='Confirm Selection', command=lambda: confirm_selection(tree))
    confirm_btn.pack(pady=10, side='right', anchor='n')  # Ensure the button is anchored to the top right

    tree.bind('<<TreeviewSelect>>', lambda event: show_confirm_button(event, tree))

def show_confirm_button(event, tree):
    global confirm_btn
    selected_item = tree.selection()
    if selected_item:
        if confirm_btn:
            confirm_btn.destroy()
        confirm_btn = ttk.Button(results_frame, text='Confirm Selection', command=lambda: confirm_selection(tree))
        confirm_btn.pack(pady=10, side='right', anchor='n')  # Ensure the button is anchored to the top right

def confirm_selection(tree):
    selected_item = tree.selection()
    if selected_item:
        selected_disease = tree.item(selected_item[0], 'values')[0]
        users_df.loc[users_df['Username'] == current_user, 'Diagnosis'] = selected_disease
        save_data()
        messagebox.showinfo('Success', f'Diagnosis "{selected_disease}" has been added to your record.')
        show_view('select_doctor')

def save_patient_data():
    try:
        with pd.ExcelWriter(os.path.join(script_dir, 'database.xlsx'), engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            users_df.to_excel(writer, sheet_name='users', index=False)
    except FileNotFoundError:
        messagebox.showerror('Error', 'Database file not found. Please check the file path.')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def save_data():
    try:
        with pd.ExcelWriter(os.path.join(script_dir, 'database.xlsx'), engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            users_df.to_excel(writer, sheet_name='users', index=False)
    except FileNotFoundError:
        messagebox.showerror('Error', 'Database file not found. Please check the file path.')
    except Exception as e:
        messagebox.showerror('Error', f'An error occurred: {e}')

def show_select_doctor():
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill='both', expand=True)

    ttk.Label(frame, text='Select Preferred Doctor:').pack(pady=10)

    # Get the city of the current patient
    patient_city = users_df.loc[users_df['Username'] == current_user, 'City'].values[0]

    columns = ('Name', 'Specialization', 'Address')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, anchor='w')
        tree.column(col, width=200, anchor='w')

    # Filter doctors based on the patient's city
    for _, row in users_df[(users_df['City'] == patient_city) & (users_df['User Type'] == 'Doctor')].iterrows():
        name = row['Name']
        specialization = textwrap.fill(str(row['Specialization']), width=30)
        address = textwrap.fill(str(row['Address']), width=30)
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
    messagebox.showinfo('Appointment', f'Appointment scheduled with Dr. {selected_doctor} at {selected_slot}')

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

    columns = ('Name', 'Diagnosis', 'Appointment Slot', 'Preferred Doctor ID')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for patient in assigned_patients:
        patient_data = users_df[users_df['Username'] == patient]
        if not patient_data.empty:
            tree.insert('', 'end', values=(patient_data['Name'].values[0], patient_data['Diagnosis'].values[0], patient_data['Appointment Slot'].values[0], patient_data['Preferred Doctor'].values[0]))

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
