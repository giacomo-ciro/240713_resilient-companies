import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Data Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://giacomo-ciro.github.io/',
        'Report a bug': "https://giacomo-ciro.github.io/",
        'About': "Resilient Companies"
    }
)

df = pd.read_csv('../save/Orbis_final.csv', index_col = 0, na_values='n.a.')

st.write('# Pre-processing')
st.markdown(
    '''
    1) Due to high percentage of missing values, I decided to drop `Equity` for now;
    2) I use the first 2 digits of the SIC code to retrieve the industry macro-group and store it in the `Industry` variable;
    3) I use the available financial data to compute the following two metrics:
        - Growth Rate: `Growth = (Turnover_t1 - Turnover_t0) / Turnover_t0`  
        by construction, this is not available for the first year observed;
        - Operating Margin: `OM = EBIT / Turnover`;
    '''
)
st.write('### Final Dataset')
st.write(df)

col1, col2 = st.columns([1, 1])  # Adjust the column widths as needed
with col1:
    st.write('### Industry Group')
    fig, ax = plt.subplots(figsize=(15, 5))
    df.Industry.value_counts().plot(kind='pie', title='Industry Group', ax = ax)
    st.pyplot(fig)

with col2:
    st.write('### Operating Margin')
    fig, ax = plt.subplots(figsize=(15, 5))
    df.plot(x = 'Growth', y = 'OM', kind='scatter', title='Revenue Growth vs Operating Margin (filtered)', ax = ax)
    st.pyplot(fig)


st.write('# Break-away Analysis')
def is_above_industry_avg(x, metric, industry_avg):
    if x[metric] > industry_avg.loc[x.Industry, metric]:
        return 1
    else:
        return 0
col1, col2 = st.columns([1, 1])  # Adjust the column widths as needed
# BEFORE
with col1:
    st.write('### Before 2020')
    temp = df.loc[df.Year < 2020].copy()
    industry_avg = temp.groupby('Industry')[['OM', 'Growth']].mean()
    fig, ax = plt.subplots(figsize=(15, 5))
    industry_avg.plot(y = 'OM', kind = 'bar', stacked=True, title='Before 2020', ax = ax)
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(15, 5))
    industry_avg.plot(y = 'Growth', kind = 'bar', stacked=True, title='Before 2020', ax = ax)
    st.pyplot(fig)
    temp['OM_above'] = temp.apply(lambda x: is_above_industry_avg(x, 'OM', industry_avg), axis = 1)
    temp['Growth_above'] = temp.apply(lambda x: is_above_industry_avg(x, 'Growth', industry_avg), axis=1)
    temp = temp.groupby(['Name', 'Industry'])[['OM_above', 'Growth_above']].all()
    temp = temp.loc[(temp.OM_above == 1) & (temp.Growth_above == 1)]
    temp = temp.reset_index()
    st.write(temp.loc[:, ['Name', 'Industry']])
    st.write(f'Break-away companies: `{temp.shape[0]}` (`{temp.shape[0] / df.shape[0]:.4%}`)')
    fig, ax = plt.subplots(figsize=(15, 5))
    temp.reset_index().Industry.value_counts().plot(kind='bar', title='Industry Group', ax = ax)
    st.pyplot(fig)

# AFTER
with col2:
    st.write('### After 2020')
    temp = df.loc[df.Year > 2020].copy()
    industry_avg = temp.groupby('Industry')[['OM', 'Growth']].mean()
    fig, ax = plt.subplots(figsize=(15, 5))
    industry_avg.plot(y = 'OM', kind = 'bar', stacked=True, title='After 2020', ax = ax)
    st.pyplot(fig)
    fig, ax = plt.subplots(figsize=(15, 5))
    industry_avg.plot(y = 'Growth', kind = 'bar', stacked=True, title='After 2020', ax = ax)
    st.pyplot(fig)
    temp['OM_above'] = temp.apply(lambda x: is_above_industry_avg(x, 'OM', industry_avg), axis = 1)
    temp['Growth_above'] = temp.apply(lambda x: is_above_industry_avg(x, 'Growth', industry_avg), axis=1)
    temp = temp.groupby(['Name', 'Industry'])[['OM_above', 'Growth_above']].all()
    temp = temp.loc[(temp.OM_above == 1) & (temp.Growth_above == 1)]
    temp = temp.reset_index()
    st.write(temp.loc[:, ['Name', 'Industry']])
    st.write(f'Break-away companies: `{temp.shape[0]}` (`{temp.shape[0] / df.shape[0]:.4%}`)')
    fig, ax = plt.subplots(figsize=(15, 5))
    temp.reset_index().Industry.value_counts().plot(kind='bar', title='Industry Group', ax = ax)
    st.pyplot(fig)

st.write('# Resilient Companies')
st.markdown(
    '''
    Companies are now classified in one of the following categories:
    '''
)
breakaway_before = pd.read_csv('../save/breakaway_before.csv', index_col = 0)
breakaway_after = pd.read_csv('../save/breakaway_after.csv', index_col = 0)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown(
        '''
        ### Resilient
        Break-away companies both _before_ and _after_ 2020
        '''
    )
    st.write(breakaway_before.loc[breakaway_before.Name.isin(breakaway_after.Name), 'Name'])

with col2:
    st.markdown(
        '''
        ### New-breakaways
        Break-away companies _after_ but _not before_ 2020
        '''
    )
    st.write(breakaway_after.loc[~breakaway_after.Name.isin(breakaway_before.Name), 'Name'])

with col3:
    st.markdown(
        '''
        ### Non-resilient
        Break-away companies _before_ but _not after_ 2020
        '''
    )
    st.write(breakaway_before.loc[~breakaway_before.Name.isin(breakaway_after.Name), 'Name'])