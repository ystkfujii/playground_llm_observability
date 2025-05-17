import os
import sys
from langfuse import Langfuse
from prompts.item1 import ITEM1


def read_file(path: str) -> tuple[str, str]:
    """
    指定されたファイルの内容を読み込み、(ファイル名, 内容) を返す。

    :param path: ファイルパス
    :return: (ファイル名, ファイルの内容)
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")

    filename = os.path.basename(path)
    filename, _ = os.path.splitext(filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return filename, content

if len(sys.argv) != 2:
    print("Usage: python read_file.py <file-path>")
    sys.exit(1)

filepath = sys.argv[1]
try:
    name, body = read_file(filepath)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Initialize Langfuse client
langfuse = Langfuse()

langfuse.create_prompt(
    name=name,
    prompt=body,
    config={
        "model":"gpt-4o",
        "temperature": 0,
    },
    labels=["staging"]
)
