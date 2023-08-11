import asyncio
from main import run_analyze, combine_scores, combine_scores_async

ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_sync():
    combine_scores(ids)


def test_async():
    asyncio.run(combine_scores_async(ids))


if __name__ == "__main__":
    print("\n\tSync:\t")
    run_analyze(test_sync)
    print("\n\tAsync Test Results\n ")
    run_analyze(test_async)
