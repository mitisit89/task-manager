import asyncio


async def task_type1(params):
    a = params.get("a", 0)
    b = params.get("b", 0)
    await asyncio.sleep(60)
    return {"result": a + b}


async def task_type2(params):
    a = params.get("a", 1)
    b = params.get("b", 1)
    await asyncio.sleep(30)
    return {"result": a * b}


async def task_type3(params):
    text = params.get("text", "")
    await asyncio.sleep(10)
    return {"result": text[::-1]}
