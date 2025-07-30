import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    all_sheets = pd.read_excel("Калории_и_Хранителни_вещества.xlsx", sheet_name=None)
    df = pd.concat(all_sheets.values(), ignore_index=True)
    df = df.dropna(subset=["Продукт"])
    return df

df_all = load_data()

st.title("Калкулатор на Калории и Хранителни Вещества")

product_names = sorted(df_all["Продукт"].unique())
num_rows = st.slider("Брой продукти", 1, 10, 3)
inputs = []

for i in range(num_rows):
    cols = st.columns([2, 1])
    with cols[0]:
        product = st.selectbox(f"Продукт {i+1}", product_names, key=f"product_{i}")
    with cols[1]:
        quantity = st.number_input(f"Количество (гр)", min_value=0.0, key=f"qty_{i}")
    inputs.append((product, quantity))

if st.button("Изчисли"):
    results = []
    for product, qty in inputs:
        row = df_all[df_all["Продукт"] == product]
        if not row.empty:
            r = row.iloc[0]
            results.append({
                "Продукт": product,
                "Грамаж": qty,
                "Калории": r["kcal/100g"] * qty / 100,
                "Белтъци": r["Белтъци (g)"] * qty / 100,
                "Мазнини": r["Мазнини (g)"] * qty / 100,
                "Въглехидрати": r["Въглехидрати (g)"] * qty / 100,
            })
    if results:
        df_result = pd.DataFrame(results)
        df_total = df_result[["Калории", "Белтъци", "Мазнини", "Въглехидрати"]].sum().to_frame().T
        st.subheader("Резултат по продукти")
        st.dataframe(df_result)
        st.subheader("Общо:")
        st.dataframe(df_total)
    else:
        st.warning("Моля, въведете поне един продукт с количество.")
