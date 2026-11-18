import streamlit as st
import pandas as pd
import io
import sqlite3

# Ρύθμιση σελίδας
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# ==========================================
# ΣΥΝΔΕΣΗ & ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (SQLITE)
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
            bank_years_from_2014 REAL,
            pososto_anapl_custom REAL,
            isoδynama_eti_tapilt REAL,
            tapilt_duration_years REAL
        )
    ''')
    cursor.execute("PRAGMA table_info(client_profile)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'merida_amount' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN merida_amount REAL")
    if 'tapilt_net' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_net REAL")
    if 'tapilt_after_expiry' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_after_expiry REAL")
    if 'bank_years_until_2013' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN bank_years_until_2013 REAL")
    if 'bank_years_from_2014' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN bank_years_from_2014 REAL")
    if 'pososto_anapl_custom' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN pososto_anapl_custom REAL")
    if 'isoδynama_eti_tapilt' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN isoδynama_eti_tapilt REAL")
    if 'tapilt_duration_years' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_duration_years REAL")
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
            bank_years_until_2013, bank_years_from_2014, pososto_anapl_custom, isoδynama_eti_tapilt, tapilt_duration_years
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["first_name"], data["last_name"], data["gender"], data["birth_date"],
        data["insurance_cat"], data["first_work_date"], data["econ_mode"],
        data["paste_input"], data["summary_years"], data["summary_avg_salary"],
        data["merida_amount"], data["tapilt_net"], data["tapilt_after_expiry"],
        data["bank_years_until_2013"], data["bank_years_from_2014"], data["pososto_anapl_custom"], 
        data["isoδynama_eti_tapilt"], data["tapilt_duration_years"]
    ))
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect('pension_bms.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT first_name, last_name, gender, birth_date, insurance_cat, first_work_date, 
               econ_mode, paste_input, summary_years, summary_avg_salary, merida_amount, tapilt_net, tapilt_after_expiry,
               bank_years_until_2013, bank_years_from_2014, pososto_anapl_custom, isoδynama_eti_tapilt, tapilt_duration_years 
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
            "tapilt_net": row[11] if row[11] is not None else 350.00,
            "tapilt_after_expiry": row[12] if row[12] is not None else 100.00,
            "bank_years_until_2013": row[13] if row[13] is not None else 22.90,
            "bank_years_from_2014": row[14] if row[14] is not None else 9.0,
            "pososto_anapl_custom": row[15] if row[15] is not None else 51.29,
            "isoδynama_eti_tapilt": row[16] if row[16] is not None else 21.37,
            "tapilt_duration_years": row[17] if row[17] is not None else 17.0
        }
    return None

def calc_ethniki_syntaksi(years: float, full_ethniki: float = 446.87) -> float:
    if years < 15.0: return 0.0
    if years >= 20.0: return full_ethniki
    return full_ethniki * (1.0 - (20.0 - years) * 0.02)

def calc_eas(gross_main: float) -> float:
    if gross_main <= 1434.0: return 0.0
    if gross_main <= 1741.0: rate = 0.03
    elif gross_main <= 2048.0: rate = 0.06
    elif gross_main <= 2355.0: rate = 0.07
    elif gross_main <= 2662.0: rate = 0.09
    elif gross_main <= 2969.0: rate = 0.10
    elif gross_main <= 3276.0: rate = 0.12
    elif gross_main <= 3583.0: rate = 0.13
    else: rate = 0.14
    return min(gross_main * rate, gross_main - 1434.0)

def calc_monthly_tax(taxable_monthly: float) -> float:
    annual = taxable_monthly * 12.0
    if annual <= 0: return 0.0
    if annual <= 10000: gross_tax = annual * 0.09
    elif annual <= 20000: gross_tax = 900.0 + (annual - 10000.0) * 0.22
    elif annual <= 30000: gross_tax = 3100.0 + (annual - 20000.0) * 0.28
    elif annual <= 40000: gross_tax = 5900.0 + (annual - 30000.0) * 0.36
    else: gross_tax = 9500.0 + (annual - 40000.0) * 0.44
    discount = max(0.0, 777.0 - ((annual - 12000.0) / 1000.0) * 20.0) if annual > 12000.0 else 777.0
    return max(0.0, gross_tax - discount) / 12.0

# CSS
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white; padding: 24px 30px; border-radius: 12px; margin-bottom: 25px;
    }
    .main-title { font-size: 26px; font-weight: bold; margin: 0; display: flex; align-items: center; gap: 12px; }
    .main-subtitle { font-size: 13px; color: #E2E8F0; margin-top: 6px; }
    .panel-card {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 24px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .panel-header { font-size: 18px; font-weight: bold; color: #1E293B; margin-bottom: 8px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; font-family: sans-serif; }
    .custom-table th { background-color: #1E3A8A; color: white; text-align: center; padding: 8px; border: 1px solid #CBD5E1; }
    .custom-table th.kratseis { background-color: #856404; }
    .custom-table td { padding: 8px; border: 1px solid #CBD5E1; text-align: right; }
    .custom-table td.left { text-align: left; font-weight: bold; }
    .custom-table td.center { text-align: center; }
    .custom-table tr.total-row { background-color: #E2E8F0; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# LOGIN
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔒 Ασφαλής Είσοδος BMS</h2>", unsafe_allow_html=True)
    username = st.text_input("Όνομα Χρήστη")
    password = st.text_input("Κωδικός (Password)", type="password")
    if st.button("🔑 ΕΙΣΟΔΟΣ", use_container_width=True, type="primary"):
        if username.strip() and password.strip() == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else: st.error("❌ Λανθασμένος κωδικός! (Δοκιμάστε: 1234)")
    st.stop()

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

if 'econ_mode' not in st.session_state: st.session_state.econ_mode = db_data["econ_mode"] if db_data else "🔄 Αναλυτικά (Πίνακας Περιόδων)"
if 'paste_input' not in st.session_state: st.session_state.paste_input = db_data["paste_input"] if db_data else "2002\t01/07/2002\t31/07/2002\tΤΡΑΠΕΖΑ\t25\t3275.91"
if 'summary_years' not in st.session_state: st.session_state.summary_years = db_data["summary_years"] if db_data else 42.57
if 'summary_avg_salary' not in st.session_state: st.session_state.summary_avg_salary = db_data["summary_avg_salary"] if db_data else 3275.91
if 'merida_amount' not in st.session_state: st.session_state.merida_amount = db_data["merida_amount"] if db_data else 71206.66
if 'tapilt_net' not in st.session_state: st.session_state.tapilt_net = db_data["tapilt_net"] if db_data else 350.00
if 'tapilt_after_expiry' not in st.session_state: st.session_state.tapilt_after_expiry = db_data["tapilt_after_expiry"] if db_data else 100.00
if 'bank_years_until_2013' not in st.session_state: st.session_state.bank_years_until_2013 = db_data["bank_years_until_2013"] if db_data else 22.90
if 'bank_years_from_2014' not in st.session_state: st.session_state.bank_years_from_2014 = db_data["bank_years_from_2014"] if db_data else 9.0
if 'pososto_anapl_custom' not in st.session_state: st.session_state.pososto_anapl_custom = db_data["pososto_anapl_custom"] if db_data else 51.29
if 'isoδynama_eti_tapilt' not in st.session_state: st.session_state.isoδynama_eti_tapilt = db_data["isoδynama_eti_tapilt"] if db_data else 21.37
if 'tapilt_duration_years' not in st.session_state: st.session_state.tapilt_duration_years = db_data["tapilt_duration_years"] if db_data else 17.0

def persist_all():
    save_to_db({
        "first_name": st.session_state.client_data["first_name"], "last_name": st.session_state.client_data["last_name"],
        "gender": st.session_state.client_data["gender"], "birth_date": st.session_state.client_data["birth_date"],
        "insurance_cat": st.session_state.client_data["insurance_cat"], "first_work_date": st.session_state.client_data["first_work_date"],
        "econ_mode": st.session_state.econ_mode, "paste_input": st.session_state.paste_input,
        "summary_years": float(st.session_state.summary_years), "summary_avg_salary": float(st.session_state.summary_avg_salary),
        "merida_amount": float(st.session_state.merida_amount), "tapilt_net": float(st.session_state.tapilt_net),
        "tapilt_after_expiry": float(st.session_state.tapilt_after_expiry),
        "bank_years_until_2013": float(st.session_state.bank_years_until_2013),
        "bank_years_from_2014": float(st.session_state.bank_years_from_2014), 
        "pososto_anapl_custom": float(st.session_state.pososto_anapl_custom),
        "isoδynama_eti_tapilt": float(st.session_state.isoδynama_eti_tapilt),
        "tapilt_duration_years": float(st.session_state.tapilt_duration_years)
    })

st.markdown(f"""
    <div class="main-header">
        <div class="main-title"><span>💼</span> Professional Pension BMS</div>
        <div class="main-subtitle">Σύστημα Διαχείρισης Συντάξεων & Εφάπαξ (Ν. 4387/2016 & Ν. 4670/2020)</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🗂️ Μενού")
app_section = st.sidebar.radio("Επιλογή:", [
    "👤 Προσωπικά Στοιχεία", 
    "💰 Οικονομικά & Ασφαλιστικά Στοιχεία", 
    "📊 Συγκεντρωτικά Αποτελέσματα & Συντάξεις", 
    "💼 Υπολογισμός Εφάπαξ", 
    "📋 Τελική Εικόνα"
])

# ΑΝΑΓΝΩΣΗ ΔΕΔΟΜΕΝΩΝ ΠΙΝΑΚΑ
df_parsed = pd.DataFrame()
if st.session_state.econ_mode == "🔄 Αναλυτικά (Πίνακας Περιόδων)" and st.session_state.paste_input.strip():
    try:
        final_data = []
        for line in st.session_state.paste_input.strip().split('\n'):
            parts = line.replace('\t', ' ').split()
            if len(parts) >= 6:
                raw_apod = parts[-1].replace('€', '').replace('.', '').replace(',', '.').strip()
                try: val_apod = float(raw_apod)
                except:
                    try: val_apod = float(parts[-2].replace('€', '').replace('.', '').replace(',', '.').strip())
                    except: val_apod = 0.0
                try: val_ens = float(parts[-3].replace(',', '.')) if '€' in parts[-1] else float(parts[-2].replace(',', '.'))
                except: val_ens = 25.0
                final_data.append({"ΕΤΟΣ": parts[0], "ΑΠΟ (ΗΜ/ΝΙΑ)": parts[1], "ΕΩΣ (ΗΜ/ΝΙΑ)": parts[2], "ΦΟΡΕΑΣ": parts[3].upper(), "ΕΝΣΗΜΑ (Η.Ε.)": val_ens, "ΑΠΟΔΟΧΕΣ (€)": val_apod})
        df_parsed = pd.DataFrame(final_data)
    except: pass

if not df_parsed.empty:
    st.session_state['df_economic'] = df_parsed

if st.session_state.econ_mode == "⚡ Συγκεντρωτικά":
    tot_years = float(st.session_state.summary_years)
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
    avg_sal = float(st.session_state.summary_avg_salary)

pososto_anapl = float(st.session_state.pososto_anapl_custom) / 100.0
isoδynama_eti = float(st.session_state.isoδynama_eti_tapilt)

# 1. Υπολογισμός Προσαύξησης Κύριας ΤΑΠΙΛΤ βάσει τύπου: Μέσος Μισθός * Ισοδύναμα Έτη * 0.005
prosafxisi_tapilt = avg_sal * isoδynama_eti * 0.005

# Υπολογισμοί Κύριας Σύνταξης
ethniki = calc_ethniki_syntaksi(tot_years, 446.87)
antapodotiki_vassiki = avg_sal * pososto_anapl
kria_mikto = ethniki + antapodotiki_vassiki + prosafxisi_tapilt

eas_main = calc_eas(kria_mikto)
ygeia_main = (kria_mikto - eas_main) * 0.06
taxable_main = max(0.0, kria_mikto - eas_main - ygeia_main)
foros_main = calc_monthly_tax(taxable_main)
krat_main_total = eas_main + ygeia_main + foros_main
katharo_main = max(kria_mikto - krat_main_total, 0.0)

# 2. Υπολογισμοί Επικουρικής ΤΑΠΙΛΤ (350€ αρχικά, 6% κράτηση υγείας -> 329€ καθαρό, και διάρκεια)
tapilt_mikto = float(st.session_state.tapilt_net) # π.χ. 350.00 €
ygeia_tapilt = tapilt_mikto * 0.06
tapilt_katharo = tapilt_mikto - ygeia_tapilt
krat_tapilt_total = ygeia_tapilt
tapilt_duration = f"{int(st.session_state.tapilt_duration_years)} έτη"
tapilt_meta_lixi = float(st.session_state.tapilt_after_expiry) # 100.00 €

# Υπολογισμοί Επικουρικής ΙΚΑ (ΕΦΚΑ)
ika_mikto = 100.58
ygeia_ika = 6.03
krat_ika_total = ygeia_ika
katharo_ika = ika_mikto - krat_ika_total

# Γενικά Σύνολα
geniko_mikto = kria_mikto + tapilt_mikto + ika_mikto
geniko_eas = eas_main
geniko_ygeia = ygeia_main + ygeia_tapilt + ygeia_ika
geniko_foros = foros_main
geniko_krat_total = krat_main_total + krat_tapilt_total + krat_ika_total
geniko_katharo = katharo_main + tapilt_katharo + katharo_ika

if app_section == "👤 Προσωπικά Στοιχεία":
    st.markdown('<div class="panel-card"><div class="panel-header">👤 Προσωπικά Στοιχεία</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.client_data["first_name"] = st.text_input("Όνομα", value=st.session_state.client_data["first_name"])
    with c2: st.session_state.client_data["last_name"] = st.text_input("Επώνυμο", value=st.session_state.client_data["last_name"])
    with c3: st.session_state.client_data["gender"] = st.selectbox("Φύλο", ["Άνδρας", "Γυναίκα"], index=0)
    if st.button("💾 Αποθήκευση", type="primary"): persist_all(); st.success("✅ Αποθηκεύτηκε!")
    st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "💰 Οικονομικά & Ασφαλιστικά Στοιχεία":
    st.markdown('<div class="panel-card"><div class="panel-header">💰 Οικονομικά Στοιχεία & Εισαγωγή Δεδομένων</div>', unsafe_allow_html=True)
    
    modes = ["🔄 Αναλυτικά (Πίνακας Περιόδων)", "⚡ Συγκεντρωτικά"]
    m_idx = modes.index(st.session_state.econ_mode) if st.session_state.econ_mode in modes else 0
    st.session_state.econ_mode = st.radio("Τρόπος καταχώρησης αποδοχών:", modes, index=m_idx, horizontal=True)

    if st.session_state.econ_mode == "🔄 Αναλυτικά (Πίνακας Περιόδων)":
        st.session_state.paste_input = st.text_area("Επικόλληση δεδομένων Excel (ΕΤΟΣ | ΑΠΟ | ΕΩΣ | ΦΟΡΕΑΣ | ΗΜΕΡΕΣ | ΑΠΟΔΟΧΕΣ):", value=st.session_state.paste_input, height=120)
        if 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
            df_edited = st.data_editor(st.session_state['df_economic'], num_rows="dynamic", use_container_width=True, hide_index=True)
            df_edited['ΕΝΣΗΜΑ (Η.Ε.)'] = pd.to_numeric(df_edited['ΕΝΣΗΜΑ (Η.Ε.)'], errors='coerce').fillna(0)
            df_edited['ΑΠΟΔΟΧΕΣ (€)'] = pd.to_numeric(df_edited['ΑΠΟΔΟΧΕΣ (€)'], errors='coerce').fillna(0.0)
            df_edited['ΕΤΟΣ_NUM'] = pd.to_numeric(df_edited['ΕΤΟΣ'], errors='coerce').fillna(0)
            st.session_state['df_economic'] = df_edited
    else:
        col_s1, col_s2 = st.columns(2)
        with col_s1: st.session_state.summary_years = st.number_input("Συνολικά Έτη Ασφάλισης", value=float(st.session_state.summary_years), step=0.01)
        with col_s2: st.session_state.summary_avg_salary = st.number_input("Συντάξιμες Αποδοχές από 2002 (€)", value=float(st.session_state.summary_avg_salary), step=10.0)

    st.markdown("---")
    st.markdown("#### ⚙️ Βασικές Παράμετροι Συνταξιοδότησης")
    col_p1, col_p2 = st.columns(2)
    with col_p1: st.session_state.summary_years = st.number_input("Χρόνια Ασφάλισης (για Κύρια)", value=float(tot_years), step=0.01)
    with col_p2: st.session_state.pososto_anapl_custom = st.number_input("Ποσοστό Αναπλήρωσης (%)", value=float(st.session_state.pososto_anapl_custom), step=0.01)

    st.markdown("---")
    st.markdown("#### 🏦 Υπολογισμός Προσαύξησης Κύριας ΤΑΠΙΛΤ (Μέσος Μισθός × Ισοδύναμα Έτη × 0,005)")
    col_t1, col_t2 = st.columns(2)
    with col_t1: st.session_state.isoδynama_eti_tapilt = st.number_input("Ισοδύναμα Έτη Προσαύξησης", value=float(st.session_state.isoδynama_eti_tapilt), step=0.01)
    st.info(f"💡 Υπολογισμένη Προσαύξηση Κύριας: **{avg_sal:,.2f} €** × **{isoδynama_eti}** × 0,005 = **{prosafxisi_tapilt:,.2f} €**")

    st.markdown("---")
    st.markdown("#### 🏦 Παράμετροι Επικουρικής ΤΑΠΙΛΤ (Αρχικό ποσό, Διάρκεια & Μετά τη λήξη)")
    col_e1, col_e2, col_e3, col_e4 = st.columns(4)
    with col_e1: st.session_state.tapilt_net = st.number_input("Μικτή Επικ. ΤΑΠΙΛΤ (€/μήνα)", value=float(st.session_state.tapilt_net), step=5.0)
    with col_e2: st.session_state.tapilt_duration_years = st.number_input("Διάρκεια (Έτη)", value=float(st.session_state.tapilt_duration_years), step=1.0)
    with col_e3: st.session_state.tapilt_after_expiry = st.number_input("Ποσό μετά τη λήξη (€)", value=float(st.session_state.tapilt_after_expiry), step=5.0)
    with col_e4: st.session_state.merida_amount = st.number_input("Ατομική Μερίδα (€)", value=float(st.session_state.merida_amount), step=100.0)

    if st.button("💾 Αποθήκευση Οικονομικών", type="primary"): persist_all(); st.success("✅ Αποθηκεύτηκαν επιτυχώς!")
    st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "📊 Συγκεντρωτικά Αποτελέσματα & Συντάξεις":
    st.markdown('<div class="panel-card"><div class="panel-header">📊 Πίνακας Εκκαθάρισης Συντάξεων</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th colspan="10">ΥΠΟΛΟΓΙΣΜΟΣ ΣΥΝΤΑΞΗΣ (2026) - ΜΕ ΠΛΗΡΕΙΣ ΚΡΑΤΗΣΕΙΣ (ΕΑΣ, ΥΓΕΙΑ 6%, ΦΟΡΟΣ 2026)</th>
                <th colspan="2" class="kratseis">ΚΡΑΤΗΣΕΙΣ (ΒΑΣΕΙ ΚΛΙΜΑΚΩΝ 2026)</th>
                <th>ΚΑΘΑΡΟ ΠΛΗΡΩΤΕΟ (€)</th>
                <th>ΔΙΑΡΚΕΙΑ ΕΠΙΚΟΥΡΙΚΟΥ</th>
            </tr>
            <tr>
                <th>Είδος Σύνταξης</th>
                <th>Μέσος Μισθός (€)</th>
                <th>Χρόνια Ασφάλισης</th>
                <th>Εθνική Σύνταξη (€)</th>
                <th>Ποσοστό Αναπλ. (%)</th>
                <th>Προσαύξ. ΤΑΠΙΛΤ (€)</th>
                <th>Μικτό Σύνολο (€)</th>
                <th class="kratseis">ΕΑΣ (€)</th>
                <th class="kratseis">Υγεία 6% (€)</th>
                <th class="kratseis">Φόρος Μην. (€)</th>
                <th class="kratseis">Σύνολο Κρατ. (€)</th>
                <th>Καθαρό (€/μήνα)</th>
                <th>Διάρκεια</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="left">ΚΥΡΙΑ ΣΥΝΤΑΞΗ</td>
                <td>{avg_sal:,.2f} €</td>
                <td class="center">{tot_years:.2f}</td>
                <td>{ethniki:,.2f} €</td>
                <td class="center">{pososto_anapl*100:.2f}%</td>
                <td>{prosafxisi_tapilt:,.2f} €</td>
                <td><b>{kria_mikto:,.2f} €</b></td>
                <td>{eas_main:,.2f} €</td>
                <td>{ygeia_main:,.2f} €</td>
                <td>{foros_main:,.2f} €</td>
                <td>{krat_main_total:,.2f} €</td>
                <td><b>{katharo_main:,.2f} €</b></td>
                <td class="center">Ισόβια</td>
            </tr>
            <tr>
                <td class="left">ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ</td>
                <td class="center">-</td>
                <td class="center">32,22</td>
                <td class="center">-</td>
                <td class="center">-</td>
                <td>{tapilt_mikto:,.2f} €</td>
                <td><b>{tapilt_mikto:,.2f} €</b></td>
                <td>0,00 €</td>
                <td>{ygeia_tapilt:,.2f} €</td>
                <td>0,00 €</td>
                <td>{krat_tapilt_total:,.2f} €</td>
                <td><b>{tapilt_katharo:,.2f} €</b></td>
                <td class="center">{tapilt_duration} (μετά {tapilt_meta_lixi}€)</td>
            </tr>
            <tr>
                <td class="left">ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)</td>
                <td>3.247,43 €</td>
                <td class="center">10,35</td>
                <td class="center">-</td>
                <td class="center">-</td>
                <td>100,58 €</td>
                <td><b>100,58 €</b></td>
                <td>0,00 €</td>
                <td>6,03 €</td>
                <td>0,00 €</td>
                <td>6,03 €</td>
                <td><b>{katharo_ika:,.2f} €</b></td>
                <td class="center">Ισόβια</td>
            </tr>
            <tr class="total-row">
                <td class="left">ΓΕΝΙΚΟ ΣΥΝΟΛΟ</td>
                <td class="center">-</td>
                <td class="center">-</td>
                <td class="center">-</td>
                <td class="center">-</td>
                <td class="center">-</td>
                <td><b>{geniko_mikto:,.2f} €</b></td>
                <td><b>{geniko_eas:,.2f} €</b></td>
                <td><b>{geniko_ygeia:,.2f} €</b></td>
                <td><b>{geniko_foros:,.2f} €</b></td>
                <td><b>{geniko_krat_total:,.2f} €</b></td>
                <td><b>{geniko_katharo:,.2f} €</b></td>
                <td class="center">-</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "💼 Υπολογισμός Εφάπαξ":
    st.markdown('<div class="panel-card"><div class="panel-header">💼 Παραμετρικός Υπολογισμός Εφάπαξ (Ν. 4387/2016)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: b_until_2013 = st.number_input("Έτη έως 31/12/2013", value=float(st.session_state.bank_years_until_2013), step=0.1)
    with col2: b_from_2014 = st.number_input("Έτη από 2014 και μετά", value=float(st.session_state.bank_years_from_2014), step=0.1)
    with col3: st.session_state.efap_repl_rate = st.number_input("Συντελεστής Αναπλήρωσης (%)", value=float(60.0), step=1.0)

    col4, col5 = st.columns(2)
    with col4: st.session_state.efap_avg_5y = st.number_input("Μέσος Μην. Μισθός Πενταετίας (€)", value=float(3479.25), step=10.0)
    with col5: st.session_state.efap_tmima_b = st.number_input("Συνολικό Τμήμα Β (€)", value=float(15478.35), step=100.0)

    tmima_a = b_until_2013 * st.session_state.efap_avg_5y * (st.session_state.efap_repl_rate / 100.0)
    total_efapax = tmima_a + st.session_state.efap_tmima_b

    st.markdown(f"""
    <table style="width:100%; border-collapse: collapse; font-size: 14px; border: 1px solid #CBD5E1; margin-top: 15px;">
        <tr class="excel-table-header"><th>ΤΜΗΜΑ ΕΦΑΠΑΞ</th><th>ΠΟΣΟ (€)</th></tr>
        <tr><td>1. Τμήμα Α (Έως 2013)</td><td style="text-align: right;">{tmima_a:,.2f} €</td></tr>
        <tr><td>2. Τμήμα Β (Από 2014)</td><td style="text-align: right;">{st.session_state.efap_tmima_b:,.2f} €</td></tr>
        <tr style="background-color: #E2E8F0; font-weight: bold;"><td>🌟 ΣΥΝΟΛΙΚΟ ΚΑΘΑΡΟ ΕΦΑΠΑΞ</td><td style="text-align: right; color: #1E3A8A;">{total_efapax:,.2f} €</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="panel-card"><div class="panel-header">📋 Τελική Εικόνα & Εκτύπωση</div>', unsafe_allow_html=True)
    monthly_tak_fin = st.session_state.efap_avg_5y
    total_efapax_fin = (st.session_state.bank_years_until_2013 * monthly_tak_fin * (60.0 / 100.0)) + st.session_state.efap_tmima_b
    c_name = f"{st.session_state.client_data['first_name']} {st.session_state.client_data['last_name']}"
    
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; padding: 20px; border-radius: 10px; font-size: 14px;">
        <h3 style="color: #1E3A8A; margin-top: 0;">📄 ΕΠΙΣΗΜΗ ΣΥΝΟΨΗ ΠΕΛΑΤΗ: {c_name}</h3>
        <hr style="margin: 10px 0;">
        <p><b>Συνολικά Έτη Ασφάλισης:</b> {tot_years:.2f} έτη</p>
        <p><b>💶 ΣΥΝΟΛΙΚΗ ΚΑΘΑΡΗ ΜΗΝΙΑΙΑ ΣΥΝΤΑΞΗ:</b> <b>{geniko_katharo:,.2f} € / μήνα</b></p>
        <hr style="margin: 10px 0;">
        <p style="font-size: 16px; color: #16A34A;"><b>💼 ΣΥΝΟΛΙΚΟ ΚΑΘΑΡΟ ΕΦΑΠΑΞ:</b> <b>{total_efapax_fin:,.2f} €</b></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🖨️ Εκτύπωση / Αποθήκευση PDF", type="primary"): st.info("💡 Πατήστε **Ctrl + P**.")
    st.markdown('</div>', unsafe_allow_html=True)
