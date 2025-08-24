from settings import config
import json

def load_welcome_text(file_name: str) -> str:
    with open(config.PATH_TO_WELCOME_TEXT / f"{file_name}.txt", encoding="utf-8") as text_file:
        return text_file.read()

def get_images_path(image_name: str) -> str:  
    return str(config.PATH_TO_IMAGES / f"{image_name}.jpg")

def get_menu_interface(interface_name: dict) -> str:
    with open(config.PATH_TO_MENUS / f"{interface_name}.json", encoding="utf-8") as interface:
        return json.load(interface)

def get_prompts(prompt_path: str) -> str:
    prompt_file = config.PATH_TO_PROMPTS / f"{prompt_path}.txt"
    return prompt_file.read_text(encoding="utf-8")
