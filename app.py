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

# Sidebar - Configurations
with st.sidebar:
    st.header("⚙️ Groq Settings")
    api_key = st.text_input(
        "Groq API Key", 
        type="password", 
        value=os.getenv("GROQ_API_KEY", ""),# can be setted in .env file or can be directly setted in web
        help="Get a free key at console.groq.com"
    )
    
    st.divider()
    st.markdown("### 📝 Message Style")
    selected_tone = st.selectbox("Tone", ["Casual & Friendly", "Professional & Direct", "Empathetic"])
    selected_goal = st.selectbox("Goal", ["Check-in / Feedback", "Product Upsell", "Re-engage Inactive User"])

# Main View - Customer Table
st.subheader("👥 Customer Database")
df = get_customers_df()

selection = st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="multi-row"
)

selected_rows = selection.selection.get("rows",[])

# Execution Block
if len(selected_rows) > 0:
    st.success(f"Selected {len(selected_rows)} customer(s) for generation.")
    selected_df = df.iloc[selected_rows]
    
    if st.button("✨ Run Generation Pipeline", type="primary"):
        try:
            # Initialize Groq via our factory
            llm = get_groq_llm(api_key)
            prompt_template = get_followup_prompt()
            chain = prompt_template | llm
            
            st.subheader("📥 Generated Copy Drafts")
            
            for _, row in selected_df.iterrows():
                with st.spinner(f"Processing draft for {row['first_name']}..."):
                    response = chain.invoke({
                        "tone": selected_tone,
                        "goal": selected_goal,
                        "first_name": row['first_name'],
                        "company": row['company'],
                        "last_purchase_item": row['last_purchase_item'],
                        "days_inactive": row['days_since_last_interaction'],
                        "notes": row['customer_notes']
                    })
                    
                    with st.container(border=True):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.markdown(f"**Customer:** {row['first_name']}\n\n*{row['company']}*")
                        with col2:
                            st.text_area(
                                label="Draft (Editable)", 
                                value=response.content, 
                                height=340, 
                                key=f"text_{row['id']}"
                            )
        except Exception as e:
            st.error(f"Execution Error: {e}")
else:
    st.info("💡 Select rows using checkboxes in the table to queue messaging drafts.")