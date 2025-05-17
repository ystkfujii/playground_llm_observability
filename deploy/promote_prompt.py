from langfuse import Langfuse
from prompts.item1 import ITEM1


langfuse = Langfuse()

def promote_prompt(key: str) -> None:
    prompt = langfuse.get_prompt(
        name=key,
        label="staging"
    )
    langfuse.update_prompt(
        name=key,
        version=prompt.version,
        new_labels=["production"]
    )

for key in ITEM1.keys():
    promote_prompt(key)
