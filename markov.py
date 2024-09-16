import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from markovchain import MarkovChain
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Function to create transition matrix
def create_transition_matrix(data):
    transition_matrix = data.div(data.sum(axis=1), axis=0).T
    return transition_matrix

# Function to plot heatmap
def plot_heatmap(matrix, state_names):
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, fmt=".4f", cmap="coolwarm", xticklabels=state_names, yticklabels=state_names)
    plt.title("Transition Matrix Heatmap")
    plt.xlabel("To State")
    plt.ylabel("From State")
    plt.xticks(rotation=45, ha='right', fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig("transition_matrix_heatmap.png")
    st.pyplot(plt)

# Function to export results to Excel
def export_to_excel(transition_matrix, state_names):
    wb = Workbook()
    ws = wb.active
    ws.title = "Transition Matrix"
    
    # Write transition matrix
    for i, state in enumerate(state_names):
        ws.cell(row=1, column=i+2, value=state)
        ws.cell(row=i+2, column=1, value=state)
        for j, value in enumerate(transition_matrix[i]):
            ws.cell(row=i+2, column=j+2, value=value)
    
    # Add heatmap image
    img = Image("transition_matrix_heatmap.png")
    ws.add_image(img, "J1")
    
    wb.save("Markov_Chain_Results.xlsx")

# Streamlit app
st.title("Markov Chain Analysis by Suman_Econ")

# File upload
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    
    # Select columns
    columns = st.multiselect("Select columns for analysis (excluding 'Total' and 'Years')", data.columns)
    if columns:
        data_selected = data[columns]
        
        # Create transition matrix
        transition_matrix = create_transition_matrix(data_selected)
        state_names = columns
        
        # Plot heatmap
        plot_heatmap(transition_matrix, state_names)
        
        # Create Markov chain object
        mc = MarkovChain(transition_matrix, state_names)
        
        # Export results to Excel
        export_to_excel(transition_matrix, state_names)
        
        st.success("Analysis complete! Results exported to 'Markov_Chain_Results.xlsx'.")

        # Interpretation
        st.subheader("Interpretation")
        st.write("""
        The transition matrix heatmap shows the probabilities of transitioning from one state to another. 
        The rows represent the current state, and the columns represent the next state. 
        Higher values indicate a higher probability of transitioning to that state.
        
        The Markov chain object created can be used to predict future states based on the current state.
        For example, if you start in a particular state, you can use the transition matrix to determine the probability of moving to other states in the next time period.
        """)
