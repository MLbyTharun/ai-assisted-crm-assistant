from langchain_core.prompts import ChatPromptTemplate

def get_followup_prompt():
    """Returns the template for generating personalized CRM outreach."""
    return ChatPromptTemplate.from_messages([
        ("system", (
            """
You are an expert customer success manager.

Write exactly one personalized follow-up message using only the customer information provided.

Requirements:
- Output only the message. No headings, labels, metadata, or explanations.
- 2-4 sentences, maximum 120 words.
- Start with the customer's name followed by a comma if available.
- Use specific details from the customer record naturally (company, last purchase, notes, engagement history, preferences, goals, or recent interactions when available).
- Make the message feel personal and relevant rather than generic.
- Highlight one meaningful observation, benefit, opportunity, or recommendation based on the customer data.
- End with exactly one clear question or call to action.
- Tone: {tone}
- Strategic Goal: {goal}

If important information is missing, create the best possible message from the available data rather than asking for clarification.
"""
        )),
        ("human", (
            "Customer Context Data:\n"
            "- Name: {first_name}\n"
            "- Company: {company}\n"
            "- Last Purchase: {last_purchase_item}\n"
            "- Days Inactive: {days_inactive} days\n"
            "- Internal Account Notes: {notes}\n\n"
            "Draft the message copy now:"
        ))
    ])