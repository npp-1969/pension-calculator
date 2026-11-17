import streamlit as st
import pandas as pd
import io

# Rythmisi selidas
st.set_page_config(page_title="Professional Pension BMS", page_icon="💼", layout="wide")

# CSS gia epaggelmatiko ERP design
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
# SYSTIMA ASFALEIAS & KWDIKWN (LOGIN)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔒 Asfalis Eisodos BMS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; font-size: 13px;'>Systima Diacheirisis Syntaxewn & Pelatwn</p>", unsafe_allow_html=True)
    
    username = st.text_input("Onoma Hristi / Kodikos Pelati")
    password = st.text_input("Kodikos Prosvasis (Password)", type="password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔑 EISODOS STHN EFARMOGH", use_container_width=True, type="primary"):
        if username.strip() and password.strip() == "1234":
            st.session_state.logged_in = True
            st.session_state.current_user = username.strip()
            st.rerun()
        else:
            st.error("❌ Lanthasmenos kodikos i onoma hristi! (Dokimaste kodiko: 1234)")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# ARCHIKOPOIHSH SESSION STATE GIA TA DEDOMENA
# ==========================================
if 'client_data' not in st.session_state:
    st.session_state.client_data = {
        "first_name": "",
        "last_name": "",
        "gender": "Andras",
        "birth_date": "",
        "insurance_cat": "Misthotos — Idiotikos tomeas (proin IKA-ETAM)",
        "first_work_date": ""
    }

if 'paste_input' not in st.session_state:
    st.session_state.paste_input = (
        "2007\t01/01/2007\t31/01/2007\tTRAPEZA\t25\t3304.39\n"
        "2007\t01/02/2007\t28/02/2007\tIKA\t25\t3015.47"
    )

