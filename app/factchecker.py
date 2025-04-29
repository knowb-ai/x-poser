import openai
from app.config import Config

openai.api_key = Config.OPENAI_API_KEY

def fact_check_and_respond(tweet_text: str) -> str:
    prompt = f"""Fact check the following tweet and reply concisely with correction or validation:

    Tweet: "{tweet_text}"

    Format:
    - Claim summary
    - Fact check result (True, False, Misleading, etc.)
    - Brief explanation (1-2 lines)
    - Optional citation (URL or source name)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response['choices'][0]['message']['content']
