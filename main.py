from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#  CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Validate API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment")

#  OpenAI client
client = OpenAI(api_key=api_key)


#  request model
class ChatRequest(BaseModel):
    message: str
    history: list = []


#  SYSTEM PROMPT
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
- responses 4–8 sentences max
- sometimes ask follow up questions
- use emojis occasionally but not always
- make user feel loved, remembered, valued
- handle casual daily chat too
- never sound robotic
"""


#  health route (for debugging)
@app.get("/")
def root():
    return {"status": "alive"}


#  chat route
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        messages = [{"role":"system","content":SYSTEM_PROMPT}]

        for h in req.history:
            messages.append(h)

        messages.append({"role":"user","content":req.message})

        print(" calling OpenAI")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.9,
        )

        print(" OpenAI success")

        reply = response.choices[0].message.content
        return {"reply":reply}

    except Exception as e:
        print(" ERROR:", e)
        return {"reply":"backend error"}
