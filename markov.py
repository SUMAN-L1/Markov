import streamlit as st
import pandas as pd
import numpy as np

# Load data
data = pd.read_excel('/mnt/data/MARKOV_SILK.xlsx')

# Exclude "Year" and "World" columns
data = data.drop(columns=['Year', 'World'])

# Define the countries (excluding "World")
countries = data.columns.tolist()

# Normalize the data to get transition probabilities
transitions = data.diff().dropna().apply(lambda x: x > 0).astype(int)

# Calculate transition probability matrix
transition_matrix = np.zeros((len(countries), len(countries)))

for i in range(len(countries)):
    for j in range(len(countries)):
        if i != j:
            transition_matrix[i, j] = transitions.iloc[:, j][transitions.iloc[:, i] == 1].sum() / transitions.iloc[:, i].sum()

# Fill diagonal with probabilities of staying in the same state
for i in range(len(countries)):
    transition_matrix[i, i] = 1 - transition_matrix[i].sum()

# Create DataFrame for the transition matrix
transition_matrix_df = pd.DataFrame(transition_matrix, index=countries, columns=countries)

# Round to 4 decimals
transition_matrix_df = transition_matrix_df.round(4)

# Streamlit app
st.title('Markov Chain Analysis of Silk Production')

st.write('## Transitional Probability Matrix')
st.dataframe(transition_matrix_df)

# Optional: download button for the matrix
csv = transition_matrix_df.to_csv().encode('utf-8')
st.download_button(
    label="Download Transition Matrix as CSV",
    data=csv,
    file_name='transition_matrix.csv',
    mime='text/csv',
)
