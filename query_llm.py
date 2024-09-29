import nest_asyncio
from httpx import stream

nest_asyncio.apply()

from llama_index.llms.lmstudio import LMStudio
from llama_index.core.base.llms.types import ChatMessage, MessageRole

llm = LMStudio(
    model_name="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
    base_url="http://localhost:1234/v1",
    # temperature=0.7,
    timeout=600
)
# response = llm.complete("Hey there, what is 2+2?")
# print(str(response))
async def get_response(query):
    print("user query: {}".format(query))
    messages = [
        ChatMessage(
            role=MessageRole.SYSTEM,
            content=f"You an expert AI assistant. Help User with their queries.",
        ),
        ChatMessage(
            role=MessageRole.USER,
            content=query,
        )
        
    ]
    response = llm.chat(messages=messages)
    res = str(response).strip("assistant: ")
    print(res)
    print("*************************************************")
    return res