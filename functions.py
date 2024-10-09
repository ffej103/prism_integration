import pandas as pd

wo_df = pd.read_excel("107_workordercharge-export.xlsx")

def add_unit_cost(df):
    revised_wo_df = df[['Property Name', 'Requested For Company ID', 'Bill To', 'Charge Name', 'Charge Code', 'Tax Amount']]
    revised_wo_df['Unit Cost'] = df['Charge Amount'] + df['Markup Amount']
    return revised_wo_df

def filter_out(df):
    revised_df = df[~df['Charge Name'].isin(['103 GeneralMaterial', '107 GeneralMaterial', 'chlwater'])]
    revised_df = revised_df[~revised_df['Charge Code'].isin(['(-) Engineering - Chilled/Cnd Water'])]     
    return revised_df

def billback(df, df2):
    gen_mat_wo_df = df[['Property Name', 'Requested For Company ID', 'Bill To', 'Charge Name', 'Charge Code', 'Total']]
    gen_mat_df = gen_mat_wo_df.loc[df2['Charge Name'].isin(['103 GeneralMaterial', '107 GeneralMaterial'])]
    gen_mat_group_df = gen_mat_df.groupby('Requested For Company ID')['Total'].sum()
    gen_mat_tenant_df = gen_mat_df[['Property Name', 'Requested For Company ID', 'Charge Code']]
    gen_mat_export_df = pd.merge(gen_mat_tenant_df, gen_mat_group_df, on ='Requested For Company ID', how='inner').drop_duplicates()
    gen_mat_export_df['Charge Code'] = 'billback'
    gen_mat_export_df['Account'] = '12003000'
    gen_mat_export_df.columns = ['Property', 'LeaseNo', 'ChargeCode', 'UnitPrice', 'Account']
    gen_mat_export_df = gen_mat_export_df[['Property', 'LeaseNo', 'ChargeCode', 'UnitPrice', 'Account']]
    return gen_mat_export_df

# def chilwater(df, df2):
#     chlwater_wo_df = df[['Property Name', 'Requested For Company ID', 'Bill To', 'Charge Code', 'Total']]
#     chlwater_df = chlwater_wo_df.loc[df2['Charge Code'].isin(['(-) Engineering - Chilled/Cnd Water'])]
#     chlwater_df['Charge_Code'] = 'chlwater'   
#     chlwater_df = chlwater_df[['Property Name', 'Requested For Company ID', 'Charge_Code', 'Total']]
#     chlwater_df['account'] = '31306000'
#     chlwater_df.columns = ['Property', 'LeaseNo', 'ChargeCode', 'UnitPrice', 'Account']
#     chlwater_df['Concat'] = chlwater_df['LeaseNo'].astype(str) + chlwater_df['UnitPrice'].astype(str)
#     chillwtr_df = pd.read_excel("chillwtr.xlsx")
#     chillwtr_df['Concat'] = chillwtr_df['Concat'].astype(str)
#     chlwtr_join_df = pd.merge(chillwtr_df, chlwater_df, on='Concat')
#     chlwtr_join_df = chlwtr_join_df.drop_duplicates()
#     return chlwtr_join_df

def map_charge_code(df):
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Labor', 'ChargeCode'] = 'svceng'
    df.loc[df['Charge Code'] == '(470-170-00) Elevator Labor', 'ChargeCode'] = 'svcelev'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Labor', 'ChargeCode'] = 'svcprot'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Supplies', 'ChargeCode'] = 'svcprot'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Elec Maint', 'ChargeCode'] = 'svceng'
    df.loc[df['Charge Code'] == '(000000) Protection - Photo IDs, Keys', 'ChargeCode'] = 'svcprot'
    df.loc[df['Charge Code'] == '470-160-00 (rr)', 'ChargeCode'] = 'svcclean'
    df.loc[df['Charge Code'] == '(470-210-00) Engineering OTAC', 'ChargeCode'] = 'svcotac'
    df.loc[df['Charge Code'] == '470-160-00 (bc)', 'ChargeCode'] = 'svcclean'
    df.loc[df['Charge Code'] == '(-) Steam', 'ChargeCode'] = 'stmsales'
    df.loc[df['Charge Code'] == '(-) Engineering - Chilled/Cnd Water', 'ChargeCode'] = 'chlwater'
    df.loc[df['Charge Code'] == '(470-210-00) 103EngineerOT', 'ChargeCode'] = 'svceng'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Vendor', 'ChargeCode'] = 'svceng'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Supplies', 'ChargeCode'] = 'svceng'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Non Reit', 'ChargeCode'] = 'engineer'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Vendor', 'ChargeCode'] = 'protct'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Other- Non Reit', 'ChargeCode'] = 'protct'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Locksmith - Non Reit', 'ChargeCode'] = 'locksmth'
    df.loc[df['Charge Code'] == '(470-140-00) Water', 'ChargeCode'] = 'wtrsales'
    return df

