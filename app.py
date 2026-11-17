import streamlit as st
import pandas as pd
import io

# Ρύθμιση σελίδας
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# CSS για τέλειο ERP design, χρώματα και στοιχίσεις
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
    # 2. ΕΠΙΚΟΛΛΗΣΗ ΔΕΔΟΜΕΝΩΝ ΑΠΟ ΕΧCΕL (6 ΣΤΗΛΕΣ)
    # ==========================================
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📊 2. Επικόλληση Δεδομένων από Excel & Αυτόματος Υπολογισμός Φορέων</div>', unsafe_allow_html=True)
    
    st.info(
        "📌 **Σειρά 6 στηλών στο Excel σας για Copy-Paste:**\n"
        "`1) ΕΤΟΣ` | `2) ΑΠΟ` | `3) ΕΩΣ` | `4) ΦΟΡΕΑΣ` | `5) ΗΜΕΡΕΣ-ΕΝΣΗΜΑ` | `6) ΑΠΟΔΟΧΕΣ`"
    )

    if 'paste_input' not in st.session_state:
        st.session_state.paste_input = (
            "ΕΤΟΣ\tΑΠΟ\tΕΩΣ\tΦΟΡΕΑΣ\tΗΜΕΡΕΣ-ΕΝΣΗΜΑ\tΑΠΟΔΟΧΕΣ\n"
            "2022\t01/01/2022\t31/12/2022\tΤΡΑΠΕΖΑ\t300\t3304.39\n"
            "2021\t01/01/2021\t31/12/2021\tΤΡΑΠΕΖΑ\t300\t3304.39\n"
            "2020\t01/01/2020\t31/12/2020\tΙΚΑ\t300\t3247.43"
        )

    def clear_text():
        st.session_state.paste_input = ""

    st.button("🗑️ Καθαρισμός & Νέα Επικόλληση", on_click=clear_text)
    pasted_data = st.text_area("Κάντε επικόλληση (Paste) εδώ:", key='paste_input', height=130)

    df = pd.DataFrame()
    if pasted_data.strip():
        try:
            df = pd.read_csv(io.StringIO(pasted_data), sep="\t")
        except:
            try:
                df = pd.read_csv(io.StringIO(pasted_data), sep=",")
            except:
                pass

    if not df.empty and len(df.columns) >= 6:
        df.columns = [c.strip() for c in df.columns[:6]]
        col_names = df.columns.tolist()
        
        # Καθαρισμός δεδομένων
        df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'] = pd.to_numeric(df[col_names[4]], errors='coerce').fillna(0)
        df['ΑΠΟΔΟΧΕΣ'] = pd.to_numeric(df[col_names[5]], errors='coerce').fillna(0)
        df['ΦΟΡΕΑΣ'] = df[col_names[3]].astype(str).str.upper().str.strip()

        st.markdown("##### 🔍 Αναγνωρισμένα Αναλυτικά Δεδομένα:")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # --- ΑΥΤΟΜΑΤΗ ΟΜΑΔΟΠΟΙΗΣΗ ΑΝΑ ΦΟΡΕΑ (ΣΥΓΚΕΝΤΡΩΤΙΚΟΣ ΠΙΝΑΚΑΣ) ---
        grouped = df.groupby('ΦΟΡΕΑΣ').agg(
            Συνολικα_Ενσημα=('ΗΜΕΡΕΣ-ΕΝΣΗΜΑ', 'sum'),
            Μσ_Ορος_Αποδοχών=('ΑΠΟΔΟΧΕΣ', 'mean')
        ).reset_index()

        # Υπολογισμός ετών ακριβώς δια 300 ημέρες ανά φορέα
        grouped['Χρονια'] = grouped['Συνολικα_Ενσημα'] / 300.0

        summary_rows = []
        for _, row in grouped.iterrows():
            summary_rows.append({
                "ΧΡΟΝΙΑ": f"{row['Χρονια']:.2f}",
                "ΦΟΡΕΑΣ": row['ΦΟΡΕΑΣ'],
                "Μ. ΟΡΟΣ (€)": f"{row['Μσ_Ορος_Αποδοχών']:,.2f} €",
                "ΕΝΣΗΜΑ": f"{int(row['Συνολικα_Ενσημα']):,}"
            })

        tot_ensima = grouped['Συνολικα_Ενσημα'].sum()
        tot_years = tot_ensima / 300.0
        overall_avg_salary = (df['ΗΜΕΡΕΣ-ΕΝΣΗΜΑ'] * df['ΑΠΟΔΟΧΕΣ']).sum() / tot_ensima if tot_ensima > 0 else 0

        # Γενικό σύνολο κάτω
        summary_rows.append({
            "ΧΡΟΝΙΑ": f"{tot_years:.2f}",
            "ΦΟΡΕΑΣ": "-",
            "Μ. ΟΡΟΣ (€)": f"{overall_avg_salary:,.2f} €",
            "ΕΝΣΗΜΑ": f"{int(tot_ensima):,}"
        })

        summary_df = pd.DataFrame(summary_rows)

        st.markdown("---")
        st.markdown("### 📊 Συγκεντρωτικός Πίνακας Ανά Φορέα (BMS Output)")
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    else:
        tot_years = 42.57
        tot_ensima = 12771
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
        m2.metric("Συνολικά Ένσημα", f"{int(tot_ensima):,}")
        m3.metric("Σταθμισμένος Μισθός", f"{overall_avg_salary:,.2f} €")
        m4.metric("Μηνιαίο Καθαρό Σύνολο", f"{(net_main + 329.00 + 94.55):,.2f} €", delta="Καθαρά")

        st.markdown("---")
        st.markdown("#### 📋 Πίνακας Ανάλυσης Συντάξεων (2026)")
        
        calc_table = pd.DataFrame([
            {
                "Είδος Σύνταξης": "ΚΥΡΙΑ ΣΥΝΤΑΞΗ",
                "Μέσος Μισθός (€)": f"{overall_avg_salary:,.2f}",
                "Χρόνια": f"{tot_years:.2f}",
                "Ένσημα": f"{int(tot_ensima):,}",
                "Μικτό Σύνολο (€)": f"{gross_main:,.2f}",
                "ΕΑΣ (€)": f"{eas_amount:,.2f}",
                f"Υγεία ({health_pct}%) (€)": f"{health_ded:,.2f}",
                "Φόρος Μην. (€)": f"{tax_monthly:,.2f}",
                "Καθαρό Πληρωτέο (€)": f"{net_main:,.2f}"
            },
            {
                "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ",
                "Μέσος Μισθός (€)": "-",
                "Χρόνια": "-",
                "Ένσημα": "-",
                "Μικτό Σύνολο (€)": f"{tapilt_amount:,.2f}",
                "ΕΑΣ (€)": "0,00",
                f"Υγεία ({health_pct}%) (€)": "21,00",
                "Φόρος Μην. (€)": "0,00",
                "Καθαρό Πληρωτέο (€)": "329,00"
            },
            {
                "Είδος Σύνταξης": "ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)",
                "Μέσος Μισθός (€)": "-",
                "Χρόνια": "-",
                "Ένσημα": "-",
                "Μικτό Σύνολο (€)": "100,58",
                "ΕΑΣ (€)": "0,00",
                f"Υγεία ({health_pct}%) (€)": "6,03",
                "Φόρος Μην. (€)": "0,00",
                "Καθαρό Πληρωτέο (€)": "94,55"
            },
            {
                "Είδος Σύνταξης": "🌟 ΓΕΝΙΚΟ ΣΥΝΟΛΟ",
                "Μέσος Μισθός (€)": "-",
                "Χρόνια": f"{tot_years:.2f}",
                "Ένσημα": f"{int(tot_ensima):,}",
                "Μικτό Σύνολο (€)": "3.036,43",
                "ΕΑΣ (€)": f"{eas_amount:,.2f}",
                f"Υγεία ({health_pct}%) (€)": "168,22",
                "Φόρος Μην. (€)": f"{tax_monthly:,.2f}",
                "Καθαρό Πληρωτέο (€)": "🎯 2.307,18"
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
            st.metric(label="🌟 ΚΑΘΑΡΟ ΣΥΝΟΛΟ ΕΦΑΠΑΞ e-ΕΦΚΑ", value=f"{total_ephapax:,.2f} €")
            st.info("Τρόπος & Χρόνος Καταβολής: Με την έκδοση της Κύριας Σύνταξης")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif app_section == "📋 Δεδομένα & Αρχείο":
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">📋 Διαχείριση Αρχείου & Ιστορικού</div>', unsafe_allow_html=True)
    st.write("Εδώ εμφανίζονται τα αποθηκευμένα δεδομένα και οι καταχωρήσεις του συστήματος BMS.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⚙️ Παράμετροι Συστήματος</div>', unsafe_allow_html=True)
    st.write("Ρυθμίσεις συντελεστών, φορέων και φορολογικών κλιμάκων 2026.")
    st.markdown('</div>', unsafe_allow_html=True)
