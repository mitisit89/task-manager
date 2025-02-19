import asyncio


async def add(params: dict[str, int]) -> dict[str, int]:
    a = params.get("a", 0)
    b = params.get("b", 0)
    await asyncio.sleep(10)
    return {"result": a + b}


async def mult(params: dict[str, int]) -> dict[str, int]:
    a = params.get("a", 1)
    b = params.get("b", 1)
    await asyncio.sleep(30)
    return {"result": a * b}


async def rev(params: dict[str, str]) -> dict[str, str]:
    text = params.get("text", "")
    await asyncio.sleep(10)
    return {"result": text[::-1]}
