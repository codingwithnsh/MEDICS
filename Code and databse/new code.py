import os
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
import textwrap
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
users_df = pd.read_excel(os.path.join(script_dir, 'database.xlsx'), sheet_name='users')
filtered_specializations = set()
users_df['Symptoms'] = users_df['Symptoms'].astype(str)
if 'Appointment Slot' not in users_df.columns:
    users_df['Appointment Slot'] = ''
if 'Preferred Doctor' not in users_df.columns:
    users_df['Preferred Doctor'] = ''
if 'Appointment Date' not in users_df.columns:
    users_df['Appointment Date'] = ''
users_df['Appointment Date'] = users_df['Appointment Date'].astype(str)


root = tk.Tk()
root.title('MEDICS: MEDICAL EXAMINATION AND DIAGNOSIS INFORMATION CARE SYSTEM')
root.geometry('800x600')

current_user = None
results_frame = None
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
    img = Image.open(os.path.join(script_dir, 'login_image.png'))
    img = img.resize((400, 399), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = ttk.Label(frame, image=img)
    img_label.image = img
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
    new_user = pd.DataFrame([[name, username, password, address, city, '', '', '', user_type, (f"The Department of {specialization.title()}"), '', '']],
                            columns=['Name', 'Username', 'Password', 'Address', 'City', 'Diagnosis', 'Appointment Slot', 'Preferred Doctor', 'User Type', 'Specialization', 'Assigned Patients', 'Doctor ID'])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    save_data()
    messagebox.showinfo('Success', 'User registered successfully.')
    show_view('login')
def authenticate_user(username_entry, password_entry):
    global current_user
    current_user = None
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
    img = Image.open(os.path.join(script_dir, 'patient_dashboard_image.png'))
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    img_label = ttk.Label(frame, image=img)
    img_label.image = img
    img_label.pack(pady=10)
    ttk.Label(frame, text='Enter Symptoms (comma-separated):').pack(pady=5)
    diagnosis_entry = ttk.Entry(frame)
    diagnosis_entry.pack(pady=5)
    submit_btn = ttk.Button(frame, text='Submit Symptoms', command=lambda: submit_symptoms(diagnosis_entry))
    submit_btn.pack(pady=10, anchor='s')
    results_frame = ttk.Frame(frame)
    results_frame.pack(pady=10, fill='both', expand=True)

def submit_symptoms(diagnosis_entry):
    symptoms = diagnosis_entry.get().strip().lower()
    users_df.loc[users_df['Username'] == current_user, 'Symptoms'] = symptoms
    save_data()
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
        'abnormal bleeding': 'The Department of General Medicine',
        'dizziness': 'The Department of General Medicine',
        'weakness': 'The Department of General Medicine',
        'high fever': 'The Department of General Medicine',
        'insomnia': 'The Department of General Medicine',
        'sleep problems': 'The Department of General Medicine',
        'body weakness': 'The Department of General Medicine',
        'food poisoning': 'The Department of General Medicine',
        'allergy': 'The Department of General Medicine',
        'allergic rash': 'The Department of General Medicine',
        'body stiffness': 'The Department of General Medicine',
        'drug reaction': 'The Department of General Medicine',
        'sinus headache': 'The Department of General Medicine',
        'migraine': 'The Department of General Medicine',
        'diabetes': 'The Department of General Medicine',
        'menstrual irregularities': 'The Department of General Medicine',
        'thyroid swelling': 'The Department of General Medicine',
        'stomach pain': 'The Department of General Medicine',
        'acid reflux': 'The Department of General Medicine',
        'constipation': 'The Department of General Medicine',
        'diarrhea': 'The Department of General Medicine',
        # Urology
        'kidney pain': 'The Department of Urology',
        'bladder pain': 'The Department of Urology',
        'painful urination': 'The Department of Urology',
        'blood in urine': 'The Department of Urology',
        'prostate issues': 'The Department of Urology',
        'pelvic pain': 'The Department of Urology',
        'burning urination': 'The Department of Urology',
        # Cardiology
        'chest pain': 'The Department of Cardiology',
        'shortness of breath': 'The Department of Cardiology',
        'swelling in legs': 'The Department of Cardiology',
        'dizziness with chest pain': 'The Department of Cardiology',
        'edema': 'The Department of Cardiology',
        'hypertension': 'The Department of Cardiology',
        'hypotension': 'The Department of Cardiology',
        'leg swelling': 'The Department of Cardiology',
        # Dermatology
        'skin rash': 'The Department of Dermatology',
        'acne': 'The Department of Dermatology',
        'hair loss': 'The Department of Dermatology',
        'skin infection': 'The Department of Dermatology',
        'dry skin': 'The Department of Dermatology',
        'dark spots': 'The Department of Dermatology',
        'urticaria': 'The Department of Dermatology',
        'hives': 'The Department of Dermatology',
        'ringworm': 'The Department of Dermatology',
        'fungal infection': 'The Department of Dermatology',
        'dandruff': 'The Department of Dermatology',
        'nail fungus': 'The Department of Dermatology',
        'sunburn': 'The Department of Dermatology',
        'boils': 'The Department of Dermatology',
        'itching': 'The Department of Dermatology',
        # Orthopedics
        'back pain': 'The Department of Orthopedics',
        'joint pain': 'The Department of Orthopedics',
        'bone fracture': 'The Department of Orthopedics',
        'muscle strain': 'The Department of Orthopedics',
        'neck pain': 'The Department of Orthopedics',
        'knee pain': 'The Department of Orthopedics',
        'low back pain': 'The Department of Orthopedics',
        'shoulder pain': 'The Department of Orthopedics',
        'elbow pain': 'The Department of Orthopedics',
        'wrist pain': 'The Department of Orthopedics',
        'ankle pain': 'The Department of Orthopedics',
        'sprain': 'The Department of Orthopedics',
        'strain': 'The Department of Orthopedics',
        'slipped disc': 'The Department of Orthopedics',
        'ligament tear': 'The Department of Orthopedics',
        # Ophthalmology
        'red eyes': 'The Department of Ophthalmology',
        'blurred vision': 'The Department of Ophthalmology',
        'cataract': 'The Department of Ophthalmology',
        'watery eyes': 'The Department of Ophthalmology',
        'eye pain': 'The Department of Ophthalmology',
        'itchy eyes': 'The Department of Ophthalmology',
        'pink eye': 'The Department of Ophthalmology',
        'dry eyes': 'The Department of Ophthalmology',
        'eye redness': 'The Department of Ophthalmology',
        'eye swelling': 'The Department of Ophthalmology',
        'floaters': 'The Department of Ophthalmology',
        'double vision': 'The Department of Ophthalmology',
        'eye trauma': 'The Department of Ophthalmology',
        'vision changes': 'The Department of Ophthalmology',
        # ENT
        'earache': 'The Department of ENT',
        'hearing loss': 'The Department of ENT',
        'nosebleed': 'The Department of ENT',
        'blocked ears': 'The Department of ENT',
        'throat pain': 'The Department of ENT',
        'ear discharge': 'The Department of ENT',
        'ear ringing': 'The Department of ENT',
        'vertigo': 'The Department of ENT',
        'nasal congestion': 'The Department of ENT',
        'runny nose': 'The Department of ENT',
        'snoring': 'The Department of ENT',
        'sleep apnea': 'The Department of ENT',
        'loss of smell': 'The Department of ENT',
        # Gastroenterology
        'vomiting blood': 'The Department of Gastroenterology',
        'indigestion': 'The Department of Gastroenterology',
        'piles': 'The Department of Gastroenterology',
        'anal pain': 'The Department of Gastroenterology',
        'blood in stool': 'The Department of Gastroenterology',
        'black stool': 'The Department of Gastroenterology',
        'diarrhoea': 'The Department of Gastroenterology',
        'hepatitis': 'The Department of Gastroenterology',
        'gas': 'The Department of Gastroenterology',
        'acid burps': 'The Department of Gastroenterology',
        'heartburn': 'The Department of Gastroenterology',
    }
    matched_specialization = None
    for symptom, specialization in specialization_map.items():
        if symptom in symptoms:
            matched_specialization = specialization
            break
    if matched_specialization:
        messagebox.showinfo('Specialization Matched', f"Please select a doctor from {matched_specialization}.")
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
    patient_city = users_df.loc[users_df['Username'] == current_user, 'City'].values[0]
    columns = ('Name', 'Specialization', 'Address')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, anchor='w')
        tree.column(col, width=300, anchor='w')
    doctor_filter = users_df[(users_df['City'].str.lower().fillna('') == str(patient_city).lower()) & (users_df['User Type'] == 'Doctor')]
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
    style = ttk.Style()
    style.configure('Treeview', rowheight=40)
    for item in tree.get_children():
        values = tree.item(item, 'values')
        max_lines = max(len(values[1].split('\n')), len(values[2].split('\n')))
        style.configure('Treeview', rowheight=max_lines * 20)
    ttk.Label(frame, text='Select Preferred Date:').pack(pady=5)
    dates = [(datetime.date.today() + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(0, 14)]
    date_var = tk.StringVar(value=dates[0])
    date_combo = ttk.Combobox(frame, values=dates, textvariable=date_var, state='readonly')
    date_combo.pack(pady=5)
    ttk.Label(frame, text='Select Preferred Time Slot:').pack(pady=10)
    slots = ['10:00 AM - 11:00 AM', '11:00 AM - 12:00 PM', '01:00 PM - 02:00 PM', '02:00 PM - 03:00 PM']
    slot_var = tk.StringVar(value=slots[0])
    for slot in slots:
        ttk.Radiobutton(frame, text=slot, variable=slot_var, value=slot).pack(pady=5)
    schedule_btn = ttk.Button(frame, text='Book Appointment', command=lambda: schedule_appointment(tree, slot_var, date_var))
    schedule_btn.pack(pady=10)

def schedule_appointment(tree, slot_var, date_var):
    SLOT_CAPACITY = 5
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'Please select a doctor.')
        return
    selected_doctor = tree.item(selected_item[0], 'values')[0]
    selected_slot = slot_var.get()
    selected_date = date_var.get()
    doctor_row = users_df[(users_df['Name'] == selected_doctor) & (users_df['User Type'] == 'Doctor')]
    if doctor_row.empty:
        messagebox.showerror('Error', 'Selected doctor not found.')
        return
    doctor_id = doctor_row['Username'].values[0]
    existing_count = users_df[(users_df['Preferred Doctor'] == doctor_id) & (users_df['Appointment Slot'] == selected_slot) & (users_df['Appointment Date'] == selected_date)].shape[0]
    if existing_count >= SLOT_CAPACITY:
        messagebox.showerror('Error', f'This slot on {selected_date} is full. Please choose another slot or date.')
        return
    users_df.loc[users_df['Username'] == current_user, 'Appointment Slot'] = str(selected_slot)
    users_df.loc[users_df['Username'] == current_user, 'Appointment Date'] = str(selected_date)
    users_df.loc[users_df['Username'] == current_user, 'Preferred Doctor'] = doctor_id
    assigned_patients = doctor_row['Assigned Patients'].values[0]
    if pd.isnull(assigned_patients) or not str(assigned_patients).strip():
        assigned_patients_list = []
    else:
        assigned_patients_list = [p.strip() for p in str(assigned_patients).split(',') if p.strip()]
    if current_user not in assigned_patients_list:
        assigned_patients_list.append(current_user)
    users_df.loc[users_df['Username'] == doctor_id, 'Assigned Patients'] = ', '.join(assigned_patients_list)
    save_data()
    messagebox.showinfo('Appointment', f'Appointment scheduled with {selected_doctor} on {selected_date} at {selected_slot}')
    for widget in root.winfo_children():
        widget.destroy()
    show_view('login')

