import streamlit as st
import pandas as pd
import io
import openai

# Set your OpenAI API key here



st.title('CSV Processor with GPT')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Original Data:")
    st.write(df)

    if st.button('Process with GPT'):
        processed_df = gpt_process_data(df)
        st.write("Processed Data:")
        st.write(processed_df)

        # Create a download button for the processed CSV
        csv = processed_df.to_csv(index=False)
        st.download_button(
            label="Download processed data as CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv",
        )