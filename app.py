import streamlit as st
import pandas as pd
import io
import sqlite3

# Rythmisi selidas
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# ==========================================
# SYNDESI & VASI DEDOMENON (SQLITE)
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
            has_tapilt INTEGER,
            tapilt_net REAL,
            tapilt_after_expiry REAL,
            bank_years_until_2013 REAL,
            bank_years_from_2014 REAL,
            pososto_anapl_custom REAL,
            tapilt_sum_ginomeno REAL,
            tapilt_syntaximos_misthos REAL,
            tapilt_duration_years REAL,
            efap_repl_rate REAL,
            efap_avg_5y REAL,
            efap_tmima_b REAL
        )
    ''')
    cursor.execute("PRAGMA table_info(client_profile)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'merida_amount' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN merida_amount REAL")
    if 'has_tapilt' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN has_tapilt INTEGER DEFAULT 0")
    if 'tapilt_net' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_net REAL")
    if 'tapilt_after_expiry' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_after_expiry REAL")
    if 'bank_years_until_2013' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN bank_years_until_2013 REAL")
    if 'bank_years_from_2014' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN bank_years_from_2014 REAL")
    if 'pososto_anapl_custom' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN pososto_anapl_custom REAL")
    if 'tapilt_sum_ginomeno' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_sum_ginomeno REAL")
    if 'tapilt_syntaximos_misthos' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_syntaximos_misthos REAL")
    if 'tapilt_duration_years' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN tapilt_duration_years REAL")
    if 'efap_repl_rate' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN efap_repl_rate REAL")
    if 'efap_avg_5y' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN efap_avg_5y REAL")
    if 'efap_tmima_b' not in columns: cursor.execute("ALTER TABLE client_profile ADD COLUMN efap_tmima_b REAL")
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
            econ_mode, paste_input, summary_years, summary_avg_salary, merida_amount, has_tapilt, tapilt_net, tapilt_after_expiry,
            bank_years_until_2013, bank_years_from_2014, pososto_anapl_custom, 
            tapilt_sum_ginomeno, tapilt_syntaximos_misthos, tapilt_duration_years,
            efap_repl_rate, efap_avg_5y, efap_tmima_b
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["first_name"], data["last_name"], data["gender"], data["birth_date"],
        data["insurance_cat"], data["first_work_date"], data["econ_mode"],
        data["paste_input"], data["summary_years"], data["summary_avg_salary"],
        data["merida_amount"], data["has_tapilt"], data["tapilt_net"], data["tapilt_after_expiry"],
        data["bank_years_until_2013"], data["bank_years_from_2014"], data["pososto_anapl_custom"],
        data["tapilt_sum_ginomeno"], data["tapilt_syntaximos_misthos"], data["tapilt_duration_years"],
        data["efap_repl_rate"], data["efap_avg_5y"], data["efap_tmima_b"]
    ))
    conn.commit()
    conn.close()

def load_from_db():
    conn = sqlite3.connect('pension_bms.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT first_name, last_name, gender, birth_date, insurance_cat, first_work_date, 
               econ_mode, paste_input, summary_years, summary_avg_salary, merida_amount, has_tapilt, tapilt_net, tapilt_after_expiry,
               bank_years_until_2013, bank_years_from_2014, pososto_anapl_custom, 
               tapilt_sum_ginomeno, tapilt_syntaximos_misthos, tapilt_duration_years,
               efap_repl_rate, efap_avg_5y, efap_tmima_b
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
            "merida_amount": row[10] if row[10] is not None else 0.0,
            "has_tapilt": int(row[11]) if row[11] is not None else 0,
            "tapilt_net": row[12] if row[12] is not None else 0.0,
            "tapilt_after_expiry": row[13] if row[13] is not None else 0.0,
            "bank_years_until_2013": row[14] if row[14] is not None else 0.0,
            "bank_years_from_2014": row[15] if row[15] is not None else 0.0,
            "pososto_anapl_custom": row[16] if row[16] is not None else 0.0,
            "tapilt_sum_ginomeno": row[17] if row[17] is not None else 0.0,
            "tapilt_syntaximos_misthos": row[18] if row[18] is not None else 0.0,
            "tapilt_duration_years": row[19] if row[19] is not None else 0.0,
            "efap_repl_rate": row[20] if row[20] is not None else 60.0,
            "efap_avg_5y": row[21] if row[21] is not None else 0.0,
            "efap_tmima_b": row[22] if row[22] is not None else 0.0
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

def calc_annual_tax_total(annual_income: float) -> float:
    if annual_income <= 0: return 0.0
    if annual_income <= 10000: gross_tax = annual_income * 0.09
    elif annual_income <= 20000: gross_tax = 900.0 + (annual_income - 10000.0) * 0.20
    elif annual_income <= 30000: gross_tax = 2900.0 + (annual_income - 20000.0) * 0.26
    elif annual_income <= 40000: gross_tax = 5500.0 + (annual_income - 30000.0) * 0.36
    else: gross_tax = 9100.0 + (annual_income - 40000.0) * 0.44
    discount = max(0.0, 777.0 - ((annual_income - 12000.0) / 1000.0) * 20.0) if annual_income > 12000.0 else 777.0
    return max(0.0, gross_tax - discount)

# Epaggelmatiko CSS Styling
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: white; padding: 22px 28px; border-radius: 12px; margin-bottom: 22px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
    }
    .main-title { font-size: 24px; font-weight: 700; margin: 0; display: flex; align-items: center; gap: 10px; letter-spacing: -0.5px; }
    .main-subtitle { font-size: 12.5px; color: #94A3B8; margin-top: 5px; font-weight: 400; }
    .panel-card {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 22px; margin-bottom: 18px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    .panel-header { font-size: 16px; font-weight: 700; color: #1E293B; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #E2E8F0 !important;
        font-weight: 500;
        font-size: 13.5px;
        padding: 8px 12px;
        border-radius: 6px;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: #1E3A8A;
        color: #FFFFFF !important;
    }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 11.5px; font-family: sans-serif; margin-bottom: 20px; }
    .custom-table th { background-color: #1E3A8A; color: white; text-align: center; vertical-align: middle; padding: 8px 10px; border: 1px solid #CBD5E1; white-space: nowrap; font-weight: 600; }
    .custom-table th.kratseis { background-color: #856404; }
    .custom-table th.katharo-header { background-color: #1E3A8A; }
    .custom-table td { padding: 7px 10px; border: 1px solid #CBD5E1; text-align: right; vertical-align: middle; white-space: nowrap; color: #334155; }
    .custom-table td.left { text-align: left; font-weight: 600; color: #0F172A; }
    .custom-table td.center { text-align: center; }
    .custom-table tr:hover { background-color: #F8FAFC; }
    .custom-table tr.total-row { background-color: #F1F5F9; font-weight: bold; color: #0F172A; }
    </style>
""", unsafe_allow_html=True)

# LOGIN
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔒 Asfalis Eisodos BMS</h2>", unsafe_allow_html=True)
    username = st.text_input("Onoma Hristi")
    password = st.text_input("Kodikos (Password)", type="password")
    if st.button("🔑 EISODOS", use_container_width=True, type="primary"):
        if username.strip() and password.strip() == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else: st.error("❌ Lanthasmenos kodikos! (Dokimaste: 1234)")
    st.stop()

db_data = load_from_db()

if 'client_data' not in st.session_state:
    st.session_state.client_data = {
        "first_name": db_data["first_name"] if db_data else "", 
        "last_name": db_data["last_name"] if db_data else "", 
        "gender": db_data["gender"] if db_data else "Andras",
        "birth_date": db_data["birth_date"] if db_data else "", 
        "insurance_cat": db_data["insurance_cat"] if db_data else "Misthotos — Idiotikos tomeas (proin IKA-ETAM)", 
        "first_work_date": db_data["first_work_date"] if db_data else ""
    }

if 'econ_mode' not in st.session_state: st.session_state.econ_mode = db_data["econ_mode"] if db_data else "🔄 Analytika (Pinakas Periodon)"
if 'paste_input' not in st.session_state: st.session_state.paste_input = db_data["paste_input"] if db_data else ""
if 'summary_years' not in st.session_state: st.session_state.summary_years = db_data["summary_years"] if db_data else 0.0
if 'summary_avg_salary' not in st.session_state: st.session_state.summary_avg_salary = db_data["summary_avg_salary"] if db_data else 0.0

if 'has_tapilt' not in st.session_state: 
    st.session_state.has_tapilt = bool(db_data["has_tapilt"] if db_data else any(kw in st.session_state.client_data["insurance_cat"].upper() for kw in ["TRAΠEZA", "ΤΑΠΙΛΤ", "IONIKH"]))

if 'merida_amount' not in st.session_state: st.session_state.merida_amount = db_data["merida_amount"] if db_data else 0.0
if 'tapilt_net' not in st.session_state: st.session_state.tapilt_net = db_data["tapilt_net"] if db_data else 0.0
if 'tapilt_after_expiry' not in st.session_state: st.session_state.tapilt_after_expiry = db_data["tapilt_after_expiry"] if db_data else 0.0
if 'bank_years_until_2013' not in st.session_state: st.session_state.bank_years_until_2013 = db_data["bank_years_until_2013"] if db_data else 0.0
if 'bank_years_from_2014' not in st.session_state: st.session_state.bank_years_from_2014 = db_data["bank_years_from_2014"] if db_data else 0.0
if 'pososto_anapl_custom' not in st.session_state: st.session_state.pososto_anapl_custom = db_data["pososto_anapl_custom"] if db_data else (51.29 if st.session_state.has_tapilt else 0.0)
if 'tapilt_sum_ginomeno' not in st.session_state: st.session_state.tapilt_sum_ginomeno = db_data["tapilt_sum_ginomeno"] if db_data else 0.0
if 'tapilt_syntaximos_misthos' not in st.session_state: st.session_state.tapilt_syntaximos_misthos = db_data["tapilt_syntaximos_misthos"] if db_data else 0.0
if 'tapilt_duration_years' not in st.session_state: st.session_state.tapilt_duration_years = db_data["tapilt_duration_years"] if db_data else 0.0
if 'efap_repl_rate' not in st.session_state: st.session_state.efap_repl_rate = db_data["efap_repl_rate"] if db_data else 60.0
if 'efap_avg_5y' not in st.session_state: st.session_state.efap_avg_5y = db_data["efap_avg_5y"] if db_data else 0.0
if 'efap_tmima_b' not in st.session_state: st.session_state.efap_tmima_b = db_data["efap_tmima_b"] if db_data else 0.0

def persist_all():
    save_to_db({
        "first_name": st.session_state.client_data["first_name"], "last_name": st.session_state.client_data["last_name"],
        "gender": st.session_state.client_data["gender"], "birth_date": st.session_state.client_data["birth_date"],
        "insurance_cat": st.session_state.client_data["insurance_cat"], "first_work_date": st.session_state.client_data["first_work_date"],
        "econ_mode": st.session_state.econ_mode, "paste_input": st.session_state.paste_input,
        "summary_years": float(st.session_state.summary_years), "summary_avg_salary": float(st.session_state.summary_avg_salary),
        "merida_amount": float(st.session_state.merida_amount), "has_tapilt": int(st.session_state.has_tapilt),
        "tapilt_net": float(st.session_state.tapilt_net), "tapilt_after_expiry": float(st.session_state.tapilt_after_expiry),
        "bank_years_until_2013": float(st.session_state.bank_years_until_2013),
        "bank_years_from_2014": float(st.session_state.bank_years_from_2014), 
        "pososto_anapl_custom": float(st.session_state.pososto_anapl_custom),
        "tapilt_sum_ginomeno": float(st.session_state.tapilt_sum_ginomeno),
        "tapilt_syntaximos_misthos": float(st.session_state.tapilt_syntaximos_misthos),
        "tapilt_duration_years": float(st.session_state.tapilt_duration_years),
        "efap_repl_rate": float(st.session_state.efap_repl_rate),
        "efap_avg_5y": float(st.session_state.efap_avg_5y),
        "efap_tmima_b": float(st.session_state.efap_tmima_b)
    })

st.markdown(f"""
    <div class="main-header">
        <div class="main-title"><span>💼</span> Professional Pension BMS</div>
        <div class="main-subtitle">Systima Diacheirisis Syntaxeon & Efapax (N. 4387/2016 & N. 4670/2020)</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='color: #94A3B8; font-size: 11.5px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;'>🗂️ Ploigisi Systimatos</h3>", unsafe_allow_html=True)
app_section = st.sidebar.radio("Epilogi:", [
    "👤 Prosopika & Asfalistika Stoicheia", 
    "💰 Oikonomiko Istoriko & Apodoches", 
    "⚙️ Rythmiseis & Eidika Tameia (TAPILT)", 
    "📊 Syngentrotika Apotelesmata & Syntaxeis", 
    "💼 Ypologismos Efapax", 
    "📋 Teliki Eikona"
], label_visibility="collapsed")

st.sidebar.markdown("---")
if st.sidebar.button("🧹 Pliris Katharismos Stoicheion Pelati", use_container_width=True):
    st.session_state.client_data = {"first_name": "", "last_name": "", "gender": "Andras", "birth_date": "", "insurance_cat": "Misthotos — Idiotikos tomeas (proin IKA-ETAM)", "first_work_date": ""}
    st.session_state.paste_input = ""
    st.session_state.summary_years = 0.0
    st.session_state.summary_avg_salary = 0.0
    st.session_state.has_tapilt = False
    st.session_state.merida_amount = 0.0
    st.session_state.tapilt_net = 0.0
    st.session_state.tapilt_after_expiry = 0.0
    st.session_state.bank_years_until_2013 = 0.0
    st.session_state.bank_years_from_2014 = 0.0
    st.session_state.tapilt_sum_ginomeno = 0.0
    st.session_state.tapilt_syntaximos_misthos = 0.0
    st.session_state.tapilt_duration_years = 0.0
    st.session_state.efap_repl_rate = 60.0
    st.session_state.efap_avg_5y = 0.0
    st.session_state.efap_tmima_b = 0.0
    
    st.session_state['df_economic'] = pd.DataFrame(columns=["ETOS", "APO (HM/NIA)", "EΩS (HM/NIA)", "FOREAS", "ENSIMA (H.E.)", "APODOCHES (€)"])
    persist_all()
    st.success("✅ Ola ta stoicheia tou pelati katharistikan pliros!")
    st.rerun()

df_parsed = pd.DataFrame()
if st.session_state.econ_mode == "🔄 Analytika (Pinakas Periodon)" and st.session_state.paste_input.strip():
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
                final_data.append({"ETOS": parts[0], "APO (HM/NIA)": parts[1], "EΩS (HM/NIA)": parts[2], "FOREAS": parts[3].upper(), "ENSIMA (H.E.)": val_ens, "APODOCHES (€)": val_apod})
        df_parsed = pd.DataFrame(final_data)
    except: pass

if not df_parsed.empty:
    st.session_state['df_economic'] = df_parsed
elif 'df_economic' not in st.session_state:
    st.session_state['df_economic'] = pd.DataFrame(columns=["ETOS", "APO (HM/NIA)", "EΩS (HM/NIA)", "FOREAS", "ENSIMA (H.E.)", "APODOCHES (€)"])

bank_ens, bank_avg, bank_y = 0.0, 0.0, 0.0
ika_ens, ika_avg, ika_y = 0.0, 0.0, 0.0
calc_tot_ensima = 0.0
avg_sal = float(st.session_state.summary_avg_salary)

if 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
    df_res = st.session_state['df_economic']
    df_res['ETOS_NUM'] = pd.to_numeric(df_res['ETOS'], errors='coerce').fillna(0)
    
    calc_tot_ensima = df_res['ENSIMA (H.E.)'].sum()
    
    df_bank = df_res[df_res['FOREAS'].str.contains('ΤΡΑΠΕΖΑ|ΙΟΝΙΚΗ', case=False, na=False)]
    if not df_bank.empty and df_bank['ENSIMA (H.E.)'].sum() > 0:
        bank_ens = df_bank['ENSIMA (H.E.)'].sum()
        bank_y = bank_ens / 300.0
        df_bank_post02 = df_bank[df_bank['ETOS_NUM'] >= 2002]
        if not df_bank_post02.empty and df_bank_post02['ENSIMA (H.E.)'].sum() > 0:
            bank_avg = (df_bank_post02['ENSIMA (H.E.)'] * df_bank_post02['APODOCHES (€)']).sum() / df_bank_post02['ENSIMA (H.E.)'].sum()

    df_ika = df_res[df_res['FOREAS'].str.contains('ΙΚΑ', case=False, na=False)]
    if not df_ika.empty and df_ika['ENSIMA (H.E.)'].sum() > 0:
        ika_ens = df_ika['ENSIMA (H.E.)'].sum()
        ika_y = ika_ens / 300.0
        df_ika_post02 = df_ika[df_ika['ETOS_NUM'] >= 2002]
        if not df_ika_post02.empty and df_ika_post02['ENSIMA (H.E.)'].sum() > 0:
            ika_avg = (df_ika_post02['ENSIMA (H.E.)'] * df_ika_post02['APODOCHES (€)']).sum() / df_ika_post02['ENSIMA (H.E.)'].sum()

    df_post_2002 = df_res[df_res['ETOS_NUM'] >= 2002]
    if not df_post_2002.empty and df_post_2002['ENSIMA (H.E.)'].sum() > 0:
        avg_sal = (df_post_2002['ENSIMA (H.E.)'] * df_post_2002['APODOCHES (€)']).sum() / df_post_2002['ENSIMA (H.E.)'].sum()

tot_years = calc_tot_ensima / 300.0 if calc_tot_ensima > 0 else float(st.session_state.summary_years)

if st.session_state.has_tapilt:
    st.session_state.tapilt_duration_years = round(tot_years, 2)

if st.session_state.pososto_anapl_custom == 0.0 and tot_years > 0:
    st.session_state.pososto_anapl_custom = 51.29 if st.session_state.has_tapilt else 50.15

pososto_anapl = float(st.session_state.pososto_anapl_custom) / 100.0

sum_ginomeno = float(st.session_state.tapilt_sum_ginomeno)
t_synt_misthos = float(st.session_state.tapilt_syntaximos_misthos)
prosafxisi_tapilt = (sum_ginomeno * 0.00075 * t_synt_misthos) if (st.session_state.has_tapilt and tot_years > 0) else 0.0

tapilt_meta_lixi = float(st.session_state.tapilt_after_expiry)

ethniki = calc_ethniki_syntaksi(tot_years, 446.87) if tot_years > 0 else 0.0
antapodotiki_vassiki = (avg_sal * pososto_anapl) if tot_years > 0 else 0.0
kria_mikto = (ethniki + antapodotiki_vassiki + prosafxisi_tapilt) if tot_years > 0 else 0.0

eas_main = calc_eas(kria_mikto) if tot_years > 0 else 0.0
ygeia_main = ((kria_mikto - eas_main) * 0.06) if tot_years > 0 else 0.0

tapilt_mikto = float(st.session_state.tapilt_net) if (st.session_state.has_tapilt and tot_years > 0) else 0.0
ygeia_tapilt = (tapilt_mikto * 0.06) if (st.session_state.has_tapilt and tot_years > 0) else 0.0

ika_mikto = (100.58 if (not st.session_state.has_tapilt and tot_years > 0) else 0.0)
ygeia_ika = (ika_mikto * 0.06) if ika_mikto > 0 else 0.0

taxable_main_annual = (kria_mikto - eas_main - ygeia_main) * 12.0
taxable_tapilt_annual = (tapilt_mikto - ygeia_tapilt) * 12.0 if st.session_state.has_tapilt else 0.0
taxable_ika_annual = (ika_mikto - ygeia_ika) * 12.0 if (not st.session_state.has_tapilt and ika_mikto > 0) else 0.0
taxable_total_annual = taxable_main_annual + taxable_tapilt_annual + taxable_ika_annual

total_annual_tax = calc_annual_tax_total(taxable_total_annual) if taxable_total_annual > 0 else 0.0
total_monthly_tax = total_annual_tax / 12.0

if taxable_total_annual > 0:
    foros_main = total_monthly_tax * (taxable_main_annual / taxable_total_annual)
    foros_tapilt = total_monthly_tax * (taxable_tapilt_annual / taxable_total_annual) if st.session_state.has_tapilt else 0.0
    foros_ika = total_monthly_tax * (taxable_ika_annual / taxable_total_annual) if (not st.session_state.has_tapilt and ika_mikto > 0) else 0.0
else:
    foros_main = 0.0
    foros_tapilt = 0.0
    foros_ika = 0.0

foros_main = round(foros_main, 2)
foros_tapilt = round(foros_tapilt, 2) if st.session_state.has_tapilt else 0.0
foros_ika = round(foros_ika, 2) if not st.session_state.has_tapilt else 0.0
geniko_foros = round(total_monthly_tax, 2)

krat_main_total = eas_main + ygeia_main + foros_main
katharo_main = max(kria_mikto - krat_main_total, 0.0) if tot_years > 0 else 0.0

krat_tapilt_total = (ygeia_tapilt + foros_tapilt) if st.session_state.has_tapilt else 0.0
tapilt_katharo = max(tapilt_mikto - krat_tapilt_total, 0.0) if st.session_state.has_tapilt else 0.0

krat_ika_total = (ygeia_ika + foros_ika) if (not st.session_state.has_tapilt and ika_mikto > 0) else 0.0
katharo_ika = max(ika_mikto - krat_ika_total, 0.0) if (not st.session_state.has_tapilt and ika_mikto > 0) else 0.0

geniko_mikto = kria_mikto + (tapilt_mikto if st.session_state.has_tapilt else 0.0) + (ika_mikto if not st.session_state.has_tapilt else 0.0)
geniko_eas = eas_main
geniko_ygeia = ygeia_main + (ygeia_tapilt if st.session_state.has_tapilt else 0.0) + (ygeia_ika if not st.session_state.has_tapilt else 0.0)
geniko_krat_total = krat_main_total + (krat_tapilt_total if st.session_state.has_tapilt else 0.0) + (krat_ika_total if not st.session_state.has_tapilt else 0.0)
geniko_katharo = katharo_main + (tapilt_katharo if st.session_state.has_tapilt else 0.0) + (katharo_ika if not st.session_state.has_tapilt else 0.0)

if app_section == "👤 Prosopika & Asfalistika Stoicheia":
    st.markdown('<div class="panel-card"><div class="panel-header">👤 Prosopika & Asfalistika Stoicheia</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.client_data["first_name"] = st.text_input("Onoma", value=st.session_state.client_data["first_name"])
    with c2: st.session_state.client_data["last_name"] = st.text_input("Eponymo", value=st.session_state.client_data["last_name"])
    with c3: st.session_state.client_data["gender"] = st.selectbox("Fylo", ["Andras", "Gynaika"], index=0 if st.session_state.client_data["gender"]=="Andras" else 1)

    c4, c5 = st.columns(2)
    with c4: st.session_state.client_data["birth_date"] = st.text_input("Imerominia Gennisis", value=st.session_state.client_data["birth_date"])
    with c5: st.session_state.client_data["first_work_date"] = st.text_input("Proti Imera Asfalisis", value=st.session_state.client_data["first_work_date"])

    cat_options = [
        "Misthotos — Trapeza / Ioniki (proin TAPILT)", 
        "Misthotos — Trapeza (Alli)", 
        "Misthotos — Idiotikos tomeas (proin IKA-ETAM)", 
        "Dimosios tomeas", 
        "Eleftheros epangelmatias (proin OAEE)"
    ]
    current_cat = st.session_state.client_data["insurance_cat"]
    cat_idx = cat_options.index(current_cat) if current_cat in cat_options else 0
    
    selected_cat = st.selectbox("Asfalistiki Katigoria / Foreas", cat_options, index=cat_idx)
    st.session_state.client_data["insurance_cat"] = selected_cat

    if any(kw in selected_cat.upper() for kw in ["TRAΠEZA", "ΤΑΠΙΛΤ", "IONIKH"]):
        st.session_state.has_tapilt = True
        st.session_state.pososto_anapl_custom = 51.29
        st.warning("⚠️ **Epilexate Trapeza/Ioniki (TAPILT).** To eidiko tameio energopoiithike aytomata. Parakalo metaveite stin enotita **«⚙️ Rythmiseis & Eidika Tameia (TAPILT)»** gia na katahorisete tin Atomiki Merida kai to Poso.")
    else:
        st.session_state.has_tapilt = False
        st.session_state.pososto_anapl_custom = 50.15

    if st.button("💾 Apothikeysi Prosopikon", type="primary"): 
        persist_all()
        st.success("✅ Ta prosopika stoicheia apothikeytikan!")
    st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "💰 Oikonomiko Istoriko & Apodoches":
    st.markdown('<div class="panel-card"><div class="panel-header">💰 Oikonomika Stoicheia & Asfalistiko Istoriko</div>', unsafe_allow_html=True)
    
    modes = ["🔄 Analytika (Pinakas Periodon)", "⚡ Syngentrotika"]
    m_idx = modes.index(st.session_state.econ_mode) if st.session_state.econ_mode in modes else 0
    st.session_state.econ_mode = st.radio("Tropos katahorisis apodochon:", modes, index=m_idx, horizontal=True)

    if st.session_state.econ_mode == "🔄 Analytika (Pinakas Periodon)":
        st.session_state.paste_input = st.text_area("Epikollisi dedomenon Excel (ETOS | APO | EΩS | FOREAS | IMERES | APODOCHES):", value=st.session_state.paste_input, height=120)
        if 'df_economic' in st.session_state:
            df_edited = st.data_editor(st.session_state['df_economic'], num_rows="dynamic", use_container_width=True, hide_index=True)
            df_edited['ENSIMA (H.E.)'] = pd.to_numeric(df_edited['ENSIMA (H.E.)'], errors='coerce').fillna(0)
            df_edited['APODOCHES (€)'] = pd.to_numeric(df_edited['APODOCHES (€)'], errors='coerce').fillna(0.0)
            df_edited['ETOS_NUM'] = pd.to_numeric(df_edited['ETOS'], errors='coerce').fillna(0)
            st.session_state['df_economic'] = df_edited
            
            total_ensima_disp = df_edited['ENSIMA (H.E.)'].sum()
            total_apodoches_disp = ((df_edited['ENSIMA (H.E.)'] / 25.0) * df_edited['APODOCHES (€)']).sum()
            df_p02 = df_edited[df_edited['ETOS_NUM'] >= 2002]
            avg_apod_disp = (df_p02['ENSIMA (H.E.)'] * df_p02['APODOCHES (€)']).sum() / df_p02['ENSIMA (H.E.)'].sum() if not df_p02.empty and df_p02['ENSIMA (H.E.)'].sum() > 0 else 0.0
            total_years_disp = total_ensima_disp / 300.0

            st.markdown(f"""
            <div style="background-color: #F1F5F9; border: 1px solid #CBD5E1; padding: 15px 20px; border-radius: 8px; margin-top: 10px; margin-bottom: 20px; font-size: 13px; color: #1E293B;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <div>📌 <b>SYNOLO ENSIMON:</b> <span style="color: #1E3A8A; font-weight: bold;">{int(total_ensima_disp):,} H.E.</span> ({total_years_disp:.2f} eti)</div>
                    <div>💶 <b>GENIKO SYNOLO APODOCHON:</b> <span style="color: #1E3A8A; font-weight: bold;">{total_apodoches_disp:,.2f} €</span></div>
                </div>
                <hr style="margin: 6px 0; border: none; border-top: 1px solid #CBD5E1;">
                <div style="text-align: right;">
                    📈 <b>STATHMISMENOS M.O. APODOCHON (apo 2002):</b> <span style="color: #16A34A; font-weight: bold;">{avg_apod_disp:,.2f} €</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        col_s1, col_s2 = st.columns(2)
        with col_s1: st.session_state.summary_years = st.number_input("Synolika Eti Asfalisis", value=float(st.session_state.summary_years), step=0.01)
        with col_s2: st.session_state.summary_avg_salary = st.number_input("Syntaximes Apodoches apo 2002 (€)", value=float(st.session_state.summary_avg_salary), step=10.0)

    st.markdown("---")
    st.markdown("#### ⚙️ Vasikes Parametroi Syntaksiodotisis")
    col_p1, col_p2 = st.columns(2)
    with col_p1: st.session_state.summary_years = st.number_input("Xronia Asfalisis (gia Kyria)", value=float(tot_years), step=0.01)
    with col_p2: st.session_state.pososto_anapl_custom = st.number_input("Pososto Anaplirosis (%)", value=float(st.session_state.pososto_anapl_custom), step=0.01)

    if st.button("💾 Apothikeysi Oikonomikon", type="primary"): persist_all(); st.success("✅ Apothikeytikan epitychos!")
    st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "⚙️ Rythmiseis & Eidika Tameia (TAPILT)":
    st.markdown('<div class="panel-card"><div class="panel-header">⚙️ Rythmiseis Parametron & Eidikon Tameion (p.x. TAPILT)</div>', unsafe_allow_html=True)
    
    st.session_state.has_tapilt = st.checkbox("✅ O pelates diathetei Epikouriki / Prosafxisi TAPILT (i paromoio eidiko tameio)", value=bool(st.session_state.has_tapilt))

    if st.session_state.has_tapilt:
        st.markdown("---")
        st.markdown("#### 🏦 Parametroi Ypologismou TAPILT")
        col_t1, col_t2 = st.columns(2)
        with col_t1: st.session_state.tapilt_sum_ginomeno = st.number_input("Athroisma Ginomenon [Eti × (Eisfora - 20)]", value=float(st.session_state.tapilt_sum_ginomeno), step=0.1)
        with col_t2: st.session_state.tapilt_syntaximos_misthos = st.number_input("Syntaximos Misthos Prosafxisis (€)", value=float(st.session_state.tapilt_syntaximos_misthos), step=10.0)
        
        st.info(f"💡 Ypologismeni Prosafxisi Kyrias: **{sum_ginomeno}** × 0,00075 × **{t_synt_misthos:,.2f} €** = **{prosafxisi_tapilt:,.2f} €**")

        st.markdown("---")
        st.markdown("#### 💶 Stoicheia Atomikis Meridas & Epikourikis TAPILT")
        col_e1, col_e2, col_e3, col_e4 = st.columns(4)
        with col_e1: 
            st.session_state.merida_amount = st.number_input("Atomiki Merida (€)", value=float(st.session_state.merida_amount), step=100.0)
        with col_e2: 
            st.session_state.tapilt_duration_years = float(tot_years)
            st.number_input("Diarkeia (Eti)", value=float(st.session_state.tapilt_duration_years), disabled=True, format="%.2f")
        with col_e3: 
            st.session_state.tapilt_after_expiry = st.number_input("Poso meta ti lixi (€)", value=float(st.session_state.tapilt_after_expiry), step=5.0)
        with col_e4: 
            st.session_state.tapilt_net = st.number_input("Poso Epik. TAPILT (€/mina)", value=float(st.session_state.tapilt_net), step=5.0)

        st.success(f"📌 Me vasi tin Atomiki Merida **{st.session_state.merida_amount:,.2f} €**, diarkeia **{tot_years:.2f} eti** kai poso **{tapilt_mikto:,.2f} €**, o ypologismos prohora kanonika.")
    else:
        st.info("ℹ️ O pelates einai typikos misthotos / asfalismenos (xoris eidiko tameio TAPILT).")

    if st.button("💾 Apothikeysi Rythmiseon", type="primary"): persist_all(); st.success("✅ Oi rythmiseis apothikeytikan!")
    st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "📊 Syngentrotika Apotelesmata & Syntaxeis":
    st.markdown('<div class="panel-card"><div class="panel-header">📊 Pinakas Ekatharisis Syntaxeon</div>', unsafe_allow_html=True)
    
    summary_rows_html = ""
    if bank_ens > 0 or bank_y > 0:
        summary_rows_html += f'<tr><td class="center">{bank_y:.2f}</td><td style="text-align: center; font-weight: bold;">TPAΠEZA</td><td style="text-align: right;">{bank_avg:,.2f} €</td><td class="center">{int(bank_ens):,}</td></tr>'
    if ika_ens > 0 or ika_y > 0:
        summary_rows_html += f'<tr><td class="center">{ika_y:.2f}</td><td style="text-align: center; font-weight: bold;">IKA</td><td style="text-align: right;">{ika_avg:,.2f} €</td><td class="center">{int(ika_ens):,}</td></tr>'
    if summary_rows_html == "":
        summary_rows_html = f'<tr><td class="center">0.00</td><td style="text-align: center; font-weight: bold;">-</td><td style="text-align: right;">0.00 €</td><td class="center">0</td></tr>'

    st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr><th colspan="4" style="background-color: #1E3A8A; color: white; text-align: center;">SYNOPSI XRONOY & APODOCHON</th></tr>
            <tr><th>XRONIA</th><th>FOREAS</th><th>M. OROS (€)</th><th>ENSIMA</th></tr>
        </thead>
        <tbody>
            {summary_rows_html}
            <tr class="total-row"><td class="center">{tot_years:.2f}</td><td style="text-align: center; font-weight: bold;">STATHMISMENOS M.O.</td><td style="text-align: right;">{avg_sal:,.2f} €</td><td class="center">{int(calc_tot_ensima):,}</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    second_row_html = ""
    if tot_years > 0:
        if st.session_state.has_tapilt:
            second_row_html = f"""
                <tr>
                    <td class="left">EΠIKOYPIKI TAPILT</td>
                    <td class="center">-</td>
                    <td class="center">{tot_years:.2f}</td>
                    <td class="center">-</td>
                    <td class="center">-</td>
                    <td>{tapilt_mikto:,.2f} €</td>
                    <td><b>{tapilt_mikto:,.2f} €</b></td>
                    <td>0,00 €</td>
                    <td>{ygeia_tapilt:,.2f} €</td>
                    <td>{foros_tapilt:,.2f} €</td>
                    <td>{krat_tapilt_total:,.2f} €</td>
                    <td><b>{tapilt_katharo:,.2f} €</b></td>
                    <td class="center">{tot_years:.2f} eti (meta {tapilt_meta_lixi}€)</td>
                </tr>
            """
        else:
            second_row_html = f"""
                <tr>
                    <td class="left">EΠIKOYPIKI IKA (EFKA)</td>
                    <td class="center">-</td>
                    <td class="center">-</td>
                    <td class="center">-</td>
                    <td class="center">-</td>
                    <td>0,00 €</td>
                    <td><b>{ika_mikto:,.2f} €</b></td>
                    <td>0,00 €</td>
                    <td>{ygeia_ika:,.2f} €</td>
                    <td>{foros_ika:,.2f} €</td>
                    <td>{krat_ika_total:,.2f} €</td>
                    <td><b>{katharo_ika:,.2f} €</b></td>
                    <td class="center">Isovia</td>
                </tr>
            """

    table_html = f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th colspan="7">YPOLOGISMOS SYNTAXIS (2026) - FOROLOGIKES KLIMAKES</th>
                <th colspan="4" class="kratseis">KRATISEIS</th>
                <th colspan="2" class="katharo-header">KATHARO PLIROTEO (€) & DIARKEIA</th>
            </tr>
            <tr>
                <th>Eidos Syntaxis</th><th>Mesos Misthos (€)</th><th>Xronia Asfal.</th><th>Ethniki Syntaxi (€)</th><th>Pososto Anapl. (%)</th><th>Prosafx. (€)</th><th>Mikto Synolo (€)</th>
                <th class="kratseis">EAS (€)</th><th class="kratseis">Ygeia 6% (€)</th><th class="kratseis">Foros Min. (€)</th><th class="kratseis">Synolo Krat. (€)</th>
                <th class="katharo-header">Katharo (€/mina)</th><th class="katharo-header">Diarkeia</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="left">KYRIA SYNTAXI</td>
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
                <td class="center">Isovia</td>
            </tr>
            {second_row_html}
            <tr class="total-row">
                <td class="left">GENIKO SYNOLO</td>
                <td class="center">-</td><td class="center">-</td><td class="center">-</td><td class="center">-</td><td class="center">-</td>
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
    """
    
    try:
        st.html(table_html)
    except:
        st.markdown(table_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "💼 Ypologismos Efapax":
    st.markdown('<div class="panel-card"><div class="panel-header">💼 Parametrikos Ypologismos Efapax (N. 4387/2016)</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.session_state.bank_years_until_2013 = st.number_input("Eti eos 31/12/2013", value=float(st.session_state.bank_years_until_2013), step=0.1)
    with col2: st.session_state.bank_years_from_2014 = st.number_input("Eti apo 2014 kai meta", value=float(st.session_state.bank_years_from_2014), step=0.1)
    with col3: st.session_state.efap_repl_rate = st.number_input("Syntelestis Anaplirosis (%)", value=float(st.session_state.efap_repl_rate), step=1.0)

    col4, col5 = st.columns(2)
    with col4: st.session_state.efap_avg_5y = st.number_input("Mesos Min. Misthos Pentaetias (€)", value=float(st.session_state.efap_avg_5y), step=10.0)
    with col5: st.session_state.efap_tmima_b = st.number_input("Synoliko Tmima B (€)", value=float(st.session_state.efap_tmima_b), step=100.0)

    tmima_a = st.session_state.bank_years_until_2013 * st.session_state.efap_avg_5y * (st.session_state.efap_repl_rate / 100.0)
    total_efapax = tmima_a + st.session_state.efap_tmima_b

    st.markdown(f"""
    <table class="custom-table" style="margin-top: 15px;">
        <thead><tr><th>TMIMA EFAPAX</th><th>POSO (€)</th></tr></thead>
        <tbody>
            <tr><td class="left">1. Tmima A (Eos 2013)</td><td>{tmima_a:,.2f} €</td></tr>
            <tr><td class="left">2. Tmima B (Apo 2014)</td><td>{st.session_state.efap_tmima_b:,.2f} €</td></tr>
            <tr class="total-row"><td class="left">🌟 SYNOLIKO KATHARO EFAPAX</td><td style="color: #1E3A8A;">{total_efapax:,.2f} €</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    if st.button("💾 Apothikeysi Efapax", type="primary"): persist_all(); st.success("✅ Apothikeytike!")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="panel-card"><div class="panel-header">📋 Teliki Eikona & Ektyposi</div>', unsafe_allow_html=True)
    monthly_tak_fin = st.session_state.efap_avg_5y
    total_efapax_fin = (st.session_state.bank_years_until_2013 * monthly_tak_fin * (st.session_state.efap_repl_rate / 100.0)) + st.session_state.efap_tmima_b
    c_name = f"{st.session_state.client_data['first_name']} {st.session_state.client_data['last_name']}".strip()
    c_name = c_name if c_name else "Anonymos Pelatis"
    
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; padding: 20px; border-radius: 10px; font-size: 14px;">
        <h3 style="color: #1E3A8A; margin-top: 0;">📄 EPIISIMI SYNOPSI PELATI: {c_name}</h3>
        <hr style="margin: 10px 0;">
        <p><b>Synolika Eti Asfalisis:</b> {tot_years:.2f} eti</p>
        <p><b>💶 SYNOLIKI KATHARI MINIAIA SYNTAXI:</b> <b>{geniko_katharo:,.2f} € / mina</b></p>
        <hr style="margin: 10px 0;">
        <p style="font-size: 16px; color: #16A34A;"><b>💼 SYNOLIKO KATHARO EFAPAX:</b> <b>{total_efapax_fin:,.2f} €</b></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🖨️ Ektyposi / Apothikeysi PDF", type="primary"): st.info("💡 Patiste **Ctrl + P**.")
    st.markdown('</div>', unsafe_allow_html=True)
