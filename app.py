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

# ==========================================
# ΝΟΜΙΚΟΙ ΥΠΟΛΟΓΙΣΜΟΙ ΣΥΝΤΑΞΗΣ (Ν. 4387/2016 & Ν. 4670/2020)
# ==========================================
def calc_pososto_anaplirosis(years: float) -> float:
    """Ακριβής πίνακας ποσοστών αναπλήρωσης Ν. 4670/2020 (Βρούτση)."""
    if years <= 0:
        return 0.0
    brackets = [
        (15.0, 0.0077),
        (18.0, 0.0084),
        (21.0, 0.0146),
        (24.0, 0.0171),
        (27.0, 0.0196),
        (30.0, 0.0221),
        (33.0, 0.0255),
        (36.0, 0.0255),
        (40.0, 0.0255),
    ]
    total_rate = 0.0
    prev_limit = 0.0
    for upper, rate in brackets:
        if years > prev_limit:
            span = min(years, upper) - prev_limit
            total_rate += span * rate
            prev_limit = upper
        else:
            break
    if years > 40.0:
        total_rate += (years - 40.0) * 0.0050
    return total_rate

def calc_ethniki_syntaksi(years: float, full_ethniki: float = 446.87) -> float:
    """Εθνική σύνταξη: Πλήρης για >= 20 έτη, -2% ανά έτος κάτω από 20 έως 15."""
    if years < 15.0:
        return 0.0
    if years >= 20.0:
        return full_ethniki
    reduction = (20.0 - years) * 0.02
    return full_ethniki * (1.0 - reduction)

def calc_eas(gross_main: float) -> float:
    """Εισφορά Αλληλεγγύης Συνταξιούχων (ΕΑΣ) επί της κύριας σύνταξης."""
    if gross_main <= 1434.0:
        return 0.0
    if gross_main <= 1741.0:
        rate = 0.03
    elif gross_main <= 2048.0:
        rate = 0.06
    elif gross_main <= 2355.0:
        rate = 0.07
    elif gross_main <= 2662.0:
        rate = 0.09
    elif gross_main <= 2969.0:
        rate = 0.10
    elif gross_main <= 3276.0:
        rate = 0.12
    elif gross_main <= 3583.0:
        rate = 0.13
    else:
        rate = 0.14
    eas = gross_main * rate
    # Κανόνας μη πτώσης κάτω από το όριο των 1.434 €
    return min(eas, gross_main - 1434.0)

def calc_monthly_tax(taxable_monthly: float, children: int = 0) -> float:
    """Υπολογισμός μηνιαίας παρακράτησης φόρου εισοδήματος (ετήσια κλίμακα / 12)."""
    annual = taxable_monthly * 12.0
    if annual <= 0:
        return 0.0

    # Κλίμακα φόρου μισθωτών/συνταξιούχων
    if annual <= 10000:
        gross_tax = annual * 0.09
    elif annual <= 20000:
        gross_tax = 900.0 + (annual - 10000.0) * 0.22
    elif annual <= 30000:
        gross_tax = 3100.0 + (annual - 20000.0) * 0.28
    elif annual <= 40000:
        gross_tax = 5900.0 + (annual - 30000.0) * 0.36
    else:
        gross_tax = 9500.0 + (annual - 40000.0) * 0.44

    # Έκπτωση φόρου (αφορολόγητο)
    base_discount = {0: 777.0, 1: 810.0, 2: 900.0, 3: 1120.0}.get(children, 1340.0)
    if annual > 12000.0:
        discount = max(0.0, base_discount - ((annual - 12000.0) / 1000.0) * 20.0)
    else:
        discount = base_discount

    annual_tax = max(0.0, gross_tax - discount)
    return annual_tax / 12.0

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
    st.session_state.summary_years = db_data["summary_years"] if db_data else 40.00

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
        <div class="main-subtitle">Επαγγελματικό Σύστημα Υπολογισμού Συντάξεων & Εφάπαξ (Ν. 4387/2016 & Ν. 4670/2020)</div>
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

# Υπολογισμός ετών & μέσου μισθού ανάλογα με τη λειτουργία (Αναλυτικά vs Συγκεντρωτικά)
if st.session_state.econ_mode == "⚡ Συγκεντρωτικά":
    tot_years = float(st.session_state.summary_years)
    tot_ensima = tot_years * 300.0
    avg_sal = float(st.session_state.summary_avg_salary)
