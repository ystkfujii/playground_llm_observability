import os
from langfuse import Langfuse

def list_files_in_directory(directory: str) -> list[str]:
    """
    指定されたディレクトリ直下のファイル一覧を返す（サブディレクトリは除外）。

    :param directory: 対象ディレクトリのパス
    :return: ファイル名のリスト（相対パス）
    """
    files = []
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            entry, _ = os.path.splitext(entry)
            files.append(entry)
    return files


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

for key in list_files_in_directory("prompts"):
    promote_prompt(key)
