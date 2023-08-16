from scipy import stats
import streamlit as st
import pandas as pd
import plotly.express as px

st.header('Аттестация')

uploaded_file = st.file_uploader("Upload a .CSV dataset", type=([".csv"]))

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df, use_container_width=True)

    numerical = df.dtypes[df.dtypes == 'int64'] + df.dtypes[df.dtypes == 'float64']

    dropdown1 = st.selectbox(
        'First column',
        (df.columns.tolist()))

    if dropdown1 in numerical:
        fig1 = px.histogram(df, x=dropdown1)
    else:
        fig1 = px.pie(df, names=dropdown1)

    st.plotly_chart(fig1, use_container_width=True)

    dropdown2 = st.selectbox(
        'Second column',
        (df.columns.tolist()))

    if dropdown2 in numerical:
        fig2 = px.histogram(df, x=dropdown2)
    else:
        fig2 = px.pie(df, names=dropdown2)

    st.plotly_chart(fig2, use_container_width=True)

    st.title('Testing')

    testing_methods = ['Nothing', 'T test', 'Mann-Whitney U-test']

    testing_dd = st.selectbox(
        'Choose testing method',
        testing_methods
    )

    if testing_dd == testing_methods[0]:
        st.write('Select testing method')
    elif testing_dd == testing_methods[1] and (dropdown1 and dropdown2) in numerical:
        res = stats.ttest_ind(
            df[dropdown1], df[dropdown2],
            equal_var=False
        )
        st.write(f'P value: {res.pvalue}')
    elif testing_dd == testing_methods[2] and (dropdown1 and dropdown2) in numerical:
        res = stats.mannwhitneyu(
            df[dropdown1], df[dropdown2]
        )
        st.write(f'P value: {res.pvalue}')
    else:
        st.write('First or second column (or both) are not numeric')
