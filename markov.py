import streamlit as st
import pandas as pd

st.title("Transitional Probability Matrix / Markov Chain Analysis")

# Upload file
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

def load_data(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx') or file.name.endswith('.xls'):
        return pd.read_excel(file)
    else:
        return None

if uploaded_file is not None:
    # Read the file
    df = load_data(uploaded_file)
    if df is not None:
        st.write("Data Preview:")
        st.write(df.head())

        # Exclude 'Year' and 'World' columns from analysis
        if 'Year' in df.columns and 'World' in df.columns:
            df = df.drop(columns=['Year', 'World'])

        # Create state transition pairs
        transitions = []
        for i in range(len(df) - 1):
            for col in df.columns:
                current_state = df.iloc[i][col]
                next_state = df.iloc[i + 1][col]
                transitions.append((current_state, next_state))

        # Get unique states
        unique_states = list(set(df.values.flatten()))
        unique_states.sort()

        # Initialize transition matrix
        transition_matrix = pd.DataFrame(0, index=unique_states, columns=unique_states)

        # Populate transition matrix with counts
        for (current_state, next_state) in transitions:
            transition_matrix.loc[current_state, next_state] += 1

        # Convert counts to probabilities
        transition_matrix = transition_matrix.div(transition_matrix.sum(axis=1), axis=0).fillna(0)
        transition_matrix = transition_matrix.applymap(lambda x: round(x, 4))

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
    else:
        st.error("The uploaded file format is not supported.")
