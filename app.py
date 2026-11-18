import streamlit as st
import pandas as pd
import io
import sqlite3

# Ρύθμιση σελίδας
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# ==========================================
# ΣΥΝΔΕΣΗ & ΔΗΜΙΟΥΡΓΙΑ / ΕΝΗΜΕΡΩΣΗ ΒΑΣΗΣ (SQLITE)
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
            summary_avg_salary REAL,
            merida_amount REAL,
            tapilt_net REAL,
            tapilt_after_expiry REAL,
            bank_years_until_2013 REAL,
            bank_years_from_2014 REAL
        )
    ''')
    cursor.execute("PRAGMA table_info(client_profile)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'merida_amount' not in columns:
        cursor.execute("ALTER TABLE client_profile ADD COLUMN merida_amount REAL")
    if 'tapilt_net' not in columns:
        cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_net REAL")
    if 'tapilt_after_expiry' not in columns:
        cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_after_expiry REAL")
    if 'bank_years_until_2013' not in columns:
        cursor.execute("ALTER TABLE client_profile ADD COLUMN bank_years_until_2013 REAL")
    if 'bank_years_from_2014' not in columns:
        cursor.execute("ALTER TABLE client_profile ADD COLUMN bank_years_from_2014 REAL")
        
    conn.commit()
    conn.close()

init_db()

def save_to_db(data):
    conn = sqlite3.connect('pension_bms.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM client_profile')
    cursor.execute('''
        INSERT INTO client_profile (
            first_name, last_name, gender, birth_date, insurance_cat, first_work_date, 
            econ_mode, paste_input, summary_years, summary_avg_salary, merida_amount, tapilt_net, tapilt_after_expiry,
            bank_years_until_2013, bank_years_from_2014
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["first_name"], data["last_name"], data["gender"], data["birth_date"],
        data["insurance_cat"], data["first_work_date"], data["econ_mode"],
        data["paste_input"], data["summary_years"], data["summary_avg_salary"],
        data["merida_amount"], data["tapilt_net"], data["tapilt_after_expiry"],
        data["bank_years_until_2013"], data["bank_years_from_2014"]
    ))
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect('pension_bms.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT first_name, last_name, gender, birth_date, insurance_cat, first_work_date, 
               econ_mode, paste_input, summary_years, summary_avg_salary, merida_amount, tapilt_net, tapilt_after_expiry,
               bank_years_until_2013, bank_years_from_2014 
        FROM client_profile LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "first_name": row[0], "last_name": row[1], "gender": row[2],
            "birth_date": row[3], "insurance_cat": row[4], "first_work_date": row[5],
            "econ_mode": row[6], "paste_input": row[7], "summary_years": row[8], 
            "summary_avg_salary": row[9], 
            "merida_amount": row[10] if row[10] is not None else 71206.66,
            "tapilt_net": row[11] if row[11] is not None else 329.00,
            "tapilt_after_expiry": row[12] if row[12] is not None else 100.00,
            "bank_years_until_2013": row[13] if row[13] is not None else 22.90,
            "bank_years_from_2014": row[14] if row[14] is not None else 9.0
        }
    return None