elif 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
    df_res = st.session_state['df_economic']
    df_res['ΕΤΟΣ_NUM'] = pd.to_numeric(df_res['ΕΤΟΣ'], errors='coerce').fillna(0)
    tot_ensima = df_res['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
    tot_years = tot_ensima / 300.0 if tot_ensima > 0 else float(st.session_state.summary_years)
    df_post_2002 = df_res[df_res['ΕΤΟΣ_NUM'] >= 2002]
    avg_sal = (
        (df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'] * df_post_2002['ΑΠΟΔΟΧΕΣ (€)']).sum() / df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
        if not df_post_2002.empty and df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum() > 0
        else float(st.session_state.summary_avg_salary)
    )
else:
    tot_years = float(st.session_state.summary_years)
    tot_ensima = tot_years * 300.0
    avg_sal = float(st.session_state.summary_avg_salary)

# Κοινός υπολογισμός Κύριας & Επικουρικής Σύνταξης (Ν. 4670/2020)
ethniki = calc_ethniki_syntaksi(tot_years, 446.87)
pososto_anapl = calc_pososto_anaplirosis(tot_years)
antapodotiki = avg_sal * pososto_anapl
kria_mikto = ethniki + antapodotiki

eas_val = calc_eas(kria_mikto)
ygeia_val = (kria_mikto - eas_val) * 0.06
taxable_main = max(0.0, kria_mikto - eas_val - ygeia_val)
foros_val = calc_monthly_tax(taxable_main)
synolo_krat = eas_val + ygeia_val + foros_val
katharo_main = max(kria_mikto - synolo_krat, 0.0)

tapilt_katharo = float(st.session_state.tapilt_net)
tapilt_mikto = tapilt_katharo / 0.94 if tapilt_katharo > 0 else 0.0
tapilt_krat = tapilt_mikto - tapilt_katharo

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
    else:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.session_state.summary_years = st.number_input("Συνολικά Έτη Ασφάλισης (π.χ. 40,00)", value=float(st.session_state.summary_years), step=0.1)
        with col_s2:
            st.session_state.summary_avg_salary = st.number_input("Συντάξιμες Αποδοχές από 2002 (€)", value=float(st.session_state.summary_avg_salary), step=10.0)

    st.markdown("---")
    st.markdown("#### 🏦 Στοιχεία Επικουρικής & ΤΑΠΙΛΤ-ΑΤ")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.session_state.merida_amount = st.number_input("Ατομική Μερίδα / Κεφάλαιο (€)", value=float(st.session_state.merida_amount), step=100.0)
    with col_t2:
        st.session_state.tapilt_net = st.number_input("Καθαρή Επικουρική ΤΑΠΙΛΤ-ΑΤ (€/μήνα)", value=float(st.session_state.tapilt_net), step=5.0)
    with col_t3:
        st.session_state.tapilt_after_expiry = st.number_input("ΤΑΠΙΛΤ μετά τη λήξη (€/μήνα)", value=float(st.session_state.tapilt_after_expiry), step=5.0)

    if st.button("💾 Αποθήκευση Οικονομικών", type="primary"):
        persist_all()
        st.success("✅ Αποθηκεύτηκαν επιτυχώς!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ ---
elif app_section == "📊 Συγκεντρωτικά Αποτελέσματα":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 Αναλυτικός Υπολογισμός Συντάξεων (Ν. 4387/2016 & Ν. 4670/2020)</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Συνολικά Έτη Ασφάλισης", f"{tot_years:.2f} έτη")
    c2.metric("Μέσος Μισθός (από 2002)", f"{avg_sal:,.2f} €")
    c3.metric("Ποσοστό Αναπλήρωσης", f"{pososto_anapl * 100:.2f}%")
    c4.metric("Συνολικό Μηνιαίο Καθαρό", f"{katharo_main + tapilt_katharo:,.2f} €")

    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-table-header"><th colspan="2">ΑΝΑΛΥΣΗ ΚΥΡΙΑΣ ΣΥΝΤΑΞΗΣ (e-ΕΦΚΑ)</th></tr>
            <tr><td>Εθνική Σύνταξη ({tot_years:.2f} έτη)</td><td style="text-align: right;">{ethniki:,.2f} €</td></tr>
            <tr><td>Ανταποδοτική ({avg_sal:,.2f} € × {pososto_anapl*100:.2f}%)</td><td style="text-align: right;">{antapodotiki:,.2f} €</td></tr>
            <tr style="background-color: #F1F5F9; font-weight: bold;"><td>Μικτή Κύρια Σύνταξη</td><td style="text-align: right;">{kria_mikto:,.2f} €</td></tr>
            <tr><td>Κράτηση ΕΑΣ (Κλιμακωτή)</td><td style="text-align: right; color: #DC2626;">-{eas_val:,.2f} €</td></tr>
            <tr><td>Κράτηση Υγείας (6%)</td><td style="text-align: right; color: #DC2626;">-{ygeia_val:,.2f} €</td></tr>
            <tr><td>Παρακράτηση Φόρου Εισοδήματος</td><td style="text-align: right; color: #DC2626;">-{foros_val:,.2f} €</td></tr>
            <tr style="background-color: #E2E8F0; font-weight: bold;"><td>🌟 ΚΑΘΑΡΗ ΚΥΡΙΑ ΣΥΝΤΑΞΗ</td><td style="text-align: right; color: #1E3A8A;">{katharo_main:,.2f} €</td></tr>
        </table>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-gold-header"><th colspan="2">ΕΠΙΚΟΥΡΙΚΗ & ΤΑΠΙΛΤ-ΑΤ</th></tr>
            <tr><td>Μικτή Επικουρική / ΤΑΠΙΛΤ</td><td style="text-align: right;">{tapilt_mikto:,.2f} €</td></tr>
            <tr><td>Κράτηση Υγείας (6%)</td><td style="text-align: right; color: #DC2626;">-{tapilt_krat:,.2f} €</td></tr>
            <tr style="background-color: #F1F5F9; font-weight: bold;"><td>Καθαρή Επικουρική / ΤΑΠΙΛΤ</td><td style="text-align: right;">{tapilt_katharo:,.2f} €</td></tr>
            <tr><td>Ποσό ΤΑΠΙΛΤ μετά τη λήξη</td><td style="text-align: right;">{st.session_state.tapilt_after_expiry:,.2f} €</td></tr>
            <tr><td>Ατομική Μερίδα</td><td style="text-align: right;">{st.session_state.merida_amount:,.2f} €</td></tr>
            <tr style="background-color: #DCFCE7; font-weight: bold;"><td>💰 ΣΥΝΟΛΙΚΟ ΚΑΘΑΡΟ ΜΗΝΙΑΙΟ</td><td style="text-align: right; color: #16A34A;">{katharo_main + tapilt_katharo:,.2f} €</td></tr>
        </table>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ (ΠΛΗΡΗΣ ΝΟΜΙΚΟΣ ΕΛΕΓΧΟΣ) ---
elif app_section == "💼 Υπολογισμός Εφάπαξ":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💼 ΠΛΗΡΗΣ ΝΟΜΙΚΟΣ & ΠΑΡΑΜΕΤΡΙΚΟΣ ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ (Ν. 4387/2016)</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Ρυθμίστε τις παραμέτρους σύμφωνα με τις επίσημες οδηγίες και τους κανόνες του Ταμείου σας.</div>', unsafe_allow_html=True)

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
        <p><b>Συνολικά Έτη Ασφάλισης:</b> {tot_years:.2f} έτη (Ποσοστό Αναπλήρωσης: {pososto_anapl*100:.2f}%)</p>
        <p><b>Συντάξιμες Αποδοχές (από 2002):</b> {avg_sal:,.2f} €</p>
        <p><b>Προβλεπόμενη Ημερομηνία Εξόδου:</b> 16/09/2031 (Στα 62 με 40ετία)</p>
        <hr style="margin: 10px 0;">
        <p><b>🏛️ Καθαρή Κύρια Σύνταξη:</b> {katharo_main:,.2f} € / μήνα (Μικτή: {kria_mikto:,.2f} €)</p>
        <p><b>🏦 Καθαρή Επικουρική / ΤΑΠΙΛΤ-ΑΤ:</b> {tapilt_katharo:,.2f} € / μήνα</p>
        <p style="font-size: 16px; color: #1E3A8A;"><b>💶 ΣΥΝΟΛΙΚΗ ΚΑΘΑΡΗ ΜΗΝΙΑΙΑ ΣΥΝΤΑΞΗ:</b> <b>{katharo_main + tapilt_katharo:,.2f} € / μήνα</b></p>
        <hr style="margin: 10px 0;">
        <p style="font-size: 16px; color: #16A34A;"><b>💼 ΣΥΝΟΛΙΚΟ ΚΑΘΑΡΟ ΕΦΑΠΑΞ:</b> <b>{total_efapax_fin:,.2f} €</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🖨️ Εκτύπωση / Αποθήκευση PDF", type="primary"):
        st.info("💡 Πατήστε **Ctrl + P** στον περιηγητή σας.")
    st.markdown('</div>', unsafe_allow_html=True)
