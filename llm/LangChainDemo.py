import os
os.environ["OPENAI_API_KEY"] = "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"
os.environ["http_proxy"] = "http://127.0.0.1:10809"
os.environ["https_proxy"] = "http://127.0.0.1:10809"
from langchain.llms import OpenAI
llm = OpenAI(model_name="text-davinci-003", max_tokens=1024)
# llm = OpenAI(model_name="gpt-3.5-turbo", max_tokens=1024)
text = "What would be a good company name for a company that makes colorful socks?"
print(llm(text))