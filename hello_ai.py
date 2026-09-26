import os
from dotenv import load_dotenv 
from openai import OpenAI



load_dotenv(override=True)

client =OpenAI(
  base_url="https://api.groq.com/openai/v1",
   api_key=os.environ["GROQ_API_KEY"]

)

response =client.chat.completions.create(
  model ="openai/gpt-oss-120b",
  messages=[
    {"role":"system", "content": "You are a concise AI tutor."},
   {"role": "user", "content": "Explain tokenization in one sentence. Then explain embeddings in one sentence. Then explain context windows in one sentence."}


  ],
  temperature=0.9,
  max_tokens=500
)


print(response.choices[0].message.content)

print("\n--- usage ---")
print("input tokens :", response.usage.prompt_tokens)
print("output tokens:", response.usage.completion_tokens)
print("total tokens :", response.usage.total_tokens)