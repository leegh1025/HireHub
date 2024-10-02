import openai
from dotenv import load_dotenv
import os
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

print("Please enter the candidate's application content (press Enter twice to finish):")
content = ""
while True:
    line = input()
    if line == "":
        break
    content += line + "\n"

completion = openai.chat.completions.create(
    model='gpt-4o',
    messages=[
        {"role" : "system", "content" : "You are a highly experienced interview assistant with a deep understanding of various technical fields. Your task is to generate sophisticated and insightful interview questions based on the candidate's application. Focus on evaluating their technical skills, problem-solving abilities, and cultural fit for the team. Provide questions that would challenge a candidate and reveal their depth of knowledge and thought process."},
        {"role" : "user", "content": content }
    ],
    max_tokens=700
)

questions = completion.choices[0].message.content
print("Generated Interview Questions:\n", questions)