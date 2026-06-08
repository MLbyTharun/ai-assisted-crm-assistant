import streamlit as st
import os
from src.database.db_manager import init_db, get_customers_df
from src.ai.llm_factory import get_groq_llm
from src.ai.prompts import get_followup_prompt
from dotenv import load_dotenv
# Initialize database
init_db()
load_dotenv()
st.set_page_config(page_title="Groq AI-CRM", layout="wide")
st.title("🤖 Groq AI CRM & Follow-Up Engine")

with st.sidebar():
    st.subheader("groq settings")
    api_key=st.text_input("Groq API Key",type="password",value=os.getenv("GROQ_API_KEY",""))
    
    st.divider()

    st.subheader("Message Style")
    
    selected_tone =st.selectbox("Tone",["cas","op2","op3"])
    selected_goal=st.selectbox("Goal",["op1","op2","op3"])

st.subheader("Customer DB")
selection = st.dataframe(
    df,
    use_container_width=True,
    selection_mode="multi-row"
)
selected_row = selection.selection.get("row",[])

if len(selected_row) > 0:
    selected_rows = df.iloc[selected_row]
    if st.button("Generate"):
        llm = get_groq_llm(api_key=api_key)
        prompt = get_followup_prompt()
        chain = llm | prompt
        for _, row in df.iterrows():
            response = chain.invoke({
                 "tone":selected_tone,
                 "Strategic Goal":selected_goal,
                 "first_name":row["first_name"],
                 "company":row["company"],
                 "last_purchase_item":row["last_purchase_item"],
                 "days_inactive":row["days_since_last_interaction"],
                 "notes":row["customer_notes"]
            }
            with st.container(border = True)
else:
    st.write("Select atleast 1 costumer")
