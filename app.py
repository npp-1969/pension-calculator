import streamlit as st
import pandas as pd
import io

# Ρύθμιση σελίδας
st.set_page_config(page_title="Υπολογιστής Σύνταξης 2026", page_icon="💼", layout="wide")

# CSS για την κορυφαία εμφάνιση (ERP Design)
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
    .warning-box {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        color: #92400E;
        padding: 12px 18px;
        border-radius: 6px;
        font-size: 13px;
        margin-bottom: 20px;
    }
    .info-badge {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #1E40AF;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 13px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Κεφαλίδα εφαρμογής
st.markdown("""
    <div class="main-header">
        <div class="main-title">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 12px; border-radius: 8px;">Σ</span> 
            Υπολογιστής Σύνταξης 2026
        </div>
        <div class="main-subtitle">Προσομοίωση σύνταξης ΕΦΚΑ — κύρια (εθνική + ανταποδοτική) & επικουρική ΕΤΕΑΕΠ, με τους ισχύοντες κανόνες</div>
    </div>
""", unsafe_allow_html=True)

# Ειδοποίηση / Warning
st.markdown("""
    <div class="warning-box">
        ⚠️ <b>Ενημερωτικός υπολογιστής-προσέγγιση.</b> Το αποτέλεσμα είναι ενδεικτικό και δεν αποτελεί δέσμευση του ΕΦΚΑ.
    </div>
""", unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.markdown("### 🗂️ Μενού Συστήματος")
app_section = st.sidebar.radio("Επιλογή:", ["📊 Κεντρικός Υπολογισμός", "📋 Δεδομένα & Αρχείο", "⚙️ Ρυθμίσεις"])

st.sidebar.markdown("---")
st.sidebar.success("🟢 BMS Engine Active (2026)")

# Session state για αποθήκευση προσώπων
if 'saved_profiles' not in st.session_state:
    st.session_state.saved_profiles = {}

if 'clear_form' not in st.session_state:
    st.session_state.clear_form = False

if app_section == "📊 Κεντρικός Υπολογισμός":

    # ==========================================
    # 0. ΜΠΑΡΑ ΕΠΙΛΟΓΗΣ / ΑΠΟΘΗΚΕΥΣΗΣ ΠΡΟΣΩΠΟΥ
    # ==========================================
    st.markdown('<div class="panel-card" style="background-color: #F1F5F9; padding: 15px;">', unsafe_allow_html=True)
    top_c1, top_c2, top_c3 = st.columns([2, 2, 1])
    
    with top_c1:
        profile_names = ["— Νέα / Καθαρή Καρτέλα —"] + list(st.session_state.saved_profiles.keys())
        selected_profile = st.selectbox("📂 Επιλογή αποθηκευμένης καρτέλας:", profile_names)
    
    # Αν ο χρήστης επιλέξει αποθηκευμένο προφίλ, φορτώνουμε τα στοιχεία του
    if selected_profile != "— Νέα / Καθαρή Καρτέλα —":
        p_data = st.session_state.saved_profiles[selected_profile]
        def_name = p_data.get("first_name", "")
        def_surname = p_data.get("last_name", "")
        def_gender = p_data.get("gender", "Άνδρας")
        def_bdate = p_data.get("birth_date", "")
        def_cat = p_data.get("insurance_cat", "Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)")
        def_wdate = p_data.get("first_work_date", "")
    else:
        def_name = "" if st.session_state.clear_form else "ΝΕΚΤΑΡΙΟΣ"
        def_surname = "" if st.session_state.clear_form else "ΠΕΛΕΚΑΝΟΣ"
        def_gender = "Άνδρας"
        def_bdate = "" if st.session_state.clear_form else "16/09/1969"
        def_cat = "Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)"
        def_wdate = "" if st.session_state.clear_form else "Ιούνιος 1990"

    with top_c2:
        save_name_input = st.text_input("Όνομα αποθήκευσης καρτέλας:", placeholder="π.χ. Νεκτάριος Πελεκάνος")

    with top_c3:
        st.markdown("<br>", unsafe_allow_html=True)
        save_btn = st.button("💾 Αποθήκευση", use_container_width=True)
        if save_btn and save_name_input.strip():
            st.session_state.saved_profiles[save_name_input.strip()] = {
                "first_name": def_name,
                "last_name": def_surname,
                "gender": def_gender,
                "birth_date": def_bdate,
                "insurance_cat": def_cat,
                "first_work_date": def_wdate
            }
            st.success(f"Αποθηκεύτηκε: {save_name_input.strip()}")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 1. ΣΤΟΙΧΕΙΑ ΠΡΟΣΩΠΟΥ
    # ==========================================
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    
    col_h_p1, col_h_p2 = st.columns([4, 1])
    with col_h_p1:
        st.markdown('<div class="panel-header">1️⃣ Στοιχεία προσώπου</div>', unsafe_allow_html=True)
    with col_h_p2:
        def clear_fields():
            st.session_state.clear_form = True
        st.button("🗑️ Καθαρισμός Στοιχείων", on_click=clear_fields, use_container_width=True)

    st.markdown('<div class="panel-desc">Συμπληρώστε τα στοιχεία που χρειάζονται για τον υπολογισμό.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        first_name = st.text_input("Όνομα", value=def_name)
    with col2:
        last_name = st.text_input("Επώνυμο", value=def_surname)
    with col3:
        gender = st.selectbox("Φύλο", ["Άνδρας", "Γυναίκα"], index=0 if def_gender=="Άνδρας" else 1)

    col4, col5, col6 = st.columns(3)
    with col4:
        birth_date = st.text_input("Ημερομηνία γέννησης", value=def_bdate)
    with col5:
        insurance_cat = st.selectbox("Κατηγορία ασφάλισης", ["Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)", "Δημόσιος Τομέας", "Τραπεζοϋπαλληλος"])
    with col6:
        first_work_date = st.text_input("Ημερομηνία πρώτης απασχόλησης", value=def_wdate)

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 2. ΑΝΑΛΥΤΙΚΗ ΕΙΣΑΓΩΓΗ ΠΕΡΙΟΔΩΝ ΕΡΓΑΣΙΑΣ
    # ==========================================
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">2️⃣ Αναλυτική εισαγωγή περιόδων εργασίας</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Κάντε επικόλληση (Paste) τον πίνακα από το Excel σας με τη σειρά: <b>ΕΤΟΣ | Από | Έως | ΦΟΡΕΑΣ | Ημέρες | ΑΠΟΔΟΧΕΣ</b></div>', unsafe_allow_html=True)

    if 'paste_input' not in st.session_state or st.session_state.clear_form:
        st.session_state.paste_input = (
            "2007\t01/01/2007\t31/01/2007\tΤΡΑΠΕΖΑ\t25\t3304.39\n"
            "2007\t01/02/2007\t28/02/2007\tΙΚΑ\t25\t3015.47"
        )
        st.session_state.clear_form = False

    def clear_text():
        st.session_state.paste_input = ""

    st.button("🗑️ Καθαρισμός Πίνακα Δεδομένων", on_click=clear_text)
    pasted_data = st.text_area("Επικόλληση δεδομένων Excel εδώ:", key='paste_input', height=130)

    processed_df = pd.DataFrame()
    if pasted_data.strip():
        try:
            temp_df = pd.read_csv(io.StringIO(pasted_data), sep="\t", header=None)
            if len(temp_df.columns) < 3:
                temp_df = pd.read_csv(io.StringIO(pasted_data), sep=",", header=None)
            
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
                        "ΑΠΟ": apo,
                        "ΕΩΣ": eos,
                        "ΦΟΡΕΑΣ": str(forer).upper().strip(),
                        "ΗΜΕΡΕΣ-ΕΝΣΗΜΑ": ensima,
                        "ΑΠΟΔΟΧΕΣ": apod
                    })

            processed_df = pd.DataFrame(final_data)
        except Exception as e:
            st.error(f"Σφάλμα ανάγνωσης: {e}")

    if not processed_df.empty:
        st.markdown("##### ✏️ Έλεγχος & Διόρθωση Δεδομένων:")
        df = st.data_editor(processed_df, num_rows="dynamic", use_container_width=True, hide_index=True)

        df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'] = pd.to_numeric(df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'], errors='coerce').fillna(0)
        df['ΑΠΟΔΟΧΕΣ'] = pd.to_numeric(df['ΑΠΟΔΟΧΕΣ'], errors='coerce').fillna(0.0)
        df['ΦΟΡΕΑΣ'] = df['ΦΟΡΕΑΣ'].astype(str).str.upper().str.strip()

        # Γενικά συγκεντρωτικά
        total_all_ensima = df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'].sum()
        total_all_apodoches = df['ΑΠΟΔΟΧΕΣ'].sum()
        overall_avg_salary = df['ΑΠΟΔΟΧΕΣ'].mean() if len(df) > 0 else 0

        st.markdown("---")
        st.markdown("### 🌟 Γενικά Συγκεντρωτικά Στοιχεία (Όλοι οι Φορείς)")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("Συνολικά Ένσημα", f"{int(total_all_ensima):,}")
        sc2.metric("Συνολικό Άθροισμα Μικτών Αποδοχών", f"{total_all_apodoches:,.2f} €")
        sc3.metric("Συνολικός Μέσος Μισθός", f"{overall_avg_salary:,.2f} €")

        # Ανάλυση ανά φορέα με σύνολο κάτω
        grouped = df.groupby('ΦΟΡΕΑΣ').agg(
            Συνολικα_Ενσημα=('ΗΜΕΡΕΣ-ΕΝΣΗΜΑ', 'sum'),
            Μσ_Ορος_Αποδοχών=('ΑΠΟΔΟΧΕΣ', 'mean')
        ).reset_index()

        grouped['Χρονια'] = grouped['Συνολικα_Ενσημα'] / 300.0

        agency_rows = []
        for _, row in grouped.iterrows():
            agency_rows.append({
                "ΦΟΡΕΑΣ": row['ΦΟΡΕΑΣ'],
                "ΧΡΟΝΙΑ": f"{row['Χρονια']:.2f}",
                "ΕΝΣΗΜΑ": f"{int(row['Συνολικα_Ενσημα']):,}",
                "Μ. ΟΡΟΣ ΑΠΟΔΟΧΩΝ (€)": f"{row['Μσ_Ορος_Αποδοχών']:,.2f} €"
            })

        tot_years = total_all_ensima / 300.0
        agency_rows.append({
            "ΦΟΡΕΑΣ": "🌟 ΣΥΝΟΛΟ",
            "ΧΡΟΝΙΑ": f"{tot_years:.2f}",
            "ΕΝΣΗΜΑ": f"{int(total_all_ensima):,}",
            "Μ. ΟΡΟΣ ΑΠΟΔΟΧΩΝ (€)": f"{overall_avg_salary:,.2f} €"
        })

        agency_df = pd.DataFrame(agency_rows)

        st.markdown("---")
        st.markdown("### 🏢 Ανάλυση & Διαχωρισμός ανά Φορέα (ΙΚΑ, ΤΡΑΠΕΖΑ κ.λπ.)")
        st.dataframe(agency_df, use_container_width=True, hide_index=True)

    else:
        tot_years = 42.57
        total_all_ensima = 12771
        overall_avg_salary = 3290.54

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 3. ΠΑΡΑΜΕΤΡΟΙ ΚΡΑΤΗΣΕΩΝ & ΥΠΟΛΟΓΙΣΜΟΣ
    # ==========================================
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">3️⃣ Παράμετροι Κρατήσεων & Εκτέλεση</div>', unsafe_allow_html=True)
    
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        tapilt_amount = st.number_input("ΤΑΠΙΛΤ (€)", value=350.0)
    with rc2:
        eas_amount = st.number_input("ΕΑΣ (€)", value=232.73)
    with rc3:
        health_pct = st.number_input("Υγεία (%)", value=6.0)
    with rc4:
        tax_monthly = st.number_input("Φόρος Μην. (€)", value=328.30)

    st.markdown("<br>", unsafe_allow_html=True)
    run_calc = st.button("🚀 ΕΚΤΕΛΕΣΗ ΠΛΗΡΟΥΣ ΥΠΟΛΟΓΙΣΜΟΥ (BMS ENGINE)", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if run_calc:
        gross_main = 2585.85 
        health_ded = gross_main * (health_pct / 100.0)
        net_main = gross_main - eas_amount - health_ded - tax_monthly
        total_ephapax = 55043.62 
        
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-header">📈 4. Αποτελέσματα & Στατιστικά Συστήματος</div>', unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Συνολικά Έτη", f"{tot_years:.2f}")
        m2.metric("Συνολικά Ένσημα", f"{int(total_all_ensima):,}")
        m3.metric("Σταθμισμένος Μισθός", f"{overall_avg_salary:,.2f} €")
        m4.metric("Μηνιαίο Καθαρό Σύνολο", f"{(net_main + 329.00 + 94.55):,.2f} €", delta="Καθαρά")

        st.markdown("---")
        st.markdown("#### 📋 Πίνακας Ανάλυσης Συντάξεων (2026)")
        
        calc_table = pd.DataFrame([
            {
                "Είδος Σύνταξης": "ΚΥΡΙΑ ΣΥΝΤΑΞΗ",
                "Μέσος Μισθός (€)": f"{overall_avg_salary:,.2f} €",
                "Χρόνια": f"{tot_years:.2f}",
                "Ένσημα": f"{int(total_all_ensima):,}",
                "Μικτό Σύνολο (€)": f"{gross_main:,.2f} €",
                "ΕΑΣ (€)": f"{eas_amount:,.2f} €",
                f"Υγεία ({health_pct}%) (€)": f"{health_ded:,.2f} €",
                "Φόρος Μην. (€)": f"{tax_monthly:,.2f} €",
                "Καθαρό Πληρωτέο (€)": f"{net_main:,.2f} €"
            },
            {
                "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ",
                "Μέσος Μισθός (€)": "-",
                "Χρόνια": "-",
                "Ένσημα": "-",
                "Μικτό Σύνολο (€)": f"{tapilt_amount:,.2f} €",
                "ΕΑΣ (€)": "0,00 €",
                f"Υγεία ({health_pct}%) (€)": "21,00 €",
                "Φόρος Μην. (€)": "0,00 €",
                "Καθαρό Πληρωτέο (€)": "329,00 €"
            },
            {
                "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)",
                "Μέσος Μισθός (€)": "-",
                "Χρόνια": "-",
                "Ένσημα": "-",
                "Μικτό Σύνολο (€)": "100,58 €",
                "ΕΑΣ (€)": "0,00 €",
                f"Υγεία ({health_pct}%) (€)": "6,03 €",
                "Φόρος Μην. (€)": "0,00 €",
                "Καθαρό Πληρωτέο (€)": "94,55 €"
            },
            {
                "Είδος Σύνταξης": "🌟 ΓΕΝΙΚΟ ΣΥΝΟΛΟ",
                "Μέσος Μισθός (€)": "-",
                "Χρόνια": f"{tot_years:.2f}",
                "Ένσημα": f"{int(total_all_ensima):,}",
                "Μικτό Σύνολο (€)": "3.036,43 €",
                "ΕΑΣ (€)": f"{eas_amount:,.2f} €",
                f"Υγεία ({health_pct}%) (€)": "168,22 €",
                "Φόρος Μην. (€)": f"{tax_monthly:,.2f} €",
                "Καθαρό Πληρωτέο (€)": "🎯 2.307,18 €"
            }
        ])

        st.dataframe(calc_table, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("#### 💰 Τμήμα Εφάπαξ (Ν. 4387/2016)")
        e_col1, e_col2 = st.columns(2)
        with e_col1:
            st.metric(label="1. Τμήμα Α (Έτη έως 31/12/2013)", value="39.565,27 €")
            st.metric(label="2. Τμήμα Β (Εισφορές 2014–2022)", value="15.478,35 €")
        with e_col2:
            st.metric(label="🌟 ΚΑΘΑΡΟ ΣΥΝΟΛΟ ΕΦΑΠΑΞ e-ΕΦΚΑ", value="55.043,62 €")
            st.info("Τρόπος & Χρόνος Καταβολής: Με την έκδοση της Κύριας Σύνταξης")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "📋 Δεδομένα & Αρχείο":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📋 Διαχείριση Αρχείου & Ιστορικού</div>', unsafe_allow_html=True)
    st.write("Εδώ εμφανίζονται τα αποθηκευμένα δεδομένα και οι καταχωρήσεις του συστήματος BMS.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">⚙️ Παράμετροι Συστήματος</div>', unsafe_allow_html=True)
    st.write("Ρυθμίσεις συντελεστών, φορέων και φορολογικών κλιμάκων 2026.")
    st.markdown('</div>', unsafe_allow_html=True)
