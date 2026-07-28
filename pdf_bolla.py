from fpdf import FPDF

class BollaPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=False)
        self.add_page()
        
    def box_testo(self, x, y, titolo, valore, font_titolo=6, font_valore=9, grassetto_valore=True):
        self.set_xy(x, y)
        self.set_font("Helvetica", "", font_titolo)
        self.cell(0, 3, titolo, ln=1)
        self.set_xy(x, y + 3)
        self.set_font("Helvetica", "B" if grassetto_valore else "", font_valore)
        self.cell(0, 4, str(valore), ln=1)

def genera_bolla_silt(dati):
    pdf = BollaPDF()
    
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(100, 150, 100)
    pdf.text(10, 20, "silt")
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_text_color(0, 0, 150)
    testo_silt = "S.I.L.T. S.r.l. Sistemi Integrati di Logistica e Trasporto\nSede Legale 20129 Milano (MI)\nDirezione e Amministrazione 16128 GENOVA"
    pdf.set_xy(35, 12)
    pdf.multi_cell(70, 3, testo_silt)
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.text(150, 22, "LETTERA DI VETTURA")
    pdf.set_font("Helvetica", "B", 10)
    pdf.text(150, 28, f"{dati.get('num_documento', '20260100008572')}")

    pdf.rect(10, 35, 190, 160)
    pdf.line(10, 45, 200, 45)
    pdf.line(10, 75, 200, 75)
    pdf.line(10, 95, 200, 95)
    pdf.line(10, 115, 200, 115)
    pdf.line(10, 125, 200, 125)
    pdf.line(10, 145, 200, 145)
    pdf.line(10, 165, 200, 165)
    pdf.line(10, 185, 200, 185)

    pdf.line(95, 35, 95, 125)
    pdf.line(95, 125, 95, 185)
    pdf.line(130, 125, 130, 185)
    pdf.line(165, 125, 165, 185)

    pdf.box_testo(12, 36, "Data", dati.get('data', ''), font_valore=11)
    pdf.box_testo(40, 36, "Ora", dati.get('ora', ''), font_valore=11)
    pdf.box_testo(70, 36, "Nr. Riferimento", dati.get('rif', ''), font_valore=11)
    pdf.box_testo(97, 36, "Compagnia", dati.get('compagnia', ''), font_valore=11)
    pdf.box_testo(145, 36, "Booking", dati.get('booking', ''), font_valore=11)

    pdf.box_testo(12, 46, "Committ.", dati.get('committente', 'SILT Srl'), font_valore=10)
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(12, 58, dati.get('comm_indirizzo', 'Piazza G. Alessi, 2'))
    pdf.text(12, 63, dati.get('comm_loc', 'Genova'))
    pdf.text(12, 68, f"Telefono: {dati.get('comm_tel', '010/8597200')}    P.Iva: {dati.get('comm_piva', '03441250101')}")
    
    pdf.box_testo(12, 76, "Term.Rit. / Caric.", dati.get('terminal_carico', ''), font_valore=9)
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(12, 86, dati.get('terminal_ind', ''))
    pdf.text(12, 91, dati.get('terminal_loc', ''))

    pdf.box_testo(12, 96, "Luogo scarico", dati.get('luogo_scarico', ''), font_valore=9)
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(12, 106, dati.get('scarico_ind', ''))
    pdf.text(12, 111, dati.get('scarico_loc', ''))

    pdf.box_testo(12, 116, "Merce", dati.get('merce', ''), font_valore=9)
    pdf.box_testo(12, 121, "KM", dati.get('km', ''), font_valore=9)

    pdf.box_testo(97, 46, "Vettore", dati.get('vettore_nome', ''), font_valore=10)
    pdf.set_font("Helvetica", "B", 9)
    pdf.text(97, 56, dati.get('vettore_ind', ''))
    pdf.text(175, 56, dati.get('vettore_piva', ''))
    
    pdf.box_testo(97, 65, "Autista", dati.get('autista', ''), font_valore=9)
    pdf.box_testo(97, 76, "Veicolo (Trattore / Rimorchio)", f"{dati.get('targa_trattore', '')}  /  {dati.get('targa_rimorchio', '')}", font_valore=10)
    pdf.box_testo(97, 85, "1° Container", dati.get('container_1', ''), font_valore=10)
    pdf.box_testo(97, 96, "Container tipo", dati.get('tipo_container', ''), font_valore=9)
    pdf.box_testo(155, 96, "Peso Tot.Kg", dati.get('peso', ''), font_valore=10)
    pdf.box_testo(97, 106, "Destinazione Porto / Spedizioniere", dati.get('spedizioniere', ''), font_valore=9)

    for i, y_start in enumerate([125, 145, 165]):
        num = i + 1
        pdf.box_testo(12, y_start + 1, f"{num}° Caricatore", "", font_valore=8)
        pdf.set_xy(105, y_start + 2)
        pdf.set_font("Helvetica", "", 7)
        pdf.cell(20, 3, "Ora arrivo")
        pdf.set_xy(140, y_start + 2)
        pdf.cell(20, 3, "Ora partenza")
        pdf.set_xy(175, y_start + 2)
        pdf.cell(20, 3, "Sigillo/i")

    pdf.box_testo(12, 186, "Osservazioni", "", font_valore=9)
    pdf.set_font("Helvetica", "", 8)
    pdf.text(12, 203, "DICHIARAZIONE RICEVITORE/DESTINATARIO")
    pdf.text(110, 203, "Constatato integro il sigillo ___________________ apposto mittente")
    pdf.text(110, 208, "Rimosso sigillo mittente e apposto sigillo      ___________________")

    condizioni = (
        "CONDIZIONI PARTICOLARI DI TRASPORTO\n"
        "Il trasporto va eseguito nel rispetto delle disposizioni legislative e regolamentari poste a tutela della sicurezza..."
    )
    pdf.set_xy(10, 215)
    pdf.set_font("Helvetica", "", 6)
    pdf.multi_cell(190, 3, condizioni)

    return pdf.output(dest='S')