# CSS για επαγγελματικό ERP design
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white; padding: 24px 30px; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15); margin-bottom: 25px;
    }
    .main-title { font-size: 26px; font-weight: bold; margin: 0; display: flex; align-items: center; gap: 12px; }
    .main-subtitle { font-size: 13px; color: #E2E8F0; margin-top: 6px; }
    .panel-card {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .panel-header { font-size: 18px; font-weight: bold; color: #1E293B; margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
    .panel-desc { font-size: 13px; color: #64748B; margin-bottom: 15px; }
    .login-box {
        max-width: 450px; margin: 80px auto; background: white; padding: 35px;
        border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.08); border: 1px solid #E2E8F0;
    }
    .excel-table-header { background-color: #1E3A8A; color: white; text-align: center; font-weight: bold; padding: 8px; border: 1px solid #CBD5E1; }
    .excel-gold-header { background-color: #856404; color: white; text-align: center; font-weight: bold; padding: 8px; border: 1px solid #CBD5E1; }
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
# ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE
# ==========================================
db_data = load_from_db()

if 'client_data' not in st.session_state:
    st.session_state.client_data = {
        "first_name": db_data["first_name"] if db_data else "Νεκτάριος", 
        "last_name": db_data["last_name"] if db_data else "Πελεκάνος", 
        "gender": db_data["gender"] if db_data else "Άνδρας",
        "birth_date": db_data["birth_date"] if db_data else "16/09/1969", 
        "insurance_cat": db_data["insurance_cat"] if db_data else "Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)", 
        "first_work_date": db_data["first_work_date"] if db_data else "01/06/1990"
    }

if 'econ_mode' not in st.session_state:
    st.session_state.econ_mode = db_data["econ_mode"] if db_data else "🔄 Αναλυτικά (Πίνακας Περιόδων)"

if 'paste_input' not in st.session_state:
    st.session_state.paste_input = db_data["paste_input"] if db_data else "2002\t01/07/2002\t31/07/2002\tΤΡΑΠΕΖΑ\t25\t3358.78"

if 'summary_years' not in st.session_state:
    st.session_state.summary_years = db_data["summary_years"] if db_data else 0.08

if 'summary_avg_salary' not in st.session_state:
    st.session_state.summary_avg_salary = db_data["summary_avg_salary"] if db_data else 3358.78

if 'merida_amount' not in st.session_state:
    st.session_state.merida_amount = db_data["merida_amount"] if db_data else 71206.66

if 'tapilt_net' not in st.session_state:
    st.session_state.tapilt_net = db_data["tapilt_net"] if db_data else 329.00

if 'tapilt_after_expiry' not in st.session_state:
    st.session_state.tapilt_after_expiry = db_data["tapilt_after_expiry"] if db_data else 100.00

if 'bank_years_until_2013' not in st.session_state:
    st.session_state.bank_years_until_2013 = db_data["bank_years_until_2013"] if db_data else 22.90

if 'bank_years_from_2014' not in st.session_state:
    st.session_state.bank_years_from_2014 = db_data["bank_years_from_2014"] if db_data else 9.0

# Ειδικές μεταβλητές για προηγμένο Εφάπαξ
if 'efap_avg_5y' not in st.session_state:
    st.session_state.efap_avg_5y = 3479.25
if 'efap_tmima_b' not in st.session_state:
    st.session_state.efap_tmima_b = 15478.35
if 'efap_repl_rate' not in st.session_state:
    st.session_state.efap_repl_rate = 60.00

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
        "summary_avg_salary": float(st.session_state.summary_avg_salary),
        "merida_amount": float(st.session_state.merida_amount),
        "tapilt_net": float(st.session_state.tapilt_net),
        "tapilt_after_expiry": float(st.session_state.tapilt_after_expiry),
        "bank_years_until_2013": float(st.session_state.bank_years_until_2013),
        "bank_years_from_2014": float(st.session_state.bank_years_from_2014)
    }
    save_to_db(full_data)

# ==========================================
# ΜΕΝΟΥ & ΕΦΑΡΜΟΓΗ
# ==========================================
st.markdown(f"""
    <div class="main-header">
        <div class="main-title">
            <span>💼</span> Professional Pension BMS — Χρήστης: <u>{st.session_state.get('current_user', 'Χρήστης')}</u>
        </div>
        <div class="main-subtitle">Επαγγελματικό Σύστημα Υπολογισμού Συντάξεων (Ν. 4387/2016) - Πλήρης Έλεγχος Εφάπαξ</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"👤 **Συνδεδεμένος:** {st.session_state.get('current_user', '')}")
if st.sidebar.button("🚪 Αποσύνδεση"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Μενού")
app_section = st.sidebar.radio("Επιλογή:", [
    "👤 Προσωπικά Στοιχεία", 
    "💰 Οικονομικά & Ασφαλιστικά Στοιχεία", 
    "📊 Συγκεντρωτικά Αποτελέσματα", 
    "💼 Υπολογισμός Εφάπαξ",
    "📋 Τελική Εικόνα & Εκτύπωση"
])

# Υπολογισμός κοινών στοιχείων
if 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
    df_res = st.session_state['df_economic']
    df_res['ΕΤΟΣ_NUM'] = pd.to_numeric(df_res['ΕΤΟΣ'], errors='coerce').fillna(0)
    tot_ensima = df_res['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
    tot_years = tot_ensima / 300.0 if tot_ensima > 0 else 0.08
    df_post_2002 = df_res[df_res['ΕΤΟΣ_NUM'] >= 2002]
    avg_sal = (df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'] * df_post_2002['ΑΠΟΔΟΧΕΣ (€)']).sum() / df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum() if not df_post_2002.empty and df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum() > 0 else 3358.78
else:
    tot_ensima = 25
    tot_years = 0.08
    avg_sal = 3358.78

# --- 1. ΠΡΟΣΩΠΙΚΑ ΣΤΟΙΧΕΙΑ ---
if app_section == "👤 Προσωπικά Στοιχεία":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">👤 Προσωπικά Στοιχεία Πελάτη</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.client_data["first_name"] = st.text_input("Όνομα", value=st.session_state.client_data["first_name"])
    with col2:
        st.session_state.client_data["last_name"] = st.text_input("Επώνυμο", value=st.session_state.client_data["last_name"])
    with col3:
        genders = ["Άνδρας", "Γυναίκα"]
        g_idx = genders.index(st.session_state.client_data["gender"]) if st.session_state.client_data["gender"] in genders else 0
        st.session_state.client_data["gender"] = st.selectbox("Φύλο", genders, index=g_idx)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.session_state.client_data["birth_date"] = st.text_input("Ημερομηνία Γέννησης", value=st.session_state.client_data["birth_date"])
    with col5:
        cats = ["Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)", "Δημόσιος Τομέας", "Τραπεζοϋπαλληλος"]
        c_idx = cats.index(st.session_state.client_data["insurance_cat"]) if st.session_state.client_data["insurance_cat"] in cats else 0
        st.session_state.client_data["insurance_cat"] = st.selectbox("Κατηγορία Ασφάλισης", cats, index=c_idx)
    with col6:
        st.session_state.client_data["first_work_date"] = st.text_input("Ημερομηνία Πρώτης Απασχόλησης", value=st.session_state.client_data["first_work_date"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Αποθήκευση", type="primary"):
        persist_all()
        st.success("✅ Τα στοιχεία αποθηκεύτηκαν!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. ΟΙΚΟΝΟΜΙΚΑ & ΑΣΦΑΛΙΣΤΙΚΑ ΣΤΟΙΧΕΙΑ ---
elif app_section == "💰 Οικονομικά & Ασφαλιστικά Στοιχεία":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💰 Οικονομικά & Ασφαλιστικά Στοιχεία</div>', unsafe_allow_html=True)
    
    modes = ["🔄 Αναλυτικά (Πίνακας Περιόδων)", "⚡ Συγκεντρωτικά"]
    m_idx = modes.index(st.session_state.econ_mode) if st.session_state.econ_mode in modes else 0
    st.session_state.econ_mode = st.radio("Τρόπος καταχώρησης:", modes, index=m_idx, horizontal=True)

    df_parsed = pd.DataFrame()
    if st.session_state.econ_mode == "🔄 Αναλυτικά (Πίνακας Περιόδων)":
        st.session_state.paste_input = st.text_area("Επικόλληση δεδομένων Excel (ΕΤΟΣ | ΑΠΟ | ΕΩΣ | ΦΟΡΕΑΣ | ΗΜΕΡΕΣ | ΑΠΟΔΟΧΕΣ):", value=st.session_state.paste_input, height=120)
        if st.session_state.paste_input.strip():
            try:
                final_data = []
                lines = st.session_state.paste_input.strip().split('\n')
                for line in lines:
                    parts = line.replace('\t', ' ').split()
                    if len(parts) >= 6:
                        raw_apod = parts[-1].replace('€', '').replace('.', '').replace(',', '.').strip()
                        try:
                            val_apod = float(raw_apod)
                        except:
                            try:
                                val_apod = float(parts[-2].replace('€', '').replace('.', '').replace(',', '.').strip())
                            except:
                                val_apod = 0.0

                        try:
                            val_ens = float(parts[-3].replace(',', '.')) if '€' in parts[-1] else float(parts[-2].replace(',', '.'))
                        except:
                            val_ens = 25.0

                        final_data.append({
                            "ΕΤΟΣ": parts[0],
                            "ΑΠΟ (ΗΜ/ΝΙΑ)": parts[1],
                            "ΕΩΣ (ΗΜ/ΝΙΑ)": parts[2],
                            "ΦΟΡΕΑΣ": parts[3].upper(),
                            "ΕΝΣΗΜΑ (Η.Ε.)": val_ens,
                            "ΑΠΟΔΟΧΕΣ (€)": val_apod
                        })
                df_parsed = pd.DataFrame(final_data)
            except Exception as e:
                st.error(f"Σφάλμα: {e}")

        if df_parsed.empty and 'df_economic' in st.session_state:
            df_parsed = st.session_state['df_economic']
        elif df_parsed.empty:
            df_parsed = pd.DataFrame([{"ΕΤΟΣ": "2002", "ΑΠΟ (ΗΜ/ΝΙΑ)": "01/07/2002", "ΕΩΣ (ΗΜ/ΝΙΑ)": "31/07/2002", "ΦΟΡΕΑΣ": "ΤΡΑΠΕΖΑ", "ΕΝΣΗΜΑ (Η.Ε.)": 25.0, "ΑΠΟΔΟΧΕΣ (€)": 3358.78}])

        if not df_parsed.empty:
            df_edited = st.data_editor(df_parsed, num_rows="dynamic", use_container_width=True, hide_index=True)
            df_edited['ΕΝΣΗΜΑ (Η.Ε.)'] = pd.to_numeric(df_edited['ΕΝΣΗΜΑ (Η.Ε.)'], errors='coerce').fillna(0)
            df_edited['ΑΠΟΔΟΧΕΣ (€)'] = pd.to_numeric(df_edited['ΑΠΟΔΟΧΕΣ (€)'], errors='coerce').fillna(0.0)
            df_edited['ΕΤΟΣ_NUM'] = pd.to_numeric(df_edited['ΕΤΟΣ'], errors='coerce').fillna(0)
            st.session_state['df_economic'] = df_edited
    
    if st.button("💾 Αποθήκευση Οικονομικών", type="primary"):
        persist_all()
        st.success("✅ Αποθηκεύτηκαν επιτυχώς!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ ---
elif app_section == "📊 Συγκεντρωτικά Αποτελέσματα":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 Συγκεντρωτικά Στοιχεία & Υπολογισμός Συντάξεων</div>', unsafe_allow_html=True)
    
    ethniki = 446.87
    pososto_anapl = min(0.15 + (tot_years * 0.012), 0.52)
    antapodotiki = avg_sal * pososto_anapl
    kria_mikto = ethniki + antapodotiki + 350.0  
    eas_val = 232.73 if kria_mikto > 1400 else 0.00
    ygeia_val = kria_mikto * 0.06
    foros_val = 328.30
    synolo_krat = eas_val + ygeia_val + foros_val
    katharo_main = max(kria_mikto - synolo_krat, 0.0)

    st.metric("Συνολικά Έτη Ασφάλισης", f"{tot_years:.2f}")
    st.metric("Μέσος Μισθός (από 2002)", f"{avg_sal:,.2f} €")
    st.metric("Εκτιμώμενη Καθαρή Κύρια Σύνταξη", f"{katharo_main:,.2f} € / μήνα")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ (ΠΛΗΡΗΣ ΝΟΜΙΚΟΣ ΕΛΕΓΧΟΣ) ---
elif app_section == "💼 Υπολογισμός Εφάπαξ":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💼 ΠΛΗΡΗΣ ΝΟΜΙΚΟΣ & ΠΑΡΑΜΕΤΡΙΚΟΣ ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ (Ν. 4387/2016)</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Ρυθμίστε τις παραμέτρους σύμφωνα με τις επίσημες οδηγίες και τους κανόνες του Ταμείου σας.</div>', unsafe_allow_html=True)

    # Αναλυτικό επεξηγητικό πλαίσιο για απόλυτη διαφάνεια
    st.info("📌 **Νομική Τεκμηρίωση & Επιλογές Υπολογισμού:**\n"
            "• **Τμήμα Α (έως 31/12/2013):** Βασίζεται στον μέσο όρο της πενταετίας 2009–2013. Μπορείτε να επιλέξετε αν θα χρησιμοποιήσετε τον μικτό μισθό (με τα δώρα) ή τον καθαρό τακτικό μισθό (χωρίς τα δώρα, με αναγωγή 12/14).\n"
            "• **Ποσοστό Αναπλήρωσης:** Ο νόμος ορίζει 60% για εισφορά 4%. Αν η συνολική σας εισφορά πρόνοιας ήταν 7% (3%+4%), δοκιμάστε να αυξήσετε το ποσοστό αναλογικά για να δείτε την επίδραση.\n"
            "• **Τμήμα Β (από 2014 και μετά):** Βασίζεται στις πραγματικές κατατεθειμένες εισφορές της ατομικής σας μερίδας.")

    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        b_until_2013 = st.number_input("Έτη έως 31/12/2013 (Τμήμα Α)", value=float(st.session_state.bank_years_until_2013), step=0.1)
    with col_in2:
        b_from_2014 = st.number_input("Έτη από 2014 και μετά (Τμήμα Β)", value=float(st.session_state.bank_years_from_2014), step=0.1)
    with col_in3:
        st.session_state.efap_repl_rate = st.number_input("Συντελεστής Αναπλήρωσης Τμήματος Α (%)", value=float(st.session_state.efap_repl_rate), step=1.0, help="60% για 4% εισφορά, ή υψηλότερο αν υπολογιστεί αναλογία για 7%")

    col_in4, col_in5 = st.columns(2)
    with col_in4:
        st.session_state.efap_avg_5y = st.number_input("Μέσος Μην. Μισθός Πενταετίας 2009–2013 (€)", value=float(st.session_state.efap_avg_5y), step=10.0, help="2.982,21 € (χωρίς δώρα) ή 3.479,25 € (με δώρα)")
    with col_in5:
        st.session_state.efap_tmima_b = st.number_input("Συνολικό Ποσό Τμήματος Β (Εισφορές από 2014) (€)", value=float(st.session_state.efap_tmima_b), step=100.0, help="Άθροισμα πραγματικών εισφορών ατομικής μερίδας")

    # Υπολογισμοί
    monthly_taktiko_tA = st.session_state.efap_avg_5y
    tmima_a = b_until_2013 * monthly_taktiko_tA * (st.session_state.efap_repl_rate / 100.0)
    tmima_b = st.session_state.efap_tmima_b
    total_efapax = tmima_a + tmima_b

    st.markdown("<br>", unsafe_allow_html=True)
    
    efap_col1, efap_col2 = st.columns(2)
    with efap_col1:
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-gold-header"><th colspan="2">ΒΑΣΙΚΕΣ ΠΑΡΑΜΕΤΡΟΙ ΕΦΑΠΑΞ</th></tr>
            <tr><td><b>Μηνιαία Βάση Τμήματος Α</b></td><td style="text-align: right; color: blue;"><b>{monthly_taktiko_tA:,.2f} €</b></td></tr>
            <tr><td><b>Συντελεστής Αναπλήρωσης</b></td><td style="text-align: center; color: blue;"><b>{st.session_state.efap_repl_rate:.2f}%</b></td></tr>
            <tr><td><b>Έτη Τμήματος Α (έως 2013)</b></td><td style="text-align: center;">{b_until_2013:.2f} έτη</td></tr>
            <tr><td><b>Έτη Τμήματος Β (από 2014)</b></td><td style="text-align: center;">{b_from_2014:.2f} έτη</td></tr>
        </table>
        """, unsafe_allow_html=True)

    with efap_col2:
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-table-header"><th colspan="2">ΤΕΛΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ (Ν. 4387/2016)</th><th>ΠΟΣΟ (€)</th></tr>
            <tr><td colspan="2">1. Τμήμα Α (Έως 2013)</td><td style="text-align: right;">{tmima_a:,.2f} €</td></tr>
            <tr><td colspan="2">2. Τμήμα Β (Εισφορές από 2014)</td><td style="text-align: right;">{tmima_b:,.2f} €</td></tr>
            <tr style="background-color: #E2E8F0; font-weight: bold;"><td colspan="2">🌟 ΣΥΝΟΛΙΚΟ ΚΑΘΑΡΟ ΕΦΑΠΑΞ</td><td style="text-align: right; color: #1E3A8A;">{total_efapax:,.2f} €</td></tr>
            <tr><td colspan="2">Φόρος Εισοδήματος</td><td style="text-align: right;">0,00 € (100% Αφορολόγητο)</td></tr>
        </table>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ΤΕΛΙΚΗ ΕΙΚΟΝΑ & ΕΚΤΥΠΩΣΗ ---
else:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📋 Συνοπτική Αναφορά & Εκτύπωση</div>', unsafe_allow_html=True)
    
    monthly_tak_fin = st.session_state.efap_avg_5y
    total_efapax_fin = (st.session_state.bank_years_until_2013 * monthly_tak_fin * (st.session_state.efap_repl_rate / 100.0)) + st.session_state.efap_tmima_b

    c_name = f"{st.session_state.client_data['first_name']} {st.session_state.client_data['last_name']}"
    
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; padding: 20px; border-radius: 10px; font-size: 14px;">
        <h3 style="color: #1E3A8A; margin-top: 0;">📄 ΕΠΙΣΗΜΗ ΣΥΝΟΨΗ ΠΕΛΑΤΗ: {c_name}</h3>
        <hr style="margin: 10px 0;">
        <p><b>Συνολικά Έτη Ασφάλισης:</b> {tot_years:.2f} έτη</p>
        <p><b>Προβλεπόμενη Ημερομηνία Εξόδου:</b> 16/09/2031 (Στα 62 με 40ετία)</p>
        <hr style="margin: 10px 0;">
        <p style="font-size: 16px; color: #16A34A;"><b>💼 ΣΥΝΟΛΙΚΟ ΚΑΘΑΡΟ ΕΦΑΠΑΞ:</b> <b>{total_efapax_fin:,.2f} €</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🖨️ Εκτύπωση / Αποθήκευση PDF", type="primary"):
        st.info("💡 Πατήστε **Ctrl + P** στον περιηγητή σας.")
    st.markdown('</div>', unsafe_allow_html=True)
