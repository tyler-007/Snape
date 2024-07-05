import streamlit as st
import pandas as pd

issue_counts_list=['WB04J0909: Air Conditioner Issue: 5, Total: 5',
 'WB04J0915: Air Conditioner Issue: 3, L Mode: 1, Total: 4',
 'WB04J0935: Air Conditioner Issue: 3, Unknown: 1, Total: 4',
 'WB04J0946: Air Conditioner Issue: 1, Unknown: 2, Total: 3',
 'WB04J0957: Air Conditioner Issue: 1, L Mode: 2, Unknown: 2, Total: 5',
 'WB04J1042: Air Conditioner Issue: 2, Overheating Issue: 3, Total: 5',
 'WB04J2224: Air Conditioner Issue: 1, Underbody Noise: 1, Unknown: 1, Total: 3',
 'WB04J2235: Periodic Service: 1, Unknown: 2, Total: 3',
 'WB04J2298: Air Conditioner Issue: 2, Unknown: 1, Total: 3',
 'WB04J2328: Air Conditioner Issue: 1, Unknown: 3, Total: 4',
 'WB04J2459: Air Conditioner Issue: 3, Total: 3',
 'WB04J2466: Air Conditioner Issue: 1, Unknown: 2, Total: 3',
 'WB04J2477: Air Conditioner Issue: 1, Underbody Noise: 1, Unknown: 1, Total: 3',
 'WB04J2508: Air Conditioner Issue: 3, Total: 3',
 'WB04J2570: Underbody Noise: 2, Unknown: 1, Total: 3',
 'WB04J2582: Underbody Noise: 2, Unknown: 1, Total: 3',
 'WB04J2599: Overheating Issue: 2, Unknown: 1, Total: 3',
 'WB04J2606: Air Conditioner Issue: 1, Underbody Noise: 1, Unknown: 1, Total: 3',
 'WB05A0207: Underbody Noise: 1, Unknown: 2, Total: 3',
 'WB05A0221: Air Conditioner Issue: 1, L Mode: 2, Total: 3',
 'WB05A0224: Air Conditioner Issue: 2, DC Charging Issue: 1, Total: 3',
 'WB05A0235: Air Conditioner Issue: 2, Overheating Issue: 1, Total: 3',
 'WB05A0267: L Mode: 1, Unknown: 2, Total: 3',
 'WB05A0274: Unknown: 3, Total: 3',
 'WB05A0287: Air Conditioner Issue: 3, Total: 3',
 'WB05A0866: Air Conditioner Issue: 1, L Mode: 1, Periodic Service: 1, Total: 3',
 'WB05A0884: Air Conditioner Issue: 2, L Mode: 1, Total: 3',
 'WB05A0893: Air Conditioner Issue: 1, Periodic Service: 2, Total: 3',
 'WB05A0897: Air Conditioner Issue: 2, Overheating Issue: 1, Periodic Service: 2, Unknown: 1, Total: 6',
 'WB05A0928: Periodic Service: 1, Underbody Noise: 3, Total: 4',
 'WB05A0934: Air Conditioner Issue: 1, Periodic Service: 1, Total: 2',
 'WB05A0948: Air Conditioner Issue: 4, Total: 4',
 'WB05A1669: Air Conditioner Issue: 1, L Mode: 1, Overheating Issue: 1, Unknown: 1, Total: 4',
 'WB05A1744: Air Conditioner Issue: 1, Unknown: 2, Total: 3',
 'WB05A1899: Periodic Service: 1, Third Free Service: 1, Unknown: 1, Total: 3',
 'WB07K0251: Air Conditioner Issue: 3, Total: 3',
 'WB07K0262: Air Conditioner Issue: 2, DC Charging Issue: 1, Unknown: 1, Total: 4',
 'WB07K0265: Air Conditioner Issue, L Mode: 1, L Mode: 2, Total: 3',
 'WB07K0271: Air Conditioner Issue: 1, L Mode: 1, Underbody Noise, Air Conditioner Issue: 1, Total: 3',
 'WB07K0276: Air Conditioner Issue: 2, Underbody Noise, Air Conditioner Issue: 1, Total: 3',
 'WB07K0293: Air Conditioner Issue: 1, DC Charging Issue: 1, Underbody Noise: 1, Unknown: 1, Total: 4',
 'WB07K0298: DC Charging Issue: 2, L Mode: 1, Underbody Noise: 1, Total: 4',
 'WB07K0301: Underbody Noise: 1, Unknown: 3, Total: 4',
 'WB07K0314: Air Conditioner Issue: 1, DC Charging Issue: 2, Total: 3',
 'WB07K0324: L Mode: 1, Unknown: 3, Total: 4',
 'WB07K0336: Unknown: 4, Total: 4',
 'WB07K0361: Air Conditioner Issue: 3, L Mode: 1, Total: 4',
 'WB07K0369: AC Charging Issue: 1, Periodic Service: 1, Unknown: 1, Total: 3',
 'WB07K0455: L Mode: 3, Total: 3',
 'WB07K0461: Air Conditioner Issue: 2, Unknown: 2, Total: 4',
 'WB07K0465: Unknown: 3, Total: 3',
 'WB07K0484: Air Conditioner Issue: 3, Total: 3',
 'WB07K0490: DC Charging Issue: 1, Periodic Service: 1, Unknown: 1, Total: 3',
 'WB07K0495: Air Conditioner Issue: 2, L Mode: 1, Total: 3',
 'WB07K0497: Air Conditioner Issue: 1, DC Charging Issue: 1, L Mode: 1, Unknown: 2, Total: 5',
 'WB07K0502: DC Charging Issue: 1, L Mode: 2, Underbody Noise: 1, Unknown: 1, Total: 5',
 'WB07K0516: Air Conditioner Issue: 1, Underbody Noise: 1, Unknown: 2, Total: 4',
 'WB07K0520: Air Conditioner Issue: 3, Total: 3',
 'WB07K0523: DC Charging Issue: 1, L Mode: 4, Overheating Issue: 1, Total: 6',
 'WB07K0525: Air Conditioner Issue: 1, Air Conditioner Issue, L Mode: 1, DC Charging Issue: 1, Total: 3',
 'WB07K0527: Air Conditioner Issue: 1, Unknown: 2, Total: 3',
 'WB07K0543: Air Conditioner Issue: 1, L Mode: 1, Unknown: 1, Total: 3',
 'WB07K0547: Air Conditioner Issue: 2, L Mode: 1, Total: 3',
 'WB07K0549: Air Conditioner Issue, L Mode: 1, L Mode: 1, Unknown: 3, Total: 5',
 'WB07K0566: Air Conditioner Issue: 2, L Mode: 1, Total: 3',
 'WB07K0581: Air Conditioner Issue: 1, Periodic Service: 1, Unknown: 1, Total: 3',
 'WB07K0605: Air Conditioner Issue: 4, Periodic Service: 1, Total: 5',
 'WB07K0607: Air Conditioner Issue: 1, L Mode: 1, Periodic Service: 1, Total: 3',
 'WB07K0611: Air Conditioner Issue: 1, DC Charging Issue: 1, Unknown: 1, Total: 3',
 'WB07K0629: Air Conditioner Issue: 3, Total: 3',
 'WB07K0633: Air Conditioner Issue: 2, Periodic Service: 1, Total: 3',
 'WB07K0637: L Mode: 1, Periodic Service: 1, Unknown: 1, Total: 3',
 'WB07K0641: Air Conditioner Issue: 2, Periodic Service: 1, Total: 3',
 'WB07K0647: L Mode: 1, Unknown: 2, Total: 3',
 'WB07K1007: Air Conditioner Issue: 2, Unknown: 2, Total: 4',
 'WB07K1033: Air Conditioner Issue: 3, Underbody Noise: 1, Total: 4',
 'WB07K1044: Air Conditioner Issue: 2, L Mode: 2, Total: 4',
 'WB07K1101: L Mode: 2, Periodic Service: 1, Total: 3',
 'WB07K1110: L Mode: 2, Unknown: 1, Total: 3',
 'WB07K1157: Air Conditioner Issue: 1, L Mode: 1, Unknown: 1, Total: 3',
 'WB07K1161: Air Conditioner Issue: 2, Unknown: 1, Total: 3',
 'WB07K1175: Air Conditioner Issue: 1, Periodic Service: 1, Underbody Noise: 1, Total: 3',
 'WB07K1200: Air Conditioner Issue: 1, Periodic Service: 1, Unknown: 1, Total: 3',
 'WB07K1209: Air Conditioner Issue: 1, Periodic Service: 1, Underbody Noise: 1, Total: 3',
 'WB07K1226: Air Conditioner Issue: 2, L Mode: 2, Total: 4',
 'WB07K1227: Air Conditioner Issue: 3, Total: 3',
 'WB07K1236: Air Conditioner Issue: 2, Unknown: 1, Total: 3',
 'WB07K1247: Air Conditioner Issue: 5, Total: 5',
 'WB07K1262: Air Conditioner Issue: 1, L Mode: 1, Overheating Issue: 1, Total: 3',
 'WB07K1275: Air Conditioner Issue: 1, Underbody Noise, Air Conditioner Issue, L Mode: 1, Unknown: 2, Total: 4',
 'WB07K1443: Air Conditioner Issue: 1, Overheating Issue: 1, Unknown: 1, Total: 3',
 'WB07K1453: Air Conditioner Issue: 2, Periodic Service: 1, Total: 3',
 'WB07K1464: Air Conditioner Issue: 3, Total: 3',
 'WB07K1472: First Free Service: 1, Periodic Service: 2, Total: 3',
 'WB07K1476: L Mode: 2, Periodic Service: 1, Total: 3',
 'WB07K1477: Air Conditioner Issue: 1, L Mode: 1, Unknown: 3, Total: 5',
 'WB07K1499: Air Conditioner Issue: 1, L Mode: 1, Periodic Service: 2, Total: 4']

def filter_data_by_total(data, total):
    filtered_data = [entry for entry in data if f'Total: {total}' in entry]
    return filtered_data

def parse_entry(entry):
    parts = entry.split(': ')
    reg_num = parts[0]
    issues = ', '.join(parts[1:-1])
    total = parts[-1].split()[-1]
    return reg_num, issues, total

# Streamlit app
st.title('Vehicle Repair Issues Dashboard')

totals = [6, 5, 4, 3]  
selected_total = st.selectbox('Select Total', totals)

filtered_data = filter_data_by_total(issue_counts_list, selected_total)

# Create a DataFrame to display as a table
data = [parse_entry(entry) for entry in filtered_data]
df = pd.DataFrame(data, columns=['Registration Number', 'Issues', 'Total'])

st.write(f"Vehicles with Total: {selected_total}")
st.table(df)
