import pandas as pd

# In the current pair_data I have more than 4000 pairs while having only 921 before.

old_shares_owned = pd.read_csv('../(8) Prep for Fabrice (Mature2)/shares_owned_clean')
new_shares_owned = pd.read_csv('../17_data_new/shares_owned')

print(len(old_shares_owned))  # 278145
print(len(new_shares_owned))  # 665507

# (1) The old scrapping work did miss some pairs. Example: Advanced Refractive Tech (007635105)/Utek corp (109842)
# (2) Compustat data sent to Fabrice did remove all cik not present in shares_owned_clean. However, some cik where
# missing in compustat. Example: Acces Midstream (0043L109)/Williams Companies Inc. (107263)
# (3) In other cases, the market value is missing while the shares outstanding is present.
# Example: Digimarc Corp (25381B101)/ Koninklijke (313216)
# or OncoMed Pharmaceuticals (68234X102)/GLAXOSMITHKLINE PLC (1131399)
# The case (3) might do the heavy lifting.
