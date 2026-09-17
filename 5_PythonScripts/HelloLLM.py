
"""
Simply right click and Run Python -> Run Python File in Terminal
"""

# Import the dotenv library 
from dotenv import load_dotenv

load_dotenv()

# import os to access the environment variables
import os
# Read the API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
# Check if the API key exists and print the first 6 characters
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:6]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")

    # import the OpenAI library 
from openai import OpenAI
# create an instance of the OpenAI class        
client = OpenAI()
# Create a list of messages in the familiar OpenAI format

# messages = "What is the capital of USA?" # Not a valid argument for the OpenAI API
messages = [
 {"role": "user", "content": "What is the capital of USA?"}   
]

#Get response from OpenAI API
response = client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages
)
# Print the response content
print(response.choices[0].message.content)


"""
Simply right click and Run Python -> Run Python File in Terminal
"""