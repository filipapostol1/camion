from fpdf import FPDF
from datetime import datetime
import io
from PIL import Image

class PDF(FPDF):
    pass 

def genera_preventivo_pdf(dati_vettore, dati_preventivo, logo_bytes):
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    if logo_bytes:
        img = Image.open(io.BytesIO(logo_bytes))
        img.save("temp_logo.png")
        pdf.image("temp_logo.png", x=10, y=10, w=40)
    else:
        pdf.set_font("Helvetica", "B", 14)
        pdf.text(10, 20, dati_vettore['nome'])
        
    pdf.set_font("Helvetica", "", 9)
    pdf.text(10, 30, f"P.IVA: {dati_vettore['piva']}")
    pdf.text(10, 35, f"{dati_vettore['indirizzo']} - {dati_vettore['loc']}")
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.text(120, 20, "PREVENTIVO DI TRASPORTO")
    pdf.set_font("Helvetica", "", 10)
    pdf.text(120, 27, f"Data emissione: {datetime.now().strftime('%d/%m/%Y')}")

    pdf.set_line_width(0.3)
    pdf.rect(10, 50, 90, 30)
    pdf.rect(105, 50, 95, 30)
    
    pdf.set_font("Helvetica", "B", 8)
    pdf.text(12, 55, "SPETT.LE COMMITTENTE:")
    pdf.set_font("Helvetica", "", 10)
    pdf.text(12, 63, dati_preventivo['cliente'])
    
    pdf.set_font("Helvetica", "B", 8)
    pdf.text(107, 55, "DETTAGLI TRATTA E MEZZO:")
    pdf.set_font("Helvetica", "", 9)
    pdf.text(107, 62, f"Partenza: {dati_preventivo['partenza'][:40]}")
    pdf.text(107, 68, f"Destinazione: {dati_preventivo['destinazione'][:40]}")

    y_tab = 90
    pdf.set_fill_color(230, 230, 230)
    pdf.rect(10, y_tab, 190, 8, "DF")
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(12, y_tab + 5, "DESCRIZIONE DEL SERVIZIO")
    pdf.text(165, y_tab + 5, "IMPORTO (EUR)")
    
    pdf.set_font("Helvetica", "", 9)
    pdf.rect(10, y_tab+8, 190, 30)
    pdf.text(12, y_tab + 16, f"Servizio trasporto ({dati_preventivo['km']} Km x {dati_preventivo['tariffa']:.2f} EUR/Km)")
    pdf.text(165, y_tab + 16, f"{dati_preventivo['costo']:.2f} €")
    pdf.text(12, y_tab + 26, "Rimborso spese pedaggio autostradale stimato")
    pdf.text(165, y_tab + 26, f"{dati_preventivo['pedaggio']:.2f} €")

    y_tot = y_tab + 45
    pdf.rect(120, y_tot, 80, 24)
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(122, y_tot + 6, "IMPONIBILE")
    pdf.text(165, y_tot + 6, f"{dati_preventivo['imponibile']:.2f} €")
    pdf.text(122, y_tot + 14, "IVA (22%)")
    pdf.text(165, y_tot + 14, f"{dati_preventivo['iva']:.2f} €")
    pdf.set_font("Helvetica", "B", 10)
    pdf.text(122, y_tot + 22, "TOTALE")
    pdf.text(165, y_tot + 22, f"{dati_preventivo['totale']:.2f} €")

    return pdf.output(dest='S')
