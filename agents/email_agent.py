from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0.3, openai_api_key="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")

prompt_template = PromptTemplate(
    input_variables=["email_content"],
    template="""
You are an assistant that analyzes customer emails.
Extract the following:
- sender email (if mentioned)
- urgency (low, medium, high)
- tone (polite, angry, threatening)
- issue/request summary (1 sentence)

Email:
{email_content}

Return JSON in the format:
{{"sender": ..., "urgency": ..., "tone": ..., "summary": ...}}
"""
)

def process_email(file_content: bytes):
    email_text = file_content.decode(errors='ignore')[:2000]  # limit for LLM
    prompt = prompt_template.format(email_content=email_text)
    llm_output = llm(prompt)

    try:
        data = eval(llm_output.strip())
    except Exception:
        data = {"sender": None, "urgency": "unknown", "tone": "unknown", "summary": "Could not parse"}

    action = "escalate" if data.get("tone") in ["angry", "threatening"] and data.get("urgency") == "high" else "log"

    return {
        "source": "email",
        "sender": data.get("sender"),
        "urgency": data.get("urgency"),
        "tone": data.get("tone"),
        "summary": data.get("summary"),
        "action": action
    }
