from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  model="deepseek/deepseek-chat-v3-0324:free",
  max_tokens=2000,
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)

print(completion.choices[0].message.content)

