import os
from langchain.llms import OpenAI
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from getpass import getpass

os.environ["OPENAI_API_KEY"] = getpass()
llm = OpenAI()

def read_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

read_file_tool = Tool(
    name="read_text_file",
    func=read_text_file,
    description="Dosya yolundan metni okur ve içeriğini döndürür."
)

summary_prompt = PromptTemplate(
    input_variables=["input_text"],
    template=(
        "Aşağıdaki metni özetle ve en önemli noktaları çıkar:\n\n"
        "{input_text}\n\n"
        "Özet + maddeler halinde önemli noktalar:"
    ),
)

summary_chain = summary_prompt | llm

advice_prompt = PromptTemplate(
    input_variables=["summary"],
    template=(
        "Aşağıdaki özetten yararlanarak kullanıcıya bazı önerilerde bulun. "
        "Özet:\n{summary}\n\n"
        "Öneriler:"
    ),
)

advice_chain = LLMChain(llm=llm, prompt=advice_prompt, verbose=True)

tools = [read_file_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

def run_agent(file_path):

    content = agent.run(f"Okuyacağın dosya şudur: {file_path}. Lütfen içeriği al.")

    summary_output = summary_chain.invoke({"input_text": content})

    advice_output = advice_chain.run(summary=summary_output)

    result = {
        "summary": summary_output,
        "advice": advice_output
    }
    return result

file_path = "example_data.txt"
outputs = run_agent(file_path)

print("\n*** ÖZET ***")
print(outputs["summary"])
print("\n-*** TAVSİYE ***")
print(outputs["advice"])
