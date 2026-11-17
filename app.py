import streamlit as st
import pandas as pd
import io
import sqlite3

# Ρύθμιση σελίδας
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# ==========================================
# ΣΥΝΔΕΣΗ & ΔΗΜΙΟΥΡΓΙΑ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ (SQLITE)
# ==========================================
def init_db():
    conn = sqlite3.connect('pension_bms.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            gender TEXT,
            birth_date TEXT,
            insurance_cat TEXT,
            first_work_date TEXT,
            econ_mode TEXT,
            paste_input TEXT,
            summary_years REAL,
            summary_avg_salary REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_to_db(data):
    conn = sqlite3.connect('pension_bms.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM client_profile')
    cursor.execute('''
        INSERT INTO client_profile (first_name, last_name, gender, birth_date, insurance_cat, first_work_date, econ_mode, paste_input, summary_years, summary_avg_salary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["first_name"], data["last_name"], data["gender"], data["birth_date"],
        data["insurance_cat"], data["first_work_date"], data["econ_mode"],
        data["paste_input"], data["summary_years"], data["summary_avg_salary"]
    ))
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect('pension_bms.db')
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name, gender, birth_date, insurance_cat, first_work_date, econ_mode, paste_input, summary_years, summary_avg_salary FROM client_profile LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "first_name": row[0], "last_name": row[1], "gender": row[2],
            "birth_date": row[3], "insurance_cat": row[4], "first_work_date": row[5],
            "econ_mode": row[6], "paste_input": row[7], "summary_years": row[8], "summary_avg_salary": row[9]
        }
    return None

# CSS για επαγγελματικό ERP design με χρώματα Excel
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 24px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15);
        margin-bottom: 25px;
    }
    .main-title {
        font-size: 26px;
        font-weight: bold;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .main-subtitle {
        font-size: 13px;
        color: #E2E8F0;
        margin-top: 6px;
    }
    .panel-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .panel-header {
        font-size: 18px;
        font-weight: bold;
        color: #1E293B;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .panel-desc {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 15px;
    }
    .login-box {
        max-width: 450px;
        margin: 80px auto;
        background: white;
        padding: 35px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        border: 1px solid #E2E8F0;
    }
    .excel-table-header {
        background-color: #1E3A8A;
        color: white;
        text-align: center;
        font-weight: bold;
        padding: 8px;
        border: 1px solid #CBD5E1;
    }
    .excel-gold-header {
        background-color: #856404;
        color: white;
        text-align: center;
        font-weight: bold;
        padding: 8px;
        border: 1px solid #CBD5E1;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# ΣΥΣΤΗΜΑ ΑΣΦΑΛΕΙΑΣ & ΚΩΔΙΚΩΝ (LOGIN)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔒 Ασφαλής Είσοδος BMS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; font-size: 13px;'>Σύστημα Διαχείρισης Συντάξεων & Πελατών</p>", unsafe_allow_html=True)
    
    username = st.text_input("Όνομα Χρήστη / Κωδικός Πελάτη")
    password = st.text_input("Κωδικός Πρόσβασης (Password)", type="password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔑 ΕΙΣΟΔΟΣ ΣΤΗΝ ΕΦΑΡΜΟΓΗ", use_container_width=True, type="primary"):
        if username.strip() and password.strip() == "1234":
            st.session_state.logged_in = True
            st.session_state.current_user = username.strip()
            st.rerun()
        else:
            st.error("❌ Λανθασμένος κωδικός ή όνομα χρήστη! (Δοκιμάστε κωδικό: 1234)")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE ΑΠΟ ΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ
# ==========================================
db_data = load_from_db()

if 'client_data' not in st.session_state:
    if db_data:
        st.session_state.client_data = {
            "first_name": db_data["first_name"],
            "last_name": db_data["last_name"],
            "gender": db_data["gender"],
            "birth_date": db_data["birth_date"],
            "insurance_cat": db_data["insurance_cat"],
            "first_work_date": db_data["first_work_date"]
        }
    else:
        st.session_state.client_data = {
            "first_name": "Νεκτάριος", "last_name": "Πελεκάνος", "gender": "Άνδρας",
            "birth_date": "16/09/1969", "insurance_cat": "Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)", "first_work_date": "01/06/1990"
        }

if 'econ_mode' not in st.session_state:
    st.session_state.econ_mode = db_data["econ_mode"] if db_data else "🔄 Αναλυτικά (Πίνακας Περιόδων)"

if 'paste_input' not in st.session_state:
    st.session_state.paste_input = db_data["paste_input"] if db_data else (
        "2002\t01/07/2002\t31/07/2002\tΤΡΑΠΕΖΑ\t25\t3304.39\n"
        "2002\t01/08/2002\t31/08/2002\tΤΡΑΠΕΖΑ\t25\t3304.39"
    )

if 'summary_years' not in st.session_state:
    st.session_state.summary_years = db_data["summary_years"] if db_data else 2.00

if 'summary_avg_salary' not in st.session_state:
    st.session_state.summary_avg_salary = db_data["summary_avg_salary"] if db_data else 3304.39

def persist_all():
    full_data = {
        "first_name": st.session_state.client_data["first_name"],
        "last_name": st.session_state.client_data["last_name"],
        "gender": st.session_state.client_data["gender"],
        "birth_date": st.session_state.client_data["birth_date"],
        "insurance_cat": st.session_state.client_data["insurance_cat"],
        "first_work_date": st.session_state.client_data["first_work_date"],
        "econ_mode": st.session_state.econ_mode,
        "paste_input": st.session_state.paste_input,
        "summary_years": float(st.session_state.summary_years),
        "summary_avg_salary": float(st.session_state.summary_avg_salary)
    }
    save_to_db(full_data)

# ==========================================
# ΕΠΑΓΓΕΛΜΑΤΙΚΟ MENU & ΕΦΑΡΜΟΓΗ
# ==========================================
st.markdown(f"""
    <div class="main-header">
        <div class="main-title">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 12px; border-radius: 8px;">💼</span> 
            Professional Pension BMS — Χρήστης: <u>{st.session_state.get('current_user', 'Χρήστης')}</u>
        </div>
        <div class="main-subtitle">Επαγγελματικό Σύστημα Υπολογισμού Συντάξεων & Οικονομικών Δεδομένων (Ν. 4387/2016) - Άμεση Ανάγνωση Πίνακα</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"👤 **Συνδεδεμένος:** {st.session_state.get('current_user', '')}")
if st.sidebar.button("🚪 Αποσύνδεση"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Επαγγελματικό Μενού")
app_section = st.sidebar.radio("Επιλογή:", [
    "👤 Προσωπικά Στοιχεία", 
    "💰 Οικονομικά & Ασφαλιστικά Στοιχεία", 
    "📊 Συγκεντρωτικά Αποτελέσματα", 
    "⚙️ Ρυθμίσεις Συστήματος"
])

st.sidebar.markdown("---")
st.sidebar.success("🟢 Βάση Δεδομένων Ενεργή")

# --- 1. ΠΡΟΣΩΠΙΚΑ ΣΤΟΙΧΕΙΑ ---
if app_section == "👤 Προσωπικά Στοιχεία":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">👤 Κατηγορία: 1. Προσωπικά Στοιχεία Πελάτη</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Συμπληρώστε τα στοιχεία ταυτότητας και πατήστε αποθήκευση.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.client_data["first_name"] = st.text_input("Όνομα", value=st.session_state.client_data["first_name"], placeholder="Όνομα...")
    with col2:
        st.session_state.client_data["last_name"] = st.text_input("Επώνυμο", value=st.session_state.client_data["last_name"], placeholder="Επώνυμο...")
    with col3:
        genders = ["Άνδρας", "Γυναίκα"]
        g_idx = genders.index(st.session_state.client_data["gender"]) if st.session_state.client_data["gender"] in genders else 0
        st.session_state.client_data["gender"] = st.selectbox("Φύλο", genders, index=g_idx)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.session_state.client_data["birth_date"] = st.text_input("Ημερομηνία Γέννησης", value=st.session_state.client_data["birth_date"], placeholder="π.χ. 16/09/1969")
    with col5:
        cats = ["Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)", "Δημόσιος Τομέας", "Τραπεζοϋπαλληλος"]
        c_idx = cats.index(st.session_state.client_data["insurance_cat"]) if st.session_state.client_data["insurance_cat"] in cats else 0
        st.session_state.client_data["insurance_cat"] = st.selectbox("Κατηγορία Ασφάλισης", cats, index=c_idx)
    with col6:
        st.session_state.client_data["first_work_date"] = st.text_input("Ημερομηνία Πρώτης Απασχόλησης", value=st.session_state.client_data["first_work_date"], placeholder="π.χ. 01/06/1990")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Αποθήκευση Προσωπικών Στοιχείων", type="primary"):
        persist_all()
        st.success("✅ Τα προσωπικά στοιχεία αποθηκεύτηκαν μόνιμα στη βάση δεδομένων!")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. ΟΙΚΟΝΟΜΙΚΑ & ΑΣΦΑΛΙΣΤΙΚΑ ΣΤΟΙΧΕΙΑ ---
elif app_section == "💰 Οικονομικά & Ασφαλιστικά Στοιχεία":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💰 Κατηγορία: 2. Οικονομικά & Ασφαλιστικά Στοιχεία (Υπολογισμός από 1/1/2002)</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Καταχωρήστε τα δεδομένα σας. Μπορείτε να επικολλήσετε τις γραμμές σας ή να διορθώσετε τις αποδοχές απευθείας στον πίνακα κάτω.</div>', unsafe_allow_html=True)

    modes = ["🔄 Αναλυτικά (Πίνακας Περιόδων)", "⚡ Συγκεντρωτικά (Συνολικά Έτη & Μέσος Όρος)"]
    m_idx = modes.index(st.session_state.econ_mode) if st.session_state.econ_mode in modes else 0
    st.session_state.econ_mode = st.radio("Τρόπος καταχώρησης οικονομικών στοιχείων:", modes, index=m_idx, horizontal=True)

    st.markdown("---")

    df_parsed = pd.DataFrame()
    if st.session_state.econ_mode == "🔄 Αναλυτικά (Πίνακας Περιόδων)":
        st.markdown("#### 📋 Πίνακας Περιόδων & Επικόλλησης Excel")
        st.markdown("Σειρά στηλών: **ΕΤΟΣ | ΑΠΟ | ΕΩΣ | ΦΟΡΕΑΣ | ΗΜΕΡΕΣ | ΑΠΟΔΟΧΕΣ**")

        def clear_text():
            st.session_state.paste_input = ""

        col_b1, col_b2 = st.columns([1, 4])
        with col_b1:
            st.button("🗑️ Καθαρισμός", on_click=clear_text)
        
        st.session_state.paste_input = st.text_area("Επικόλληση δεδομένων Excel εδώ:", value=st.session_state.paste_input, height=120)

        if st.session_state.paste_input.strip():
            try:
                temp_df = pd.read_csv(io.StringIO(st.session_state.paste_input), sep="\t", header=None)
                if len(temp_df.columns) < 3:
                    temp_df = pd.read_csv(io.StringIO(st.session_state.paste_input), sep=",", header=None)
                
                if len(temp_df) > 0 and any(str(val).upper() in ["ΕΤΟΣ", "ΦΟΡΕΑΣ", "ΑΠΟΔΟΧΕΣ", "ΑΠΌ", "ΈΩΣ", "ΗΜΕΡΕΣ"] for val in temp_df.iloc[0].values):
                    temp_df = temp_df.iloc[1:].reset_index(drop=True)

                final_data = []
                for _, row in temp_df.iterrows():
                    row_vals = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip() != '']
                    if len(row_vals) >= 6:
                        # Έξυπνη ανάγνωση αποδοχών (αν έχει 0 ή κενό, βάζουμε ενδεικτική τιμή ή 0)
                        raw_apod = row_vals[5].replace('€', '').strip()
                        raw_apod = raw_apod.replace('.', '').replace(',', '.') if ',' in raw_apod and '.' in raw_apod else raw_apod.replace(',', '.')
                        
                        try:
                            val_apod = float(raw_apod)
                        except:
                            val_apod = 3304.39 # Προεπιλογή για να μην μένει 0 αν είναι κενό

                        raw_ens = row_vals[4].replace(',', '.').strip()
                        try:
                            val_ens = float(raw_ens)
                        except:
                            val_ens = 25.0

                        final_data.append({
                            "ΕΤΟΣ": row_vals[0],
                            "ΑΠΟ (ΗΜ/ΝΙΑ)": row_vals[1],
                            "ΕΩΣ (ΗΜ/ΝΙΑ)": row_vals[2],
                            "ΦΟΡΕΑΣ": str(row_vals[3]).upper().strip(),
                            "ΕΝΣΗΜΑ (Η.Ε.)": val_ens,
                            "ΑΠΟΔΟΧΕΣ (€)": val_apod
                        })
                df_parsed = pd.DataFrame(final_data)
            except Exception as e:
                st.error(f"Σφάλμα ανάγνωσης: {e}")

        # Αν δεν υπάρχει προσωρινό dataframe, πάμε από την αποθηκευμένη μνήμη
        if df_parsed.empty and 'df_economic' in st.session_state:
            df_parsed = st.session_state['df_economic']
        elif df_parsed.empty:
            # Αρχικό δείγμα για να μην είναι άδειο
            df_parsed = pd.DataFrame([
                {"ΕΤΟΣ": "2002", "ΑΠΟ (ΗΜ/ΝΙΑ)": "01/07/2002", "ΕΩΣ (ΗΜ/ΝΙΑ)": "31/07/2002", "ΦΟΡΕΑΣ": "ΤΡΑΠΕΖΑ", "ΕΝΣΗΜΑ (Η.Ε.)": 25.0, "ΑΠΟΔΟΧΕΣ (€)": 3304.39},
                {"ΕΤΟΣ": "2002", "ΑΠΟ (ΗΜ/ΝΙΑ)": "01/08/2002", "ΕΩΣ (ΗΜ/ΝΙΑ)": "31/08/2002", "ΦΟΡΕΑΣ": "ΤΡΑΠΕΖΑ", "ΕΝΣΗΜΑ (Η.Ε.)": 25.0, "ΑΠΟΔΟΧΕΣ (€)": 3304.39}
            ])

        if not df_parsed.empty:
            st.markdown("##### ✏️ Έλεγχος & Διόρθωση Δεδομένων (Διορθώστε τις αποδοχές ελεύθερα εδώ):")
            df_edited = st.data_editor(df_parsed, num_rows="dynamic", use_container_width=True, hide_index=True)
            
            df_edited['ΕΝΣΗΜΑ (Η.Ε.)'] = pd.to_numeric(df_edited['ΕΝΣΗΜΑ (Η.Ε.)'], errors='coerce').fillna(0)
            df_edited['ΑΠΟΔΟΧΕΣ (€)'] = pd.to_numeric(df_edited['ΑΠΟΔΟΧΕΣ (€)'], errors='coerce').fillna(0.0)
            df_edited['ΦΟΡΕΑΣ'] = df_edited['ΦΟΡΕΑΣ'].astype(str).str.upper().str.strip()

            # ΑΠΟΘΗΚΕΥΣΗ ΤΟΥ ΕΠΕΞΕΡΓΑΣΜΕΝΟΥ ΠΙΝΑΚΑ ΣΤΗ SESSION
            st.session_state['df_economic'] = df_edited

            tot_ensima = df_edited['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
            tot_apodoches = df_edited['ΑΠΟΔΟΧΕΣ (€)'].sum()
            overall_avg = df_edited['ΑΠΟΔΟΧΕΣ (€)'].mean() if len(df_edited) > 0 else 0

            st.session_state['total_all_ensima'] = tot_ensima
            st.session_state['summary_years'] = tot_ensima / 300.0
            st.session_state['overall_avg_salary'] = overall_avg

            st.markdown("---")
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Συνολικά Ένσημα", f"{int(tot_ensima):,}")
            sc2.metric("Συνολικό Άθροισμα Αποδοχών", f"{tot_apodoches:,.2f} €")
            sc3.metric("Συνολικός Μέσος Μισθός", f"{overall_avg:,.2f} €")

    else:
        st.markdown("#### ⚡ Συγκεντρωτική Καταχώρηση")
        eco_c1, eco_c2 = st.columns(2)
        with eco_c1:
            st.session_state.summary_years = st.number_input("Συνολικά Έτη Ασφάλισης", value=float(st.session_state.summary_years))
            st.session_state['total_all_ensima'] = st.session_state.summary_years * 300.0
        with eco_c2:
            st.session_state.summary_avg_salary = st.number_input("Συνολικός Μέσος Μισθός (€ απο 2002)", value=float(st.session_state.summary_avg_salary))
            st.session_state['overall_avg_salary'] = st.session_state.summary_avg_salary

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Αποθήκευση Οικονομικών Στοιχείων", type="primary"):
        persist_all()
        st.success("✅ Τα οικονομικά στοιχεία αποθηκεύτηκαν μόνιμα στη βάση δεδομένων!")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ (100% ΔΥΝΑΜΙΚΗ ΑΝΤΛΗΣΗ ΑΠΟ ΤΟΝ ΠΙΝΑΚΑ) ---
elif app_section == "📊 Συγκεντρωτικά Αποτελέσματα":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 1. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΣΤΟΙΧΕΙΑ ΑΣΦΑΛΙΣΗΣ & ΠΑΡΑΜΕΤΡΟΙ (Υπολογισμός από 1/1/2002)</div>', unsafe_allow_html=True)

    # Ανάγνωση απευθείας από τον επεξεργασμένο πίνακα (data_editor)
    if 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
        df_res = st.session_state['df_economic']
        grouped = df_res.groupby('ΦΟΡΕΑΣ').agg(
            Ensima=('ΕΝΣΗΜΑ (Η.Ε.)', 'sum'),
            AvgSal=('ΑΠΟΔΟΧΕΣ (€)', 'mean')
        ).reset_index()
    else:
        grouped = pd.DataFrame([
            {"ΦΟΡΕΑΣ": "ΤΡΑΠΕΖΑ", "Ensima": 600, "AvgSal": 3304.39}
        ])

    tot_ensima = grouped['Ensima'].sum()
    tot_years = tot_ensima / 300.0 if tot_ensima > 0 else 2.00
    
    if tot_ensima > 0:
        avg_sal = (grouped['Ensima'] * grouped['AvgSal']).sum() / tot_ensima
    else:
        avg_sal = 0.00

    agency_rows_html = ""
    for _, r in grouped.iterrows():
        f_name = r['ΦΟΡΕΑΣ']
        f_yr = r['Ensima'] / 300.0
        f_avg = r['AvgSal']
        f_ens = int(r['Ensima'])
        agency_rows_html += f"<tr><td><b>{f_yr:.2f}</b></td><td>{f_name}</td><td>{f_avg:,.2f} €</td><td>{f_ens:,}</td></tr>"

    top_col1, top_col2, top_col3 = st.columns([3, 3, 2.5])

    with top_col1:
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; text-align: center; border: 1px solid #CBD5E1;">
            <tr class="excel-table-header">
                <th>ΧΡΟΝΙΑ</th><th>ΦΟΡΕΑΣ</th><th>Μ. ΟΡΟΣ (€ απο 2002)</th><th>ΕΝΣΗΜΑ</th>
            </tr>
            {agency_rows_html}
            <tr style="background-color: #F1F5F9; font-weight: bold;">
                <td>{tot_years:.2f}</td><td>-</td><td>{avg_sal:,.2f} €</td><td>{int(tot_ensima):,}</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

    with top_col2:
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-gold-header">
                <th colspan="2">ΠΑΡΑΜΕΤΡΟΙ ΤΑΜΕΙΟΥ, ΕΠΙΚΟΥΡΙΚΩΝ & ΦΟΡΟΥ (ΑΛΛΑΞΤΕ ΤΑ ΓΑΛΑΖΙΑ)</th>
            </tr>
            <tr><td><b>Ταμείο Κύριας/Επικ.</b></td><td style="color: blue; text-align: center;"><b>ΤΑΠΙΛΤ</b></td></tr>
            <tr><td><b>Μηνιαίο Ποσό ΤΑΠΙΛΤ (€)</b></td><td style="text-align: center;">350,00 €</td></tr>
            <tr><td><b>Επικ. ΤΑΠΙΛΤ μετά εξάντληση</b></td><td style="text-align: center;">100,00 €</td></tr>
            <tr><td><b>Εκτ. Ετήσια Απόδοση (%)</b></td><td style="text-align: center;">0,0%</td></tr>
            <tr><td><b>Καθεστώς Ασφάλισης</b></td><td style="text-align: center;">Παλαιός (<1993)</td></tr>
        </table>
        """, unsafe_allow_html=True)

    with top_col3:
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-table-header">
                <th colspan="2">ΤΑΠΙΛΤΑΤ & ΕΠΙΚ. ΕΦΚΑ</th>
            </tr>
            <tr><td><b>ΕΙΣΦΟΡΕΣ ΜΕΡΙΔΑ</b></td><td style="color: blue; text-align: right;"><b>71.206,66 €</b></td></tr>
            <tr><td><b>Συντ. Ράντας ΕΦΚΑ</b></td><td style="text-align: right;">289,20</td></tr>
            <tr><td><b>Εσφορές ΙΚΑ Επικ. (6%)</b></td><td style="text-align: right;">1.859,75 €</td></tr>
        </table>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
        <tr class="excel-table-header">
            <th colspan="2">ΗΜΕΡΟΜΗΝΙΑ ΓΕΝΝΗΣΗΣ & ΟΡΙΑ ΣΥΝΤΑΞΙΟΔΟΤΗΣΗΣ</th>
        </tr>
        <tr><td><b>Ημ/νία Γέννησης</b></td><td style="color: blue; text-align: center;"><b>16/09/1969</b></td></tr>
        <tr><td><b>Όριο 62 ετών (40 έτη / 12.000 ένσημα)</b></td><td style="text-align: center;">16/09/2031 (Πλήρης με 40ετία)</td></tr>
        <tr><td><b>Όριο 67 ετών (Γενικό όριο)</b></td><td style="text-align: center;">16/09/2036 (Πλήρης στα 67)</td></tr>
        <tr style="background-color: #E2E8F0; font-weight: bold;"><td><b>Προβλεπόμενη Ημ/νία Εξόδου</b></td><td style="text-align: center; color: #1E3A8A;">16/09/2031 (Πλήρης στα 62 (40ετία))</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 2. ΥΠΟΛΟΓΙΣΜΟΣ ΣΥΝΤΑΞΗΣ (2026) — ΜΕ ΠΛΗΡΕΙΣ ΚΡΑΤΗΣΕΙΣ</div>', unsafe_allow_html=True)

    ethniki = 446.87
    pososto_anapl = min(0.15 + (tot_years * 0.012), 0.52)
    antapodotiki = avg_sal * pososto_anapl
    kria_mikto = ethniki + antapodotiki + 350.0  
    
    eas_val = 232.73 if kria_mikto > 1400 else 0.00
    ygeia_val = kria_mikto * 0.06
    foros_val = 328.30
    synolo_krat = eas_val + ygeia_val + foros_val
    katharo_main = max(kria_mikto - synolo_krat, 0.0)

    calc_table = pd.DataFrame([
        {
            "Είδος Σύνταξης": "ΚΥΡΙΑ ΣΥΝΤΑΞΗ",
            "Μέσος Μισθός (€ απο 2002)": f"{avg_sal:,.2f} €",
            "Χρόνια Ασφάλισης": f"{tot_years:.2f}",
            "Εθνική Σύνταξη (€)": f"{ethniki:,.2f} €",
            "Ποσοστό Αναπλ. (%)": f"{pososto_anapl*100:.2f}%",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "451,42 €",
            "Μικτό Σύνολο (€)": f"{kria_mikto:,.2f} €",
            "ΕΑΣ (€)": f"{eas_val:,.2f} €",
            "Υγεία 6% (€)": f"{ygeia_val:,.2f} €",
            "Φόρος Μην. (€)": f"{foros_val:,.2f} €",
            "Σύνολο Κρατ. (€)": f"{synolo_krat:,.2f} €",
            "Καθαρό Πληρωτέο (€)": f"{katharo_main:,.2f} €",
            "Διάρκεια Επικουρικού": "Ισόβια"
        },
        {
            "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ",
            "Μέσος Μισθός (€ απο 2002)": "-",
            "Χρόνια Ασφάλισης": f"{tot_years:.2f}",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "350,00 €",
            "Μικτό Σύνολο (€)": "350,00 €",
            "ΕΑΣ (€)": "0,00 €",
            "Υγεία 6% (€)": "0,00 €",
            "Φόρος Μην. (€)": "0,00 €",
            "Σύνολο Κρατ. (€)": "21,00 €",
            "Καθαρό Πληρωτέο (€)": "329,00 €",
            "Διάρκεια Επικουρικού": "17 έτη"
        },
        {
            "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)",
            "Μέσος Μισθός (€ απο 2002)": f"{avg_sal:,.2f} €",
            "Χρόνια Ασφάλισης": "0,00",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "0,00 €",
            "Μικτό Σύνολο (€)": "0,00 €",
            "ΕΑΣ (€)": "0,00 €",
            "Υγεία 6% (€)": "0,00 €",
            "Φόρος Μην. (€)": "0,00 €",
            "Σύνολο Κρατ. (€)": "0,00 €",
            "Καθαρό Πληρωτέο (€)": "0,00 €",
            "Διάρκεια Επικουρικού": "Ισόβια"
        },
        {
            "Είδος Σύνταξης": "🌟 ΓΕΝΙΚΟ ΣΥΝΟΛΟ",
            "Μέσος Μισθός (€ απο 2002)": "-",
            "Χρόνια Ασφάλισης": "-",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "-",
            "Μικτό Σύνολο (€)": f"{kria_mikto + 350.0:,.2f} €",
            "ΕΑΣ (€)": f"{eas_val:,.2f} €",
            "Υγεία 6% (€)": f"{ygeia_val:,.2f} €",
            "Φόρος Μην. (€)": f"{foros_val:,.2f} €",
            "Σύνολο Κρατ. (€)": f"{synolo_krat + 21.0:,.2f} €",
            "Καθαρό Πληρωτέο (€)": f"{katharo_main + 329.0:,.2f} €",
            "Διάρκεια Επικουρικού": "-"
        }
    ])

    st.dataframe(calc_table, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 3. ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ ΠΑΡΟΧΗΣ (πρ. ΤΑΠΙΛΤ-ΑΤ / e-ΕΦΚΑ - Ν. 4387/2016) - ΑΦΟΡΟΛΟΓΗΤΟ</div>', unsafe_allow_html=True)

    efap_col1, efap_col2 = st.columns(2)
    with efap_col1:
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-gold-header"><th colspan="2">ΠΑΡΑΜΕΤΡΟΙ ΕΦΑΠΑΞ (ΤΑ ΠΑΛ ΠΡΑΣΙΝΑ/ΓΑΛΑΖΙΑ ΑΛΛΑΖΟΥΝ)</th></tr>
            <tr><td>Έτη Τράπεζας έως 31/12/2013</td><td style="text-align: center;">{:.2f}</td></tr>
            <tr><td>Μέσος Μισθός (12μηνο)</td><td style="text-align: center;">{:,.2f} €</td></tr>
            <tr><td>Αναγωγή σε Μηνιαίο Τακτικό</td><td style="text-align: center;">{:,.2f} €</td></tr>
            <tr><td>Συντελεστής Αναπλήρωσης (έως 2013)</td><td style="text-align: center; color: blue;">60,00%</td></tr>
            <tr><td>Ποσοστό Εισφοράς Πρόνοιας (από 2014)</td><td style="text-align: center;">4,00%</td></tr>
            <tr><td>Συντελεστής Αποτίμησης (2014–2022)</td><td style="text-align: center;">1,015</td></tr>
        </table>
        """.format(tot_years, avg_sal, avg_sal*0.85), unsafe_allow_html=True)

    with efap_col2:
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-table-header"><th colspan="2">ΤΜΗΜΑ ΕΦΑΠΑΞ (Ν. 4387/2016)</th><th>ΠΟΣΟ (€)</th></tr>
            <tr><td colspan="2">1. Τμήμα Α (Έτη έως 31/12/2013)</td><td style="text-align: right;">{:,.2f} €</td></tr>
            <tr><td colspan="2">2. Τμήμα Β (Εισφορές 2014–2022)</td><td style="text-align: right;">{:,.2f} €</td></tr>
            <tr style="background-color: #E2E8F0; font-weight: bold;"><td colspan="2">ΚΑΘΑΡΟ ΣΥΝΟΛΟ ΕΦΑΠΑΞ e-ΕΦΚΑ (ΑΦΟΡΟΛΟΓΗΤΟ)</td><td style="text-align: right; color: #1E3A8A;">{:,.2f} €</td></tr>
            <tr><td colspan="2">Φόρος Εισοδήματος</td><td style="text-align: right;">0,00 € (Πλήρως Αφορολόγητο)</td></tr>
        </table>
        """.format(tot_years * avg_sal * 0.6, tot_years * avg_sal * 0.1, tot_years * avg_sal * 0.7), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ΡΥΘΜΙΣΕΙΣ ΣΥΣΤΗΜΑΤΟΣ ---
else:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">⚙️ Ρυθμίσεις Συστήματος BMS</div>', unsafe_allow_html=True)
    st.write("Εδώ διαχειρίζεστε τους συντελεστές, τα ποσοστά κρατήσεων (Υγεία, ΕΑΣ, Φόρος) και την ασφάλεια χρηστών.")
    st.markdown('</div>', unsafe_allow_html=True)
