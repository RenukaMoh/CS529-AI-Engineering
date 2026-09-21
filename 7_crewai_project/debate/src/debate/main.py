
from debate.crew import Debate

def run():
    """
    Run the crew.
    """
    inputs = {
        'motion': 'There needs to be strict laws to regulate LLMs',
    }
    
    try:
        # Retrieve the result from the crew or Debate().crew().kickoff(inputs=inputs) without stroing the result in a variable and print it
        result = Debate().crew().kickoff(inputs=inputs) 
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
