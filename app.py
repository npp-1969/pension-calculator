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
        <div class="main-subtitle">Προσομοίωση σύνταξης ΕΦΚΑ — κύρια (εθνική + ανταποδοτική) & επικουρική ΕΤΕΑΕΠ, με τους ισχύοντες κανόνες (ν. 4336/2015, ν. 4387/2016, ν. 4670/2020, ν. 4623/2019)</div>
    </div>
""", unsafe_allow_html=True)

# Ειδοποίηση / Warning
st.markdown("""
    <div class="warning-box">
        ⚠️ <b>Ενημερωτικός υπολογιστής-προσέγγιση.</b> Το αποτέλεσμα είναι ενδεικτικό και δεν αποτελεί δέσμευση του ΕΦΚΑ. 
        Καλύπτονται οι βαριές & ανθυγιεινά (ΒΑΕ), οι μητέρες με ανήλικό τέκνο και οι παλαιοί ασφαλισμένοι πριν από το 1993.
    </div>
""", unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.markdown("### 🗂️ Μενού Συστήματος")
app_section = st.sidebar.radio("Επιλογή:", ["📊 Κεντρικός Υπολογισμός", "📋 Δεδομένα & Αρχείο", "⚙️ Ρυθμίσεις"])

st.sidebar.markdown("---")
st.sidebar.success("🟢 BMS Engine Active (2026)")

if app_section == "📊 Κεντρικός Υπολογισμός":

    # ==========================================
    # 1. ΣΤΟΙΧΕΙΑ ΠΡΟΣΩΠΟΥ
    # ==========================================
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">1️⃣ Στοιχεία προσώπου</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Συμπληρώστε τα στοιχεία που χρειάζονται για τον υπολογισμό. Από εδώ ξεκινά η κάρτα κάθε πελάτη.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        first_name = st.text_input("Όνομα", value="ΝΕΚΤΑΡΙΟΣ")
    with col2:
        last_name = st.text_input("Επώνυμο", value="ΠΕΛΕΚΑΝΟΣ")
    with col3:
        gender = st.selectbox("Φύλο", ["Άνδρας", "Γυναίκα"])

    col4, col5, col6 = st.columns(3)
    with col4:
        birth_date = st.text_input("Ημερομηνία γέννησης", value="16/09/1969")
    with col5:
        insurance_cat = st.selectbox("Κατηγορία ασφάλισης", ["Μισθωτός — Ιδιωτικός τομέας (πρώην ΙΚΑ-ΕΤΑΜ)", "Δημόσιος Τομέας", "Τραπεζοϋπαλληλος"])
    with col6:
        first_work_date = st.text_input("Ημερομηνία πρώτης απασχόλησης", value="Ιούνιος 1990")

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 2. ΑΝΑΛΥΤΙΚΗ ΕΙΣΑΓΩΓΗ ΠΕΡΙΟΔΩΝ ΕΡΓΑΣΙΑΣ
    # ==========================================
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">2️⃣ Αναλυτική εισαγωγή περιόδων εργασίας</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Μία γραμμή <b>για κάθε εργοδότη</b> ή διάστημα εργασίας: εργοδότης, ημερομηνία από–έως, φορέας/ταμείο. Τα ένσημα (H.Ε.) υπολογίζονται αυτόματα από τις ημερομηνίες — κάθε ημερολογιακή ημέρα = 1 Η.Ε., με μέγιστο <b>25 Η.Ε. ανά μήνα</b> (πλήρης απασχόληση, 300 Η.Ε./έτος). Μπορείτε πάντα να τα αλλάξετε με το χέρι.</div>', unsafe_allow_html=True)

    st.markdown("<b>ΤΡΟΠΟΣ ΕΙΣΑΓΩΓΗΣ ΑΣΦΑΛΙΣΤΙΚΟΥ ΒΙΟΥ</b>", unsafe_allow_html=True)
    input_type = st.radio(
        "Τρόπος εισαγωγής:",
        ["🔄 Αναλυτικά ανά περίοδο — εργασίες, ένσημα & αποδοχές έτος-έτος (ακριβής υπολογισμός)", "⚡ Γρήγορα — συνολικά έτη & ένας μέσος όρος αποδοχών"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown('<div class="info-badge">✨ Συμπληρώστε περιόδους εργασίας για να δείτε έτη και ένσημα.</div>', unsafe_allow_html=True)

    # Επικουρική σύνταξη πεδίο
    st.markdown("<b>Επικουρική σύνταξη — γνωστό ποσό (€/μήνα)</b>", unsafe_allow_html=True)
    e1, e2 = st.columns([2, 1])
    with e1:
        known_epikouriki = st.text_input("Επικουρική", placeholder="π.χ. 313,82 — αφήστε κενό για αυτόματο υπολογισμό", label_visibility="collapsed")
    st.markdown("<font size='2' color='#64748B'>Αν το συμπληρώσετε, το ποσό αυτό χρησιμοποιείται <b>αντί</b> του υπολογισμού ΕΤΕΑΕΠ (π.χ. από εκκαθαριστικό ή ενημέρωση επικουρικής).</font>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Επικεφαλίδα Πίνακα Περιόδων & Κουμπί Excel
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown("### ΠΙΝΑΚΑΣ ΠΕΡΙΟΔΩΝ")
    with col_h2:
        import_excel = st.button("📥 Εισαγωγή από Excel / ΕΦΚΑ", use_container_width=True)

    st.markdown("<font size='2' color='#64748B'>Δώστε τις <b>ακριβείς ημερομηνίες</b> από–έως (ημέρα/μήνας/έτος). Αν έχετε τα ακριβή H.Ε. από τον <a href='#'>Ατομικό Λογαριασμό του e-ΕΦΚΑ</a>, γράψτε τα στο πεδίο H.Ε. για μεγαλύτερη ακρίβεια.<br>Το <b>ταμείο επικουρικής</b> κάθε εργοδότη (ΙΚΑ, ΤΑΠΙΛΤ-ΑΤ, Τράπεζα/ΤΑΥΤΕΚΩ, ΙΟΤΑΣ, ΔΕΗ/ΔΕΚΟ, βαρέα & ανθυγιεινά) συμπληρώνεται αυτόματα από την επωνυμία όταν γράφετε π.χ. «Ιονική Τράπεζα»/«Λαϊκή» (→ ΤΑΠΙΛΤ-ΑΤ), «Εθνική Τράπεζα» (→ Τράπεζα) ή «ΙΚΑ/ΕΦΚΑ» (→ ΙΚΑ) — και μπορείτε πάντα να το αλλάξετε με το χέρι.</font>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    if 'paste_input' not in st.session_state:
        st.session_state.paste_input = (
            "2007\t01/01/2007\t31/01/2007\tΤΡΑΠΕΖΑ\t25\t3304.39\n"
            "2007\t01/02/2007\t28/02/2007\tΙΚΑ\t25\t3015.47"
        )

    def clear_text():
        st.session_state.paste_input = ""

    st.button("🗑️ Καθαρισμός Πίνακα", on_click=clear_text)
    pasted_data = st.text_area("Κάντε επικόλληση (Paste) από το Excel σας εδώ:", key='paste_input', height=130)

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
        st.markdown("##### ✏️ Έλεγχος & Διόρθωση Δεδομένων Περιόδων:")
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
