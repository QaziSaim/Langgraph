from langgraph.graph import StateGraph,START,END

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
import os
from dotenv import load_dotenv
load_dotenv()


class llm_state(TypedDict):
    question:str
    answer:str

graph = StateGraph(llm_state)


def llm_qa(state:llm_state)->llm_state:
    # extract state
    question = state['question']
    # form a prompt
    prompt = f'Answer the following question {question}'
    # ask that question
    model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash'
)
    answer = model.invoke(prompt).content
    # update the answer 
    state['answer'] = answer

    return state
# add node
graph.add_node('llm_qa',llm_qa)
# add your edges
graph.add_edge(START,'llm_qa')
graph.add_edge('llm_qa',END)

workflow =graph.compile()

initial_state = {'question':'How far is sun fromm'}
os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

final_state = workflow.invoke(initial_state)
print(final_state['answer'])

from PIL import Image as PILImage
import io
img = PILImage.open(io.BytesIO(workflow.get_graph().draw_mermaid_png()))
img.show()