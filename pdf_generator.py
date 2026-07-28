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
    pdf.set_margins(10, 10, 10)
    pdf.add_page()
    pdf.set_auto_page_break(False)
    
    # 1. Logo / Intestazione Vettore
    if logo_bytes:
        try:
            img = Image.open(io.BytesIO(logo_bytes))
            img.save("temp_logo.png")
            pdf.image("temp_logo.png", x=10, y=10, w=38)
        except Exception:
            pdf.set_font("Helvetica", "B", 13)
            pdf.text(10, 15, pulisci_testo(dati_vettore.get('nome', '')))
    else:
        pdf.set_font("Helvetica", "B", 13)
        pdf.text(10, 15, pulisci_testo(dati_vettore.get('nome', '')))
        
    pdf.set_font("Helvetica", "", 8.5)
    pdf.text(10, 26, f"P.IVA: {pulisci_testo(dati_vettore.get('piva', ''))}")
    pdf.text(10, 31, f"{pulisci_testo(dati_vettore.get('indirizzo', ''))} - {pulisci_testo(dati_vettore.get('loc', ''))}")
    
    # Intestazione Documento (Destra)
    pdf.set_font("Helvetica", "B", 13)
    pdf.text(130, 15, "PREVENTIVO DI TRASPORTO")
    pdf.set_font("Helvetica", "", 9)
    data_em = dati_preventivo.get('data', datetime.now().strftime('%d/%m/%Y'))
    pdf.text(130, 22, f"Data emissione: {pulisci_testo(data_em)}")

    # 2. Riquadri Committente e Tratta
    y_box = 42
    h_box = 28
    pdf.set_line_width(0.2)
    
    # Committente (Sinistra)
    pdf.rect(10, y_box, 92, h_box)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.text(12, y_box + 5, "SPETT.LE COMMITTENTE:")
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_xy(12, y_box + 8)
    pdf.multi_cell(88, 4.5, pulisci_testo(dati_preventivo.get('cliente', '')))
    
    # Tratta e Mezzo (Destra)
    pdf.rect(106, y_box, 94, h_box)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.text(108, y_box + 5, "DETTAGLI TRATTA E MEZZO:")
    pdf.set_font("Helvetica", "", 8.5)
    
    partenza_txt = pulisci_testo(dati_preventivo.get('partenza', ''))
    destinazione_txt = pulisci_testo(dati_preventivo.get('destinazione', ''))
    
    pdf.text(108, y_box + 12, f"Partenza: {partenza_txt[:42]}")
    pdf.text(108, y_box + 18, f"Destinazione: {destinazione_txt[:42]}")

    # 3. Tabella Descrizione Servizi
    y_tab = 78
    h_header = 7
    h_body = 28
    
    # Intestazione Tabella
    pdf.set_fill_color(235, 235, 235)
    pdf.rect(10, y_tab, 190, h_header, "DF")
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.text(12, y_tab + 4.8, "DESCRIZIONE DEL SERVIZIO")
    pdf.text(160, y_tab + 4.8, "IMPORTO (EUR)")
    
    # Corpo Tabella
    pdf.rect(10, y_tab + h_header, 190, h_body)
    pdf.line(155, y_tab, 155, y_tab + h_header + h_body) # Linea divisoria verticale
    
    km = dati_preventivo.get('km', 0)
    tariffa = dati_preventivo.get('tariffa', 0.0)
    costo = dati_preventivo.get('costo', 0.0)
    pedaggio = dati_preventivo.get('pedaggio', 0.0)
    imponibile = dati_preventivo.get('imponibile', 0.0)
    iva = dati_preventivo.get('iva', 0.0)
    totale = dati_preventivo.get('totale', 0.0)

    pdf.set_font("Helvetica", "", 8.5)
    # Riga 1: Servizio trasporto
    y_riga1 = y_tab + h_header + 8
    pdf.text(12, y_riga1, f"Servizio trasporto ({km} Km x {tariffa:.2f} EUR/Km)")
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.text(160, y_riga1, f"{costo:.2f} EUR")
    
    # Riga 2: Pedaggio
    y_riga2 = y_riga1 + 10
    pdf.set_font("Helvetica", "", 8.5)
    pdf.text(12, y_riga2, "Rimborso spese pedaggio autostradale stimato")
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.text(160, y_riga2, f"{pedaggio:.2f} EUR")

    # 4. Box Totali (In Basso a Destra)
    y_tot = y_tab + h_header + h_body + 10
    w_tot = 75
    x_tot = 125
    
    pdf.rect(x_tot, y_tot, w_tot, 22)
    pdf.line(x_tot + 35, y_tot, x_tot + 35, y_tot + 22) # Divisorio etichetta / valore
    
    pdf.set_font("Helvetica", "", 8)
    pdf.text(x_tot + 3, y_tot + 5.5, "IMPONIBILE")
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.text(x_tot + 38, y_tot + 5.5, f"{imponibile:.2f} EUR")
    
    pdf.line(x_tot, y_tot + 7.5, x_tot + w_tot, y_tot + 7.5)
    
    pdf.set_font("Helvetica", "", 8)
    pdf.text(x_tot + 3, y_tot + 12.5, "IVA (22%)")
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.text(x_tot + 38, y_tot + 12.5, f"{iva:.2f} EUR")
    
    pdf.line(x_tot, y_tot + 14.5, x_tot + w_tot, y_tot + 14.5)
    
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.text(x_tot + 3, y_tot + 19.5, "TOTALE")
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(x_tot + 38, y_tot + 19.5, f"{totale:.2f} EUR")

    # Output Byte
    out = pdf.output()
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return str(out).encode('latin-1', 'replace')
