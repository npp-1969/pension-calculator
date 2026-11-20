import streamlit as st
import pandas as pd
import sqlite3
import re

st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

def parse_gr_float(val_str: str, default: float = 0.0) -> float:
    if val_str is None:
        return default
    clean = str(val_str).replace('€', '').replace('%', '').strip()
    if not clean:
        return default
    if ',' in clean and '.' in clean:
        clean = clean.replace('.', '').replace(',', '.')
    elif ',' in clean:
        clean = clean.replace(',', '.')
    elif '.' in clean:
        parts = clean.split('.')
        if len(parts) == 2 and len(parts[1]) == 3:
            clean = clean.replace('.', '')
    try:
        return float(clean)
    except:
        return default

def fmt_gr(val: float, decimals: int = 2) -> str:
    return f"{val:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")

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
            art30_years REAL,
            art30_extra_units REAL,
            efap_repl_rate REAL,
            efap_avg_5y REAL,
            efap_tmima_b REAL,
            efap_apodoches_14_22 REAL,
            efap_pronoia_rate REAL,
            efap_apousia_factor REAL
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
        INSERT INTO client_profile (
            first_name, last_name, gender, birth_date, insurance_cat, first_work_date, 
            econ_mode, paste_input, summary_years, summary_avg_salary, merida_amount, has_tapilt, tapilt_net, tapilt_after_expiry,
            bank_years_until_2013, bank_years_from_2014, pososto_anapl_custom, 
            tapilt_sum_ginomeno, tapilt_syntaximos_misthos, tapilt_duration_years,
            art30_years, art30_extra_units, efap_repl_rate, efap_avg_5y, efap_tmima_b,
            efap_apodoches_14_22, efap_pronoia_rate, efap_apousia_factor
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["first_name"], data["last_name"], data["gender"], data["birth_date"],
        data["insurance_cat"], data["first_work_date"], data["econ_mode"],
        data["paste_input"], data["summary_years"], data["summary_avg_salary"],
        data["merida_amount"], data["has_tapilt"], data["tapilt_net"], data["tapilt_after_expiry"],
        data["bank_years_until_2013"], data["bank_years_from_2014"], data["pososto_anapl_custom"],
        data["tapilt_sum_ginomeno"], data["tapilt_syntaximos_misthos"], data["tapilt_duration_years"],
        data["art30_years"], data["art30_extra_units"],
        data["efap_repl_rate"], data["efap_avg_5y"], data["efap_tmima_b"],
        data["efap_apodoches_14_22"], data["efap_pronoia_rate"], data["efap_apousia_factor"]
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
               art30_years, art30_extra_units, efap_repl_rate, efap_avg_5y, efap_tmima_b,
               efap_apodoches_14_22, efap_pronoia_rate, efap_apousia_factor
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
            "art30_years": row[20] if row[20] is not None else 0.0,
            "art30_extra_units": row[21] if row[21] is not None else 0.0,
            "efap_repl_rate": row[22] if row[22] is not None else 60.0,
            "efap_avg_5y": row[23] if row[23] is not None else 0.0,
            "efap_tmima_b": row[24] if row[24] is not None else 0.0,
            "efap_apodoches_14_22": row[25] if row[25] is not None else 0.0,
            "efap_pronoia_rate": row[26] if row[26] is not None else 4.0,
            "efap_apousia_factor": row[27] if row[27] is not None else 1.015
        }
    return None

