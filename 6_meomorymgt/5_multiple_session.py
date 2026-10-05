from agents import Agent, Runner, SQLiteSession, function_tool
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


# -------------------------------------------------------------
# Tool: Returns behavior rules based on the education use case
# -------------------------------------------------------------
@function_tool
def get_education_mode(use_case: str) -> dict:
    """
    Returns a small mode profile that the agent can follow.
    """

    use_case = (use_case or "").strip().lower()

    if use_case == "tutor":
        return {
            "mode": "TUTOR",
            "style_rules": [
                "Explain in simple English.",
                "Use a small example.",
                "Ask 1 quick check question at the end."
            ],
        }

    if use_case == "assignment":
        return {
            "mode": "ASSIGNMENT",
            "style_rules": [
                "Guide step-by-step.",
                "Do not give a full final solution immediately.",
                "Ask what the student has tried and provide hints."
            ],
        }

    # General mode
    return {
        "mode": "GENERAL",
        "style_rules": [
            "Be helpful and clear.",
            "Keep answers concise."
        ],
    }


# -------------------------------------------------------------
# Main Education Assistant Agent
# -------------------------------------------------------------
agent = Agent(
    name="EduAssistant",
    instructions=(
        "You are an education-focused assistant for university students.\n"
        "Call the tool get_education_mode(use_case) to determine "
        "how you should respond.\n"
        "Use the returned mode and style_rules to shape your responses.\n"
        "Keep explanations simple and practical."
    ),
    tools=[get_education_mode],
)


# -------------------------------------------------------------
# Database location
# All sessions are stored in the SAME database
# -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "educonversations.db")


# -------------------------------------------------------------
# Function: Select session and automatically determine use case
# -------------------------------------------------------------
def select_session():

    while True:

        session_id = input(
            "\nEnter session "
            "(tutor_session / assignment_session / general_session): "
        ).strip().lower()

        if session_id == "tutor_session":
            use_case = "tutor"

        elif session_id == "assignment_session":
            use_case = "assignment"

        elif session_id == "general_session":
            use_case = "general"

        else:
            print("Invalid session. Please choose one of the listed sessions.")
            continue

        # Create/open the selected session
        session = SQLiteSession(
            session_id,
            db_path=DB_PATH
        )

        return session_id, use_case, session


# -------------------------------------------------------------
# Start Program
# -------------------------------------------------------------
print("\nMulti-Session Education Assistant")
print("---------------------------------")
print("Available sessions:")
print("  tutor_session")
print("  assignment_session")
print("  general_session")
print("\nCommands: /switch, /exit")


# Select initial session
current_session_id, current_use_case, session = select_session()

print(
    f"\nCurrent session: {current_session_id} "
    f"| Mode: {current_use_case}"
)


# -------------------------------------------------------------
# Conversation Loop
# -------------------------------------------------------------
while True:

    user_text = input("\nYou: ").strip()

    # Ignore empty messages
    if not user_text:
        continue

    # Exit program
    if user_text.lower() in ["/exit", "exit", "quit"]:
        print("Agent: Goodbye!")
        break

    # Switch to another session
    if user_text.lower() == "/switch":

        current_session_id, current_use_case, session = select_session()

        print(
            f"\nSwitched to: {current_session_id} "
            f"| Mode: {current_use_case}"
        )

        continue

    # Add use case information to the user's prompt
    prompt = f"[USE_CASE={current_use_case}] {user_text}"

    # Run agent using the selected SQLite session
    result = Runner.run_sync(
        agent,
        prompt,
        session=session
    )

    print("Agent:", result.final_output)