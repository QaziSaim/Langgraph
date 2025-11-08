from langgraph.graph import StateGraph,START,END
from typing import TypedDict

# define state
class BMIState(TypedDict):
    weight_kg:float
    height_m:float
    bmi:float
    category:str
# define your graph

def calculate_bmi(state:BMIState) -> BMIState:
    
    weight = state['weight_kg']
    height = state['height_m']
    state['bmi'] = round(weight/(height**2),2)

    return state

def category_bmi(state:BMIState) -> BMIState:
    bmi = state['bmi']
    if bmi < 18.5:
        state["category"] = "Underweight"
    elif 18.5 <= bmi < 25:
        state["category"] = "Normal"
    elif 25 <= bmi < 30:
        state["category"] = "Overweight"
    else:
        state["category"] = "Obese"

    return state


graph = StateGraph(BMIState)
#add nodes to your graph
graph.add_node('calculate_bmi',calculate_bmi)
graph.add_node('category_bmi',category_bmi)
# add edges to your graph
graph.add_edge(START,'calculate_bmi')
graph.add_edge('calculate_bmi','category_bmi')
graph.add_edge('category_bmi',END)

# compile the graph
workflow = graph.compile()
initial_state = {'weight_kg':80,'height_m':1.73}
final_state = workflow.invoke(initial_state)
print(final_state)

from PIL import Image as PILImage
import io
img = PILImage.open(io.BytesIO(workflow.get_graph().draw_mermaid_png()))
img.show()
# execute the graph