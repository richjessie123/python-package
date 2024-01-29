import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, image_path, product_id, product_name, amount_purchased,
             price_per_unit, total_price):
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Invoice nr{invoice_nr}", align="L", ln=1)

        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Date: {date}", align="L", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Add a header
        column_headers = list(df.columns)
        column_headers = [item.replace("_", " ").title() for item in column_headers]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=column_headers[0], border=1)
        pdf.cell(w=65, h=8, txt=column_headers[1], border=1)
        pdf.cell(w=35, h=8, txt=column_headers[2], border=1)
        pdf.cell(w=30, h=8, txt=column_headers[3], border=1)
        pdf.cell(w=30, h=8, txt=column_headers[4], border=1, ln=1)

        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=65, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=35, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        total_sum = df[total_price].sum()

        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=65, h=8, txt="", border=1)
        pdf.cell(w=35, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        # Add Total Price Text
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)

        # Add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt="PythonHow")
        pdf.image(image_path, w=10)

        os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
