import pandas as pd

def filter_charge_names(df):

    revised_df = df[['Property Name', 'Charge Name', 'Charge Code', 'Tax Amount', 'Charge Amount', 'Markup Amount', 'Total']]
    revised_df = revised_df[~revised_df['Charge Name'].isin(['103 GeneralMaterial', '107 GeneralMaterial'])]
    return revised_df

def map_expense(df):

    df.loc[df['Charge Code'] == '(470-190-00) Engineering Labor', 'Expense'] = '47019000'
    df.loc[df['Charge Code'] == '(470-170-00) Elevator Labor', 'Expense'] = '47017000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Labor', 'Expense'] = '47015000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Supplies', 'Expense'] = '47015000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Elec Maint', 'Expense'] = '47019000'
    df.loc[df['Charge Code'] == '(000000) Protection - Photo IDs, Keys', 'Expense'] = '47015000'
    df.loc[df['Charge Code'] == '470-160-00 (rr)', 'Expense'] = '47016000'
    df.loc[df['Charge Code'] == '(470-210-00) Engineering OTAC', 'Expense'] = '47021000'
    df.loc[df['Charge Code'] == '470-160-00 (bc)', 'Expense'] = '47016000'
    df.loc[df['Charge Code'] == '(-) Steam', 'Expense'] = '47013000'
    df.loc[df['Charge Code'] == '(-) Engineering - Chilled/Cnd Water', 'Expense'] = '47019000'
    df.loc[df['Charge Code'] == '(470-210-00) 103EngineerOT', 'Expense'] = '47021000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Vendor', 'Expense'] = '47019000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Supplies', 'Expense'] = '47019000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Non Reit', 'Expense'] = '47019000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Vendor', 'Expense'] = '47015000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Other- Non Reit', 'Expense'] = '47015000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Locksmith - Non Reit', 'Expense'] = '47015000'
    df.loc[df['Charge Code'] == '(470-140-00) Water', 'Expense'] = '47014000'

    return df

def map_revenue(df):

    df.loc[df['Charge Code'] == '(470-190-00) Engineering Labor', 'Revenue'] = '31305000'
    df.loc[df['Charge Code'] == '(470-170-00) Elevator Labor', 'Revenue'] = '31303000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Labor', 'Revenue'] = '31301000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Supplies', 'Revenue'] = '31301000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Elec Maint', 'Revenue'] = '31305000'
    df.loc[df['Charge Code'] == '(000000) Protection - Photo IDs, Keys', 'Revenue'] = '31301000'
    df.loc[df['Charge Code'] == '470-160-00 (rr)', 'Revenue'] = '31302000'
    df.loc[df['Charge Code'] == '(470-210-00) Engineering OTAC', 'Revenue'] = '31307000'
    df.loc[df['Charge Code'] == '470-160-00 (bc)', 'Revenue'] = '31302000'
    df.loc[df['Charge Code'] == '(-) Steam', 'Revenue'] = '31202000'
    df.loc[df['Charge Code'] == '(-) Engineering - Chilled/Cnd Water', 'Revenue'] = '31306000'
    df.loc[df['Charge Code'] == '(470-210-00) 103EngineerOT', 'Revenue'] = '31307000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Vendor', 'Revenue'] = '31305000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Supplies', 'Revenue'] = '31305000'
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Non Reit', 'Revenue'] = '31305500'
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Vendor', 'Revenue'] = '31301000'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Other- Non Reit', 'Revenue'] = '31301500'
    df.loc[df['Charge Code'] == '(470-150-00) Protection Locksmith - Non Reit', 'Revenue'] = '31300500'
    df.loc[df['Charge Code'] == '(470-140-00) Water', 'Revenue'] = '31203000'

    return df

def sum_by_expense(df):
    print(df)
    df['Tax'] = '20430000'
    expense_df = df.groupby('Revenue')[['Charge Amount', 'Markup Amount', 'Tax Amount']].sum()
    expense_df.reset_index(inplace=True)
    expense_df['Credit'] = expense_df['Charge Amount'] + expense_df['Markup Amount']
    expense_df = expense_df[['Revenue', 'Credit']]
    expense_df['Debit'] = 0
    tax = df.groupby('Tax')['Tax Amount'].sum()
    tax_df = pd.DataFrame(data=tax)
    tax_df.reset_index(inplace=True)
    tax_df.columns = ['Revenue', 'Credit']
    tax_df['Debit'] = 0
    expensetax_df = pd.concat([expense_df, tax_df], ignore_index=True)

    return expensetax_df

def add_debit(df):

    debit = df['Total'].sum()
    debit_df = pd.DataFrame(
        {
            'Revenue': ['12001000'],
            'Debit': [debit],
            'Credit': 0
        }
    )

    return debit_df

def merge_revenue(df1, df2):

    revenueje_df = pd.concat([df1, df2], ignore_index=True)

    return revenueje_df

