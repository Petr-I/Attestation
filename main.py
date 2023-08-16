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

    dropdown_1 = st.selectbox(
        'First column for visualisation',
        (df.columns.tolist()))

    if dropdown_1 in numerical:
        fig1 = px.histogram(df, x=dropdown_1)
    else:
        fig1 = px.pie(df, names=dropdown_1)

    st.plotly_chart(fig1, use_container_width=True)

    dropdown_2 = st.selectbox(
        'Second column for visualisation',
        (df.columns.tolist()))

    if dropdown_2 in numerical:
        fig2 = px.histogram(df, x=dropdown_2)
    else:
        fig2 = px.pie(df, names=dropdown_2)

    st.plotly_chart(fig2, use_container_width=True)

    st.title('Testing')

    testing_methods = ['Nothing', 'T test', 'Mann-Whitney U-test']

    testing_dd = st.selectbox(
        'Choose testing method',
        testing_methods
    )

    categor = []
    for i in df.columns.values.tolist():
        if i in numerical:
            continue
        else:
            categor.append(i)

    categor_column = st.selectbox(
        'Select a categorical column to test the hypothesis',
        categor
    )

    categor_perem = st.multiselect(
        f'Select 2 column values {categor_column}',
        df[categor_column].unique(), max_selections=2
    )

    if len(categor_perem) == 2:
        value_dropdown = st.selectbox(
            f'Select the column by which to compare {categor_perem[0]} and {categor_perem[1]}',
            [column for column in df if isinstance(df[column][0], int) or isinstance(df[column][0], float)], key='1'
        )

        if testing_dd == testing_methods[0]:
            st.write('Select testing method')
        elif testing_dd == testing_methods[1]:
            res = stats.ttest_ind(
                df[df[categor_column] == categor_perem[0]][value_dropdown],
                df[df[categor_column] == categor_perem[1]][value_dropdown],
                equal_var=False
            )
            st.write(f'P value: {res.pvalue}')
        elif testing_dd == testing_methods[2]:
            res = stats.mannwhitneyu(
                df[df[categor_column] == categor_perem[0]][value_dropdown],
                df[df[categor_column] == categor_perem[1]][value_dropdown]
            )
            st.write(f'P value: {res.pvalue}')
