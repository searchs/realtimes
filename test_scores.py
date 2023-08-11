from pprint import pprint
import asyncio
from faker import Faker
from main import run_analyze, combine_scores, combine_scores_async, generate_gamers_data


fake = Faker()
test_users = generate_gamers_data(150)
ids = test_users.keys()


def test_sync():
    combine_scores(ids)


def test_async():
    asyncio.run(combine_scores_async(ids))


if __name__ == "__main__":
    print("\n\tSync:\t")
    run_analyze(test_sync)
    print("\n\tAsync Test Results\n ")
    run_analyze(test_async)
