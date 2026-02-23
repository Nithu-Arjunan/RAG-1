from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True, project='genaiacademy-487009', location='us-central1'
)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=types.Part.from_text(text='Why is the sky blue?'),
    config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=20,
    ),
)

print(response.text)




    
   






