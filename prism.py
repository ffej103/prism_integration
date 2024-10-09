import pandas as pd

wo_df = pd.read_excel('103 workordercharge-export.xlsx')

# Recreate DataFrame with only necessary columns
revised_wo_df = wo_df[['Property Name', 'Requested For Company ID', 'Bill To', 'Charge Code', 'Charge Name', 'Tax Amount']]
revised_wo_df['Unit Cost'] = wo_df['Charge Amount'] + wo_df['Markup Amount']
revised_df = revised_wo_df[~revised_wo_df['Charge Name'].isin(['103 GeneralMaterial', '107 GeneralMaterial'])]

# Separate out BillBack
gen_mat_wo_df = wo_df[['Property Name', 'Requested For Company ID', 'Bill To', 'Charge Code', 'Charge Name', 'Total']]
gen_mat_df = gen_mat_wo_df.loc[revised_wo_df['Charge Name'].isin(['103 GeneralMaterial', '107 GeneralMaterial'])]

gen_mat_group_df = gen_mat_df.groupby('Requested For Company ID')['Total'].sum()

gen_mat_tenant_df = gen_mat_df[['Property Name', 'Requested For Company ID', 'Charge Code', 'Charge Name']]
gen_mat_export_df = pd.merge(gen_mat_tenant_df, gen_mat_group_df, on ='Requested For Company ID', how='inner').drop_duplicates()
gen_mat_export_df['Charge_Code'] = 'billback'
gen_mat_export_df['Account'] = '12003000'

gen_mat_export_df.columns = ['Property', 'Lease_Code', 'ChargeCode', 'Notes', 'Amount', 'Charge_Code', 'Account']
print(gen_mat_export_df)

# Map Charge Codes
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering Labor', 'Charge_Code'] = 'svceng'
revised_df.loc[revised_df['Charge Code'] == '(470-170-00) Elevator Labor', 'Charge_Code'] = 'svcelev'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection - Labor', 'Charge_Code'] = 'svcprot'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection - Supplies', 'Charge_Code'] = 'svcprot'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering Elec Maint', 'Charge_Code'] = 'svceng'
revised_df.loc[revised_df['Charge Code'] == '(000000) Protection - Photo IDs, Keys', 'Charge_Code'] = 'svcprot'
revised_df.loc[revised_df['Charge Code'] == '470-160-00 (rr)', 'Charge_Code'] = 'svcclean'
revised_df.loc[revised_df['Charge Code'] == '(470-210-00) Engineering OTAC', 'Charge_Code'] = 'svcotac'
revised_df.loc[revised_df['Charge Code'] == '470-160-00 (bc)', 'Charge_Code'] = 'svcclean'
revised_df.loc[revised_df['Charge Code'] == '(-) Steam', 'Charge_Code'] = 'stmsales'
revised_df.loc[revised_df['Charge Code'] == '(-) Engineering - Chilled/Cnd Water', 'Charge_Code'] = 'chlwater'
revised_df.loc[revised_df['Charge Code'] == '(470-210-00) 103EngineerOT', 'Charge_Code'] = 'svceng'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering - Vendor', 'Charge_Code'] = 'svceng'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering Supplies', 'Charge_Code'] = 'svceng'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering - Non Reit', 'Charge_Code'] = 'engineer'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection - Vendor', 'Charge_Code'] = 'protct'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection Other- Non Reit', 'Charge_Code'] = 'protct'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection Locksmith - Non Reit', 'Charge_Code'] = 'locksmth'
revised_df.loc[revised_df['Charge Code'] == '(470-140-00) Water', 'Charge_Code'] = 'wtrsales'

