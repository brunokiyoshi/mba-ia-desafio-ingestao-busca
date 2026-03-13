from search import search_prompt, PROMPT_TEMPLATE
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import cmd
from dotenv import load_dotenv

def main():

    load_dotenv()

    class simpleRagChat(cmd.Cmd):
        intro = "Faça uma pergunta sobre o documento. Diga 'tchau' para sair."
        prompt = "pergunta: "
        chat = ChatOpenAI(
            model="gpt-5-nano",
            temperature=0.77,
            max_completion_tokens=None,
            timeout=None,
            max_retries=5,
        )

        template = PromptTemplate(
            input_variables=["contexto", "pergunta"], template=PROMPT_TEMPLATE
        )

        chain = template | chat

        def do_ask(self, question):
            results = search_prompt(question)
            response = self.chain.invoke({"pergunta": question, "contexto": results})
            print(response.content)


        def precmd(self, question:str):
            if question.lower() == "tchau":
                raise SystemExit
            return f"ask '{question}'"
    try:
        simpleRagChat().cmdloop()
    except KeyboardInterrupt:
        print("Saindo do chat.")
        raise SystemExit

if __name__ == "__main__":
    main()
