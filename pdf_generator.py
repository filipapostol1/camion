import io
from datetime import datetime
from fpdf import FPDF
from PIL import Image

def pulisci_testo(testo):
    if not testo:
        return ""
    testo_str = str(testo).replace("€", "EUR")
    return testo_str.encode('latin-1', 'replace').decode('latin-1')

def genera_preventivo_pdf(dati_vettore, dati_preventivo, logo_bytes=None):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # 1. Logo o Nome Vettore
    if logo_bytes:
        try:
            img = Image.open(io.BytesIO(logo_bytes))
            img.save("temp_logo.png")
            pdf.image("temp_logo.png", x=10, y=10, w=40)
        except Exception:
            pdf.set_font("Helvetica", "B", 14)
            pdf.text(10, 20, pulisci_testo(dati_vettore.get('nome', '')))
    else:
        pdf.set_font("Helvetica", "B", 14)
        pdf.text(10, 20, pulisci_testo(dati_vettore.get('nome', '')))
        
    pdf.set_font("Helvetica", "", 9)
    pdf.text(10, 30, f"P.IVA: {pulisci_testo(dati_vettore.get('piva', ''))}")
    pdf.text(10, 35, f"{pulisci_testo(dati_vettore.get('indirizzo', ''))} - {pulisci_testo(dati_vettore.get('loc', ''))}")
    
    # Intestazione Documento
    pdf.set_font("Helvetica", "B", 14)
    pdf.text(120, 20, "PREVENTIVO DI TRASPORTO")
    pdf.set_font("Helvetica", "", 10)
    data_em = dati_preventivo.get('data', datetime.now().strftime('%d/%m/%Y'))
    pdf.text(120, 27, f"Data emissione: {pulisci_testo(data_em)}")

    # Riquadri Committente e Tratta
    pdf.set_line_width(0.3)
    pdf.rect(10, 50, 90, 30)
    pdf.rect(105, 50, 95, 30)
    
    pdf.set_font("Helvetica", "B", 8)
    pdf.text(12, 55, "SPETT.LE COMMITTENTE:")
    pdf.set_font("Helvetica", "", 10)
    pdf.text(12, 63, pulisci_testo(dati_preventivo.get('cliente', '')))
    
    pdf.set_font("Helvetica", "B", 8)
    pdf.text(107, 55, "DETTAGLI TRATTA E MEZZO:")
    pdf.set_font("Helvetica", "", 9)
    pdf.text(107, 62, f"Partenza: {pulisci_testo(dati_preventivo.get('partenza', ''))[:40]}")
    pdf.text(107, 68, f"Destinazione: {pulisci_testo(dati_preventivo.get('destinazione', ''))[:40]}")

    # Tabella Costi
    y_tab = 90
    pdf.set_fill_color(230, 230, 230)
    pdf.rect(10, y_tab, 190, 8, "DF")
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(12, y_tab + 5, "DESCRIZIONE DEL SERVIZIO")
    pdf.text(165, y_tab + 5, "IMPORTO (EUR)")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.rect(10, y_tab + 8, 190, 30)
    
    km = dati_preventivo.get('km', 0)
    tariffa = dati_preventivo.get('tariffa', 0.0)
    costo = dati_preventivo.get('costo', 0.0)
    pedaggio = dati_preventivo.get('pedaggio', 0.0)
    imponibile = dati_preventivo.get('imponibile', 0.0)
    iva = dati_preventivo.get('iva', 0.0)
    totale = dati_preventivo.get('totale', 0.0)

    pdf.text(12, y_tab + 16, f"Servizio trasporto ({km} Km x {tariffa:.2f} EUR/Km)")
    pdf.text(165, y_tab + 16, f"{costo:.2f} EUR")
    
    pdf.text(12, y_tab + 26, "Rimborso spese pedaggio autostradale stimato")
    pdf.text(165, y_tab + 26, f"{pedaggio:.2f} EUR")

    # Totali
    y_tot = y_tab + 45
    pdf.rect(120, y_tot, 80, 24)
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(122, y_tot + 6, "IMPONIBILE")
    pdf.text(165, y_tot + 6, f"{imponibile:.2f} EUR")
    pdf.text(122, y_tot + 14, "IVA (22%)")
    pdf.text(165, y_tot + 14, f"{iva:.2f} EUR")
    pdf.set_font("Helvetica", "B", 10)
    pdf.text(122, y_tot + 22, "TOTALE")
    pdf.text(165, y_tot + 22, f"{totale:.2f} EUR")

    # Output sicuro in bytes per Streamlit
    out = pdf.output()
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return str(out).encode('latin-1', 'replace')
