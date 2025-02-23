from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from typing import List
from .generators import *
import json

class AgentState(TypedDict):
    complaint_description: str
    instructions: str
    iterations: int
    department: str
    review: str

def instructionGenerator(state: AgentState):
    complaint_description = state['complaint_description']
    instructions = f"Categorize this complaint: {complaint_description}"
    print('Instructions generated for complaint categorization')
    return {'instructions': instructions, 'iterations': 0}

# Complaint categorizer that classifies complaints into sanitation, ticketing, or miscellaneous
def complaintCategorizer(state: AgentState):
    try:
        complaint = state['complaint_description'].lower()
        if "clean" in complaint or "dirty" in complaint or "trash" in complaint:
            department = 'sanitation'
        elif "ticket" in complaint or "refund" in complaint:
            department = 'ticketing'
        else:
            department = 'miscellaneous'
        print(f'Complaint categorized under {department}')
        return {'department': department}
    except Exception as e: 
        print("Error in categorizing the complaint.\n", e)
        return

def reviewer(state: AgentState):
    department = state['department']
    # Dummy review process (you can extend this logic)
    if department in ['sanitation', 'ticketing', 'miscellaneous']:
        review = f"Complaint is correctly categorized under {department}."
    else:
        review = "Complaint categorization needs review."
    print('Review Generated')
    return {'review': review}

# Re-evaluating the categorization based on feedback
def reevaluation(state: AgentState):
    complaint_description = state['complaint_description']
    department = 'miscellaneous'  # Default fallback if review fails
    if "clean" in complaint_description or "dirty" in complaint_description:
        department = 'sanitation'
    elif "ticket" in complaint_description:
        department = 'ticketing'
    print('Re-evaluation done')
    return {'department': department, 'iterations': state['iterations'] + 1}

# Conditional function to determine if re-evaluation is needed
def reflect(state: AgentState):
    review = state['review']
    print('\n\n REVIEW \n\n', review)
    try:
        if state['iterations'] > 3:
            return END
        if "correctly categorized" in review:
            return END
        return 'reevaluateComplaint'
    except Exception as e:
        print('Exception occurred: ', e)
        return END

# Create the state graph for the complaint categorization process
graph = StateGraph(AgentState)
graph.add_node('generate_instructions', instructionGenerator)
graph.add_node('categorizeComplaint', complaintCategorizer)
graph.add_node('generateReview', reviewer)
graph.add_node('reevaluateComplaint', reevaluation)

graph.set_entry_point('generate_instructions')
graph.add_edge('generate_instructions', 'categorizeComplaint')
graph.add_edge('categorizeComplaint', 'generateReview')
graph.add_edge('reevaluateComplaint', 'generateReview')
graph.add_conditional_edges('generateReview', reflect)

# Compile the graph
agent = graph.compile()