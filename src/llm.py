from openai import OpenAI


class LLM:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://127.0.0.1:51596/v1",
            api_key="foundry"
        )

        self.model = "phi-4-mini"

    def ask(self, question):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        return response.choices[0].message.content