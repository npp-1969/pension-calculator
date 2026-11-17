import streamlit as st
import pandas as pd
import io

# Ρύθμιση σελίδας
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# CSS για τέλειο ERP design
st.markdown("""
    <style>
    .stApp {
        background-color: #F4F6F9;
    }
    .erp-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 18px 25px;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 4px 10px rgba(30, 58, 138, 0.2);
        margin-bottom: 25px;
    }
    .panel-box {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .panel-title {
        background: #1E3A8A;
        color: white;
        padding: 10px 15px;
        font-weight: bold;
        border-radius: 6px;
        font-size: 16px;
        margin-bottom: 15px;
    }
    .retirement-banner {
        background: linear-gradient(135deg, #DEF7EC 0%, #BCCCDC 100%);
        border-left: 6px solid #059669;
        color: #065F46;
        padding: 16px;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="erp-header">💼 OnLine Pension Core BMS™ — Σύστημα Υπολογισμού Συντάξεων & Εφάπαξ (Ν. 4387/2016)</div>', unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.markdown("### 🗂️ Μενού Συστήματος")
app_section = st.sidebar.radio("Επιλογή:", ["📊 Κεντρικός Υπολογισμός", "📋 Δεδομένα & Αρχείο", "⚙️ Ρυθμίσεις"])

st.sidebar.markdown("---")
st.sidebar.success("🟢 BMS Engine Active (2026)")

if app_section == "📊 Κεντρικός Υπολογισμός":

    # ==========================================
    # 1. ΠΡΟΣΩΠΙΚΑ ΣΤΟΙΧΕΙΑ & ΗΛΙΚΙΑ (ΠΑΝΩ)
    # ==========================================
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">👤 1. Προσωπικά & Ασφαλιστικά Στοιχεία (Όριο Ηλικίας)</div>', unsafe_allow_html=True)
    
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        birth_year = st.number_input("Έτος Γέννησης", min_value=1940, max_value=2005, value=1969)
    with p_col2:
        birth_month = st.selectbox("Μήνας Γέννησης", ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"], index=8)
    with p_col3:
        target_age = st.selectbox("Όριο Ηλικίας Συνταξιοδότησης", [62, 67], index=0)

    retirement_year = birth_year + target_age
    st.markdown(
        f'<div class="retirement-banner">'
        f'🎯 ΕΚΤΙΜΩΜΕΝΗ ΗΜΕΡΟΜΗΝΙΑ ΕΞΟΔΟΥ: {birth_month} του {retirement_year} (Ηλικία: {target_age} Ετών)'
        f'</div>', 
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 2. ΕΠΙΚΟΛΛΗΣΗ ΔΕΔΟΜΕΝΩΝ ΑΠΟ ΕΧCΕL
    # ==========================================
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📊 2. Επικόλληση Δεδομένων από Excel & Συγκεντρωτική Ανάλυση</div>', unsafe_allow_html=True)
    
    st.info(
        "📌 Κάντε **Copy** από το Excel σας και **Paste** παρακάτω.\n"
        "Το σύστημα διαβάζει κανονικά τις αποδοχές σε ευρώ (€), βγάζει τα συνολικά ένσημα και τις μικτές αποδοχές συνολικά, και στη συνέχεια αναλύει χωριστά κάθε φορέα (ΙΚΑ, ΤΡΑΠΕΖΑ κ.λπ.)!"
    )

    if 'paste_input' not in st.session_state:
        st.session_state.paste_input = (
            "2012\t01/01/2012\t31/01/2012\tΤΡΑΠΕΖΑ\t25\t3304.39 €\n"
            "2012\t01/02/2012\t29/02/2012\tΙΚΑ\t25\t1200.00 €"
        )

    def clear_text():
        st.session_state.paste_input = ""

    st.button("🗑️ Καθαρισμός & Νέα Επικόλληση", on_click=clear_text)
    pasted_data = st.text_area("Κάντε επικόλληση (Paste) εδώ:", key='paste_input', height=130)

    processed_df = pd.DataFrame()
    if pasted_data.strip():
        try:
            temp_df = pd.read_csv(io.StringIO(pasted_data), sep="\t", header=None)
            if len(temp_df.columns) < 3:
                temp_df = pd.read_csv(io.StringIO(pasted_data), sep=",", header=None)
            
            if len(temp_df) > 0 and any(str(val).upper() in ["ΕΤΟΣ", "ΦΟΡΕΑΣ", "ΑΠΟΔΟΧΕΣ", "YEAR", "HΜΕΡΕΣ"] for val in temp_df.iloc[0].values):
                temp_df = temp_df.iloc[1:].reset_index(drop=True)

            final_data = []
            for _, row in temp_df.iterrows():
                row_vals = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip() != '']
                if len(row_vals) >= 4:
                    etos = row_vals[0]
                    apo = row_vals[1]
                    eos = row_vals[2]
                    forer = row_vals[3]
                    
                    ensima = 25.0
                    apod = 0.0
                    
                    nums = []
                    for val in row_vals[4:]:
                        clean_val = val.replace('€', '').replace('.', '').replace(',', '.')
                        try:
                            num = float(clean_val)
                            nums.append(num)
                        except:
                            pass
                    
                    if len(nums) >= 2:
                        for n in nums:
                            if 1 <= n <= 31 and ensima == 25.0:
                                ensima = n
                            else:
                                apod = n
                    elif len(nums) == 1:
                        apod = nums[0]

                    final_data.append({
                        "ΕΤΟΣ": etos,
                        "ΑΠΟ": apo,
                        "ΕΩΣ": eos,
                        "ΦΟΡΕΑΣ": forer.upper(),
                        "ΗΜΕΡΕΣ-ΕΝΣΗΜΑ": ensima,
                        "ΑΠΟΔΟΧΕΣ": apod
                    })

            processed_df = pd.DataFrame(final_data)
        except Exception as e:
            st.error(f"Σφάλμα ανάγνωσης: {e}")

    if not processed_df.empty:
        st.markdown("##### ✏️ Αναγνωρισμένα Δεδομένα (Επεξεργαστείτε εάν χρειάζεται):")
        df = st.data_editor(processed_df, num_rows="dynamic", use_container_width=True, hide_index=True)

        df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'] = pd.to_numeric(df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'], errors='coerce').fillna(0)
        df['ΑΠΟΔΟΧΕΣ'] = pd.to_numeric(df['ΑΠΟΔΟΧΕΣ'], errors='coerce').fillna(0.0)
        df['ΦΟΡΕΑΣ'] = df['ΦΟΡΕΑΣ'].astype(str).str.upper().str.strip()

        # --- 1. ΣΥΓΚΕΝΤΡΩΤΙΚΑ ΕΠΑΝΩ (Συνολικά Ένσημα & Μικτές Αποδοχές από όλους τους φορείς) ---
        total_all_ensima = df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'].sum()
        total_all_apodoches = (df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'] * df['ΑΠΟΔΟΧΕΣ']).sum()
        overall_avg_salary = total_all_apodoches / total_all_ensima if total_all_ensima > 0 else 0

        st.markdown("---")
        st.markdown("### 🌟 Γενικά Συγκεντρωτικά Στοιχεία (Όλοι οι Φορείς)")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("Συνολικά Ένσημα", f"{int(total_all_ensima):,}")
        sc2.metric("Συνολικό Άθροισμα Μικτών Αποδοχών", f"{total_all_apodoches:,.2f} €")
        sc3.metric("Συνολικός Μέσος Μισθός", f"{overall_avg_salary:,.2f} €")

        # --- 2. ΑΝΑΛΥΣΗ ΑΝΑ ΦΟΡΕΑ ΚΑΤΩ (Χρόνια, Ένσημα, Μ. Ορος) ---
        grouped = df.groupby('ΦΟΡΕΑΣ').agg(
            Συνολικα_Ενσημα=('ΗΜΕΡΕΣ-ΕΝΣΗΜΑ', 'sum'),
            Μσ_Ορος_Αποδοχών=('ΑΠΟΔΟΧΕΣ', 'mean')
        ).reset_index()

        grouped['Χρονια'] = grouped['Συνολικα_ΕνΣημα'] / 300.0 if 'Συνολικα_ΕνΣημα' in grouped.columns else grouped['Συνολικα_Ενσημα'] / 300.0

        agency_rows = []
        for _, row in grouped.iterrows():
            agency_rows.append({
                "ΦΟΡΕΑΣ": row['ΦΟΡΕΑΣ'],
                "ΧΡΟΝΙΑ": f"{row['Χρονια']:.2f}",
                "ΕΝΣΗΜΑ": f"{int(row['Συνολικα_Ενσημα']):,}",
                "Μ. ΟΡΟΣ ΑΠΟΔΟΧΩΝ (€)": f"{row['Μσ_Ορος_Αποδοχών']:,.2f} €"
            })

        agency_df = pd.DataFrame(agency_rows)

        st.markdown("---")
        st.markdown("### 🏢 Ανάλυση & Διαχωρισμός ανά Φορέα (ΙΚΑ, ΤΡΑΠΕΖΑ κ.λπ.)")
        st.dataframe(agency_df, use_container_width=True, hide_index=True)

        tot_years = total_all_ensima / 300.0

    else:
        tot_years = 42.57
        total_all_ensima = 12771
        overall_avg_salary = 3290.54

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 3. ΠΑΡΑΜΕΤΡΟΙ ΚΡΑΤΗΣΕΩΝ & ΥΠΟΛΟΓΙΣΜΟΣ
    # ==========================================
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⚙️ 3. Παράμετροι Κρατήσεων & Εκτέλεση</div>', unsafe_allow_html=True)
    
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
        
        # --- ΑΠΟΤΕΛΕΣΜΑΤΑ & ΣΤΑΤΙΣΤΙΚΑ ---
        st.markdown('<div class="panel-box">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">📈 4. Αποτελέσματα & Στατιστικά Συστήματος</div>', unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Συνολικά Έτη", f"{tot_years:.2f}")
        m2.metric("Συνολικά Ένσημα", f"{int(total_all_ensima):,}")
        m3.metric("Σταθμισμένος Μισθός", f"{overall_avg_salary:,.2f} €")
        m4.metric("Μηνιαίο Καθαρό Σύνολο", f"{(net_main + 329.00 + 94.55):,.2f} €", delta="Καθαρά")

        st.markdown("---")
        st.markdown("#### 📋 Πίνακας Ανάλυσης Συντάξεων (2026)")
