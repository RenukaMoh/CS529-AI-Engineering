#!/usr/bin/env python
from memory_demo.crew import MemoryDemo

def run():
    inputs = {
        'customer_request': 'I need help with my account'
    }
    MemoryDemo().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()

# On the terminal to start chat, crewai chat
# If you face issue for not installed chat, then do 
# crewai install
# crewai chat