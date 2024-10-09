import pandas as pd
import numpy as np
import os
from functions import *
from je_functions import *
import streamlit as st

def main():
	# Streamlit file uploader
	uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

	if uploaded_file is not None:
		# Read the uploaded file into a DataFrame
		wo_df = pd.read_excel(uploaded_file)

		# Process the DataFrame through the functions
		first_df = add_unit_cost(wo_df)
		second_df = filter_out(first_df)
		third_df = billback(wo_df, first_df)
		fourth_df = map_charge_code(second_df)
		fifth_df = map_account(fourth_df)
		sixth_df = reformat(fifth_df, wo_df)
		seventh_df = add_tax(sixth_df, first_df)
		eighth_df = create_etl(third_df, seventh_df)

		# Export the processed DataFrame to a CSV file
		output_csv = 'october_billing_export.csv'
		eighth_df.to_csv(output_csv, index=False, header=True, mode='w')

		# Provide a download link for the CSV file
		st.success("ETL File processed successfully!")
		st.download_button(
			label="Download Yardi ETL File",
			data=open(output_csv, 'rb').read(),
			file_name=output_csv,
			mime='text/csv'
		)

		# Process the DataFrame through the second set of functions
		wo_df = pd.read_excel(uploaded_file)

		one_df = filter_charge_names(wo_df)
		two_df = map_expense(one_df)
		three_df = map_revenue(two_df)
		four_df = add_debit(three_df)
		five_df = sum_by_expense(three_df)
		six_df = merge_revenue(five_df, four_df)
		seven_df = map_revenue_accounts(six_df)
		eight_df = reformat_revenue(seven_df)
		nine_df = cost_of_sales_calculate(three_df)
		ten_df = map_cos(three_df)
		eleven_df = add_utility(ten_df)
		twelve_df = map_charge_code_to_cos(eleven_df)

		eight_df.name = 'Sales Revenue Accrual'
		twelve_df.name = 'Cost of Sales'

		writer = pd.ExcelWriter('Tenant_Sales.xlsx', engine='xlsxwriter')
		workbook = writer.book
		worksheet = workbook.add_worksheet('Entries')
		cell_format = workbook.add_format({'bold': False})
		writer.sheets['Entries'] = worksheet
		worksheet.write_string(0, 0, eight_df.name, cell_format)

		eight_df.to_excel(writer, sheet_name='Entries', startrow=1, startcol=0)
		worksheet.write_string(eight_df.shape[0] + 10, 0, twelve_df.name, cell_format)
		twelve_df.to_excel(writer, sheet_name='Entries', startrow=eight_df.shape[0] + 11, startcol=0)
		writer.close()

		# Provide a download link for the Excel file
		st.success("Journal Entry File processed successfully!")
		st.download_button(
			label="Download Journal Entry File",
			data=open('Tenant_Sales.xlsx', 'rb').read(),
			file_name='Tenant_Sales.xlsx',
			mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		)

if __name__ == "__main__":
	main()