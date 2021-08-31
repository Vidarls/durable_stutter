# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import random
import asyncio

random.seed('A random sentence for seed')
options = [True, False]
odds = [5, 95]

def maybe_fail():
    fail = random.choices(options, odds)[0]
    if fail:
        raise Exception('Chaos monkey do bad')

async def main(i: int) -> str:
    duration = random.randint(1,10)
    await asyncio.sleep(duration)
    maybe_fail()
    return i