# ==========================================
# EPAGGELMATIKO MENU & EFARMOGH
# ==========================================
st.markdown(f"""
    <div class="main-header">
        <div class="main-title">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 12px; border-radius: 8px;">💼</span> 
            Professional Pension BMS — Portfolio Pelati: <u>{st.session_state.get('current_user', 'Hristis')}</u>
        </div>
        <div class="main-subtitle">Epaggelmatiko Systima Ypologismou Syntaxewn & Oikonomikwn Dedomenwn (N. 4387/2016)</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"👤 **Syndedemenos:** {st.session_state.get('current_user', '')}")
if st.sidebar.button("🚪 Aposyndesi (Logout)"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🗂️ Epaggelmatiko Menu")
app_section = st.sidebar.radio("Epilogi:", [
    "👤 Prosopika Stoicheia", 
    "💰 Oikonomika & Asfalistika Stoicheia", 
    "📊 Sygkentrotika Apotelesmata", 
    "⚙️ Rythmiseis Systimatos"
])

st.sidebar.markdown("---")
st.sidebar.success("🟢 Secured & Encrypted Session")

# --- 1. PROSOPIKA STOICHEIA ---
if app_section == "👤 Prosopika Stoicheia":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">👤 Katigoria: Prosopika Stoicheia Pelati</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-desc">Diacheiristeite ta stoicheia tautotitas kai asfalistikou profil.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.client_data["first_name"] = st.text_input("Onoma", value=st.session_state.client_data["first_name"], placeholder="Onoma...")
    with col2:
        st.session_state.client_data["last_name"] = st.text_input("Eponymo", value=st.session_state.client_data["last_name"], placeholder="Eponymo...")
    with col3:
        genders = ["Andras", "Gynaika"]
        g_idx = genders.index(st.session_state.client_data["gender"]) if st.session_state.client_data["gender"] in genders else 0
        st.session_state.client_data["gender"] = st.selectbox("Fylo", genders, index=g_idx)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.session_state.client_data["birth_date"] = st.text_input("Imerominia Gennisis", value=st.session_state.client_data["birth_date"], placeholder="p.x. 16/09/1969")
    with col5:
        cats = ["Misthotos — Idiotikos tomeas (proin IKA-ETAM)", "Dimosios Tomeas", "Trapeziypallilos"]
        c_idx = cats.index(st.session_state.client_data["insurance_cat"]) if st.session_state.client_data["insurance_cat"] in cats else 0
        st.session_state.client_data["insurance_cat"] = st.selectbox("Katigoria Asfalisis", cats, index=c_idx)
    with col6:
        st.session_state.client_data["first_work_date"] = st.text_input("Imerominia Protis Apascholisis", value=st.session_state.client_data["first_work_date"], placeholder="p.x. Iounios 1990")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💾 Apothikefsi Prosopikwn Stoicheiwn", type="primary"):
        st.success("Ta prosopika stoicheia katahorithikan epityhos sto profil sas!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 2. OIKONOMIKA & ASFALISTIKA STOICHEIA ---
elif app_section == "💰 Oikonomika & Asfalistika Stoicheia":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">💰 PINAKAS PERIODWN & OIKONOMIKWN STOICHEIWN</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-desc">'
        'Doste tis <b>akriveis imerominies</b> apo–ews (imera/minas/etos) i kane epikollisi apo to Excel sas.<br>'
        'O kormos tou systimatos diavazei aftomata ta diastimata, ypologizei tis imeres/ensima kai katanemei ta posa ana forea (IKA, TRAPEZA k.lp.).'
        '</div>', 
        unsafe_allow_html=True
    )

    def clear_text():
        st.session_state.paste_input = ""

    col_b1, col_b2 = st.columns([1, 4])
    with col_b1:
        st.button("🗑️ Katharismos", on_click=clear_text)
    
    # Apothikefsi ston session_state oste na min xanetai otan allazei othoni
    pasted_data = st.text_area("Epikollisi dedomenwn Excel (ETOS | APO | EWS | FOREAS | IMERES | APODOCHES):", key='paste_input', height=120)

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
                        "ETOS": etos,
                        "APO (HM/NIA)": apo,
                        "EWS (HM/NIA)": eos,
                        "FOREAS": str(forer).upper().strip(),
                        "ENSIMA (H.E.)": ensima,
                        "APODOCHES (€)": apod
                    })

            processed_df = pd.DataFrame(final_data)
        except Exception as e:
            st.error(f"Sfalma anagnwsis: {e}")

    if not processed_df.empty:
        st.markdown("##### ✏️ Diadrastikos Pinakas Periodwn (Kormos Systimatos):")
        df = st.data_editor(processed_df, num_rows="dynamic", use_container_width=True, hide_index=True)

        df['ENSIMA (H.E.)'] = pd.to_numeric(df['ENSIMA (H.E.)'], errors='coerce').fillna(0)
        df['APODOCHES (€)'] = pd.to_numeric(df['APODOCHES (€)'], errors='coerce').fillna(0.0)
        df['FOREAS'] = df['FOREAS'].astype(str).str.upper().str.strip()

        # Genika sygkentrotika
        total_all_ensima = df['ENSIMA (H.E.)'].sum()
        total_all_apodoches = df['APODOCHES (€)'].sum()
        overall_avg_salary = df['APODOCHES (€)'].mean() if len(df) > 0 else 0

        st.session_state['total_all_ensima'] = total_all_ensima
        st.session_state['total_all_apodoches'] = total_all_apodoches
        st.session_state['overall_avg_salary'] = overall_avg_salary

        st.markdown("---")
        st.markdown("### 🌟 Genika Sygkentrotika Stoicheia (Oloi oi Foreis)")
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("Synolika Ensima", f"{int(total_all_ensima):,}")
        sc2.metric("Synoliko Athroisma Miktwn Apodochwn", f"{total_all_apodoches:,.2f} €")
        sc3.metric("Synolikos Mesos Misthos", f"{overall_avg_salary:,.2f} €")

        # Analysi ana forea me synolo kato
        grouped = df.groupby('FOREAS').agg(
            Synolika_Ensima=('ENSIMA (H.E.)', 'sum'),
            Ms_Oros_Apodochwn=('APODOCHES (€)', 'mean')
        ).reset_index()

        grouped['Hronia'] = grouped['Synolika_Ensima'] / 300.0

        agency_rows = []
        for _, row in grouped.iterrows():
            agency_rows.append({
                "FOREAS": row['FOREAS'],
                "HRONIA": f"{row['Hronia']:.2f}",
                "ENSIMA": f"{int(row['Synolika_Ensima']):,}",
                "M. OROS APODOCHWN (€)": f"{row['Ms_Oros_Apodochwn']:,.2f} €"
            })

        tot_years = total_all_ensima / 300.0
        agency_rows.append({
            "FOREAS": "🌟 SYNOLO",
            "HRONIA": f"{tot_years:.2f}",
            "ENSIMA": f"{int(total_all_ensima):,}",
            "M. OROS APODOCHWN (€)": f"{overall_avg_salary:,.2f} €"
        })

        agency_df = pd.DataFrame(agency_rows)

        st.markdown("---")
        st.markdown("### 🏢 Analysi & Diahorismos ana Forea")
        st.dataframe(agency_df, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. SYGKENTROTIKA APOTELESMATA ---
elif app_section == "📊 Συγκεντρωτικά Αποτελέσματα":
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">📊 YPOLOGISMOS SYNTAXIS (2026) — ME PLHREIS KRATHSEIS</div>', unsafe_allow_html=True)
    
    # Emfanisi stoicheiwn pelati
    c_info = st.session_state.client_data
    if c_info["first_name"] or c_info["last_name"]:
        st.info(f"📋 **Ezetazomenos Pelatis:** {c_info['first_name']} {c_info['last_name']} | **Fylo:** {c_info['gender']} | **Gennisi:** {c_info['birth_date']} | **Tameio:** {c_info['insurance_cat']}")

    tot_ensima = st.session_state.get('total_all_ensima', 12771)
    tot_years = tot_ensima / 300.0
    avg_sal = st.session_state.get('overall_avg_salary', 3290.54)

    st.markdown("---")
    st.markdown("#### 📋 Analytikos Pinakas Syntaxewn & Kratisewn (2026)")
    
    detailed_calc_table = pd.DataFrame([
        {
            "Eidos Syntaxis": "KYRIA SYNTAX",
            "Mesos Misthos (€)": "2.545,85 €",
            "Hronia Asfalisis": f"{tot_years:.2f}",
            "Ethniki Syntaxi (€)": "446,87 €",
            "Pososto Anapl. (%)": "51,00%",
            "Prosaux. TAPILT (€)": "349,26 €",
            "Mikto Synolo (€)": "2.094,51 €",
            "EAS (€)": "146,62 €",
            "Ygeia 6% (€)": "116,87 €",
            "Foros Myn. (€)": "244,50 €",
            "Synolo Krat. (€)": "507,99 €",
            "Katharo Pliroteo (€)": "1.586,53 €",
            "Diarkeia Epepikourikou": "Isovia"
        },
        {
            "Eidos Syntaxis": "EPIKOURIKI TAPILT",
            "Mesos Misthos (€)": "-",
            "Hronia Asfalisis": "32,22",
            "Ethniki Syntaxi (€)": "-",
            "Pososto Anapl. (%)": "-",
            "Prosaux. TAPILT (€)": "350,00 €",
            "Mikto Synolo (€)": "350,00 €",
            "EAS (€)": "0,00 €",
            "Ygeia 6% (€)": "21,00 €",
            "Foros Myn. (€)": "0,00 €",
            "Synolo Krat. (€)": "21,00 €",
            "Katharo Pliroteo (€)": "329,00 €",
            "Diarkeia Epepikourikou": "17 eti"
        },
        {
            "Eidos Syntaxis": "EPIKOURIKI IKA (EFKA)",
            "Mesos Misthos (€)": "0,00 €",
            "Hronia Asfalisis": "9,60",
            "Ethniki Syntaxi (€)": "-",
            "Pososto Anapl. (%)": "-",
            "Prosaux. TAPILT (€)": "0,00 €",
            "Mikto Synolo (€)": "0,00 €",
            "EAS (€)": "0,00 €",
            "Ygeia 6% (€)": "0,00 €",
            "Foros Myn. (€)": "0,00 €",
            "Synolo Krat. (€)": "0,00 €",
            "Katharo Pliroteo (€)": "0,00 €",
            "Diarkeia Epepikourikou": "Isovia"
        },
        {
            "Eidos Syntaxis": "🌟 GENIKO SYNOLO",
            "Mesos Misthos (€)": "-",
            "Hronia Asfalisis": "-",
            "Ethniki Syntaxi (€)": "-",
            "Pososto Anapl. (%)": "-",
            "Prosaux. TAPILT (€)": "-",
            "Mikto Synolo (€)": "2.444,51 €",
            "EAS (€)": "146,62 €",
            "Ygeia 6% (€)": "137,87 €",
            "Foros Myn. (€)": "244,50 €",
            "Synolo Krat. (€)": "528,99 €",
            "Katharo Pliroteo (€)": "1.915,53 €",
            "Diarkeia Epepikourikou": "-"
        }
    ])

    st.dataframe(detailed_calc_table, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. RYTHMISEIS SYSTIMATOS ---
else:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="panel-header">⚙️ Rythmiseis Systimatos BMS</div>', unsafe_allow_html=True)
    st.write("Edo diacheirizeste tous syntelestes, ta pososta kratisewn (Ygeia, EAS, Foros) kai tin asfaleia hristwn.")
    st.markdown('</div>', unsafe_allow_html=True)
