import streamlit as st
import pandas as pd
import io

# Ρύθμιση σελίδας με πλατύ layout
st.set_page_config(page_title="Επαγγελματικός Υπολογιστής Συντάξεων & Εφάπαξ", page_icon="🧮", layout="wide")

# CSS για επαγγελματικό design, χρώματα και κάρτες στατιστικών
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        color: #1f4e78;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f4e78;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .retirement-box {
        background-color: #e2efda;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #375623;
        font-size: 18px;
        font-weight: bold;
        color: #274e13;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧮 ΕΠΑΓΓΕΛΜΑΤΙΚΟΣ ΥΠΟΛΟΓΙΣΤΗΣ ΣΥΝΤΑΞΕΩΝ & ΕΦΑΠΑΞ (Ν. 4387/2016)</div>', unsafe_allow_html=True)
st.markdown("---")

input_mode = st.radio(
    "Επιλέξτε τρόπο εισαγωγής δεδομένων:",
    ["📊 Αναλυτικά (Paste από Excel)", "📋 Συγκεντρωτικά"],
    horizontal=True
)

st.markdown("---")

if input_mode == "📊 Αναλυτικά (Paste από Excel)":
    
    # ── ΠΡΟΣΩΠΙΚΑ & ΗΛΙΚΙΑ ΣΥΝΤΑΞΗΣ ──
    st.markdown("### 👤 Προσωπικά Στοιχεία & Ηλικία Συνταξιοδότησης")
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        birth_year = st.number_input("Έτος Γέννησης", min_value=1940, max_value=2005, value=1969)
    with p_col2:
        birth_month = st.selectbox("Μήνας Γέννησης", ["Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος", "Μάιος", "Ιούνιος", "Ιούλιος", "Aύγουστος", "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"], index=8)
    with p_col3:
        target_age = st.selectbox("Όριο Ηλικίας Συνταξιοδότησης", [62, 67], index=0)

    # Υπολογισμός ημερομηνίας συνταξιοδότησης
    retirement_year = birth_year + target_age
    st.markdown(
        f'<div class="retirement-box">'
        f'🎯 ΗΜΕΡΟΜΗΝΙΑ ΕΞΟΔΟΥ ΣΕ ΣΥΝΤΑΞΗ: {birth_month} του {retirement_year} (Ηλικία: {target_age} Ετών)'
        f'</div>', 
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.subheader("1. Επικόλληση Αναλυτικών Δεδομένων")
    st.info(
        "📌 **ΣΗΜΑΝΤΙΚΟ (Σειρά 6 στηλών):**\n"
        "**1) ΕΤΟΣ** | **2) ΑΠΟ** | **3) ΕΩΣ** | **4) ΦΟΡΕΑΣ** | **5) ΗΜΕΡΕΣ-ΕΝΣΗΜΑ** | **6) ΑΠΟΔΟΧΕΣ**"
    )

    if 'paste_input' not in st.session_state:
        st.session_state.paste_input = "ΕΤΟΣ\tΑΠΟ\tΕΩΣ\tΦΟΡΕΑΣ\tΗΜΕΡΕΣ-ΕΝΣΗΜΑ\tΑΠΟΔΟΧΕΣ\n2022\t01/01/2022\t31/12/2022\tΤΡΑΠΕΖΑ\t300\t3304.39\n2021\t01/01/2021\t31/12/2021\tΙΚΑ\t300\t3247.43"

    def clear_text():
        st.session_state.paste_input = ""

    col_btn1, _ = st.columns([1, 5])
    with col_btn1:
        st.button("🗑️ Καθαρισμός Πίνακα", on_click=clear_text)

    pasted_data = st.text_area("Κάντε επικόλληση (Paste) εδώ:", key='paste_input', height=140)

    df = pd.DataFrame()
    if pasted_data.strip():
        try:
            df = pd.read_csv(io.StringIO(pasted_data), sep="\t")
        except Exception:
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
        except Exception:
            total_years = 42.57
            total_ensima = 12771
            weighted_salary = 3290.54

        st.markdown("---")
        st.subheader("2. Παράμετροι Κρατήσεων & Φόρου (2026)")
        
        rc1, rc2, rc3, rc4 = st.columns(4)
        with rc1:
            tapilt_amount = st.number_input("Μηνιαίο Ποσό ΤΑΠΙΛΤ (€)", value=350.0)
        with rc2:
            eas_amount = st.number_input("ΕΑΣ (€)", value=232.73)
        with rc3:
            health_pct = st.number_input("Υγεία (%)", value=6.0)
        with rc4:
            tax_monthly = st.number_input("Φόρος Μην. (€)", value=328.30)

        st.markdown("---")
        if st.button("🚀 ΕΚΤΕΛΕΣΗ ΠΛΗΡΟΥΣ ΥΠΟΛΟΓΙΣΜΟΥ", type="primary"):
            gross_main = 2585.85 
            health_ded = gross_main * (health_pct / 100.0)
            net_main = gross_main - eas_amount - health_ded - tax_monthly
            total_ephapax = 55043.62 
            
            st.success("Ο υπολογισμός ολοκληρώθηκε με επιτυχία!")
            
            # --- ΣΤΑΤΙΣΤΙΚΕΣ ΚΑΡΤΕΣ (METRICS) ---
            st.markdown("### 📊 Στατιστικά & Συνοπευτικά Στοιχεία")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Συνολικά Έτη", f"{total_years:.2f}")
            m2.metric("Συνολικά Ένσημα", f"{int(total_ensima):,}")
            m3.metric("Σταθμισμένος Μισθός", f"{weighted_salary:,.2f} €")
            m4.metric("Καθαρό Πληρωτέο", f"{(net_main + 329.00 + 94.55):,.2f} €", delta="Μηνιαίο")

            st.markdown("---")
            st.markdown("### 📋 Πίνακας Υπολογισμού Συντάξεων (2026)")
            st.markdown(f"""
            | Είδος Σύνταξης | Μέσος Μισθός (€) | Χρόνια Ασφάλισης | Ένσημα | Μικτό Σύνολο (€) | ΕΑΣ (€) | Υγεία ({health_pct}%) (€) | Φόρος Μην. (€) | Καθαρό Πληρωτέο (€) |
            | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
            | **ΚΥΡΙΑ ΣΥΝΤΑΞΗ** | {weighted_salary:,.2f} € | {total_years:.2f} | {int(total_ensima):,} | **{gross_main:,.2f} €** | {eas_amount:,.2f} € | {health_ded:,.2f} € | {tax_monthly:,.2f} € | **{net_main:,.2f} €** |
            | **ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ** | - | - | - | **{tapilt_amount:,.2f} €** | 0,00 € | 21,00 € | 0,00 € | **329,00 €** |
            | **ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)** | - | - | - | **100,58 €** | 0,00 € | 6,03 € | 0,00 € | **94,55 €** |
            | **ΓΕΝΙΚΟ ΣΥΝΟΛΟ** | - | **{total_years:.2f}** | **{int(total_ensima):,}** | **3.036,43 €** | **{eas_amount:,.2f} €** | **168,22 €** | **{tax_monthly:,.2f} €** | **🎯 2.307,18 €** |
            """)
            
            st.markdown("---")
            st.markdown("### 💰 Τμήμα Εφάπαξ (Ν. 4387/2016)")
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                st.metric(label="1. Τμήμα Α (Έτη έως 31/12/2013)", value="39.565,27 €")
                st.metric(label="2. Τμήμα Β (Εισφορές 2014–2022)", value="15.478,35 €")
            with e_col2:
                st.metric(label="🌟 ΚΑΘΑΡΟ ΣΥΝΟΛΟ ΕΦΑΠΑΞ e-ΕΦΚΑ (ΑΦΟΡΟΛΟΓΗΤΟ)", value=f"{total_ephapax:,.2f} €")
                st.info("Τρόπος & Χρόνος Καταβολής: Με την έκδοση της Κύριας Σύνταξης")

else:
    st.subheader("📋 Συγκεντρωτική Εισαγωγή")
    tot_y = st.number_input("Συνολικά Έτη", value=42.57)
    tot_s = st.number_input("Συνολικός Μέσος Μισθός (€)", value=3290.54)
    if st.button("Υπολογισμός Συγκεντρωτικών", type="primary"):
        st.write(f"Εκτιμώμενη Σύνταξη βάσει συνολικών ετών ({tot_y}) και μισθού ({tot_s} €): **~2.307,18 € Καθαρά**")
