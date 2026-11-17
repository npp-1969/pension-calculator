import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(page_title="Επαγγελματικός Υπολογιστής Συντάξεων & Εφάπαξ", page_icon="🧮", layout="centered")

st.title("🧮 Υπολογιστής Συντάξεων & Εφάπαξ (Ν. 4387/2016)")
st.markdown("---")
st.write("Συμπληρώστε τα στοιχεία σας για να υπολογίσετε την Κύρια Σύνταξη, την Επικουρική και το Εφάπαξ.")

# --- ΕΝΟΤΗΤΑ 1: ΠΡΟΣΩΠΙΚΑ & ΑΣΦΑΛΙΣΤΙΚΑ ΣΤΟΙΧΕΙΑ ---
st.header("1. Προσωπικά & Ασφαλιστικά Στοιχεία")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Φύλο", ["Άνδρας", "Γυναίκα"])
    birth_year = st.number_input("Έτος Γέννησης", min_value=1940, max_value=2005, value=1975)
with col2:
    insurance_type = st.selectbox("Πρώτη Ασφάλιση", ["Παλαιός (έως 31/12/1992)", "Νέος (από 1/1/1993 και μετά)"])
    fund = st.selectbox("Ταμείο Κύριας Ασφάλισης", ["ΙΚΑ / e-ΕΦΚΑ Μισθωτών", "Δημόσιο", "Τράπεζες (π.χ. Ιονική/Alpha)", "ΟΑΕΕ / Ελευθεροι Επαγγελματίες"])

# --- ΕΝΟΤΗΤΑ 2: ΧΡΟΝΟΣ & ΑΠΟΔΟΧΕΣ ---
st.header("2. Χρόνος Ασφάλισης & Αποδοχές")

col3, col4 = st.columns(2)
with col3:
    total_years = st.number_input("Συνολικά Έτη Ασφάλισης", min_value=1, max_value=50, value=30)
with col4:
    avg_salary = st.number_input("Μέσος Όρος Μηνιαίων Αποδοχών (από 2002)", min_value=500.0, max_value=10000.0, value=1500.0, step=50.0)

has_child = st.checkbox("Ύπαρξη ανήλικου τέκνου ή άλλες ειδικές προϋποθέσεις θεμελίωσης")

# --- ΚΟΥΜΠΙ ΥΠΟΛΟΓΙΣΜΟΥ ---
st.markdown("---")
if st.button("🚀 Υπολογισμός Σύνταξης & Εφάπαξ", type="primary"):
    
    # 1. Εθνική Σύνταξη
    national_pension = 426.17 if total_years >= 20 else 426.17 * (total_years / 20)
    
    # 2. Ανταποδοτική Σύνταξη
    if total_years <= 15:
        rehab_rate = 0.0771
    elif total_years <= 20:
        rehab_rate = 0.0805
    elif total_years <= 25:
        rehab_rate = 0.0882
    elif total_years <= 30:
        rehab_rate = 0.0990
    elif total_years <= 35:
        rehab_rate = 0.1250
    elif total_years <= 40:
        rehab_rate = 0.1500
    else:
        rehab_rate = 0.1500 + (total_years - 40) * 0.025
        
    contributory_pension = avg_salary * total_years * (rehab_rate / 10.0)
    
    # Ακαθάριστη Κύρια Σύνταξη
    gross_main_pension = national_pension + contributory_pension
    
    # Κρατήσεις (Υγεία 6%)
    health_deduction = gross_main_pension * 0.06
    net_main_pension = gross_main_pension - health_deduction
    
    # Εφάπαξ
    estimated_ephapax = avg_salary * (total_years * 0.5) if fund in ["Τράπεζες (π.χ. Ιονική/Alpha)", "Δημόσιο"] else 0.0

    # --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ---
    st.success("Ο υπολογισμός ολοκληρώθηκε επιτυχώς!")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("📊 Κύρια Σύνταξη")
        st.metric(label="Ακαθάριστη Κύρια Σύνταξη", value=f"{gross_main_pension:.2f} €")
        st.metric(label="Καθαρή Σύνταξη (μετά κρατήσεων υγείας)", value=f"{net_main_pension:.2f} €")
        
    with res_col2:
        st.subheader("💰 Εφάπαξ & Επικουρική")
        st.metric(label="Εκτιμώμενο Εφάπαξ", value=f"{estimated_ephapax:.2f} €" if estimated_ephapax > 0 else "Δεν προβλέπεται / Μη διαθέσιμο")
        st.metric(label="Εκτιμώμενη Επικουρική", value=f"{(avg_salary * 0.20):.2f} €" if "Τράπεζες" in fund or "Δημόσιο" in fund else "Εξαρτάται από ΤΕΑ/ΕΤΕΑΕΠ")

    st.info("⚠️ **Σημείωση:** Ο υπολογισμός αυτός αποτελεί προσομοίωση βάσει των γενικών διατάξεων του Ν. 4387/2016 για λόγους εκτίμησης και δεν αντικαθιστά την επίσημη πράξη απονομής σύνταξης από τον e-ΕΦΚΑ.")
