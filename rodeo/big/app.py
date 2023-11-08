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
Here is a file content on which you need to do some analysis:
{file_content}

Answer these from the user: {input}
```"""


settings = {
    "model": "gpt-4-1106-preview",
    "temperature": 0,
    "max_tokens": 4096,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["```"],
}


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


SUPPORTED_FILE_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    # Add other MIME types as needed for supported file formats
]


@cl.on_chat_start
async def start():
    files = None

    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a file to begin!",
            accept=SUPPORTED_FILE_TYPES,
            max_size_mb=20,
        ).send()

    # Get the uploaded file
    uploaded_file = files[0]

    # Save the file content to a temporary file
    with NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
    ) as tmp:
        tmp.write(uploaded_file.content)  # Write the byte content to temp file
        tmp_path = tmp.name  # Save the path to the temp file

    # Let the user know that the file is being processed
    await cl.Message(
        content=f"`{uploaded_file.name}` uploaded and is being processed..."
    ).send()

    # Call partition with the path to the temporary file
    elements = partition(filename=tmp_path)
    file_content = "\n\n".join([str(el) for el in elements])
    cl.user_session.set("file_content", file_content)

    print(file_content)
    os.remove(tmp_path)

    tokens_number = num_tokens_from_string(file_content, "gpt-4")

    # Let the user know that the processing is complete
    await cl.Message(
        content=f"Processing of `{uploaded_file.name}` is complete!"
    ).send()
    await cl.Message(content=f"**Number of tokens:** {tokens_number}").send()


@cl.on_message
async def main(message: cl.Message):
    # Create the prompt object for the Prompt Playground
    message_history = cl.user_session.get("message_history", [])
    message_history.append({"role": "user", "content": message.content})
    file_content = cl.user_session.get("file_content")
    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="user",
                template=template,
                formatted=template.format(
                    input=message.content, file_content=file_content
                ),
            )
        ],
        settings=settings,
        inputs={"input": message.content},
    )

    print(prompt)

    # Prepare the message for streaming
    msg = cl.Message(
        content="",
        author=settings.get("model", "Unknown"),
    )

    # Call OpenAI
    client = AsyncOpenAI()

    async for chunk in await client.chat.completions.create(
        messages=[m.to_openai() for m in prompt.messages], stream=True, **settings  # type: ignore
    ):
        if chunk.choices[0].delta.content is not None:  # Check if content is not None
            print(chunk.choices[0].delta.content)
            await msg.stream_token(chunk.choices[0].delta.content)

    # Append the assistant's response to the message history

    # Send the final message after streaming is complete
    print(msg.content)
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.send()
