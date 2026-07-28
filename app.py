import streamlit as st
import database
import api_client
import pdf_generator
import pdf_bolla

database.init_db()

st.set_page_config(page_title="Apostol Trasporti - ERP", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style> [data-testid='collapsedControl'] { display: none; } </style>", unsafe_allow_html=True)

if 'logo_bytes' not in st.session_state: st.session_state.logo_bytes = None
if 'km_suggeriti' not in st.session_state: st.session_state.km_suggeriti = 0.0

def stima_pedaggio(km_totali, classe):
    tariffe = {"Bilico (4/5 Assi)": 0.19, "Camion (3 Assi)": 0.14, "Auto / Furgone": 0.09}
    return round((km_totali * 0.75) * tariffe.get(classe, 0.19), 2)

st.title("🚛 Gestionale Trasporti & Preventivi")
st.markdown("---")

tab_impostazioni, tab_preventivi, tab_bolla, tab_cronologia = st.tabs([
    "⚙️ Impostazioni Azienda", "📊 Preventivi & Percorsi", "📄 Bolle / DDT", "📜 Cronologia"
])

# --- TAB 1: IMPOSTAZIONI ---
with tab_impostazioni:
    col1, col2 = st.columns([1, 2])
    with col1:
        uploaded_logo = st.file_uploader("Carica Logo Aziendale", type=["png", "jpg", "jpeg"])
        if uploaded_logo: st.session_state.logo_bytes = uploaded_logo.read()
        if st.session_state.logo_bytes: st.image(st.session_state.logo_bytes, width=200)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Ragione Sociale Vettore", value="APOSTOL TRASPORTI DI APOSTOL C", key="v_nome")
        st.text_input("Partita IVA", value="01595470111", key="v_piva")
        st.text_input("Indirizzo", value="VIA EMILIO BIONE 8", key="v_ind")
        st.text_input("Località", value="LA SPEZIA", key="v_loc")
    with c2:
        st.text_input("Nome Autista", value="APOSTOL CATALIN", key="autista")
        st.text_input("Targa Trattore", value="GD613CR", key="trattore")
        st.text_input("Targa Rimorchio", value="XA762KF", key="rimorchio")

# --- TAB 2: PREVENTIVI ---
with tab_preventivi:
    col_p1, col_p2 = st.columns([1, 1], gap="large")

    with col_p1:
        cliente = st.text_input("Nome Cliente", value="ACME S.r.l.")
        partenza = st.text_input("Partenza", value="Via Sommacampagna 61, Verona")
        destinazione = st.text_input("Destinazione", value="Via Tiburtina 1000, Roma")
        tipo_viaggio = st.radio("Tipologia", ["Solo Andata", "Andata e Ritorno"], horizontal=True)
        
        if st.button("📍 Ottieni Stima KM da Mappa", use_container_width=True):
            with st.spinner("Calcolo rotte..."):
                lat1, lon1 = api_client.ottieni_coordinate(partenza)
                lat2, lon2 = api_client.ottieni_coordinate(destinazione)
                
                if lat1 and lat2:
                    api_key = st.secrets.get("ORS_API_KEY", None)
                    km_calc = api_client.calcola_rotta_camion(lat1, lon1, lat2, lon2, api_key)
                    if km_calc:
                        st.session_state.km_suggeriti = km_calc * 2 if tipo_viaggio == "Andata e Ritorno" else km_calc
                        st.success(f"Distanza stimata: {st.session_state.km_suggeriti} Km")
                    else:
                        st.error("Errore nel calcolo del percorso.")
                else:
                    st.error("Impossibile trovare le coordinate.")

    with col_p2:
        km_finali = st.number_input("KM Effettivi", value=float(st.session_state.km_suggeriti), step=5.0)
        classe = st.selectbox("Mezzo", ["Bilico (4/5 Assi)", "Camion (3 Assi)", "Auto / Furgone"])
        tariffa = st.number_input("Tariffa (€/Km)", value=1.70, step=0.05)
        
        pedaggio = stima_pedaggio(km_finali, classe)
        costo = round(km_finali * tariffa, 2)
        imponibile = round(costo + pedaggio, 2)
        totale = round(imponibile * 1.22, 2)

        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("Trasporto", f"€ {costo:.2f}")
        c_m2.metric("Pedaggi", f"€ {pedaggio:.2f}")
        c_m3.metric("TOTALE + IVA", f"€ {totale:.2f}")

        if st.button("🖨️ GENERA PREVENTIVO (PDF)", type="primary", use_container_width=True):
            if km_finali > 0:
                database.salva_in_cronologia("Preventivo", cliente, f"{partenza} -> {destinazione}", f"€ {totale:.2f}")
                
                dati_vettore = {
                    "nome": st.session_state.v_nome, "piva": st.session_state.v_piva,
                    "indirizzo": st.session_state.v_ind, "loc": st.session_state.v_loc
                }
                dati_prev = {
                    "cliente": cliente, "partenza": partenza, "destinazione": destinazione,
                    "km": km_finali, "tariffa": tariffa, "costo": costo, "pedaggio": pedaggio,
                    "imponibile": imponibile, "iva": round(imponibile * 0.22, 2), "totale": totale
                }
                
                pdf_bytes = pdf_generator.genera_preventivo_pdf(dati_vettore, dati_prev, st.session_state.logo_bytes)
                st.download_button("📥 SCARICA PREVENTIVO", data=pdf_bytes, file_name="Preventivo.pdf", mime="application/pdf")

# --- TAB 3: BOLLA / DDT ---
with tab_bolla:
    st.subheader("📄 Compilazione Lettera di Vettura (Standard Intermodale)")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        bolla_data = st.date_input("Data Viaggio", format="DD/MM/YYYY")
        bolla_ora = st.time_input("Ora")
        bolla_rif = st.text_input("Nr. Riferimento", value="01 8572")
    with c2:
        bolla_compagnia = st.text_input("Compagnia", value="ONE")
        bolla_booking = st.text_input("Booking / Import-Export", value="IMPORT")
        bolla_merce = st.text_input("Natura Merce", value="MERCE VARIA")
    with c3:
        bolla_container = st.text_input("Sigla Container", value="ONEU 504737 / 3")
        bolla_tipo_cont = st.selectbox("Tipo Container", ["40 HC", "20 DV", "40 DV", "45 HC", "20 OT", "40 OT"])
        bolla_peso = st.text_input("Peso Tot. Kg", value="30.115")

    st.markdown("---")
    
    col_carico, col_scarico = st.columns(2)
    with col_carico:
        st.markdown("**📍 Terminal Ritiro / Carico**")
        bolla_term_carico = st.text_input("Nome Terminal", value="LA SPEZIA CONTAINER TRML LSCT")
        bolla_term_ind = st.text_input("Indirizzo Terminal", value="MOLO FORNELLI")
        bolla_term_loc = st.text_input("Località Terminal", value="LA SPEZIA")
        
    with col_scarico:
        st.markdown("**📍 Luogo di Scarico**")
        bolla_scarico = st.text_input("Nome Scarico", value="CONTREPAIR LA SPEZIA")
        bolla_scarico_ind = st.text_input("Indirizzo Scarico", value="VIA BOLANO 20")
        bolla_scarico_loc = st.text_input("Località Scarico", value="SANTO STEFANO MAGRA")

    st.markdown("---")
    if st.button("🖨️ GENERA BOLLA SILT", type="primary", use_container_width=True):
        dati_bolla = {
            "data": bolla_data.strftime("%d/%m/%Y"),
            "ora": bolla_ora.strftime("%H:%M"),
            "rif": bolla_rif,
            "compagnia": bolla_compagnia,
            "booking": bolla_booking,
            "committente": "SILT Srl",
            "comm_indirizzo": "Piazza G. Alessi, 2",
            "comm_loc": "Genova",
            "comm_piva": "03441250101",
            "terminal_carico": bolla_term_carico,
            "terminal_ind": bolla_term_ind,
            "terminal_loc": bolla_term_loc,
            "luogo_scarico": bolla_scarico,
            "scarico_ind": bolla_scarico_ind,
            "scarico_loc": bolla_scarico_loc,
            "merce": bolla_merce,
            "km": str(st.session_state.km_suggeriti),
            "vettore_nome": st.session_state.v_nome,
            "vettore_ind": f"{st.session_state.v_ind} {st.session_state.v_loc}",
            "vettore_piva": st.session_state.v_piva,
            "autista": st.session_state.autista,
            "targa_trattore": st.session_state.trattore,
            "targa_rimorchio": st.session_state.rimorchio,
            "container_1": bolla_container,
            "tipo_container": bolla_tipo_cont,
            "peso": bolla_peso,
            "spedizioniere": "SAVINO"
        }
        
        pdf_bytes = pdf_bolla.genera_bolla_silt(dati_bolla)
        st.success("Bolla generata con successo!")
        st.download_button(
            label="📥 SCARICA LETTERA DI VETTURA (PDF)", 
            data=pdf_bytes, 
            file_name=f"Bolla_{bolla_container.replace('/', '-')}.pdf", 
            mime="application/pdf",
            use_container_width=True
        )

# --- TAB 4: CRONOLOGIA ---
with tab_cronologia:
    st.subheader("Storico Operazioni")
    dati = database.carica_cronologia()
    if dati:
        st.dataframe(dati, use_container_width=True)
    else:
        st.info("Nessuna operazione registrata.")
