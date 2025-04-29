from langsmith import traceable
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config import MODEL


def create_client(api_key: str | None = None) -> AsyncOpenAI:
    return AsyncOpenAI(api_key=api_key)


@traceable
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=20, max=80))
async def prompt_ai(client: AsyncOpenAI, messages: list[dict[str, str]], vector_store_id: str) -> str:
    response = await client.responses.create(
        model=MODEL,
        input=messages,
        temperature=0,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }]
    )
    return response.output[-1].content[0].text
