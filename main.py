import os
import datetime
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
import warnings

# Ignora os avisos de depreciação para limpar o terminal
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()

# Definição das Ferramentas
@tool
def obter_hora_atual() -> str:
    """Retorna a hora atual no formato HH:MM:SS."""
    return datetime.datetime.now().strftime("%H:%M:%S")

@tool
def obter_data_atual() -> str:
    """Retorna a data atual no formato DD/MM/AAAA."""
    return datetime.datetime.now().strftime("%d/%m/%Y")

@tool
def obter_dia_da_semana() -> str:
    """Retorna o dia da semana atual por extenso."""
    dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"]
    hoje = datetime.datetime.now().weekday()
    return dias[hoje]

# Agrupamos as ferramentas em uma lista
ferramentas = [obter_hora_atual, obter_data_atual, obter_dia_da_semana]

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Prompt de Sistema
instrucoes_sistema = (
    "Você é um assistente útil que responde em português. "
    "Para responder perguntas sobre o horário, a data ou o dia da semana atual, "
    "você deve obrigatoriamente chamar a ferramenta correspondente."
)

# Criação do Agente
agente = create_react_agent(llm, ferramentas, prompt=instrucoes_sistema)

# Loop de interação com o usuário
if __name__ == "__main__":
    print("Faça uma pergunta sobre datas e horários (ou digite 'sair').\n")
    
    while True:
        print("-" * 50)
        pergunta = input("> ")
        if pergunta.lower() in ['sair', 'encerrar', 'parar', '0']:
            print("Encerrando o assistente...")
            break
            
        if not pergunta.strip():
            continue
            
        try:
            resposta = agente.invoke({"messages": [("user", pergunta)]})
            resposta_final = response_text = resposta["messages"][-1].content

            print("-" * 50)            
            print(f"\n{resposta_final}\n")
        except Exception as e:
            print(f"\nErro ao processar: {e}\n")