def map_account(df):
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Labor', 'Account'] = '31305000'
    df.loc[df['Charge Code'] == '(470-170-00) Elevator Labor', 'Account'] = '31303000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Labor', 'Account'] = '31301000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Supplies', 'Account'] = '31301000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Elec Maint', 'Account'] = '31305000'
    df.loc[df['Charge Code'] == '(000000) Protection - Photo IDs, Keys', 'Account'] = '31301000'
    df.loc[df['Charge Code'] == '470-160-00 (rr)', 'Account'] = '31302000'
    df.loc[df['Charge Code'] == '(470-210-00) Engineering OTAC', 'Account'] = '31307000'
    df.loc[df['Charge Code'] == '470-160-00 (bc)', 'Account'] = '31302000'
    df.loc[df['Charge Code'] == '(-) Steam', 'Account'] = '31202000'
    df.loc[df['Charge Code'] == '(-) Engineering - Chilled/Cnd Water', 'Account'] = '31306000'
    df.loc[df['Charge Code'] == '(470-210-00) 103EngineerOT', 'Account'] = '31305000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Vendor', 'Account'] = '31305000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Supplies', 'Account'] = '31305000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Non Reit', 'Account'] = '31305500'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Vendor', 'Account'] = '31301500'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Other- Non Reit', 'Account'] = '31301500'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Locksmith - Non Reit', 'Account'] = '31300500'
    df.loc[df['Charge Code'] == '(470-140-00) Water', 'Account'] = '31203000'
    return df

def reformat(df1, df2):
    df1['Concat'] = df2['Requested For Company ID'].astype(str) + df1['ChargeCode']
    df1 = df1[['Property Name', 'Requested For Company ID', 'Bill To', 'Charge Code', 'Tax Amount', 'Unit Cost', 'ChargeCode', 'Account', 'Concat']]
    df1.columns = ['Property', 'LeaseNo', 'Tenant', 'Charge Code', 'TaxAmount', 'UnitPrice', 'ChargeCode', 'Account', 'Concat']
    return df1

def add_tax(df1, df2):
    cost_df = df1[['LeaseNo','Concat', 'UnitPrice', 'TaxAmount']]
    cost_group_df = cost_df.groupby('Concat')['UnitPrice'].sum()
    tax_df = cost_df.groupby('LeaseNo')['TaxAmount'].sum()
    tenant_df = df1[['Property', 'LeaseNo', 'Concat', 'ChargeCode', 'Account']]
    tenant_tax_df = df1[['Property', 'LeaseNo']]
    tenant_tax_df['ChargeCode'] = pd.Series(['tsaletx' for x in range(len(df2.index))])
    export_df = pd.merge(tenant_df, cost_group_df, on ='Concat', how='inner').drop_duplicates()
    tax_export_df = pd.merge(tenant_tax_df, tax_df, on = 'LeaseNo', how= 'inner').drop_duplicates()
    cost_export_df = export_df[['Property', 'LeaseNo', 'ChargeCode', 'UnitPrice', 'Account']]
    tax_export_df.rename(columns={'TaxAmount':'UnitPrice'}, inplace=True)
    tax_export_df['Account'] = '20430000'
    append_export_df = pd.concat([cost_export_df, tax_export_df]).sort_values(by=['LeaseNo'])
    return append_export_df

