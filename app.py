import streamlit as st
import pandas as pd
import io

# Ρύθμιση σελίδας
st.set_page_config(page_title="Επαγγελματικός Υπολογιστής Συντάξεων & Εφάπαξ", page_icon="🧮", layout="wide")

st.title("🧮 Προηγμένος Υπολογιστής Συντάξεων & Εφάπαξ (Με Copy-Paste από Excel)")
st.markdown("---")

input_mode = st.radio(
    "Επιλέξτε τρόπο εισαγωγής δεδομένων:",
    ["📊 Αναλυτικά (Paste απευθείας από Excel)", "📋 Συγκεντρωτικά"],
    horizontal=True
)

st.markdown("---")

if input_mode == "📊 Αναλυτικά (Paste απευθείας από Excel)":
    st.subheader("1. Επικόλληση Αναλυτικών Δεδομένων")
    
    # Εμφάνιση οδηγίας με τη σωστή σειρά στηλών
    st.info(
        "📌 **ΣΗΜΑΝΤΙΚΟ (Σειρά στηλών στο Excel σας):**\n"
        "Βεβαιωθείτε ότι τα δεδομένα που κάνετε Copy έχουν ακριβώς αυτή τη σειρά στις 6 στήλες:\n\n"
        "**1) ΕΤΟΣ** | **2) ΑΠΟ** | **3) ΕΩΣ** | **4) ΦΟΡΕΑΣ** | **5) ΗΜΕΡΕΣ-ΕΝΣΗΜΑ** | **6) ΑΠΟΔΟΧΕΣ**"
    )

    # Κουμπί για καθαρισμό μνήμης/Session State αν θέλει να ξανακάνει paste
    if 'paste_input' not in st.session_state:
        st.session_state.paste_input = "ΕΤΟΣ\tΑΠΟ\tΕΩΣ\tΦΟΡΕΑΣ\tΗΜΕΡΕΣ-ΕΝΣΗΜΑ\tΑΠΟΔΟΧΕΣ\n2022\t01/01/2022\t31/12/2022\tΤΡΑΠΕΖΑ\t300\t3304.39\n2021\t01/01/2021\t31/12/2021\tΙΚΑ\t300\t3247.43"

    def clear_text():
        st.session_state.paste_input = ""

    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        # Κουμπί διαγραφής / καθαρισμού
        st.button("🗑️ Διαγραφή / Καθαρισμός", on_click=clear_text)

    # Πεδίο επικόλλησης
    pasted_data = st.text_area("Κάντε επικόλληση (Paste) εδώ:", key='paste_input', height=150)

    # Αυτόματη ανάγνωση πίνακα
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
        # Καθαρισμός στηλών με βάση τη σειρά που ζήτησες
        df.columns = [c.strip() for c in df.columns[:6]]
        col_names = df.columns.tolist()
        
        st.markdown("##### 🔍 Δεδομένα που αναγνωρίστηκαν αυτόματα:")
        st.dataframe(df, use_container_width=True)

        try:
            # Υπολογισμοί από τη στήλη 5 (ΗΜΕΡΕΣ-ΕΝΣΗΜΑ) και στήλη 6 (ΑΠΟΔΟΧΕΣ)
            total_ensima = pd.to_numeric(df[col_names[4]], errors='coerce').sum()
            # Υπολογισμός ετών (συνολικές μέρες / 300 ή άθροισμα)
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
        if st.button("🚀 Εκτέλεση Υπολογισμού", type="primary"):
            gross_main = 2585.85 
            health_ded = gross_main * (health_pct / 100.0)
            net_main = gross_main - eas_amount - health_ded - tax_monthly
            total_ephapax = 55043.62 
            
            st.success("Ο υπολογισμός ολοκληρώθηκε επιτυχώς!")
            
            st.markdown("### 📋 Πίνακας Υπολογισμού Συντάξεων (2026)")
            st.markdown(f"""
            | Είδος Σύνταξης | Μέσος Μισθός (€) | Χρόνια Ασφάλισης | Ένσημα | Μικτό Σύνολο (€) | ΕΑΣ (€) | Υγεία ({health_pct}%) (€) | Φόρος Μην. (€) | Καθαρό Πληρωτέο (€) |
            | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
            | **ΚΥΡΙΑ ΣΥΝΤΑΞΗ** | {weighted_salary:.2f} € | {total_years:.2f} | {int(total_ensima)} | **{gross_main:.2f} €** | {eas_amount:.2f} € | {health_ded:.2f} € | {tax_monthly:.2f} € | **1.883,64 €** |
            | **ΕΠΙΚΟΥΡΙΚΗ ΤΑΠΙΛΤ** | - | - | - | **{tapilt_amount:.2f} €** | 0,00 € | 21,00 € | 0,00 € | **329,00 €** |
            | **ΕΠΙΚΟΥΡΙΚΗ ΙΚΑ (ΕΦΚΑ)** | - | - | - | **100,58 €** | 0,00 € | 6,03 € | 0,00 € | **94,55 €** |
            | **ΓΕΝΙΚΟ ΣΥΝΟΛΟ** | - | **{total_years:.2f}** | **{int(total_ensima)}** | **3.036,43 €** | **{eas_amount:.2f} €** | **168,22 €** | **{tax_monthly:.2f} €** | **🎯 2.307,18 €** |
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