# Map Account Codes
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering Labor', 'Account'] = '31305000'
revised_df.loc[revised_df['Charge Code'] == '(470-170-00) Elevator Labor', 'Account'] = '31303000'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection - Labor', 'Account'] = '31301000'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection - Supplies', 'Account'] = '31301000'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering Elec Maint', 'Account'] = '31305000'
revised_df.loc[revised_df['Charge Code'] == '(000000) Protection - Photo IDs, Keys', 'Account'] = '31301000'
revised_df.loc[revised_df['Charge Code'] == '470-160-00 (rr)', 'Account'] = '31302000'
revised_df.loc[revised_df['Charge Code'] == '(470-210-00) Engineering OTAC', 'Account'] = '31307000'
revised_df.loc[revised_df['Charge Code'] == '470-160-00 (bc)', 'Account'] = '31302000'
revised_df.loc[revised_df['Charge Code'] == '(-) Steam', 'Account'] = '31202000'
revised_df.loc[revised_df['Charge Code'] == '(-) Engineering - Chilled/Cnd Water', 'Account'] = '31306000'
revised_df.loc[revised_df['Charge Code'] == '(470-210-00) 103EngineerOT', 'Account'] = '31305000'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering - Vendor', 'Account'] = '31305000'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering Supplies', 'Account'] = '31305000'
revised_df.loc[revised_df['Charge Code'] == '(470-190-00) Engineering - Non Reit', 'Account'] = '31305500'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection - Vendor', 'Account'] = '31301500'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection Other- Non Reit', 'Account'] = '31301500'
revised_df.loc[revised_df['Charge Code'] == '(470-150-00) Protection Locksmith - Non Reit', 'Account'] = '31300500'
revised_df.loc[revised_df['Charge Code'] == '(470-140-00) Water', 'Account'] = '31203000'

revised_df['Concat'] = wo_df['Requested For Company ID'].astype(str) + revised_df['Charge Name']
revised_df.columns = ['Property', 'Lease_Code', 'Tenant', 'ChargeCode', 'Notes', 'Tax', 'Amount', 'Charge_Code', 'Account', 'Concat']
charge_df = revised_df[['Lease_Code', 'Notes', 'Concat', 'Amount', 'Tax']]

tax_df =  charge_df.groupby('Lease_Code')['Tax'].sum()
charge_grouped_df = charge_df.groupby('Concat')['Amount'].sum()

tenant_df = revised_df[['Property', 'Lease_Code', 'Notes', 'Concat','Charge_Code', 'Account']]
tenant_tax_df = revised_df[['Property', 'Lease_Code']]
tenant_tax_df['Charge_Code'] = pd.Series(['Tax' for x in range(len(revised_wo_df.index))])

export_df = pd.merge(tenant_df, charge_grouped_df, on='Concat', how='inner').drop_duplicates()

tax_df = tax_df.to_frame()
tax_df.rename(columns={'Tax':'Amount'}, inplace=True)
print(type(tax_df['Amount']))
tax_export_df = pd.merge(tenant_tax_df, tax_df, on='Lease_Code', how='inner').drop_duplicates()
cost_export_df = export_df[['Property', 'Lease_Code', 'Notes', 'Charge_Code', 'Amount', 'Account']]
tax_export_df['Account'] = '20430000'
tax_export_df['Notes'] = 'Tax'

append_export_df = pd.concat([cost_export_df, tax_export_df]).sort_values(by=['Lease_Code'])
etl_df = pd.concat([gen_mat_export_df, append_export_df]).sort_values(by=['Lease_Code'])

etl_df.loc[etl_df['Property'] == '1271 Avenue of the Americas', 'Property_Code'] = '103'
etl_df.loc[etl_df['Property'] == '1221 Avenue of the Americas', 'Property_Code'] = '107'

