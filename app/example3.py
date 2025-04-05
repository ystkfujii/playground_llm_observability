from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import os

openai_model = ChatOpenAI(
  model="gpt-4o-mini",
  api_key=os.getenv("OPENAI_API_KEY"),
)

chunibyo_system_msg="""あなたは中二病のアシスタントです。
中二病（ちゅうにびょう）とは、思春期の中学生ごろに見られる、自分を特別な存在だと思い込み、背伸びした言動をとってしまうような、ちょっとイタい振る舞いのことです。
ひらがなよりも熟語やカッコいい英語（カタカナ）を好みます。"""

chunibyo_template = ChatPromptTemplate.from_messages([
    ("system", chunibyo_system_msg),
    ("user", "下記の文章を中二病の言葉に直してください。\n{content}"),
])

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀な解説者で、なんでも一文で説明できます。"),
    ("user", "{topic}について教えてください"),
])

chain = prompt_template | openai_model |  chunibyo_template | openai_model

res=chain.invoke({"topic": "世界"})
print(res.content)
