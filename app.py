# main.py
from fastapi import FastAPI, UploadFile, File
from agents.classifier_agent import classify_input
from agents.email_agent import process_email
from agents.json_agent import process_json
from agents.pdf_agent import process_pdf
from router.action_router import route_action
from memory.memory_store import log_to_memory, init_memory
import uvicorn

from fastapi import FastAPI

app = FastAPI()

from fastapi.responses import HTMLResponse


# Initialize memory DB on startup
init_memory()

@app.post("/upload")
async def upload_input(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename

    # Step 1: Classify format + intent
    classification = classify_input(content, filename)
    log_to_memory({"stage": "classified", **classification})

    # Step 2: Route to correct agent
    fmt = classification.get("format")
    if fmt == "email":
        agent_result = process_email(content)
    elif fmt == "json":
        agent_result = process_json(content)
    elif fmt == "pdf":
        agent_result = process_pdf(content)
    else:
        return {"error": "Unsupported format"}

    log_to_memory({"stage": "agent_result", **agent_result})

    # Step 3: Route action based on agent result + classification
    action_result = route_action(agent_result, classification)
    log_to_memory({"stage": "action_routed", **action_result})

    # Final response with trace
    return {
        "classification": classification,
        "agent_result": agent_result,
        "action_result": action_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app",host="127.0.0.1", port=8001, reload=True)