st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: white; padding: 20px 26px; border-radius: 12px; margin-bottom: 20px;
    }
    .panel-card {
        background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;
        padding: 20px; margin-bottom: 18px;
    }
    .efapax-table { width: 100%; border-collapse: collapse; font-size: 13px; font-family: sans-serif; margin-top: 12px; margin-bottom: 18px; }
    .efapax-table th.efapax-banner {
        background-color: #102A54; color: #FFFFFF; text-align: center;
        padding: 10px 12px; border: 1px solid #94A3B8; font-size: 14px; font-weight: 700;
    }
    .efapax-table td { padding: 8px 12px; border: 1px solid #94A3B8; vertical-align: middle; color: #0F172A; }
    .efapax-table td.label-cell { background-color: #F8FAFC; font-weight: 600; text-align: left; width: 25%; }
    .efapax-table td.val-blue { background-color: #EEF5FF; color: #1D4ED8; font-weight: 700; text-align: center; width: 14%; }
    .efapax-table td.formula-cell { background-color: #FFFFFF; font-weight: 600; text-align: center; width: 31%; }
    .efapax-table td.result-cell { background-color: #FFFFFF; font-weight: 700; text-align: right; width: 30%; }
    .efapax-table td.total-green-lbl { background-color: #E8F5E9; color: #15803D; font-weight: 700; text-align: center; }
    .efapax-table td.total-green-val { background-color: #E8F5E9; color: #15803D; font-weight: 800; text-align: right; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔒 Ασφαλής Είσοδος BMS</h2>", unsafe_allow_html=True)
    username = st.text_input("Όνομα Χρήστη")
    password = st.text_input("Κωδικός (Password)", type="password")
    if st.button("🔑 ΕΙΣΟΔΟΣ", use_container_width=True, type="primary"):
        if username.strip() and password.strip() == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Λανθασμένος κωδικός! (Δοκιμάστε: 1234)")
    st.stop()

db_data = load_from_db()

if 'client_data' not in st.session_state:
    st.session_state.client_data = {
        "first_name": db_data["first_name"] if db_data else "",
        "last_name": db_data["last_name"] if db_data else "",
        "gender": db_data["gender"] if db_data else "Άνδρας",
        "birth_date": db_data["birth_date"] if db_data else "",
        "insurance_cat": db_data["insurance_cat"] if db_data else "Μισθωτός — Τράπεζα / Ιονική (πρώην ΤΑΠΙΛΤ)",
        "first_work_date": db_data["first_work_date"] if db_data else ""
    }

if 'econ_mode' not in st.session_state: st.session_state.econ_mode = db_data["econ_mode"] if db_data else "🔄 Αναλυτικά (Πίνακας Περιόδων)"
if 'paste_input' not in st.session_state: st.session_state.paste_input = db_data["paste_input"] if db_data else ""
if 'summary_years' not in st.session_state: st.session_state.summary_years = db_data["summary_years"] if db_data else 0.0
if 'summary_avg_salary' not in st.session_state: st.session_state.summary_avg_salary = db_data["summary_avg_salary"] if db_data else 0.0
if 'has_tapilt' not in st.session_state: st.session_state.has_tapilt = bool(db_data["has_tapilt"]) if db_data else True
if 'merida_amount' not in st.session_state: st.session_state.merida_amount = db_data["merida_amount"] if db_data else 0.0
if 'tapilt_net' not in st.session_state: st.session_state.tapilt_net = db_data["tapilt_net"] if db_data else 0.0
if 'tapilt_after_expiry' not in st.session_state: st.session_state.tapilt_after_expiry = db_data["tapilt_after_expiry"] if db_data else 0.0
if 'bank_years_until_2013' not in st.session_state: st.session_state.bank_years_until_2013 = db_data["bank_years_until_2013"] if db_data else 0.0
if 'bank_years_from_2014' not in st.session_state: st.session_state.bank_years_from_2014 = db_data["bank_years_from_2014"] if db_data else 0.0
if 'pososto_anapl_custom' not in st.session_state: st.session_state.pososto_anapl_custom = db_data["pososto_anapl_custom"] if db_data else 51.29
if 'tapilt_sum_ginomeno' not in st.session_state: st.session_state.tapilt_sum_ginomeno = db_data["tapilt_sum_ginomeno"] if db_data else 0.0
if 'tapilt_syntaximos_misthos' not in st.session_state: st.session_state.tapilt_syntaximos_misthos = db_data["tapilt_syntaximos_misthos"] if db_data else 0.0
if 'tapilt_duration_years' not in st.session_state: st.session_state.tapilt_duration_years = db_data["tapilt_duration_years"] if db_data else 0.0
if 'art30_years' not in st.session_state: st.session_state.art30_years = db_data["art30_years"] if db_data else 0.0
if 'art30_extra_units' not in st.session_state: st.session_state.art30_extra_units = db_data["art30_extra_units"] if db_data else 0.0
if 'efap_repl_rate' not in st.session_state: st.session_state.efap_repl_rate = db_data["efap_repl_rate"] if db_data else 60.0
if 'efap_avg_5y' not in st.session_state: st.session_state.efap_avg_5y = db_data["efap_avg_5y"] if db_data else 0.0
if 'efap_tmima_b' not in st.session_state: st.session_state.efap_tmima_b = db_data["efap_tmima_b"] if db_data else 0.0
if 'efap_apodoches_14_22' not in st.session_state: st.session_state.efap_apodoches_14_22 = db_data["efap_apodoches_14_22"] if db_data else 0.0
if 'efap_pronoia_rate' not in st.session_state: st.session_state.efap_pronoia_rate = db_data["efap_pronoia_rate"] if db_data else 4.0
if 'efap_apousia_factor' not in st.session_state: st.session_state.efap_apousia_factor = db_data["efap_apousia_factor"] if db_data else 1.015

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
        "art30_years": float(st.session_state.art30_years),
        "art30_extra_units": float(st.session_state.art30_extra_units),
        "efap_repl_rate": float(st.session_state.efap_repl_rate),
        "efap_avg_5y": float(st.session_state.efap_avg_5y),
        "efap_tmima_b": float(st.session_state.efap_tmima_b),
        "efap_apodoches_14_22": float(st.session_state.efap_apodoches_14_22),
        "efap_pronoia_rate": float(st.session_state.efap_pronoia_rate),
        "efap_apousia_factor": float(st.session_state.efap_apousia_factor)
    })

st.markdown("""
    <div class="main-header">
        <div style="font-size: 23px; font-weight: 700;">💼 Professional Pension BMS</div>
        <div style="font-size: 12.5px; color: #94A3B8; margin-top: 4px;">Αυτόματος Υπολογισμός Εφάπαξ από Οικονομικά Στοιχεία & Ασφαλιστικό Ιστορικό</div>
    </div>
""", unsafe_allow_html=True)

app_section = st.sidebar.radio("Ενότητα:", [
    "💰 Οικονομικά Στοιχεία & Ασφαλιστικό Ιστορικό",
    "💼 Υπολογισμός Εφάπαξ"
])

if st.sidebar.button("🧹 Πλήρης Καθαρισμός Στοιχείων Πελάτη", use_container_width=True):
    st.session_state.client_data = {"first_name": "", "last_name": "", "gender": "Άνδρας", "birth_date": "", "insurance_cat": "Μισθωτός — Τράπεζα / Ιονική (πρώην ΤΑΠΙΛΤ)", "first_work_date": ""}
    st.session_state.paste_input = ""
    st.session_state.summary_years = 0.0
    st.session_state.summary_avg_salary = 0.0
    st.session_state.bank_years_until_2013 = 0.0
    st.session_state.efap_avg_5y = 0.0
    st.session_state.efap_apodoches_14_22 = 0.0
    st.session_state.efap_tmima_b = 0.0
    st.session_state['df_economic'] = pd.DataFrame(columns=["ΕΤΟΣ", "ΑΠΟ (ΗΜ/ΝΙΑ)", "ΕΩΣ (ΗΜ/ΝΙΑ)", "ΦΟΡΕΑΣ", "ΕΝΣΗΜΑ (Η.Ε.)", "ΑΠΟΔΟΧΕΣ (€)"])
    persist_all()
    st.rerun()

# Ανάλυση επικολλημένων στοιχείων
df_parsed = pd.DataFrame()
if st.session_state.paste_input.strip():
    try:
        final_data = []
        for line in st.session_state.paste_input.strip().split('\n'):
            parts = line.replace('\t', ' ').split()
            if len(parts) >= 6:
                raw_apod = parts[-1].replace('€', '').replace('.', '').replace(',', '.').strip()
                try:
                    val_apod = float(raw_apod)
                except:
                    val_apod = parse_gr_float(parts[-2], 0.0)
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
    except:
        pass

if not df_parsed.empty:
    st.session_state['df_economic'] = df_parsed
elif 'df_economic' not in st.session_state:
    st.session_state['df_economic'] = pd.DataFrame(columns=["ΕΤΟΣ", "ΑΠΟ (ΗΜ/ΝΙΑ)", "ΕΩΣ (ΗΜ/ΝΙΑ)", "ΦΟΡΕΑΣ", "ΕΝΣΗΜΑ (Η.Ε.)", "ΑΠΟΔΟΧΕΣ (€)"])

auto_bank_years_until_2013 = 0.0
auto_avg_09_13 = 0.0
auto_apod_14_22 = 0.0

if 'df_economic' in st.session_state and not st.session_state['df_economic'].empty:
    df_calc = st.session_state['df_economic'].copy()

    def extract_year_from_row(row):
        for val in row.values:
            match = re.search(r'(19\d{2}|20\d{2})', str(val))
            if match:
                y = int(match.group(1))
                if 1950 <= y <= 2050:
                    return y
        return 0

    def check_bank_row(row):
        row_str = " ".join([str(v).upper() for v in row.values])
        return any(kw in row_str for kw in ['ΤΡΑΠΕΖΑ', 'ΙΟΝΙΚΗ', 'ALPHA', 'ΤΑΠΙΛΤ'])

    df_calc['ΕΤΟΣ_CLEAN'] = df_calc.apply(extract_year_from_row, axis=1)
    df_calc['ΕΝΣΗΜΑ (Η.Ε.)'] = pd.to_numeric(df_calc['ΕΝΣΗΜΑ (Η.Ε.)'], errors='coerce').fillna(0.0)
    df_calc['ΑΠΟΔΟΧΕΣ (€)'] = pd.to_numeric(df_calc['ΑΠΟΔΟΧΕΣ (€)'], errors='coerce').fillna(0.0)

    df_bank = df_calc[df_calc.apply(check_bank_row, axis=1)]
    if not df_bank.empty:
        ens_until_2013 = df_bank[(df_bank['ΕΤΟΣ_CLEAN'] > 0) & (df_bank['ΕΤΟΣ_CLEAN'] <= 2013)]['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
        auto_bank_years_until_2013 = ens_until_2013 / 300.0

        df_09_13 = df_bank[(df_bank['ΕΤΟΣ_CLEAN'] >= 2009) & (df_bank['ΕΤΟΣ_CLEAN'] <= 2013)]
        if not df_09_13.empty and df_09_13['ΕΝΣΗΜΑ (Η.Ε.)'].sum() > 0:
            auto_avg_09_13 = (df_09_13['ΕΝΣΗΜΑ (Η.Ε.)'] * df_09_13['ΑΠΟΔΟΧΕΣ (€)']).sum() / df_09_13['ΕΝΣΗΜΑ (Η.Ε.)'].sum()

        df_14_22 = df_bank[(df_bank['ΕΤΟΣ_CLEAN'] >= 2014) & (df_bank['ΕΤΟΣ_CLEAN'] <= 2022)]
        if not df_14_22.empty:
            auto_apod_14_22 = ((df_14_22['ΕΝΣΗΜΑ (Η.Ε.)'] / 25.0) * df_14_22['ΑΠΟΔΟΧΕΣ (€)']).sum()

# Αυτόματη ενημέρωση από τα Οικονομικά Στοιχεία
st.session_state.bank_years_until_2013 = auto_bank_years_until_2013
st.session_state.efap_avg_5y = auto_avg_09_13
st.session_state.efap_apodoches_14_22 = auto_apod_14_22

anagogi_14minou_exact = st.session_state.efap_avg_5y * (12.0 / 14.0)
tmima_a_exact = st.session_state.bank_years_until_2013 * anagogi_14minou_exact * (st.session_state.efap_repl_rate / 100.0)
tmima_b_exact = st.session_state.efap_apodoches_14_22 * (st.session_state.efap_pronoia_rate / 100.0) * st.session_state.efap_apousia_factor
total_efapax_exact = tmima_a_exact + tmima_b_exact

anagogi_14minou = round(anagogi_14minou_exact, 2)
tmima_a = round(tmima_a_exact, 2)
tmima_b = round(tmima_b_exact, 2)
st.session_state.efap_tmima_b = tmima_b
total_efapax = round(total_efapax_exact, 2)

if app_section == "💰 Οικονομικά Στοιχεία & Ασφαλιστικό Ιστορικό":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("#### 💰 Οικονομικά Στοιχεία & Ασφαλιστικό Ιστορικό")
    st.session_state.paste_input = st.text_area(
        "Επικόλληση δεδομένων Excel (ΕΤΟΣ | ΑΠΟ | ΕΩΣ | ΦΟΡΕΑΣ | ΗΜΕΡΕΣ | ΑΠΟΔΟΧΕΣ):",
        value=st.session_state.paste_input,
        height=130
    )
    df_edited = st.data_editor(st.session_state['df_economic'], num_rows="dynamic", use_container_width=True, hide_index=True)
    st.session_state['df_economic'] = df_edited
    if st.button("💾 Αποθήκευση Οικονομικών Στοιχείων", type="primary"):
        persist_all()
        st.success("✅ Τα οικονομικά στοιχεία αποθηκεύτηκαν και τα ποσά ενημερώθηκαν αυτόματα!")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    efapax_table_html = f"""
    <table class="efapax-table">
        <thead>
            <tr>
                <th colspan="4" class="efapax-banner">ΥΠΟΛΟΓΙΣΜΟΣ ΕΦΑΠΑΞ ΠΑΡΟΧΗΣ (πρ. ΤΑΠΙΛΤ-ΑΤ / e-ΕΦΚΑ - Ν. 4387/2016) - ΑΦΟΡΟΛΟΓΗΤΟ</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="label-cell">Έτη Τράπεζας έως 31/12/2013</td>
                <td class="val-blue">{fmt_gr(st.session_state.bank_years_until_2013, 2)}</td>
                <td class="formula-cell">1. Τμήμα Α (Έτη έως 31/12/2013 × Αναγωγή 14μήνου × {fmt_gr(st.session_state.efap_repl_rate, 0)}%)</td>
                <td class="result-cell">{fmt_gr(tmima_a, 2)} €</td>
            </tr>
            <tr>
                <td class="label-cell">Μέσος Μισθός 2009–2013 (12μηνο)</td>
                <td class="val-blue">{fmt_gr(st.session_state.efap_avg_5y, 2)} €</td>
                <td class="formula-cell">Βάση Υπολογισμού Τμήματος Β (Αποδοχές 2014–2022)</td>
                <td class="result-cell">{fmt_gr(st.session_state.efap_apodoches_14_22, 2)} €</td>
            </tr>
            <tr>
                <td class="label-cell">Αναγωγή σε Μηνιαίο Τακτικό (14μηνο)</td>
                <td class="val-blue">{fmt_gr(anagogi_14minou, 2)} €</td>
                <td class="formula-cell">2. Τμήμα Β (Αποδοχές 2014–2022 × {fmt_gr(st.session_state.efap_pronoia_rate, 0)}% × {fmt_gr(st.session_state.efap_apousia_factor, 3)})</td>
                <td class="result-cell">{fmt_gr(tmima_b, 2)} €</td>
            </tr>
            <tr>
                <td class="label-cell">Συντελεστής Αναπλήρωσης (έως 2013)</td>
                <td class="val-blue">{fmt_gr(st.session_state.efap_repl_rate, 2)}%</td>
                <td class="total-green-lbl">ΚΑΘΑΡΟ ΣΥΝΟΛΟ ΕΦΑΠΑΞ e-ΕΦΚΑ (ΑΦΟΡΟΛΟΓΗΤΟ)</td>
                <td class="total-green-val">{fmt_gr(total_efapax, 2)} €</td>
            </tr>
            <tr>
                <td class="label-cell">Ποσοστό Εισφοράς Πρόνοιας (από 2014)</td>
                <td class="val-blue">{fmt_gr(st.session_state.efap_pronoia_rate, 2)}%</td>
                <td class="formula-cell">Τρόπος & Χρόνος Καταβολής</td>
                <td class="result-cell" style="text-align: center;">Με την έκδοση της Κύριας Σύνταξης</td>
            </tr>
            <tr>
                <td class="label-cell">Συντελεστής Αποτίμησης (2014–2022)</td>
                <td class="val-blue">{fmt_gr(st.session_state.efap_apousia_factor, 3)}</td>
                <td class="formula-cell">Φόρος Εισοδήματος</td>
                <td class="result-cell" style="text-align: center;">0,00 € (Πλήρως Αφορολόγητο)</td>
            </tr>
        </tbody>
    </table>
    """
    try:
        st.html(efapax_table_html)
    except:
        st.markdown(efapax_table_html, unsafe_allow_html=True)

    if st.button("💾 Αποθήκευση Αποτελέσματος", type="primary"):
        persist_all()
        st.success("✅ Το αποτέλεσμα αποθηκεύτηκε!")
    st.markdown('</div>', unsafe_allow_html=True)
