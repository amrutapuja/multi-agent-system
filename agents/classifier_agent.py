
#model_name="gpt-4o-mini", openai_api_key="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")  # Replace with your API key

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from datetime import datetime

llm = OpenAI(temperature=0.2,model_name="gpt-3.5-turbo", openai_api_key="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")  # Replace with your API key

# Few-shot examples + prompt template
examples = """
Input: Subject: Request for Quotation
Body: We would like to request a quotation for the attached items.
Output: format=email, intent=RFQ

Input: {{
  "event": "fraud_attempt",
  "amount": 15000,
  "location": "NYC"
}}
Output: format=json, intent=Fraud Risk

Input: Invoice #2023-11
Total: $13,500.00
Thank you for your business.
Output: format=pdf, intent=Invoice
"""

template_str = examples + "\nInput: {input_text}\nOutput:"

prompt_template = PromptTemplate(
    input_variables=["input_text"],
    template=template_str
)

def classify_input(content: bytes, filename: str) -> dict:
    # TEMP MOCK RESPONSE
    if filename.endswith(".txt"):
        return {"format": "email", "intent": "send_email"}
    elif filename.endswith(".json"):
        return {"format": "json", "intent": "update_record"}
    elif filename.endswith(".pdf"):
        return {"format": "pdf", "intent": "read_content"}
    else:
        return {"format": "unknown", "intent": "none"}