def show_doctor_dashboard():
    global action_frame
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill='both', expand=True)
    ttk.Label(frame, text='Doctor Dashboard').pack(pady=10)
    load_patient_data(current_user, frame)
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
    today_str = datetime.date.today().strftime('%Y-%m-%d')
    rows_inserted = 0
    for patient in assigned_patients:
        patient_data = users_df[users_df['Username'] == patient]
        if not patient_data.empty:
            appt_date = str(patient_data['Appointment Date'].values[0]) if 'Appointment Date' in patient_data.columns else ''
            if appt_date == today_str:
                tree.insert('', 'end', values=(patient_data['Name'].values[0], patient_data['Symptoms'].values[0], patient_data['Appointment Slot'].values[0], patient_data['Preferred Doctor'].values[0]))
                rows_inserted += 1
    if rows_inserted == 0:
        ttk.Label(frame, text='No patients scheduled for today.').pack(pady=10)
        return
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
        for widget in action_frame.winfo_children():
            widget.destroy()
        btn_done = ttk.Button(action_frame, text='Done', command=lambda p=patient_username: mark_done(p, username, assigned_patients))
        btn_done.pack(pady=5)
        btn_progress = ttk.Button(action_frame, text='Next Patient', command=lambda p=patient_username: mark_in_progress(p, assigned_patients, tree))
        btn_progress.pack(pady=5)

