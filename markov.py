import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from markovchain import MarkovChain
from sklearn.preprocessing import normalize

# Function to normalize the data to create transition probabilities
def create_transition_matrix(data):
    transition_matrix = data.div(data.sum(axis=1), axis=0)
    return transition_matrix

# Function to plot the heatmap using seaborn and matplotlib
def plot_heatmap(transition_matrix, state_names):
    plt.figure(figsize=(10, 8))
    sns.heatmap(transition_matrix, annot=True, fmt=".4f", cmap="coolwarm", xticklabels=state_names, yticklabels=state_names)
    plt.title("Transition Matrix Heatmap", fontsize=16, fontweight='bold')
    plt.xlabel("To State", fontsize=14, fontweight='bold')
    plt.ylabel("From State", fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig("transition_matrix_heatmap.png")
    st.pyplot(plt)

# Function to export transition matrix and heatmap to Excel
def export_to_excel(transition_matrix, state_names):
    wb = Workbook()
    ws = wb.active
    ws.title = "Transition Matrix"
    
    # Write transition matrix to Excel
    for i, row in enumerate(state_names):
        ws.cell(row=i+2, column=1, value=row)
        for j, col in enumerate(state_names):
            ws.cell(row=1, column=j+2, value=col)
            ws.cell(row=i+2, column=j+2, value=transition_matrix.loc[row, col])
    
    # Add heatmap image
    img = Image("transition_matrix_heatmap.png")
    ws.add_image(img, "J1")
    
    wb.save("Markov_Chain_Results.xlsx")

# Streamlit app interface
st.title("Markov Chain Analysis")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type="xlsx")

if uploaded_file:
    # Load data
    data = pd.read_excel(uploaded_file)
    
    # Exclude 'Year' and 'Total' columns
    columns = [col for col in data.columns if col.lower() not in ['year', 'years', 'total']]
    
    if columns:
        # Extract relevant columns (states)
        states = data[columns]
        st.write(f"Selected columns: {columns}")
        
        # Normalize the data to create the transition matrix
        transition_matrix = create_transition_matrix(states)
        state_names = columns
        
        # Display the transition matrix
        st.subheader("Transition Probability Matrix")
        st.dataframe(transition_matrix)
        
        # Plot heatmap
        plot_heatmap(transition_matrix, state_names)
        
        # Export results to Excel
        export_to_excel(transition_matrix, state_names)
        
        st.success("Analysis complete! Results exported to 'Markov_Chain_Results.xlsx'.")
        
        # Interpretation
        st.subheader("Interpretation")
        st.write("""
        The transition probability matrix shows the likelihood of transitioning from one state to another. 
        Higher values indicate a stronger probability of transitioning to the corresponding state.
        The heatmap provides a visual representation of these probabilities, with color intensity representing the magnitude of the probability.
        """)
