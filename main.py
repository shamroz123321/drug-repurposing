import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Drug Repurposing for Disease Treatment",
    page_icon="💊",
    layout="wide"
)

# Title and description
st.title("Drug Repurposing for Disease Treatment")
st.markdown("Enter an immune disease name to get recommended drugs, their mechanisms of action, targets, and clinical phases.")

def preprocess_data(df):
    df = df.dropna(subset=['indication'])
    df = df.assign(indication=df['indication'].str.split('|')).explode('indication')
    df = df.assign(disease_area=df['disease_area'].str.replace('/', '|')).explode('disease_area')
    return df

# Function to load data (replace with your actual data loading logic)
@st.cache_data
def load_drug_data():
    df = pd.read_csv('./data.csv')
    df = preprocess_data(df)
    return df

drug_data = load_drug_data()

# Main input
disease_input = st.text_input("Enter disease name:", "Rheumatoid Arthritis")

# Filter data based on input
if disease_input:
    filtered_data = drug_data[drug_data["indication"].str.lower() == disease_input.lower()]
    
    # Display results
    if not filtered_data.empty:
        st.success(f"Found {len(filtered_data)} drugs for {disease_input}")
        
        # Display drugs in a table
        st.subheader("Recommended Drugs")
        similar = filtered_data.rename(columns={"pert_iname": "Drug Name", "clinical_phase": "Clinical Phase", "moa": "Mechanism of Action", "target": "Target"})
        similar = similar[["Drug Name", "Clinical Phase", "Mechanism of Action", "Target"]].reset_index(drop=True)
        similar.index += 1
        st.dataframe(similar)

        # Display MOA distribution
        st.subheader("MOA Distribution for Recommended Drugs")
        moa_counts = similar["Mechanism of Action"].value_counts().reset_index()
        moa_counts.columns = ["Mechanism of Action", "Count"]
        top_5_moa = moa_counts.head(5)
        # fig = px.bar(similar, x="Mechanism of Action", title=f"MOA for {disease_input} Drugs")
        fig = px.bar(
            top_5_moa, 
            x="Mechanism of Action", 
            y="Count",
            title=f"Top 5 MOA for {disease_input} Drugs"
        )
        st.plotly_chart(fig)
        
    else:
        st.warning(f"No drugs found for {disease_input}. Please try another disease.")

# Footer
st.markdown("---")
st.markdown("""
            This is a drug repurposing application for immune diseases.
            Built by:
            - Shamroz Khanum    (23MSI0172)
            - Sijenna G         (23MSI0153)
            - B Mahalakshmi	    (23MSI0129)
            - Shree Varsha.A.R	(23MSI0164)
            """)
