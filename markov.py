import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from openpyxl import Workbook

# Load the Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Load your data
    data = pd.read_excel(uploaded_file)

    # Extract the relevant columns (excluding 'Year/Years' and 'Total')
    columns_to_exclude = ['Year', 'Years', 'Total']
    states = data.drop(columns=columns_to_exclude, errors='ignore')

    # Normalize the data to create transition probabilities
    transition_matrix = states.div(states.sum(axis=1), axis=0)

    # Ensure the transition matrix is square and has appropriate row and column names
    state_names = states.columns
    transition_matrix = transition_matrix.iloc[:len(state_names), :len(state_names)]
    transition_matrix.index = state_names
    transition_matrix.columns = state_names

    # Display the transition matrix
    st.write("Transition Probability Matrix:")
    st.dataframe(transition_matrix)

    # Create a heatmap with seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(transition_matrix, annot=True, fmt=".4f", cmap="coolwarm")
    plt.title("Transition Matrix Heatmap")
    plt.xlabel("To State")
    plt.ylabel("From State")

    # Display the heatmap in Streamlit
    st.pyplot(plt)

    # Export results to Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Transition Matrix"
    
    # Write the transition matrix to the Excel file
    for i, col in enumerate(transition_matrix.columns, 1):
        ws.cell(row=1, column=i + 1, value=col)
    for i, row in enumerate(transition_matrix.index, 2):
        ws.cell(row=i, column=1, value=row)
        for j, value in enumerate(transition_matrix.loc[row], 2):
            ws.cell(row=i, column=j, value=value)

    # Save Excel file
    output_filename = "Markov_Chain_Results.xlsx"
    wb.save(output_filename)

    # Offer download of the Excel file
    with open(output_filename, "rb") as file:
        btn = st.download_button(label="Download Results", data=file, file_name=output_filename)
