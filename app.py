import chainlit as cl

from query_llm import get_response


@cl.on_chat_start
async def start():

    await cl.Message(
        author="Assistant", content="Hello! Im an AI assistant. How may I help you?"
    ).send()


@cl.on_message
async def main(message: cl.Message):

    res = get_response(message.content)

    await cl.Message(
        content=res,
    ).send()
