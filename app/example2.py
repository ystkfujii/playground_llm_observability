# pip install portkey_ai
from portkey_ai import Portkey
import uuid
import os
from langfuse.decorators import observe, langfuse_context
from langfuse import Langfuse

langfuse = Langfuse()

PORTKEYAI_API_KEY=os.getenv('PORTKEY_API_KEY')
PORTKEY_VIRTUAL_OPENAI_KEY=os.getenv('PORTKEY_VIRTUAL_OPENAI_KEY')

session_id = str(uuid.uuid4())
user_id = "user123"

portkey = Portkey(
    api_key=PORTKEYAI_API_KEY,
    virtual_key=PORTKEY_VIRTUAL_OPENAI_KEY,
).with_options(
    metadata={
        "_user": user_id,
        "user_plan": "free",
        "environment": "production",
        "session_id": session_id,
    }
)

from langfuse.api import AnnotationQueueObjectType, CreateAnnotationQueueItemRequest, AnnotationQueueStatus
from langfuse.client import FernLangfuse

@observe()
def main2():
    langfuse_context.update_current_trace(
        session_id=session_id,
        user_id=user_id,
    )

    content = "世界について教えてください"

    res = Explainer(portkey).ask(content)
    res = ChuniByoAdapter(portkey).rewrite(res)

    langfuse_context.update_current_observation(
        input= content,
        output = res,
    )

    langfuse.api.annotation_queues.create_queue_item(
        queue_id="cm9a1dv7k0bt4ad07wq1ko2nn",
        request=CreateAnnotationQueueItemRequest(
            object_id=langfuse_context.get_current_observation_id(),
            object_type=AnnotationQueueObjectType.OBSERVATION,
            status=AnnotationQueueStatus.PENDING,
        ),
    )
    print(res)

@observe()
def main():
    main2()

class Explainer:
    def __init__(self, portkey):
        self.portkey = portkey.with_options(config="pc-sample-5c1bdf")

    @observe(as_type="generation")
    def ask(self, text):
        messages =[
                {"role": "system", "content": "あなたは有能な解説者です。一文で説明してください。"},
                {"role": "user", "content": text},
            ]
        response = self.portkey.chat.completions.create(
            messages = messages,
        )
        langfuse_context.update_current_observation(
            input= messages,
            model= response.model,
            usage_details= {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens,
            },
        )
        return response.choices[0].message.content

class CharacterAdapter:
    def __init__(self, portkey):
        self.portkey = portkey

    def rewrite(self, content):
        response = self.portkey.chat.completions.create(
            messages=[{"role": "user", "content": content}],
            temperature=0.5,
        )
        return response.choices[0].message.content

class ChuniByoAdapter(CharacterAdapter):
    @observe(as_type="generation")
    def rewrite(self, content):
        prompt = langfuse.get_prompt("ChuniByo", label="latest")
        messages = prompt.compile(content=content)
        response = self.portkey.chat.completions.create(
            messages=messages,
            temperature=0.5,
        )
        langfuse_context.update_current_observation(
            input= messages,
            model= response.model,
            usage_details= {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens,
            },
            prompt=prompt,
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    main()
