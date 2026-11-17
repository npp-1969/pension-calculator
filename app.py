import streamlit as st

# Rithmisi selidas
st.set_page_config(page_title="Epaggelmatikos Ypologistis Syntaxewn & Efapax", page_icon="🧮", layout="centered")

st.title("🧮 Ypologistis Syntaxewn & Efapax (N. 4387/2016)")
st.markdown("---")
st.write("Symplirwste ta stoicheia sas gia na ypologisete tin Kyria Syntaxi, tin Epikouriki kai to Efapax me dynatotita pollaplwn tameiwn.")

# --- ENOTYTA 1: PROSWPIKA & ASFALISTIKA STOICHEIA ---
st.header("1. Prosopika & Asfalistika Stoicheia")

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Fylo", ["Andras", "Gynaika"])
    birth_year = st.number_input("Etos Gennisis", min_value=1940, max_value=2005, value=1975)
with col2:
    insurance_type = st.selectbox("Proti Asfalisi", ["Palaios (ews 31/12/1992)", "Neos (apo 1/1/1993 kai meta)"])
    funds = st.multiselect("Tameia Asfalisis (Epilexte ola ta tameia pou exete ensima)", 
                           ["IKA / e-EFKA Misthwtwn", "Dimosio", "Trapezes (p.x. Ioniaki/Alpha)", "OAEE / Eleftheroi Epangelmaties"],
                           default=["IKA / e-EFKA Misthwtwn"])

# --- ENOTYTA 2: CHRONOS & APODOCHES ---
st.header("2. Chronos Asfalisis & Apodoches")

col3, col4 = st.columns(2)
with col3:
    total_years = st.number_input("Synolika Eti Asfalisis", min_value=1, max_value=50, value=30)
with col4:
    avg_salary = st.number_input("Mesos Oros Miniaiwn Apodochwn (apo 2002)", min_value=500.0, max_value=10000.0, value=1500.0, step=50.0)

has_child = st.checkbox("Yparxi anilikou teknou i alles eidikes proypotheseis themeliwsis")

# --- KOUMPI YPOLOGISMOY ---
st.markdown("---")
if st.button("🚀 Ypologismos Syntaxis & Efapax", type="primary"):
    
    # 1. Ethniki Syntaxi
    national_pension = 426.17 if total_years >= 20 else 426.17 * (total_years / 20)
    
    # 2. Antapodotiki Syntaxi
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
    
    # Akatharisti Kyria Syntaxi
    gross_main_pension = national_pension + contributory_pension
    
    # Kratiseis (Ygeia 6%)
    health_deduction = gross_main_pension * 0.06
    net_main_pension = gross_main_pension - health_deduction
    
    # Efapax (An yparchei Trapeza i Dimosio sta epilegmena tameia)
    has_bank_or_public = any(f in funds for f in ["Trapezes (p.x. Ioniaki/Alpha)", "Dimosio"])
    estimated_ephapax = avg_salary * (total_years * 0.5) if has_bank_or_public else 0.0

    # --- EMFANISI APOTELESMATWN ---
    st.success("O ypologismos oloklirothike epitychws!")
    
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.subheader("📊 Kyria Syntaxi")
        st.metric(label="Akatharisti Kyria Syntaxi", value=f"{gross_main_pension:.2f} €")
        st.metric(label="Kathari Syntaxi (meta kratiseon ygeias)", value=f"{net_main_pension:.2f} €")
        
    with res_col2:
        st.subheader("💰 Efapax & Epikouriki")
        st.metric(label="Ektimwmeno Efapax", value=f"{estimated_ephapax:.2f} €" if estimated_ephapax > 0 else "Den provlepetai / Mi diathesimo")
        st.metric(label="Ektimwmeni Epikouriki", value=f"{(avg_salary * 0.20):.2f} €" if has_bank_or_public else "Exartatai apo TEA/ETEAEp")

    st.info("⚠️ **Simeiosei:** O ypologismos autos apotelei prosomoiosei vasei ton genikwn diataxeon tou N. 4387/2016 gia logous ektimiseos kai den antikatista tin episimi praxi aponomis syntaxis apo ton e-EFKA.")
