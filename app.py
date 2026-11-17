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
        "2002\t01/07/2002\t31/07/2002\tΤΡΑΠΕΖΑ\t25\t3304.39"
    )

if 'summary_years' not in st.session_state:
    st.session_state.summary_years = db_data["summary_years"] if db_data else 0.08

if 'summary_avg_salary' not in st.session_state:
    st.session_state.summary_avg_salary = db_data["summary_avg_salary"] if db_data else 3304.39

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
# ΕΠΑΓΓΕΛΜΑΤΙΚΟ MENU & ΕΦΑΡΜΟΓΗ
# ==========================================
st.markdown(f"""
    <div class="main-header">
        <div class="main-title">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 12px; border-radius: 8px;">💼</span> 
            Professional Pension BMS — Χρήστης: <u>{st.session_state.get('current_user', 'Χρήστης')}</u>
        </div>
        <div class="main-subtitle">Επαγγελματικό Σύστημα Υπολογισμού Συντάξεων (Ν. 4387/2016) - Ορθός Τύπος Εφάπαξ</div>
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
    "💼 Υπολογισμός Εφάπαξ",
    "📋 Τελική Εικόνα & Εκτύπωση",
    "⚙️ Ρυθμίσεις Συστήματος"
])

st.sidebar.markdown("---")
st.sidebar.success("🟢 Βάση Δεδομένων Ενεργή")

# Υπολογισμός συνολικών ετών / ενσήμων και μέσου όρου για κοινή χρήση στις καρτέλες
if 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
    df_res = st.session_state['df_economic']
    df_res['ΕΤΟΣ_NUM'] = pd.to_numeric(df_res['ΕΤΟΣ'], errors='coerce').fillna(0)
    tot_ensima = df_res['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
    tot_years = tot_ensima / 300.0 if tot_ensima > 0 else 0.08
    df_post_2002 = df_res[df_res['ΕΤΟΣ_NUM'] >= 2002]
    if not df_post_2002.empty and df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum() > 0:
        avg_sal = (df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'] * df_post_2002['ΑΠΟΔΟΧΕΣ (€)']).sum() / df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
    else:
        avg_sal = 3358.78
else:
    tot_ensima = 25
    tot_years = 0.08
    avg_sal = 3358.78

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
    st.markdown('<div class="panel-desc">Καταχωρήστε τα δεδομένα σας. Ο μέσος όρος αποδοχών υπολογίζεται αυτόματα αυστηρά από 1/1/2002 και μετά.</div>', unsafe_allow_html=True)

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
                        raw_apod = row_vals[5].replace('€', '').strip()
                        if ',' in raw_apod and '.' in raw_apod:
                            if raw_apod.find('.') < raw_apod.find(','):
                                raw_apod = raw_apod.replace('.', '').replace(',', '.')
                            else:
                                raw_apod = raw_apod.replace(',', '')
                        elif ',' in raw_apod:
                            raw_apod = raw_apod.replace(',', '.')
                        
                        try:
                            val_apod = float(raw_apod)
                        except:
                            val_apod = 0.0

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

        if df_parsed.empty and 'df_economic' in st.session_state:
            df_parsed = st.session_state['df_economic']
        elif df_parsed.empty:
            df_parsed = pd.DataFrame([
                {"ΕΤΟΣ": "2002", "ΑΠΟ (ΗΜ/ΝΙΑ)": "01/07/2002", "ΕΩΣ (ΗΜ/ΝΙΑ)": "31/07/2002", "ΦΟΡΕΑΣ": "ΤΡΑΠΕΖΑ", "ΕΝΣΗΜΑ (Η.Ε.)": 25.0, "ΑΠΟΔΟΧΕΣ (€)": 3358.78}
            ])

        if not df_parsed.empty:
            st.markdown("##### ✏️ Έλεγχος & Διόρθωση Δεδομένων:")
            df_edited = st.data_editor(df_parsed, num_rows="dynamic", use_container_width=True, hide_index=True)
            
            df_edited['ΕΝΣΗΜΑ (Η.Ε.)'] = pd.to_numeric(df_edited['ΕΝΣΗΜΑ (Η.Ε.)'], errors='coerce').fillna(0)
            df_edited['ΑΠΟΔΟΧΕΣ (€)'] = pd.to_numeric(df_edited['ΑΠΟΔΟΧΕΣ (€)'], errors='coerce').fillna(0.0)
            df_edited['ΕΤΟΣ_NUM'] = pd.to_numeric(df_edited['ΕΤΟΣ'], errors='coerce').fillna(0)
            df_edited['ΦΟΡΕΑΣ'] = df_edited['ΦΟΡΕΑΣ'].astype(str).str.upper().str.strip()

            st.session_state['df_economic'] = df_edited

            tot_ensima = df_edited['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
            tot_apodoches = df_edited['ΑΠΟΔΟΧΕΣ (€)'].sum()
            
            df_post_2002 = df_edited[df_edited['ΕΤΟΣ_NUM'] >= 2002]
            if not df_post_2002.empty and df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum() > 0:
                overall_avg = (df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'] * df_post_2002['ΑΠΟΔΟΧΕΣ (€)']).sum() / df_post_2002['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
            else:
                overall_avg = 0.00

            st.session_state['total_all_ensima'] = tot_ensima
            st.session_state['summary_years'] = tot_ensima / 300.0
            st.session_state['overall_avg_salary'] = overall_avg

            st.markdown("---")
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Συνολικά Ένσημα", f"{int(tot_ensima):,}")
            sc2.metric("Συνολικό Άθροισμα Αποδοχών", f"{tot_apodoches:,.2f} €")
            sc3.metric("Μ.Ο. Μισθός (από 2002)", f"{overall_avg:,.2f} €")

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

# --- 3. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ ---
elif app_section == "📊 Συγκεντρωτικά Αποτελέσματα":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 1. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΣΤΟΙΧΕΙΑ ΑΣΦΑΛΙΣΗΣ & ΠΑΡΑΜΕΤΡΟΙ (Υπολογισμός από 1/1/2002)</div>', unsafe_allow_html=True)

    if 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
        df_res = st.session_state['df_economic']
        grouped_ensima = df_res.groupby('ΦΟΡΕΑΣ')['ΕΝΣΗΜΑ (Η.Ε.)'].sum().reset_index()
        
        df_post_2002 = df_res[df_res['ΕΤΟΣ_NUM'] >= 2002]
        if not df_post_2002.empty:
            grouped_avg = df_post_2002.groupby('ΦΟΡΕΑΣ').apply(
                lambda x: pd.Series({
                    'AvgSal': (x['ΕΝΣΗΜΑ (Η.Ε.)'] * x['ΑΠΟΔΟΧΕΣ (€)']).sum() / x['ΕΝΣΗΜΑ (Η.Ε.)'].sum() if x['ΕΝΣΗΜΑ (Η.Ε.)'].sum() > 0 else 0.0
                })
            ).reset_index()
            grouped = pd.merge(grouped_ensima, grouped_avg, on='ΦΟΡΕΑΣ', how='left').fillna({'AvgSal': 0.0})
        else:
            grouped = grouped_ensima.copy()
            grouped['AvgSal'] = 0.00
    else:
        grouped = pd.DataFrame([
            {"ΦΟΡΕΑΣ": "ΤΡΑΠΕΖΑ", "ΕΝΣΗΜΑ (Η.Ε.)": 25, "AvgSal": 3358.78}
        ])

    agency_rows_html = ""
    for _, r in grouped.iterrows():
        f_name = r['ΦΟΡΕΑΣ']
        f_ens = int(r['ΕΝΣΗΜΑ (Η.Ε.)'])
        f_yr = f_ens / 300.0
        f_avg = r['AvgSal']
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
            <tr><td><b>Επικ. ΤΑΠΙΛΤ μετά εξάντληση</b></td><td style="text-align: center;">{:.2f} €</td></tr>
            <tr><td><b>Εκτ. Ετήσια Απόδοση (%)</b></td><td style="text-align: center;">0,0%</td></tr>
            <tr><td><b>Καθεστώς Ασφάλισης</b></td><td style="text-align: center;">Παλαιός (<1993)</td></tr>
        </table>
        """.format(st.session_state.tapilt_after_expiry), unsafe_allow_html=True)

    annual_tapilt_total = st.session_state.tapilt_net * 12
    years_to_expiry = (st.session_state.merida_amount / annual_tapilt_total) if annual_tapilt_total > 0 else 0.0

    with top_col3:
        st.markdown(f"""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-table-header">
                <th colspan="2">ΤΑΠΙΛΤΑΤ & ΜΕΡΙΔΑ (ΡΥΘΜΙΣΜΕΝΑ)</th>
            </tr>
            <tr><td><b>ΕΙΣΦΟΡΕΣ ΜΕΡΙΔΑ</b></td><td style="color: blue; text-align: right;"><b>{st.session_state.merida_amount:,.2f} €</b></td></tr>
            <tr><td><b>Αρχικό Καθαρό ΤΑΠΙΛΤ</b></td><td style="color: blue; text-align: right;"><b>{st.session_state.tapilt_net:,.2f} € / μήνα</b></td></tr>
            <tr><td><b>Διάρκεια Αρχικού Ποσού</b></td><td style="text-align: right; color: #1E3A8A; font-weight: bold;"><b>{years_to_expiry:.1f} έτη</b></td></tr>
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
    st.markdown('<div class="panel-header">📊 2. ΥΠΟΛΟΓΙΣΜΟΣ ΣΥΝΤΑΞΗΣ (2026) — ΜΕ ΡΥΘΜΙΣΜΕΝΕΣ ΕΠΙΚΟΥΡΙΚΕΣ</div>', unsafe_allow_html=True)

    ethniki = 446.87
    pososto_anapl = min(0.15 + (tot_years * 0.012), 0.52)
    antapodotiki = avg_sal * pososto_anapl
    kria_mikto = ethniki + antapodotiki + 350.0  
    
    eas_val = 232.73 if kria_mikto > 1400 else 0.00
    ygeia_val = kria_mikto * 0.06
    foros_val = 328.30
    synolo_krat = eas_val + ygeia_val + foros_val
    katharo_main = max(kria_mikto - synolo_krat, 0.0)

    tapilt_katharo = st.session_state.tapilt_net
    tapilt_krat = tapilt_katharo * 0.06 / 0.94
    tapilt_mikto = tapilt_katharo + tapilt_krat
    tapilt_duration_str = f"Πρώτα {years_to_expiry:.1f} έτη (μετά {st.session_state.tapilt_after_expiry:.2f} € ισόβια)"

    ika_ensima = df_res[df_res['ΦΟΡΕΑΣ'].str.contains('ΙΚΑ|ΕΦΚΑ', na=False)]['ΕΝΣΗΜΑ (Η.Ε.)'].sum() if 'df_res' in locals() else 0
    ika_years = ika_ensima / 300.0
    ika_mikto = avg_sal * ika_years * 0.0045 if ika_years > 0 else 0.00
    ika_krat = ika_mikto * 0.06
    ika_katharo = max(ika_mikto - ika_krat, 0.0)

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
            "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ (ΡΥΘΜΙΣΜΕΝΗ)",
            "Μέσος Μισθός (€ απο 2002)": f"{avg_sal:,.2f} €",
            "Χρόνια Ασφάλισης": f"{tot_years:.2f}",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "0,00 €",
            "Μικτό Σύνολο (€)": f"{tapilt_mikto:,.2f} €",
            "ΕΑΣ (€)": "0,00 €",
            "Υγεία 6% (€)": f"{tapilt_krat:,.2f} €",
            "Φόρος Μην. (€)": "0,00 €",
            "Σύνολο Κρατ. (€)": f"{tapilt_krat:,.2f} €",
            "Καθαρό Πληρωτέο (€)": f"{tapilt_katharo:,.2f} €",
            "Διάρκεια Επικουρικού": tapilt_duration_str
        },
        {
            "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)",
            "Μέσος Μισθός (€ απο 2002)": f"{avg_sal:,.2f} €",
            "Χρόνια Ασφάλισης": f"{ika_years:.2f}",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "0,00 €",
            "Μικτό Σύνολο (€)": f"{ika_mikto:,.2f} €",
            "ΕΑΣ (€)": "0,00 €",
            "Υγεία 6% (€)": f"{ika_krat:,.2f} €",
            "Φόρος Μην. (€)": "0,00 €",
            "Σύνολο Κρατ. (€)": f"{ika_krat:,.2f} €",
            "Καθαρό Πληρωτέο (€)": f"{ika_katharo:,.2f} €",
            "Διάρκεια Επικουρικού": "Ισόβια"
        },
        {
            "Είδος Σύνταξης": "🌟 ΓΕΝΙΚΟ ΣΥΝΟΛΟ",
            "Μέσος Μισθός (€ απο 2002)": "-",
            "Χρόνια Ασφάλισης": "-",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "-",
            "Μικτό Σύνολο (€)": f"{kria_mikto + tapilt_mikto + ika_mikto:,.2f} €",
            "ΕΑΣ (€)": f"{eas_val:,.2f} €",
            "Υγεία 6% (€)": f"{ygeia_val + tapilt_krat + ika_krat:,.2f} €",
            "Φόρος Μην. (€)": f"{foros_val:,.2f} €",
            "Σύνολο Κρατ. (€)": f"{synolo_krat + tapilt_krat + ika_krat:,.2f} €",
            "Καθαρό Πληρωτέο (€)": f"{katharo_main + tapilt_katharo + ika_katharo:,.2f} €",
            "Διάρκεια Επικουρικού": "-"
        }
    ])

    st.dataframe(calc_table, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ (ΟΡΘΟΣ Ν. 4387/2016) ---
elif app_section == "💼 Υπολογισμός Εφάπαξ":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ ΠΑΡΟΧΗΣ (πρ. ΤΑΠΙΛΤ-ΑΤ / e-ΕΦΚΑ - Ν. 4387/2016) - ΑΦΟΡΟΛΟΓΗΤΟ</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Ακριβής υπολογισμός βάσει του Ν. 4387/2016 (60% επί του μηνιαίου τακτικού μισθού για το Τμήμα Α).</div>', unsafe_allow_html=True)

    b_until_2013 = st.session_state.bank_years_until_2013
    b_from_2014 = st.session_state.bank_years_from_2014
    
    monthly_taktiko = avg_sal * (12.0 / 14.0) # Αναγωγή σε 12μηνο τακτικό

    # ΟΡΘΟΣ ΤΥΠΟΣ Ν. 4387/2016
    tmima_a = b_until_2013 * monthly_taktiko * 0.60
    tmima_b = b_from_2014 * avg_sal * 12 * 0.04 * 1.015
    total_efapax_correct = tmima_a + tmima_b

    efap_col1, efap_col2 = st.columns(2)
    with efap_col1:
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-gold-header"><th colspan="2">ΠΑΡΑΜΕΤΡΟΙ ΕΦΑΠΑΞ (Ν. 4387/2016)</th></tr>
            <tr><td>Έτη Τράπεζας έως 31/12/2013</td><td style="text-align: center; color: blue; font-weight: bold;">{:.2f}</td></tr>
            <tr><td>Μέσος Μισθός (12μηνο)</td><td style="text-align: center;">{:,.2f} €</td></tr>
            <tr><td>Αναγωγή σε Μηνιαίο Τακτικό</td><td style="text-align: center;">{:,.2f} €</td></tr>
            <tr><td>Συντελεστής Αναπλήρωσης (έως 2013)</td><td style="text-align: center;">60,00%</td></tr>
            <tr><td>Ποσοστό Εισφοράς Πρόνοιας (από 2014)</td><td style="text-align: center;">4,00%</td></tr>
            <tr><td>Συντελεστής Αποτίμησης (2014–2022)</td><td style="text-align: center;">1,015</td></tr>
        </table>
        """.format(b_until_2013, avg_sal, monthly_taktiko), unsafe_allow_html=True)

    with efap_col2:
        st.markdown("""
        <table style="width:100%; border-collapse: collapse; font-size: 13px; border: 1px solid #CBD5E1;">
            <tr class="excel-table-header"><th colspan="2">ΤΜΗΜΑ ΕΦΑΠΑΞ (Ν. 4387/2016)</th><th>ΠΟΣΟ (€)</th></tr>
            <tr><td colspan="2">1. Τμήμα Α (Έτη έως 31/12/2013)</td><td style="text-align: right;">{:,.2f} €</td></tr>
            <tr><td colspan="2">2. Τμήμα Β (Εισφορές 2014–2022)</td><td style="text-align: right;">{:,.2f} €</td></tr>
            <tr style="background-color: #E2E8F0; font-weight: bold;"><td colspan="2">ΚΑΘΑΡΟ ΣΥΝΟΛΟ ΕΦΑΠΑΞ e-ΕΦΚΑ (ΑΦΟΡΟΛΟΓΗΤΟ)</td><td style="text-align: right; color: #1E3A8A;">{:,.2f} €</td></tr>
            <tr><td colspan="2">Φόρος Εισοδήματος</td><td style="text-align: right;">0,00 € (Πλήρως Αφορολόγητο)</td></tr>
        </table>
        """.format(tmima_a, tmima_b, total_efapax_correct), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. ΤΕΛΙΚΗ ΕΙΚΟΝΑ & ΕΚΤΥΠΩΣΗ ---
else:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📋 ΣΥΝΟΨΗ & ΤΕΛΙΚΗ ΕΙΚΟΝΑ ΣΥΝΤΑΞΙΟΔΟΤΙΚΟΥ ΠΡΟΦΙΛ</div>', unsafe_allow_html=True)
    
    ethniki = 446.87
    pososto_anapl = min(0.15 + (tot_years * 0.012), 0.52)
    antapodotiki = avg_sal * pososto_anapl
    kria_mikto = ethniki + antapodotiki + 350.0  
    eas_val = 232.73 if kria_mikto > 1400 else 0.00
    ygeia_val = kria_mikto * 0.06
    foros_val = 328.30
    synolo_krat = eas_val + ygeia_val + foros_val
    katharo_main = max(kria_mikto - synolo_krat, 0.0)

    annual_tapilt_total = st.session_state.tapilt_net * 12
    years_to_expiry = (st.session_state.merida_amount / annual_tapilt_total) if annual_tapilt_total > 0 else 0.0
    tapilt_katharo = st.session_state.tapilt_net

    ika_ensima = df_res[df_res['ΦΟΡΕΑΣ'].str.contains('ΙΚΑ|ΕΦΚΑ', na=False)]['ΕΝΣΗΜΑ (Η.Ε.)'].sum() if 'df_res' in locals() else 0
    ika_years = ika_ensima / 300.0
    ika_mikto = avg_sal * ika_years * 0.0045 if ika_years > 0 else 0.00
    ika_krat = ika_mikto * 0.06
    ika_katharo = max(ika_mikto - ika_krat, 0.0)

    total_net_monthly = katharo_main + tapilt_katharo + ika_katharo
    monthly_taktiko_fin = avg_sal * (12.0 / 14.0)
    total_efapax = (st.session_state.bank_years_until_2013 * monthly_taktiko_fin * 0.60) + (st.session_state.bank_years_from_2014 * avg_sal * 12 * 0.04 * 1.015)

    c_name = f"{st.session_state.client_data['first_name']} {st.session_state.client_data['last_name']}"
    c_birth = st.session_state.client_data['birth_date']
    c_work = st.session_state.client_data['first_work_date']

    st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; padding: 20px; border-radius: 10px; font-size: 14px;">
        <h3 style="color: #1E3A8A; margin-top: 0;">📄 ΕΠΙΣΗΜΗ ΣΥΝΟΨΗ ΠΕΛΑΤΗ</h3>
        <hr style="margin: 10px 0;">
        <p><b>Ονοματεπώνυμο Πελάτη:</b> <span style="color: #2563EB;">{c_name}</span></p>
        <p><b>Ημερομηνία Γέννησης:</b> {c_birth}</p>
        <p><b>Ημερομηνία Έναρξης Εργασίας:</b> <span style="color: #16A34A; font-weight: bold;">{c_work}</span></p>
        <p><b>Συνολικά Έτη Ασφάλισης:</b> {tot_years:.2f} έτη ({int(tot_ensima):,} ένσημα)</p>
        <p><b>Προβλεπόμενη Ημερομηνία / Όριο Συνταξιοδότησης:</b> <span style="color: #D97706; font-weight: bold;">16/09/2031 (Στα 62 έτη με 40ετία)</span></p>
        <br>
        <h4 style="color: #1E3A8A;">💰 ΤΕΛΙΚΑ ΟΙΚΟΝΟΜΙΚΑ ΠΟΣΑ</h4>
        <ul>
            <li><b>Καθαρή Κύρια Σύνταξη:</b> {katharo_main:,.2f} € / μήνα</li>
            <li><b>Καθαρή Επικουρική ΤΑΠΙΛΤ:</b> {tapilt_katharo:,.2f} € / μήνα</li>
            <li><b>Καθαρή Επικουρική ΙΚΑ:</b> {ika_katharo:,.2f} € / μήνα</li>
            <li style="font-size: 16px; color: #1E3A8A; margin-top: 5px;"><b>🌟 ΣΥΝΟΛΙΚΟ ΜΗΝΙΑΙΟ ΚΑΘΑΡΟ ΠΛΗΡΩΤΕΟ:</b> <b>{total_net_monthly:,.2f} € / μήνα</b></li>
        </ul>
        <hr style="margin: 10px 0;">
        <p style="font-size: 16px; color: #16A34A;"><b>💼 ΣΥΝΟΛΙΚΟ ΚΑΘΑΡΟ ΕΦΑΠΑΞ (Αφορολόγητο - Ορθός Τύπος Ν. 4387/2016):</b> <b>{total_efapax:,.2f} €</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🖨️ Εκτύπωση / Αποθήκευση Αναφοράς", type="primary"):
        st.info("💡 Πατήστε **Ctrl + P** στον περιηγητή σας για εκτύπωση ή αποθήκευση ως PDF.")

    st.markdown('</div>', unsafe_allow_html=True)
