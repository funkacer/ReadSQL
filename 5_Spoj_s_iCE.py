import pandas as pd
pd.options.display.max_columns = 999

from okno import zobraz

#ID záznamu      Datum         ECC                                   volajici_s1_text

names = ["ID záznamu", "Datum záznamu", "PARTNER", "volajici_s1_text"]
#dtypes = {'col1': 'str', 'col2': 'str', 'col3': 'str', 'col4': 'float', 'col5': 'float', 'col6': 'float'}
dtypes = {"ID záznamu":'int64', "Datum záznamu":'str', "PARTNER":'int64', "volajici_s1_text":'str'}
#parse_dates = ['col1', 'col2']
parse_dates = ['Datum záznamu']

#data_prepisy_df = pd.read_csv("3_prepis_data_OP.csv", encoding = "utf-8", sep = ";", index_col = 2)
data_prepisy_df = pd.read_csv("3_prepis_data_OP.csv", encoding = "utf-8", sep = ";", header = 1, names = names, dtype = dtypes, parse_dates = parse_dates)
print(data_prepisy_df.head())
#udela to same tak proc to tam je ???
print(data_prepisy_df[:10])

print(data_prepisy_df.dtypes)
print("Přepisy počet: ", len(data_prepisy_df.index))

zobraz(data_prepisy_df.to_string())

indexes_prepisy = list(data_prepisy_df.index)
print(indexes_prepisy[:10])

#quit()

# nejdelší
#print(data.loc[36400587, 'volajici_s1_text'][:100])
#print(type(data.loc[36400587, 'volajici_s1_text']))

#headers = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6'] Číslo OP
names = ["ID dotazníku", "Datum vyplnění", "Metoda sběru dat", "PARTNER", "Důvod ne/spokojenosti", "NPS", "UNOR", "DATUM", "DIFF", "DIFFABS", "detraktor"]
#dtypes = {'col1': 'str', 'col2': 'str', 'col3': 'str', 'col4': 'float', 'col5': 'float', 'col6': 'float'}
dtypes = {"ID dotazníku":'int64', "Datum vyplnění":'str', "Metoda sběru dat":'str', "PARTNER":'int64', "Důvod ne/spokojenosti":'str', "NPS":'int64', "UNOR":'str', "DATUM":'str', "DIFF":'int64', "DIFFABS":'int64', "detraktor":'int64'}
#parse_dates = ['col1', 'col2']
parse_dates = ['Datum vyplnění', 'UNOR', 'DATUM']

#data_detraktori_df = pd.read_csv("4_priprava_detraktori_OP.csv", encoding = "utf-8", sep = ";", index_col = ["Číslo OP"])
data_detraktori_df = pd.read_csv("4_priprava_detraktori_OP.csv", encoding = "utf-8", sep = ";", header = 1, names = names, dtype = dtypes, parse_dates = parse_dates)

#data = pd.read_csv("priprava_churn_final_2019_JC_utf8_vyber.csv", encoding = "utf-8", sep = ";", dtype =  {"Číslo OP": "str"} )
#data = pd.read_csv("priprava_churn_final_2019_JC_utf8_vyber.csv", encoding = "utf-8", sep = ";", index_col = 3)
#data_df = pd.read_csv(filepath, encoding = "utf-8", sep = ";", parse_dates=["Datum vyplnění"])

print(data_detraktori_df.head())

print(data_detraktori_df.dtypes)
print("ICE počet: ", len(data_detraktori_df.index))

zobraz(data_detraktori_df.to_string())

indexes_detraktori = list(data_detraktori_df.index)
print(indexes_detraktori[:10])

data_df = data_prepisy_df.merge(data_detraktori_df, how = "inner", left_on = "PARTNER", right_on = "PARTNER")

print(data_df.head())
print("Merge počet: ", len(data_df.index))
print("Merge detraktoři počet: ", data_df["detraktor"].sum())

zobraz(data_df.to_string())

#data_df.to_csv("5_final.csv", encoding = "utf-8", sep = ";")

print("\nDone")
input("Enter = konec")
