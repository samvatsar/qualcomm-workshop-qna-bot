import chainlit as cl
from openai import AsyncOpenAI

client = AsyncOpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# Instrument the OpenAI client
cl.instrument_openai()

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0,
    # ... more settings
}


@cl.on_chat_start
async def start_chat():
    await cl.Message(
        author="Assistant",
        content="Hello! I'm an AI assistant. How may I help you?"
    ).send()
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant. "
                                       "Keep your answers within 5 sentences."}],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
