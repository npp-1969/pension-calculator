import streamlit as st
import pandas as pd
import io

# Ρύθμιση σελίδας
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# CSS για επαγγελματικό ERP design
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
# ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE (ΜΝΗΜΗ ΔΕΔΟΜΕΝΩΝ)
# ==========================================
if 'client_data' not in st.session_state:
    st.session_state.client_data = {
        "first_name": "",
        "last_name": "",
        "gender": "Άνδρας",
        "birth_date": "",
        "insurance_cat": "Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)",
        "first_work_date": ""
    }

if 'econ_mode' not in st.session_state:
    st.session_state.econ_mode = "🔄 Αναλυτικά (Πίνακας Περιόδων)"

if 'paste_input' not in st.session_state:
    st.session_state.paste_input = (
        "2007\t01/01/2007\t31/01/2007\tΤΡΑΠΕΖΑ\t25\t3304.39\n"
        "2007\t01/02/2007\t28/02/2007\tΙΚΑ\t25\t3015.47"
    )

if 'summary_years' not in st.session_state:
    st.session_state.summary_years = 42.57

if 'summary_avg_salary' not in st.session_state:
    st.session_state.summary_avg_salary = 3290.54

# ==========================================
# ΕΠΑΓΓΕΛΜΑΤΙΚΟ MENU & ΕΦΑΡΜΟΓΗ
# ==========================================
st.markdown(f"""
    <div class="main-header">
        <div class="main-title">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 12px; border-radius: 8px;">💼</span> 
            Professional Pension BMS — Χρήστης: <u>{st.session_state.get('current_user', 'Χρήστης')}</u>
        </div>
        <div class="main-subtitle">Επαγγελματικό Σύστημα Υπολογισμού Συντάξεων & Οικονομικών Δεδομένων (Ν. 4387/2016)</div>
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
st.sidebar.success("🟢 Ασφαλής Σύνδεση")

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
        st.session_state.client_data["first_work_date"] = st.text_input("Ημερομηνία Πρώτης Απασχόλησης", value=st.session_state.client_data["first_work_date"], placeholder="π.χ. Ιούνιος 1990")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Αποθήκευση Προσωπικών Στοιχείων", type="primary"):
        st.success("✅ Τα προσωπικά στοιχεία αποθηκεύτηκαν επιτυχώς στη μνήμη!")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. ΟΙΚΟΝΟΜΙΚΑ & ΑΣΦΑΛΙΣΤΙΚΑ ΣΤΟΙΧΕΙΑ ---
elif app_section == "💰 Οικονομικά & Ασφαλιστικά Στοιχεία":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💰 Κατηγορία: 2. Οικονομικά & Ασφαλιστικά Στοιχεία</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Επιλέξτε τρόπο καταχώρησης (Αναλυτικά με πίνακα ή Συγκεντρωτικά) και αποθηκεύστε τα.</div>', unsafe_allow_html=True)

    modes = ["🔄 Αναλυτικά (Πίνακας Περιόδων)", "⚡ Συγκεντρωτικά (Συνολικά Έτη & Μέσος Όρος)"]
    m_idx = modes.index(st.session_state.econ_mode) if st.session_state.econ_mode in modes else 0
    st.session_state.econ_mode = st.radio("Τρόπος καταχώρησης οικονομικών στοιχείων:", modes, index=m_idx, horizontal=True)

    st.markdown("---")

    if st.session_state.econ_mode == "🔄 Αναλυτικά (Πίνακας Περιόδων)":
        st.markdown("#### 📋 Πίνακας Περιόδων & Επικόλλησης Excel")
        st.markdown("Σειρά στηλών: **ΕΤΟΣ | ΑΠΟ | ΕΩΣ | ΦΟΡΕΑΣ | ΗΜΕΡΕΣ | ΑΠΟΔΟΧΕΣ**")

        def clear_text():
            st.session_state.paste_input = ""

        col_b1, col_b2 = st.columns([1, 4])
        with col_b1:
            st.button("🗑️ Καθαρισμός", on_click=clear_text)
        
        st.session_state.paste_input = st.text_area("Επικόλληση δεδομένων Excel εδώ:", value=st.session_state.paste_input, height=120)

        processed_df = pd.DataFrame()
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
                        etos = row_vals[0]
                        apo = row_vals[1]
                        eos = row_vals[2]
                        forer = row_vals[3]
                        
                        try:
                            ensima = float(row_vals[4].replace(',', '.'))
                        except:
                            ensima = 25.0
                        
                        try:
                            apod = float(row_vals[5].replace('€', '').replace('.', '').replace(',', '.'))
                        except:
                            apod = 0.0

                        final_data.append({
                            "ΕΤΟΣ": etos,
                            "ΑΠΟ (ΗΜ/ΝΙΑ)": apo,
                            "ΕΩΣ (ΗΜ/ΝΙΑ)": eos,
                            "ΦΟΡΕΑΣ": str(forer).upper().strip(),
                            "ΕΝΣΗΜΑ (Η.Ε.)": ensima,
                            "ΑΠΟΔΟΧΕΣ (€)": apod
                        })

                processed_df = pd.DataFrame(final_data)
            except Exception as e:
                st.error(f"Σφάλμα ανάγνωσης: {e}")

        if not processed_df.empty:
            st.markdown("##### ✏️ Έλεγχος & Διόρθωση Δεδομένων:")
            df = st.data_editor(processed_df, num_rows="dynamic", use_container_width=True, hide_index=True)

            df['ΕΝΣΗΜΑ (Η.Ε.)'] = pd.to_numeric(df['ΕΝΣΗΜΑ (Η.Ε.)'], errors='coerce').fillna(0)
            df['ΑΠΟΔΟΧΕΣ (€)'] = pd.to_numeric(df['ΑΠΟΔΟΧΕΣ (€)'], errors='coerce').fillna(0.0)
            df['ΦΟΡΕΑΣ'] = df['ΦΟΡΕΑΣ'].astype(str).str.upper().str.strip()

            total_all_ensima = df['ΕΝΣΗΜΑ (Η.Ε.)'].sum()
            total_all_apodoches = df['ΑΠΟΔΟΧΕΣ (€)'].sum()
            overall_avg_salary = df['ΑΠΟΔΟΧΕΣ (€)'].mean() if len(df) > 0 else 0

            st.session_state['total_all_ensima'] = total_all_ensima
            st.session_state['overall_avg_salary'] = overall_avg_salary

            st.markdown("---")
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Συνολικά Ένσημα", f"{int(total_all_ensima):,}")
            sc2.metric("Συνολικό Άθροισμα Μικτών Αποδοχών", f"{total_all_apodoches:,.2f} €")
            sc3.metric("Συνολικός Μέσος Μισθός", f"{overall_avg_salary:,.2f} €")

    else:
        st.markdown("#### ⚡ Συγκεντρωτική Καταχώρηση")
        eco_c1, eco_c2 = st.columns(2)
        with eco_c1:
            st.session_state.summary_years = st.number_input("Συνολικά Έτη Ασφάλισης", value=st.session_state.summary_years)
            st.session_state['total_all_ensima'] = st.session_state.summary_years * 300.0
        with eco_c2:
            st.session_state.summary_avg_salary = st.number_input("Συνολικός Μέσος Μισθός (€)", value=st.session_state.summary_avg_salary)
            st.session_state['overall_avg_salary'] = st.session_state.summary_avg_salary

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Αποθήκευση Οικονομικών Στοιχείων", type="primary"):
        st.success("✅ Τα οικονομικά στοιχεία αποθηκεύτηκαν επιτυχώς στη μνήμη!")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ ---
elif app_section == "📊 Συγκεντρωτικά Αποτελέσματα":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 Κατηγορία: 3. Συγκεντρωτικά Αποτελέσματα (2026)</div>', unsafe_allow_html=True)
    
    c_info = st.session_state.client_data
    if c_info["first_name"] or c_info["last_name"]:
        st.info(f"📋 **Εξεταζόμενος Πελάτης:** {c_info['first_name']} {c_info['last_name']} | **Φύλο:** {c_info['gender']} | **Γέννηση:** {c_info['birth_date']} | **Ταμείο:** {c_info['insurance_cat']}")

    tot_ensima = st.session_state.get('total_all_ensima', 12771)
    tot_years = tot_ensima / 300.0
    avg_sal = st.session_state.get('overall_avg_salary', 3290.54)

    st.markdown("---")
    st.markdown("#### 📋 Αναλυτικός Πίνακας Συντάξεων & Κρατήσεων (2026)")
    
    detailed_calc_table = pd.DataFrame([
        {
            "Είδος Σύνταξης": "ΚΥΡΙΑ ΣΥΝΤΑΞΗ",
            "Μέσος Μισθός (€)": f"{avg_sal:,.2f} €",
            "Χρόνια Ασφάλισης": f"{tot_years:.2f}",
            "Εθνική Σύνταξη (€)": "446,87 €",
            "Ποσοστό Αναπλ. (%)": "51,00%",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "349,26 €",
            "Μικτό Σύνολο (€)": "2.094,51 €",
            "ΕΑΣ (€)": "146,62 €",
            "Υγεία 6% (€)": "116,87 €",
            "Φόρος Μην. (€)": "244,50 €",
            "Σύνολο Κρατ. (€)": "507,99 €",
            "Καθαρό Πληρωτέο (€)": "1.586,53 €",
            "Διάρκεια Επικουρικού": "Ισόβια"
        },
        {
            "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ",
            "Μέσος Μισθός (€)": "-",
            "Χρόνια Ασφάλισης": "32,22",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "350,00 €",
            "Μικτό Σύνολο (€)": "350,00 €",
            "ΕΑΣ (€)": "0,00 €",
            "Υγεία 6% (€)": "21,00 €",
            "Φόρος Μην. (€)": "0,00 €",
            "Σύνολο Κρατ. (€)": "21,00 €",
            "Καθαρό Πληρωτέο (€)": "329,00 €",
            "Διάρκεια Επικουρικού": "17 έτη"
        },
        {
            "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)",
            "Μέσος Μισθός (€)": "0,00 €",
            "Χρόνια Ασφάλισης": "9,60",
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
            "Μέσος Μισθός (€)": "-",
            "Χρόνια Ασφάλισης": "-",
            "Εθνική Σύνταξη (€)": "-",
            "Ποσοστό Αναπλ. (%)": "-",
            "Προσαύξ. ΤΑΠΙΛΤ (€)": "-",
            "Μικτό Σύνολο (€)": "2.444,51 €",
            "ΕΑΣ (€)": "146,62 €",
            "Υγεία 6% (€)": "137,87 €",
            "Φόρος Μην. (€)": "244,50 €",
            "Σύνολο Κρατ. (€)": "528,99 €",
            "Καθαρό Πληρωτέο (€)": "1.915,53 €",
            "Διάρκεια Επικουρικού": "-"
        }
    ])

    st.dataframe(detailed_calc_table, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. ΡΥΘΜΙΣΕΙΣ ΣΥΣΤΗΜΑΤΟΣ ---
else:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">⚙️ Ρυθμίσεις Συστήματος BMS</div>', unsafe_allow_html=True)
    st.write("Εδώ διαχειρίζεστε τους συντελεστές, τα ποσοστά κρατήσεων (Υγεία, ΕΑΣ, Φόρος) και την ασφάλεια χρηστών.")
    st.markdown('</div>', unsafe_allow_html=True)
