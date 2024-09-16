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
    plt.figure(figsize=(12, 10))
    sns.heatmap(transition_matrix, annot=True, fmt=".4f", cmap="viridis", linewidths=0.5, linecolor='black')
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

    # Interpretation
    st.subheader("Heatmap Interpretation")
    st.write("""
    The heatmap visualizes the transition probabilities between different states. The cells in the heatmap represent the likelihood of transitioning from one state to another. 
    - **Higher Values**: Indicate a higher probability of transitioning to that state from the current state.
    - **Lower Values**: Indicate a lower probability of transitioning to that state.

    **Key Points to Note:**
    - Each row represents the current state, and each column represents the next state.
    - The color gradient from dark purple to bright yellow represents the range of probabilities, with darker colors indicating lower probabilities and lighter colors indicating higher probabilities.
    - The exact probability values are displayed on the heatmap, providing precise information on transition likelihoods.

    By analyzing this heatmap, you can infer which states have strong tendencies to transition into other states and identify any patterns or anomalies in state transitions.
    """)
