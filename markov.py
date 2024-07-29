import streamlit as st
import pandas as pd
import numpy as np

st.title("Transitional Probability Matrix / Markov Chain Analysis")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df.head())

    # Select the column containing the states (countries/crop names)
    state_column = st.selectbox("Select the state column", df.columns)

    # Select the year column
    year_column = st.selectbox("Select the year column", df.columns)

    if state_column and year_column:
        # Ensure the data is sorted by year
        df = df.sort_values(by=year_column)

        # Create the state transition pairs
        state_pairs = list(zip(df[state_column][:-1], df[state_column][1:]))

        # Create the transition matrix
        unique_states = df[state_column].unique()
        transition_matrix = pd.DataFrame(0, index=unique_states, columns=unique_states)

        for (current_state, next_state) in state_pairs:
            transition_matrix.loc[current_state, next_state] += 1

        # Convert counts to probabilities
        transition_matrix = transition_matrix.div(transition_matrix.sum(axis=1), axis=0)

        st.write("Transitional Probability Matrix:")
        st.write(transition_matrix)

        # Provide an option to download the transition matrix
        @st.cache_data
        def convert_df(df):
            return df.to_csv().encode('utf-8')

        csv = convert_df(transition_matrix)

        st.download_button(
            label="Download Transition Matrix as CSV",
            data=csv,
            file_name='transition_matrix.csv',
            mime='text/csv',
        )
