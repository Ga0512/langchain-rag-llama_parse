import nest_asyncio
import json
import os
import shutil
from create_database import create_data

nest_asyncio.apply()

from llama_parse import LlamaParse


def llama_parse_md(files = list(), agent_name='default', api_key=str, openai_api_key=str):
    parser = LlamaParse(
        api_key=api_key,  # can also be set in your env as LLAMA_CLOUD_API_KEY
        result_type="markdown",
    )


    for file in files:
        file_name = os.path.basename(file)
        _, extensao = os.path.splitext(file_name)

        # Remover o ponto da extensão, se necessário
        extensao = extensao.lstrip('.')
        print(extensao)

        if extensao != "md":
            documents = str(parser.load_data(file))

            with open(f"{file}.md", 'w', encoding='utf-8') as arquivo:
                arquivo.write(documents)
            novo_caminho = os.path.join('data/books', f"{file_name}.md")
            shutil.move(f"{file}.md", novo_caminho)
        else:
            novo_caminho = os.path.join('data/books', f"{file_name}")
            shutil.move(f"{file}", novo_caminho)

    create_data(agent_name, openai_api_key)
            