def mark_done(patient_username, username, assigned_patients):
    if patient_username in assigned_patients:
        assigned_patients.remove(patient_username)
        users_df.loc[users_df['Username'] == username, 'Assigned Patients'] = ', '.join(assigned_patients)
        users_df.loc[users_df['Username'] == patient_username, 'Preferred Doctor'] = ''
        users_df.loc[users_df['Username'] == patient_username, 'Appointment Slot'] = ''
        users_df.loc[users_df['Username'] == patient_username, 'Appointment Date'] = ''
        save_data()
        show_view('doctor')
    else:
        messagebox.showerror('Error', 'Patient not found in the assigned list.')

def mark_in_progress(patient_username, assigned_patients, tree):
    if not assigned_patients:
        messagebox.showinfo('Next Patient', 'No patients are currently assigned.')
        return
    selected = tree.selection()
    if not selected:
        messagebox.showinfo('Next Patient', 'No patient is currently selected.')
        return
    children = tree.get_children()
    current_index = tree.index(selected[0])
    next_index = current_index + 1
    if next_index < len(children):
        next_item = children[next_index]
        tree.selection_set(next_item)
        tree.focus(next_item)
        tree.see(next_item)
        tree.event_generate('<<TreeviewSelect>>')
    else:
        tree.selection_remove(selected[0])
        tree.focus('')
        for widget in action_frame.winfo_children():
            widget.destroy()
        messagebox.showinfo('Next Patient', 'No more patients in the schedule.')
show_view('login')
root.mainloop()
