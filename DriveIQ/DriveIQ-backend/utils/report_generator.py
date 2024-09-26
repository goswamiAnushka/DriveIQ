from fpdf import FPDF
import pandas as pd

def generate_pdf_report(driver_data, output):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)

    pdf.cell(200, 10, f'Driver Report - {driver_data["name"]}', ln=True)
    pdf.cell(200, 10, f'Total Trips: {driver_data["total_trips"]}', ln=True)
    pdf.cell(200, 10, f'Average Score: {driver_data["average_score"]}', ln=True)

    pdf.set_font('Arial', '', 12)
    for trip in driver_data['trips']:
        pdf.cell(200, 10, f'Trip ID: {trip["trip_id"]} | Score: {trip["score"]}', ln=True)

    pdf.output(output)

def generate_excel_report(driver_data, output):
    df = pd.DataFrame(driver_data['trips'])
    df.to_excel(output, index=False)
