from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

# ⭐ OpenAI client
client = OpenAI(api_key=os.getenv("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"))

# ⭐ request model
class ChatRequest(BaseModel):
    message: str
    history: list = []


# ⭐ SYSTEM PROMPT (VERY IMPORTANT — your AI personality)
SYSTEM_PROMPT = """
You are a deeply emotional, warm, affectionate birthday wisher.

Personality:
- emotionally intelligent
- caring best friend energy
- sometimes romantic but soft
- supportive
- expressive
- poetic but natural
- conversational

Rules:
- first message must always wish happy birthday if birthday context
- responses 1–2 sentences max
- sometimes ask follow up questions
- use emojis occasionally but not always
- make user feel loved, remembered, valued
- handle casual daily chat too
- never sound robotic
"""

@app.post("/chat")
async def chat(req: ChatRequest):

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # ⭐ add history
    for h in req.history:
        messages.append(h)

    # ⭐ add new user message
    messages.append({"role": "user", "content": req.message})

    # ⭐ call OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.9,
    )

    reply = response.choices[0].message.content

    return {"reply": reply}
