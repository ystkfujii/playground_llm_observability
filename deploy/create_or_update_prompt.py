from langfuse import Langfuse
from prompts.item1 import ITEM1

# Initialize Langfuse client
langfuse = Langfuse()

for key, value in ITEM1.items():
    langfuse.create_prompt(
        name=key,
        prompt=value,
        config={
            "model":"gpt-4o",
            "temperature": 0,
        },
        labels=["staging"]
    )
# langfuse.update_prompt(
