# pip install portkey_ai
from portkey_ai import Portkey
import uuid
import os

PORTKEYAI_API_KEY=os.getenv('PORTKEY_API_KEY')
PORTKEY_VIRTUAL_OPENAI_KEY=os.getenv('PORTKEY_VIRTUAL_OPENAI_KEY')

portkey = Portkey(
    api_key=PORTKEYAI_API_KEY,
    virtual_key=PORTKEY_VIRTUAL_OPENAI_KEY,
).with_options(
    metadata={
        "_user": "user123",
        "user_plan": "free",
        "environment": "production",
        "session_id": str(uuid.uuid4()),
    }
)

def main():
    # Construct a client with a virtual key

    content = "世界について教えてください"

    res = Explainer(portkey).ask(content)
    res = ChuniByoAdapter(portkey).rewrite(res)

    print(res)

class Explainer:
    def __init__(self, portkey):
        self.portkey = portkey.with_options(config="pc-sample-5c1bdf")

    def ask(self, text):
        response = self.portkey.chat.completions.create(
            messages= [
                {"role": "system", "content": "あなたは有能な解説者です。端的に説明してください。"},
                {"role": "user", "content": text},
            ],
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
    def rewrite(self, content):
        response = self.portkey.prompts.completions.create(
            prompt_id="pp-chunibyo-5676fa",
            variables={
                "content": content,
            },
            temperature=0.5,
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    main()