def create_etl(df1, df2):
    append_export_df = pd.concat([df1, df2]).sort_values(by=['LeaseNo'])
    append_export_df['UnitCode'] = ''
    amendment_type_df = pd.read_excel('amendmenttype.xlsx')
    final_append_export_df = pd.merge(append_export_df, amendment_type_df, on='LeaseNo')
    # final_append_export_df = pd.concat([append_export_df, df3]).sort_values(by=['LeaseNo'])
    final_append_export_df.loc[final_append_export_df['Property'] == '1271 Avenue of the Americas', 'Property_Code'] = '103'
    final_append_export_df.loc[final_append_export_df['Property'] == '1221 Avenue of the Americas', 'Property_Code'] = '107'
    final_append_export_df.rename(columns={'LeaseNo': 'Lease_Code', 'ChargeCode': 'Charge_Code', 'UnitPrice': 'Amount'}, inplace=True)
    final_etl_df = final_append_export_df.reindex(columns=['Property_Code',	'Lease_Code',	'Rate_Code',	'Schedule_From_Date',	'Sfchedule_To_Date',	'Charge_Code',	'Price',	'Quantity',	'Amount',	'Amount_Period',	'Estimate_Type',	'Currency',	'Ref_property_Id',	'Ref_lease_Id',	'Ref_Rate_Id',	'Mgmt_Fee_Code',	'Mgmt_Fee_Percentage',	'Sales_Tax_Code',	'Sales_Tax_Percentage',	'Description',	'Rent_Increase_Start_Date',	'Rent_Increase_End_Date',	'Invoice_Frequency',	'Bill_Day',	'Days_Due',	'Days_Due_After_Method',	'Unit_Code', 'Area_column_overide',	'Bill_Jan',	'Bill_Feb',	'Bill_Mar',	'Bill_Apr',	'Bill_May',	'Bill_Jun',	'Bill_Jul',	'Bill_Aug',	'Bill_Sep',	'Bill_Oct',	'Bill_Nov',	'Bill_Dec',	'Last_Day_of_Period',	'Subject_To_Late_Fee',	'Rent_Increase_Type',	'Rent_Increase_Value',	'Who_Initiates',	'Earliest_Notice_Date',	'Latest_Notice_Date',	'Max_Days_To_Dispute',	'Max_Days_To_Negotiate_New_Rent',	'Max_Days_To_Appoint_Valuer',	'Max_Days_To_Deliver_Valuation',	'Third_Party',	'Arbitrator_Referred_by',	'Min_Increase_Type',	'Min_Increase_Value',	'Max_Increase_Type',	'Max_Increase_Value',	'Market_Rent',	'Settlement_Rent',	'Settlement_Date',	'Notice_served_Date',	'Market_Review_Notes',	'CPI_Index1_Code',	'CPI_Min_Percent',	'CPI_Max_Percent',	'CPI_CPI_2_Ratio_Percentage',	'Fixed_Percent',	'Index_Month',	'Base_month',	'Index_Interval',	'Index_Date',	'Next_Increase_Date_After',	'CPI_Increase_Factor',	'CPI_Increase_Type',	'CPI_Index2_Code',	'Index_Method',	'Decrease_Possible',	'Number_of_Months_before_Index_Month',	'CPI_Breakpoint_1',	'CPI_Breakpoint_2',	'CPI_Breakpoint_3',	'CPI_Breakpoint_4',	'CPI_Breakpoint_5',	'CPI_Index_Step_1_Percent',	'CPI_Index_Step_2_Percent',	'CPI_Index_Step_3_Percent',	'CPI_Index_Step_4_Percent',	'CPI_Index_Step_5_Percent',	'Next_Increase_Interval',	'Check_Annually',	'Increase_As_Point',	'Step_Indexation',	'LI_Charge_Code',	'LI_Correction_Percentage',	'Rounding',	'Scandinavian_Indexation',	'Proration_Method',	'Method_Of_Payment',	'Sales_Tran_Type',	'TaxPoint_Day',	'Bill_In_Arrears',	'Set_Invoice_Date_To_Due_Date',	'Suppress_paper_Invoice',	'Print_Invoice_On_Change',	'Invoice_Is_LeaseCurrency',	'Vat_Currency_Is_Local',	'Payment_Schedule',	'Rate_provider',	'Rate_Type',	'Min_Exchange_Rate',	'Do_not_Bill',	'Do_not_Bill_Before',	'GL_Segment_1',	'GL_Segment_2',	'GL_Segment_3',	'GL_Segment_4',	'Late_Fee_Grace_Period',	'Late_Fee_Interest_Free_Period',	'LateFeeCalculationType',	'LateFeeCalculationBasis',	'LateFeeInterestIndex_Code',	'Charge_On_Unpaid',	'Days_In_Year',	'LateFeePercentage',	'LateFeeFactor',	'LateFeeAdjustment',	'LateFeeMinThreshold',	'LateFeeMaxThreshold',	'LateFeeMinPercentage',	'LateFeeMaxPercentage',	'Additional_Fee',	'Amendment_Type',	'Amendment_Sequence',	'Parent_Amendment_Type',	'Parent_Amendment_Sequence',	'Amendment_Start_Date',	'Proposal_Type',	'EFT',	'Notes',	'Date_Last_Billed',	'Userdefined_1',	'Userdefined_2',	'Userdefined_3',	'Userdefined_4',	'Userdefined_5',	'Userdefined_6',	'Userdefined_7',	'Userdefined_8',	'Userdefined_9',	'Userdefined_10',	'Userdefined_11',	'Userdefined_12',	'Userdefined_13',	'Userdefined_14',	'Userdefined_15',	'Userdefined_16',	'Userdefined_17',	'Userdefined_18',	'Userdefined_19',	'Userdefined_20',	'Estimated_Rent',	'Review_Type',	'Ninety_Day_Due_Date',	'Ext_Schedule_Id'])
    final_etl_df['Schedule_From_Date'] = '09-01-2024'
    final_etl_df['Schedule_To_Date'] = '09-30-2024'
    final_etl_df['Amount_Period'] = 2
    final_etl_df['Estimate_Type'] = 2
    final_etl_df['Currency'] = 'usd'
    final_etl_df['Rent_Increase_Start_Date'] = '09-01-2024'
    final_etl_df['Rent_Increase_End_Date'] = '09-30-2024'
    return final_etl_df