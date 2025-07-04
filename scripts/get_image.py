from os import getenv
from asyncio import run
from requests import get


from openai import DefaultAioHttpClient # type: ignore
from openai import AsyncOpenAI # type: ignore


def build_prompt(sentence: str, focus_word: str) -> str:
    return (
        f"Create an anime-style image inspired by Studio Ghibli that visually conveys the sentence '{sentence}' "
        f"highliting the word: '{focus_word}'. "
        f"Use atmosphere, motion, composition, lighting, and character expression to evoke the word's emotional and conceptual essence. "
        f"Avoid any written text in the image."
    )


async def main() -> None:
    async with AsyncOpenAI(
        api_key=getenv("OPENAI_KEY"),
        http_client=DefaultAioHttpClient(),
    ) as client:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=build_prompt(sentence="Je prends un taxi pour aller à l'aéroport ce matin.", focus_word="aéroport"),
            n=1,
            size="1024x1024",
            quality="standard",
            response_format="url"
        )
    
    image_url = response.data[0].url

    img_data = get(image_url).content
    with open("new_one_3.png", "wb") as f:
        f.write(img_data)

run(main())