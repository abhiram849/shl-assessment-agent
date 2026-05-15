from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.retriever import search_assessments


app = FastAPI()


# -----------------------------------
# Root Endpoint
# -----------------------------------

@app.get("/")
def root():

    return {
        "message": "SHL Assessment Recommendation API is running"
    }


# -----------------------------------
# Health Endpoint
# -----------------------------------

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# -----------------------------------
# Request Schema
# -----------------------------------

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# -----------------------------------
# Chat Endpoint
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages


    # -----------------------------------
    # Combine Full Conversation
    # -----------------------------------

    conversation_text = ""

    for msg in messages:

        if msg.role == "user":

            conversation_text += msg.content + " "


    user_text = conversation_text.lower()


    # -----------------------------------
    # Refusal Handling
    # -----------------------------------

    forbidden_topics = [
        "salary prediction",
        "legal advice",
        "medical advice",
        "politics",
        "religion"
    ]


    for topic in forbidden_topics:

        if topic in user_text:

            return {

                "reply": (
                    "I can only assist with "
                    "SHL assessment recommendations."
                ),

                "recommendations": [],

                "end_of_conversation": False
            }


    # -----------------------------------
    # Clarification Handling
    # -----------------------------------

    if len(user_text.split()) < 4:

        return {

            "reply": (
                "Could you provide more details "
                "about the role, skills, seniority, "
                "or hiring requirements?"
            ),

            "recommendations": [],

            "end_of_conversation": False
        }


    # -----------------------------------
    # Comparison Handling
    # -----------------------------------

    if "compare" in user_text:

        return {

            "reply": (
                "Please specify the two SHL assessments "
                "you would like compared."
            ),

            "recommendations": [],

            "end_of_conversation": False
        }


    # -----------------------------------
    # Retrieve Recommendations
    # -----------------------------------

    results = search_assessments(
        conversation_text,
        top_k=5
    )


    recommendations = []


    for item in results:

        description = item.get(
            "description",
            ""
        ).lower()


        # -----------------------------------
        # Dynamic Test Type
        # -----------------------------------

        test_type = "K"


        if "personality" in description:
            test_type = "P"

        elif "behavior" in description:
            test_type = "B"

        elif "cognitive" in description:
            test_type = "C"

        elif "knowledge" in description:
            test_type = "K"


        recommendations.append({

            "name": item.get("name", ""),

            "url": item.get("url", ""),

            "test_type": test_type
        })


    # -----------------------------------
    # Final Response
    # -----------------------------------

    return {

        "reply": (
            f"I found {len(recommendations)} "
            f"SHL assessments matching your request."
        ),

        "recommendations": recommendations,

        "end_of_conversation": False
    }