def map_revenue_accounts(df):

    df_copy = df.copy()

    # df_copy.loc[df_copy['Revenue'] == '31203000', 'Revenue Description'] = 'Utility sales - water'
    # df_copy.loc[df_copy['Revenue'] == '31202000', 'Revenue Description'] = 'Utility sales - steam'
    df_copy.loc[df_copy['Revenue'] == '31300500', 'Revenue Description'] = 'Non-REIT Sales - Locksmith'
    df_copy.loc[df_copy['Revenue'] == '31301000', 'Revenue Description'] = 'Service Sales - protection'
    df_copy.loc[df_copy['Revenue'] == '31301500', 'Revenue Description'] = 'Non-REIT Sales - Protection'
    df_copy.loc[df_copy['Revenue'] == '31302000', 'Revenue Description'] = 'Service Sales - cleaning'
    df_copy.loc[df_copy['Revenue'] == '31303000', 'Revenue Description'] = 'Service Sales - elevator'
    df_copy.loc[df_copy['Revenue'] == '31305000', 'Revenue Description'] = 'Service Sales - engineering'
    df_copy.loc[df_copy['Revenue'] == '31305500', 'Revenue Description'] = 'Non-REIT Sales - Engineering'
    df_copy.loc[df_copy['Revenue'] == '31307000', 'Revenue Description'] = 'Service Sales - OTAC'
    df_copy.loc[df_copy['Revenue'] == '12001000', 'Revenue Description'] = 'Accounts Receiveable'
    df_copy.loc[df_copy['Revenue'] == '31306000', 'Revenue Description'] = 'Service Sales - Chilled Water'
    df_copy.loc[df_copy['Revenue'] == '20430000', 'Revenue Description'] = 'Sales Tax'

    return df_copy

def reformat_revenue(df):

    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)

    final_revenueje_df = df[['Revenue', 'Revenue Description', 'Debit', 'Credit']]
    final_revenueje_df.name = "Sales Revenue Accrual"

    return final_revenueje_df

def cost_of_sales_calculate(df):

    cos_df = df.groupby('Expense')['Charge Amount'].sum().to_frame(name='Debit').reset_index()
    cos_df['Credit'] = 0
    return cos_df

def map_cos(df):

    df_copy = df.copy()

    df.loc[df['Charge Code'] == '(470-190-00) Engineering Labor', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-170-00) Elevator Labor', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Labor', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Supplies', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Elec Maint', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(000000) Protection - Photo IDs, Keys', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '470-160-00 (rr)', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-210-00) Engineering OTAC', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '470-160-00 (bc)', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(-) Engineering - Chilled/Cnd Water', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-210-00) 103EngineerOT', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Vendor', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-190-00) Engineering Supplies', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-190-00) Engineering - Non Reit', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-150-00) Protection - Vendor', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-150-00) Protection Other- Non Reit', 'Debit'] = df['Charge Amount']
    df.loc[df['Charge Code'] == '(470-150-00) Protection Locksmith - Non Reit', 'Debit'] = df['Charge Amount']
 

    add_to_cos_df = df.groupby('Expense')['Debit'].sum().to_frame(name='Debit').reset_index()
    add_to_cos_df['Credit'] = 0

    return add_to_cos_df

def add_utility(df):

    otac_df = df.loc[df['Expense'] == '47021000', ['Debit']]
    otac = list(otac_df['Debit'])[0]

    total = df['Debit'].sum()
    cos = total - otac 
    credit = [{'Expense': '40035000', 'Debit': 0, 'Credit': otac}, {'Expense': '40067000', 'Debit': 0, 'Credit': cos}]
    credit_df = pd.DataFrame(credit)
    df = pd.concat([df, credit_df])
    df['Debit'] = df['Debit'].astype(float)
    df['Credit'] = df['Credit'].astype(float)

    return df

def map_charge_code_to_cos(df):

    df.loc[df['Expense'] == '47021000', 'Expense Description'] = 'Service Sales - OTAC'
    df.loc[df['Expense'] == '47019000', 'Expense Description'] = 'Service Sales - engineering'
    df.loc[df['Expense'] == '47017000', 'Expense Description'] = 'Service Sales - elevator'
    df.loc[df['Expense'] == '47016000', 'Expense Description'] = 'Service Sales - cleaning'
    df.loc[df['Expense'] == '47015000', 'Expense Description'] = 'Service Sales - protection'
    df.loc[df['Expense'] == '47014000', 'Expense Description'] = 'Utility sales - Water'
    df.loc[df['Expense'] == '47013000', 'Expense Description'] = 'Utility sales - Steam'
    df.loc[df['Expense'] == '40012000', 'Expense Description'] = 'Water'
    df.loc[df['Expense'] == '40011000', 'Expense Description'] = 'Steam'
    df.loc[df['Expense'] == '40035000', 'Expense Description'] = 'OTAC'
    df.loc[df['Expense'] == '40067000', 'Expense Description'] = 'Applied to COS'

    cos_df = df[['Expense', 'Expense Description', 'Debit', 'Credit']]

    # cos_df = cos_df.drop(labels=0, axis=0)
    cos_df.name = 'Cost of Sales'

    return cos_df