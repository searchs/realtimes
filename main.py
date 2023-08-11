from pprint import pprint
import asyncio
import random
import time
from dataclasses import dataclass
from typing import Dict, List, Callable
from dotenv import load_dotenv, dotenv_values
import redis.asyncio as redis
import aiohttp
from fastapi import FastAPI
from starlette.websockets import WebSocket
import requests

# Dev
from faker import Faker

app = FastAPI()
load_dotenv()
fake = Faker()

config = dotenv_values(".env")
redis_conn_pool = redis.ConnectionPool(
    host=config["REDIS_HOST"], port=config["REDIS_PORT"], password=config["REDIS_PASS"]
)


def redis_connection() -> redis.Redis:
    return redis.Redis(connection_pool=redis_conn_pool)


@dataclass
class UserInfo:
    id: int
    name: str
    score: int


def generate_score():
    return random.randint(6, 22)


def generate_gamers_data(gamers_count):
    gamers = dict()
    for _ in range(1, gamers_count + 1):
        gamers[_] = UserInfo(_, fake.unique.first_name(), generate_score())
    return gamers


users = generate_gamers_data(16)
print("==" * 45)
pprint(users)
print("==" * 45)


@app.get("/")
async def root():
    return {"hola": "Ola"}


@app.websocket("/ws")
async def ws_root(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Hello")
    await websocket.close()


@app.get("/user/{user_id}")
async def get_user(user_id: int):
    await asyncio.sleep(0.2)
    if user_id in users:
        return {"ok": True, "user": users[user_id]}
    return {"ok": False, "error": "user not found."}


def get_user_info(user_id: int) -> dict | None:
    response = requests.get(f"http://127.0.0.1:8000/user/{user_id}").json()
    if "ok" not in response or not response["ok"]:
        return None
    return response["user"]


async def get_user_info_async(user_id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8000/user/{user_id}") as response:
            response = await response.json()
            if "ok" not in response or not response["ok"]:
                return None
            return response["user"]


def combine_scores(ids: List[int]) -> None:
    users_list = [get_user_info(user_id) for user_id in ids]
    scores = [user["score"] for user in users_list if user is not None]
    print(f"Total Scores: {sum(scores)}")


async def combine_scores_async(ids: List[int]) -> None:
    futures = [get_user_info_async(user_id) for user_id in ids]
    users_list_async = await asyncio.gather(*futures)
    scores = [user["score"] for user in users_list_async if user is not None]
    print(f"Async Total Sum: {sum(scores)}")


def run_analyze(method: Callable) -> None:
    start = time.time_ns()
    method()
    duration = time.time_ns() - start
    duration_ms = duration / 1_000_000
    print(f"\n\tTook {duration_ms}ms\n")
