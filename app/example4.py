from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from langfuse.callback import CallbackHandler

import os

from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL


PORTKEYAI_API_KEY=os.getenv('PORTKEY_API_KEY')
PORTKEY_VIRTUAL_OPENAI_KEY=os.getenv('PORTKEY_VIRTUAL_OPENAI_KEY')

openai_model = ChatOpenAI(
  base_url=PORTKEY_GATEWAY_URL,
  default_headers=createHeaders(
        api_key=PORTKEYAI_API_KEY,
        virtual_key=PORTKEY_VIRTUAL_OPENAI_KEY, # Pass your virtual key saved on Portkey for any provider you'd like (Anthropic, OpenAI, Groq, etc.). if using this, no need to pass openai api key
        config = "pc-sample-5c1bdf"
  ),
)

langfuse_handler = CallbackHandler()

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

res=chain.invoke({"topic": "世界"}, config={"callbacks": [langfuse_handler]})
print(res.content)