# final_etl_df = etl_df.reindex(columns=['Property_Code', 'Lease_Code', 'Schedule_From_Date', 'Schedule_To_Date', 'Charge_Code', 'Price',	'Quantity', 'Amount', 'Amount_Period', 'Estimate_Type', 'Currency', 'Ref_Property_Id', 'Ref_Lease_Id', 'Mgmt_Fee_Code',	'Mgmt_Fee_Percentage', 'Sales_Tax_Code', 'Sales_Tax_Percentage', 'Description', 'Rent_Increase_Start_Date', 'Rent_Increase_End_Date', 'Invoice_Frequency', 'Bill_Day', 'Days_Due', 'Days_Due_After_Method',	'Unit_code', 'Area_column_overide',	'Bill_Jan',	'Bill_Feb',	'Bill_Mar',	'Bill_Apr',	'Bill_May',	'Bill_Jun',	'Bill_Jul',	'Bill_Aug',	'Bill_Sep',	'Bill_Oct',	'Bill_Nov',	'Bill_Dec',	'Last_Day_Of_Period	Subject_To_Late_Fee	Ninety_Day_Due_Date	Rent_Increase_Type', 'Rent_Increase_Value',	'Who_Initiates', 'Earliest_Notice_Date', 'Latest_Notice_Date',	'Max_Days_To_Dispute',	'Max_Days_To_Negotiate_New_Rent	Max_Days_To_Appoint_Valuer', 'Max_Days_To_Deliver_Valuation', 'Third_Party', 'Arbitrator_Referred_By', 'Min_Increase_Type', 'Min_Increase_Value	Max_Increase_Type', 'Max_Increase_Value', 'Market_Rent', 'Settlement_Rent', 'Settlement_Date', 'Notice_Served_Date', 'Market_Review_Notes', 'CPI_Index1_Code', 'CPI_Min_Percent', 'CPI_Max_Percent', 'Min_Decrease_Amount', 'CPI_CPI_2_Ratio_Percentage', 'Fixed_Percent', 'Index_Month', 'Base_month',	'Index_Interval', 'Index_Date', 'CPI_Increase_Factor', 'CPI_Increase_Type', 'CPI_Index2_Code', 'Index_Method', 'Decrease_Possible', 'Number_Of_Months_Before_Index_Month', 'CPI_Breakpoint_1', 'CPI_Breakpoint_2', 'CPI_Breakpoint_3', 'CPI_Breakpoint_4', 'CPI_Breakpoint_5', 'CPI_Index_Step_1_Percent', 'CPI_Index_Step_2_Percent', 'CPI_Index_Step_3_Percent', 'CPI_Index_Step_4_Percent', 'CPI_Index_Step_5_Percent', 'Next_Increase_Interval', 'Next_Increase_Date_After', 'Check_Annually', 'Increase_As_Point', 'Step_Indexation', 'LI_Charge_Code', 'LI_Correction_Percentage', 'Rounding', 'Scandinavian_Indexation', 'Proration_Method', 'Method_Of_Payment', 'Sales_Tran_Type', 'TaxPoint_Day', 'Bill_In_Arrears', 'Set_Invoice_Date_To_Due_Date', 'Suppress_Paper_Invoice', 'Print_Invoice_On_Change',	'Invoice_Is_LeaseCurrency', 'Vat_Currency_Is_Local', 'Payment_Schedule', 'Rate_Provider', 'Rate_Type', 'Do_Not_Bill', 'Do_Not_Bill_Before',	'GL_Segment_1', 'GL_Segment_2', 'GL_Segment_3', 'GL_Segment_4', 'Late_Fee_Grace_Period', 'Late_Fee_Interest_Free_Period', 'LateFeeCalculationType', 'LateFeeCalculationBasis', 'Charge_On_Unpaid', 'Days_in_year', 'LateFeeInterestIndex_Code', 'LateFeePercentage', 'LateFeeFactor', 'LateFeeAdjustment', 'LateFeeMinThreshold', 'LateFeeMaxThreshold', 'LateFeeMinPercentage', 'LateFeeMaxPercentage', 'Additional_Fee', 'Amendment_Type', 'Amendment_Sequence', 'Parent_Amendment_Type', 'Parent_Amendment_Sequence', 'Proposal_Type', 'EFT', 'Notes', 'Date_Last_Billed', 'Userdefined_1', 'Userdefined_2', 'Userdefined_3', 'Userdefined_4', 'Userdefined_5', 'Userdefined_6', 'Userdefined_7', 'Userdefined_8', 'Userdefined_9', 'Userdefined_10', 'Userdefined_11', 'Userdefined_12', 'Userdefined_13', 'Userdefined_14', 'Userdefined_15', 'Userdefined_16', 'Userdefined_17', 'Userdefined_18', 'Userdefined_19', 'Userdefined_20', 'Estimated_Rent', 'Review_Type', 'Ext_Schedule_Id'])
final_etl_df= etl_df.reindex(columns=['Property_Code',	'Lease_Code',	'Rate_Code',	'Schedule_From_Date',	'Schedule_To_Date',	'Charge_Code',	'Price',	'Quantity',	'Amount',	'Amount_Period',	'Estimate_Type',	'Currency',	'Ref_property_Id',	'Ref_lease_Id',	'Ref_Rate_Id',	'Mgmt_Fee_Code',	'Mgmt_Fee_Percentage',	'Sales_Tax_Code',	'Sales_Tax_Percentage',	'Description',	'Rent_Increase_Start_Date',	'Rent_Increase_End_Date',	'Invoice_Frequency',	'Bill_Day',	'Days_Due',	'Days_Due_After_Method',	'Unit_Code',	'Area_column_overide',	'Bill_Jan',	'Bill_Feb',	'Bill_Mar',	'Bill_Apr',	'Bill_May',	'Bill_Jun',	'Bill_Jul',	'Bill_Aug',	'Bill_Sep',	'Bill_Oct',	'Bill_Nov',	'Bill_Dec',	'Last_Day_of_Period',	'Subject_To_Late_Fee',	'Rent_Increase_Type',	'Rent_Increase_Value',	'Who_Initiates',	'Earliest_Notice_Date',	'Latest_Notice_Date',	'Max_Days_To_Dispute',	'Max_Days_To_Negotiate_New_Rent',	'Max_Days_To_Appoint_Valuer',	'Max_Days_To_Deliver_Valuation',	'Third_Party',	'Arbitrator_Referred_by',	'Min_Increase_Type',	'Min_Increase_Value',	'Max_Increase_Type',	'Max_Increase_Value',	'Market_Rent',	'Settlement_Rent',	'Settlement_Date',	'Notice_served_Date',	'Market_Review_Notes',	'CPI_Index1_Code',	'CPI_Min_Percent',	'CPI_Max_Percent',	'CPI_CPI_2_Ratio_Percentage',	'Fixed_Percent',	'Index_Month',	'Base_month',	'Index_Interval',	'Index_Date',	'Next_Increase_Date_After',	'CPI_Increase_Factor',	'CPI_Increase_Type',	'CPI_Index2_Code',	'Index_Method',	'Decrease_Possible',	'Number_of_Months_before_Index_Month',	'CPI_Breakpoint_1',	'CPI_Breakpoint_2',	'CPI_Breakpoint_3',	'CPI_Breakpoint_4',	'CPI_Breakpoint_5',	'CPI_Index_Step_1_Percent',	'CPI_Index_Step_2_Percent',	'CPI_Index_Step_3_Percent',	'CPI_Index_Step_4_Percent',	'CPI_Index_Step_5_Percent',	'Next_Increase_Interval',	'Check_Annually',	'Increase_As_Point',	'Step_Indexation',	'LI_Charge_Code',	'LI_Correction_Percentage',	'Rounding',	'Scandinavian_Indexation',	'Proration_Method',	'Method_Of_Payment',	'Sales_Tran_Type',	'TaxPoint_Day',	'Bill_In_Arrears',	'Set_Invoice_Date_To_Due_Date',	'Suppress_paper_Invoice',	'Print_Invoice_On_Change',	'Invoice_Is_LeaseCurrency',	'Vat_Currency_Is_Local',	'Payment_Schedule',	'Rate_provider',	'Rate_Type',	'Min_Exchange_Rate',	'Do_not_Bill',	'Do_not_Bill_Before',	'GL_Segment_1',	'GL_Segment_2',	'GL_Segment_3',	'GL_Segment_4',	'Late_Fee_Grace_Period',	'Late_Fee_Interest_Free_Period',	'LateFeeCalculationType',	'LateFeeCalculationBasis',	'LateFeeInterestIndex_Code',	'Charge_On_Unpaid',	'Days_In_Year',	'LateFeePercentage',	'LateFeeFactor',	'LateFeeAdjustment',	'LateFeeMinThreshold',	'LateFeeMaxThreshold',	'LateFeeMinPercentage',	'LateFeeMaxPercentage',	'Additional_Fee',	'Amendment_Type',	'Amendment_Sequence',	'Parent_Amendment_Type',	'Parent_Amendment_Sequence',	'Amendment_Start_Date',	'Proposal_Type',	'EFT',	'Notes',	'Date_Last_Billed',	'Userdefined_1',	'Userdefined_2',	'Userdefined_3',	'Userdefined_4',	'Userdefined_5',	'Userdefined_6',	'Userdefined_7',	'Userdefined_8',	'Userdefined_9',	'Userdefined_10',	'Userdefined_11',	'Userdefined_12',	'Userdefined_13',	'Userdefined_14',	'Userdefined_15',	'Userdefined_16',	'Userdefined_17',	'Userdefined_18',	'Userdefined_19',	'Userdefined_20',	'Estimated_Rent',	'Review_Type',	'Ninety_Day_Due_Date',	'Ext_Schedule_Id'])


final_etl_df['Schedule_From_Date'] = '05-01-2024'
final_etl_df['Schedule_To_Date'] = '05-31-2024'
final_etl_df['Amount_Period'] = 2
final_etl_df['Estimate_Type'] = 2

final_etl_df.to_csv('export.csv',index=False,header=True,mode='w')
# charge_grouped_df.to_csv('charges.csv',index=True,header=True,mode='w')