# SHL Assessment Recommendation API

## Overview

This project is an AI-powered SHL assessment recommendation system built using FastAPI, Sentence Transformers, and FAISS.

The system accepts conversational hiring requirements and recommends relevant SHL assessments using semantic retrieval.

The API follows the exact schema specified in the SHL internship assignment.

---

## Features

- Semantic assessment retrieval
- FastAPI backend
- Stateless conversation handling
- Clarification logic
- Refusal handling
- Evaluator-compatible API schema
- SHL assessment recommendation engine

---

## Tech Stack

- Python
- FastAPI
- Sentence Transformers
- FAISS
- Selenium
- Uvicorn

---

## Project Structure

```text
app/
├── main.py
├── retriever.py
└── data/
    └── assessments.json

scripts/
└── scrape_catalog.py