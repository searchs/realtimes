import asyncio
import time
from dataclasses import dataclass
from typing import Dict, List, Callable

import aiohttp
from fastapi import FastAPI
import requests

app = FastAPI()


@dataclass
class UserInfo:
    id: int
    name: str
    score: int


users: Dict[int, UserInfo] = {
    1: UserInfo(1, "Sola", 12),
    2: UserInfo(2, "Alex", 15),
    3: UserInfo(2, "Sara", 9),
    4: UserInfo(2, "Sara", 9),
    5: UserInfo(2, "Sara", 9),
    6: UserInfo(2, "Sara", 9),
    7: UserInfo(2, "Sara", 9),
    8: UserInfo(2, "Sara", 9),
    9: UserInfo(2, "Sara", 9),
    10: UserInfo(2, "Sara", 9),
}


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
