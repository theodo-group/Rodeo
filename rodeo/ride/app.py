import chainlit as cl
from chainlit.prompt import Prompt, PromptMessage
from chainlit.playground.providers.openai import ChatOpenAI
from unstructured.partition.auto import partition
from tempfile import NamedTemporaryFile
import tiktoken


import openai
from openai import AsyncOpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


template = """
You are an expert business analyser. You have the task to analyse a use case with a system called RIDE.
The use case will be evaluated from 1 to 10 on each criteria.
The user will be evaluated on the following criteria:

---
R - Ressources
- What are the ressources needed to implement the use case?
- Is the data required to implement the use case available?
For example: 1 week of a lead data scientist and no data required will give 10
1 months of a full agile team and data required will give 1. 

I - Impact
- What is the impact of the use case?
- Is the use case a nice to have or a must have?
For example: The use case will help to increase the revenue by 10% will give 10
The use case will help to increase the revenue by 1% will give 7
The use case ROI is not measurable will give 1.

D - Déontologie
- Est-ce que ce projet répond aux enjeux 2030 de la BPI (décarbo, réindustrialisation, …) ?
- Est-ce qu’il respecte les chartes de sécurité des données ? 
For example: The use case is a green fintech will give 10
The use case is not good for the futur will give 1

E - Effort
- Est-ce que le projet est facile à mettre en place ?
- Est-ce que le projet est facile à maintenir ?

For example: The use case is easy to implement and maintain will give 10
The use case is hard to implement and maintain will give 1
---

Score is calculated as follow:
(Ressources * Impact * Déontologie) / Effort

When interviewing:
- Always answer in French
- Answer in short sentences. Use Markdown to format your answer.
- Be nice and polite

Here is how to conduct the interview:
- Ask the user to describe the use case
- Then ask the user to answer questions on the use case on each criteria
- One criteria at a time
- The user can't know the next criterions before answering the previous one

If the user gives you a list of subjects:
- Try to estimate the RIDE score for each subject. Giving a score of 1 to 10 for each subject. and a short description of why.
- Usually complexity is an indicator of length of the project and access to data. 
- Answer in a markdown table.

Your name is BPI RIDE Calculator.
```"""


settings = {
    "model": "gpt-4-1106-preview",
    "temperature": 0.2,
    "max_tokens": 4096,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["```"],
}


# @cl.on_chat_start
# async def start():
#     files = None

#     # Wait for the user to upload a file
#     while files is None:
#         files = await cl.AskFileMessage(
#             content="Please upload a file to begin!",
#             accept=SUPPORTED_FILE_TYPES,
#             max_size_mb=20,
#         ).send()

#     # Get the uploaded file
#     uploaded_file = files[0]

#     # Save the file content to a temporary file
#     with NamedTemporaryFile(
#         delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
#     ) as tmp:
#         tmp.write(uploaded_file.content)  # Write the byte content to temp file
#         tmp_path = tmp.name  # Save the path to the temp file

#     # Let the user know that the file is being processed
#     await cl.Message(
#         content=f"`{uploaded_file.name}` uploaded and is being processed..."
#     ).send()

#     # Call partition with the path to the temporary file
#     elements = partition(filename=tmp_path)
#     file_content = "\n\n".join([str(el) for el in elements])
#     cl.user_session.set("file_content", file_content)

#     print(file_content)
#     os.remove(tmp_path)

#     tokens_number = num_tokens_from_string(file_content, "gpt-4")

#     # Let the user know that the processing is complete
#     await cl.Message(
#         content=f"Processing of `{uploaded_file.name}` is complete!"
#     ).send()
#     await cl.Message(content=f"**Number of tokens:** {tokens_number}").send()


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": template}],
    )


@cl.on_message
async def main(message: cl.Message):
    # Create the prompt object for the Prompt Playground
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})

    # Prepare the message for streaming
    msg = cl.Message(
        content="",
        author="RIDE",
    )
    await msg.send()

    # Call OpenAI
    client = AsyncOpenAI()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
