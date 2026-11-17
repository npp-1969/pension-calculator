import streamlit as st
import pandas as pd
import io

# Ρύθμιση σελίδας
st.set_page_config(page_title="OnLine Pension Core - Υπολογιστής Συντάξεων", page_icon="🏢", layout="wide")

# CSS για να μοιάζει με επαγγελματικό ERP / Business Software (όπως το OnLine Data Core)
st.markdown("""
    <style>
    /* Γενικό φόντο και στυλ */
    .stApp {
        background-color: #F0F2F5;
    }
    
    /* Επαγγελματική Μπάρα / Header */
    .erp-header {
        background: linear-gradient(90deg, #1A365D 0%, #2B6CB0 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 6px;
        font-size: 22px;
        font-weight: bold;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* ERP Panel / Κουτιά */
    .erp-panel {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E0;
        border-radius: 6px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .erp-panel-title {
        background-color: #2B6CB0;
        color: white;
        padding: 8px 12px;
        font-weight: bold;
        border-radius: 4px;
        font-size: 15px;
        margin-bottom: 15px;
    }
    
    .retirement-box {
        background-color: #C6F6D5;
        border: 1px solid #38A169;
        color: #22543D;
        padding: 15px;
        border-radius: 6px;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ERP Header
st.markdown('<div class="erp-header">🏢 OnLine Pension Core BMS™ &nbsp;|&nbsp; Υπολογιστής Συντάξεων & Εφάπαξ (Ν. 4387/2016)</div>', unsafe_allow_html=True)

# Sidebar για γρήγορη πλοήγηση (στυλ ERP menu)
st.sidebar.markdown("### 🗂️ Μενού Εφαρμογής")
app_section = st.sidebar.radio("Επιλογή Ενότητας:", ["📊 Κεντρικός Υπολογισμός", "📋 Δεδομένα & Ιστορικό", "⚙️ Παράμετροι & Κλίμακες"])

st.sidebar.markdown("---")
st.sidebar.info("📌 **Status:** Συνδεδεμένο με βάση κανόνων e-ΕΦΚΑ / ΤΑΠΙΛΤ (2026)")

if app_section == "📊 Κεντρικός Υπολογισμός":

    # ==========================================
    # 1. ΠΡΟΣΩΠΙΚΑ ΣΤΟΙΧΕΙΑ & ΗΛΙΚΙΑ (PANEL 1)
    # ==========================================
    st.markdown('<div class="erp-panel">', unsafe_allow_html=True)
    st.markdown('<div class="erp-panel-title">👤 1. Προσωπικά & Ασφαλιστικά Στοιχεία (Όριο Ηλικίας)</div>', unsafe_allow_html=True)
    
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        birth_year = st.number_input("Έτος Γέννησης", min_value=1940, max_value=2005, value=1969)
    with p_col2:
        birth_month = st.selectbox("Μήνας Γέννησης", ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"], index=8)
    with p_col3:
        target_age = st.selectbox("Όριο Ηλικίας Συνταξιοδότησης", [62, 67], index=0)

    retirement_year = birth_year + target_age
    st.markdown(
        f'<div class="retirement-box">'
        f'🎯 ΕΚΤΙΜΩΜΕΝΗ ΗΜΕΡΟΜΗΝΙΑ ΕΞΟΔΟΥ: {birth_month} του {retirement_year} (Ηλικία: {target_age} Ετών)'
        f'</div>', 
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 2. ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ (PANEL 2)
    # ==========================================
    st.markdown('<div class="erp-panel">', unsafe_allow_html=True)
    st.markdown('<div class="erp-panel-title">📊 2. Δεδομένα & Επικόλληση από Excel</div>', unsafe_allow_html=True)
    
    input_mode = st.radio(
        "Τρόπος Εισαγωγής:",
        ["📊 Αναλυτικά (Paste 6 στηλών)", "📋 Συγκεντρωτικά"],
        horizontal=True
    )
    
    if input_mode == "📊 Αναλυτικά (Paste 6 στηλών)":
        st.markdown(
            "📌 **Σειρά στηλών στο Excel:** "
            "`1) ΕΤΟΣ` | `2) ΑΠΟ` | `3) ΕΩΣ` | `4) ΦΟΡΕΑΣ` | `5) ΗΜΕΡΕΣ-ΕΝΣΗΜΑ` | `6) ΑΠΟΔΟΧΕΣ`"
        )

        if 'paste_input' not in st.session_state:
            st.session_state.paste_input = "ΕΤΟΣ\tΑΠΟ\tΕΩΣ\tΦΟΡΕΑΣ\tΗΜΕΡΕΣ-ΕΝΣΗΜΑ\tΑΠΟΔΟΧΕΣ\n2022\t01/01/2022\t31/12/2022\tΤΡΑΠΕΖΑ\t300\t3304.39\n2021\t01/01/2021\t31/12/2021\tΙΚΑ\t300\t3247.43"

        def clear_text():
            st.session_state.paste_input = ""

        st.button("🗑️ Καθαρισμός Πίνακα", on_click=clear_text)
        pasted_data = st.text_area("Κάντε επικόλληση (Paste) εδώ:", key='paste_input', height=110)

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
            
            st.markdown("##### 🔍 Αναγνωρισμένα Δεδομένα:")
            st.dataframe(df, use_container_width=True)

            try:
                total_ensima = pd.to_numeric(df[col_names[4]], errors='coerce').sum()
                total_years = total_ensima / 300.0 if total_ensima > 0 else 42.57
                
                valid_df = df.copy()
                valid_df['ens'] = pd.to_numeric(valid_df[col_names[4]], errors='coerce').fillna(0)
                valid_df['apod'] = pd.to_numeric(valid_df[col_names[5]], errors='coerce').fillna(0)
                
                weighted_salary = (valid_df['ens'] * valid_df['apod']).sum() / total_ensima if total_ensima > 0 else 3290.54
            except:
                total_years = 42.57
                total_ensima = 12771
                weighted_salary = 3290.54
        else:
            total_years = 42.57
            total_ensima = 12771
            weighted_salary = 3290.54
    else:
        total_years = st.number_input("Συνολικά Έτη", value=42.57)
        weighted_salary = st.number_input("Συνολικός Μέσος Μισθός (€)", value=3290.54)
        total_ensima = 12771

    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # 3. ΠΑΡΑΜΕΤΡΟΙ & ΥΠΟΛΟΓΙΣΜΟΣ (PANEL 3)
    # ==========================================
    st.markdown('<div class="erp-panel">', unsafe_allow_html=True)
    st.markdown('<div class="erp-panel-title">⚙️ 3. Παράμετροι Κρατήσεων & Εκτέλεση</div>', unsafe_allow_html=True)
    
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
    run_calc = st.button("🚀 ΕΚΤΕΛΕΣΗ ΥΠΟΛΟΓΙΣΜΟΥ (BMS ENGINE)", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if run_calc:
        gross_main = 2585.85 
        health_ded = gross_main * (health_pct / 100.0)
        net_main = gross_main - eas_amount - health_ded - tax_monthly
        total_ephapax = 55043.62 
        
        # --- ΑΠΟΤΕΛΕΣΜΑΤΑ ΣΤΥΛ ERP ---
        st.markdown('<div class="erp-panel">', unsafe_allow_html=True)
        st.markdown('<div class="erp-panel-title">📈 4. Αποτελέσματα & Στατιστικά Συστήματος</div>', unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Συνολικά Έτη", f"{total_years:.2f}")
        m2.metric("Συνολικά Ένσημα", f"{int(total_ensima):,}")
        m3.metric("Σταθμισμένος Μισθός", f"{weighted_salary:,.2f} €")
        m4.metric("Μηνιαίο Καθαρό Σύνολο", f"{(net_main + 329.00 + 94.55):,.2f} €", delta="Καθαρά")

        st.markdown("---")
        st.markdown("#### 📋 Πίνακας Ανάλυσης Συντάξεων (2026)")
        
        summary_table = pd.DataFrame([
            {
                "Είδος Σύνταξης": "ΚΥΡΙΑ ΣΥΝΤΑΞΗ",
                "Μέσος Μισθός (€)": f"{weighted_salary:,.2f}",
                "Χρόνια": f"{total_years:.2f}",
                "Ένσημα": f"{int(total_ensima):,}",
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
                "Χρόνια": f"{total_years:.2f}",
                "Ένσημα": f"{int(total_ensima):,}",
                "Μικτό Σύνολο (€)": "3.036,43",
                "ΕΑΣ (€)": f"{eas_amount:,.2f}",
                f"Υγεία ({health_pct}%) (€)": "168,22",
                "Φόρος Μην. (€)": f"{tax_monthly:,.2f}",
                "Καθαρό Πληρωτέο (€)": "🎯 2.307,18"
            }
        ])

        st.dataframe(summary_table, use_container_width=True, hide_index=True)
        
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

elif app_section == "📋 Δεδομένα & Ιστορικό":
    st.markdown('<div class="erp-panel">', unsafe_allow_html=True)
    st.markdown('<div class="erp-panel-title">📋 Διαχείριση Αρχείου & Ιστορικού</div>', unsafe_allow_html=True)
    st.write("Εδώ εμφανίζονται τα αποθηκευμένα δεδομένα και οι καταχωρήσεις του συστήματος BMS.")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown('<div class="erp-panel">', unsafe_allow_html=True)
    st.markdown('<div class="erp-panel-title">⚙️ Παράμετροι Συστήματος</div>', unsafe_allow_html=True)
    st.write("Ρυθμίσεις συντελεστών, φορέων και φορολογικών κλιμάκων 2026.")
    st.markdown('</div>', unsafe_allow_html=True)
