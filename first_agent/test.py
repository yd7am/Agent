import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件
print("正在加载 .env 文件...")
load_result = load_dotenv()
print(f"load_dotenv() 结果: {load_result}")

# 检查环境变量
api_key = os.getenv("LLM_API_KEY")
print(f"LLM_API_KEY 的值: {api_key}")

if not api_key:
    print("LLM_API_KEY 环境变量未设置")
    print("请检查 .env 文件是否包含: LLM_API_KEY=your_token_here")
    exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://api-inference.modelscope.cn/v1/"
)


response = client.chat.completions.create(
    model="Qwen/Qwen2.5-Coder-32B-Instruct", # ModelScope Model-Id
    messages=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant.'
        },
        {
            'role': 'user',
            'content': '用python写一下快排'
        }
    ],
    stream=True
)

for chunk in response:
    print(chunk.choices[0].delta.content, end='', flush=True)