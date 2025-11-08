from langgraph.graph import StateGraph,START,END

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
import os
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash'
)

class BlogState(TypedDict):
    title:str
    outline:str
    content:str
    evaluate:int

graph = StateGraph(BlogState)

def create_outline(state:BlogState)->BlogState:

    # fetch title
    title = state['title']
    # call llm
    prompt = f'Generate a detaild the outline for the topic - {title}'
    outline=model.invoke(prompt).content
    

    # update state
    state['outline'] = outline
    return state

def create_blog(state:BlogState)->BlogState:

    title = state['title']
    outline = state['outline']

    prompt = f'write a detail blog on the title {title} - using the following outline \n {outline}'
    content = model.invoke(prompt).content
    state['content'] = content
    return state
def final_score(state:BlogState)->BlogState:
    outline = state['outline']
    blog = state['content']
    prompt = f'Evaluate the blog {blog} base on the oultine {outline} and generate the integer score of accuracy'
    score = model.invoke(prompt)
    state['evaluate'] = score
    return state
graph.add_node('create_outline',create_outline)
graph.add_node('create_blog',create_blog)
graph.add_node('final_score',final_score)

graph.add_edge(START,'create_outline')
graph.add_edge('create_outline','create_blog')
graph.add_edge('create_blog','final_score')
graph.add_edge('final_score',END)
workflow = graph.compile()

initila_workflow = {'title':'rise of ai in india'}
final_state = workflow.invoke(initila_workflow)
print(final_state['evaluate'])


from PIL import Image as PILImage
import io
img = PILImage.open(io.BytesIO(workflow.get_graph().draw_mermaid_png()))
img.show()