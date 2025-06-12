from fastapi import FastAPI, HTTPException
from LLM_generated_engine.LLM_engine import Chatbot
from utils.async_utils import async_retry
from models.chatbot_query_model import ChatbotQueryInput, ChatbotQueryOutput
import asyncio
import os 
import dotenv
dotenv.load_dotenv()


app = FastAPI(
    title="Sector Investment Chatbot",
    description="Endpoints for a Sector Investment Chatbot"
)

chatbot = Chatbot()

@async_retry(max_retries=10, delay=1)
async def query_with_retry(query: str):
    """Retry the search if a tool fails to run.
    
    This can help when there are intermittent connection issues
    to external APIs.
    """
    loop = asyncio.get_running_loop()
    search_response = await loop.run_in_executor(None, chatbot.query, query)
    external_data = {
        "input": query,
        "output": search_response
    }
    return ChatbotQueryOutput(**external_data)

@app.get("/")
async def get_status():
    return {"status": "running"}

@app.post("/query")
async def chatbot_query(query: ChatbotQueryInput) -> ChatbotQueryOutput:
    query_response = await query_with_retry(query.text)
    return query_response

    



   
   



