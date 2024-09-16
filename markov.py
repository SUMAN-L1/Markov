import streamlit as st
import pandas as pd
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

    # Adding annotations with specific font size for better visibility
    sns.heatmap(transition_matrix, annot=True, fmt=".4f", cmap="coolwarm", annot_kws={"size": 10}, linewidths=0.5, linecolor='black')

    plt.title("Transition Matrix Heatmap", fontsize=16)
    plt.xlabel("To State", fontsize=12)
    plt.ylabel("From State", fontsize=12)

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
    The heatmap shows transition probabilities between different states. The numbers in each cell represent the exact probability of moving from one state (row) to another state (column).

    **Key Interpretation Points:**
    - Higher probabilities indicate a stronger likelihood of transitioning to a particular state.
    - Each row shows the probability distribution from a specific current state, giving you an idea of future behavior.
    - Use this matrix to identify dominant state transitions or areas where probabilities are very low, suggesting infrequent transitions.

    This tool helps analyze the dynamics between different categories or states over time, providing insight into patterns and potential areas for improvement or change.
    """)

