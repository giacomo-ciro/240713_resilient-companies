import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Resilient Companies",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://giacomo-ciro.github.io/',
        'Report a bug': "https://giacomo-ciro.github.io/",
        'About': "Resilient Companies"
    }
)

st.write('# Resilient Companies')
st.markdown(
    '''
    Below you can find the dataset used (retrieved from [Orbis](https://login.bvdinfo.com/R0/Orbis)) and some metadata.
    '''
)
df = pd.read_csv('./data/Orbis_processed.csv', index_col = 0, na_values='n.a.')
print(df.columns)
st.write(df)
df = df.rename(columns={
    'Company name Latin alphabet': 'Name',
    'US SIC, primary code(s)': 'SIC',
    'Operating profit (loss) [EBIT]\r\nm USD': 'EBIT',
    'Operating revenue (Turnover)\r\nm USD': 'Turnover',
    'Profit (loss) for the period [Net income]\r\nm USD': 'Profit',
    'Total equity\r\nm USD': 'Equity',
})
st.write(f'Shape: (`{df.shape[0]:,}`,`{df.shape[1]:,}`)')
st.write(f'Unique Companies: `{df.Name.unique().shape[0]:,}`')
df = df[['Name', 'SIC', 'Year', 'EBIT', 'Turnover', 'Profit', 'Equity']]

# Visualize Nulls
col1, col2, col3 = st.columns([1, 3, 1])  # Adjust the column widths as needed
with col2:
    temp = df.set_index('Year').copy()
    temp = temp.isna().astype(float).groupby(temp.index).sum().iloc[:, 2:]
    temp = temp / (df.shape[0] / 7) # number of observations per year
    temp['Year'] = temp.index
    fig, ax = plt.subplots(figsize=(15, 5))
    temp.plot(x='Year', kind='bar', title='Missing Values (%)', ax = ax)
    st.pyplot(fig)