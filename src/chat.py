from search import search_prompt, PROMPT_TEMPLATE
from langchain_openai import  ChatOpenAI
from langchain_core.prompts import PromptTemplate
import sys
from dotenv import load_dotenv


def main():
    load_dotenv()
    pergunta = sys.argv[1]
    print(pergunta)
    results = search_prompt(pergunta)

    chat = ChatOpenAI(model='gpt-5-nano',temperature=0.77, max_completion_tokens=None,timeout=None,max_retries=5)

    template = PromptTemplate(input_variables=["contexto", "pergunta"], template=PROMPT_TEMPLATE)

    chain = template | chat

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    print(chain.invoke({"pergunta": pergunta, "contexto":results}))

if __name__ == "__main__":
    main()