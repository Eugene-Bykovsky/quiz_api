import os
import requests
import time

from datetime import datetime
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime)


app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


async def fetch_from_api(questions_num: int):
    try:
        url = f"https://jservice.io/api/random?count={questions_num}"
        response = requests.get(url)
        return response.json()
    except requests.RequestException:
        print("Failed to fetch data from API.")
        return None
    except ValueError:
        print("Failed to parse JSON.")
        return None


async def store_question_if_not_exists(db, item: dict):
    while True:
        existing_question = db.query(Question).filter(Question.question == item["question"]).first()
        if existing_question:
            time.sleep(10)
            continue
        question = Question(
            question=item["question"],
            answer=item["answer"],
            created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
        )
        db.add(question)
        try:
            db.commit()
            return question
        except SQLAlchemyError:
            db.rollback()
            print("Failed to commit new question to the database. Rolling back.")


@app.post("/quiz/")
async def generate_questions(request: dict) -> dict:
    questions_num: int = request.get("questions_num", 0)
    if questions_num <= 0:
        raise HTTPException(status_code=400, detail="Number of questions must be greater than 0.")

    db = SessionLocal()

    api_data = await fetch_from_api(questions_num)
    if not api_data:
        raise HTTPException(status_code=500, detail="External API failure.")
    for item in api_data:
        await store_question_if_not_exists(db, item)

    last_question = db.query(Question).order_by(Question.id.desc()).first()

    db.close()

    if last_question:
        return {
            "id": last_question.id,
            "question": last_question.question,
            "answer": last_question.answer,
            "created_at": last_question.created_at,
        }
    else:
        return {}
