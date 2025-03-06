from openai import OpenAI

class AIClient:
    def __init__(self, ai_client: OpenAI) -> None:
        self.ai_client = ai_client
    
    def generate_image(self):
        self.ai_client.images.generate(
            model='dall-e-3',
            prompt="",
            size="1024x1024",
            quality="standard",
            n=1
        )
