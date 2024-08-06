import pandas as pd

pair_data = pd.read_csv('pair_data_nf.csv')
accounting_data = pd.read_csv('accounting_quarterly.csv')
mkt_annual_data = pd.read_csv('mkt_annual.csv')

id_pair = list(set(pair_data['pair_id']))
print(f'{len(id_pair)} unique pairs.')

merged_data = pd.merge(pair_data, accounting_data,
                       left_on=['date_sample', 'cusips'],
                       right_on=['datadate', 'cusip'],
                       how='left')

id_pair = list(set(merged_data['pair_id']))
print(f'{len(id_pair)} unique pairs.')

accounting_data.columns = [f'{col}_o' for col in accounting_data.columns]
merged_data = pd.merge(merged_data, accounting_data,
                       left_on=['date_sample', 'cusip_o'],
                       right_on=['datadate_o', 'cusip_o'],
                       how='left')

merged_data = pd.merge(merged_data, mkt_annual_data,
                       left_on=['date_sample', 'cusips'],
                       right_on=['datadate', 'cusip'],
                       how='left')

mkt_annual_data.columns = [f'{col}_o' for col in mkt_annual_data.columns]
merged_data = pd.merge(merged_data, mkt_annual_data,
                       left_on=['date_sample', 'cusip_o'],
                       right_on=['datadate_o', 'cusip_o'],
                       how='left')

merged_data = merged_data.drop(columns=merged_data.filter(like='_y').columns)
merged_data = merged_data.drop(columns=merged_data.filter(like='_x').columns)

col_index = merged_data.columns.get_loc('cusip6_o')
col_to_fill = merged_data.columns[col_index+1:]
merged_data[col_to_fill] = merged_data.groupby('pair_id')[col_to_fill].fillna(method='ffill')

id_pair = list(set(merged_data['pair_id']))
print(f'{len(id_pair)} unique pairs.')
merged_data.to_csv('pair_data_nf_accounting.csv', index=False)