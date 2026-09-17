from agents import Agent, Runner, SQLiteSession, function_tool
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
# -------------------------------------------------------------
# Tool: returns behavior rules based on the education use case
# -------------------------------------------------------------
@function_tool
def get_education_mode(use_case: str) -> dict:
    """
    Returns a small 'mode profile' that the agent can follow.
    """
    use_case = (use_case or "").strip().lower()

    if use_case in ["tutor", "teaching", "concept"]:
        return {
            "mode": "TUTOR",
            "style_rules": [
                "Explain in simple English.",
                "Use a small example.",
                "Ask 1 quick check question at the end."
            ],
        }

    if use_case in ["assignment", "coach", "project"]:
        return {
            "mode": "ASSIGNMENT",
            "style_rules": [
                "Guide step-by-step.",
                "Do not give a full final solution immediately.",
                "Ask what the student has tried and provide hints."
            ],
        }

    # Default mode
    return {
        "mode": "GENERAL",
        "style_rules": [
            "Be helpful and clear.",
            "Keep answers concise.",
        ],
    }


# -------------------------------------------------
# Main Education Assistant  Agent (uses the tool)
# -------------------------------------------------
agent = Agent(
    name="EduAssistant",
    instructions=(
        "You are an education-focused assistant for university students.\n"
        "Always call the tool get_education_mode(use_case) at the start of a session (first user message).\n"
        "Use the returned mode/style_rules to shape your responses.\n"
        "Keep explanations simple and practical."
    ),
    tools=[get_education_mode],
)


# ---------------------------------------------------------------
# Two sessions(tutor and assignment) stored in the SAME DB file
# ---------------------------------------------------------------

# To store in the current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "educonversations.db")

print("\nMulti-Session Demo (same DB):")
print("Type a session id like: tutor_session or assignment_session")
print("Commands: /switch, /exit\n")

current_session_id = input("Enter session id: ").strip()
current_use_case = input("Choose use case (tutor / assignment): ").strip()

session = SQLiteSession(current_session_id, db_path=DB_PATH)

# "Seed" the session with the use case (so the agent can call tool using this value)
# We pass it as part of the first user turn context.
first_turn_prefix = f"[USE_CASE={current_use_case}] "

while True:
    user_text = input("You: ").strip()

    if not user_text:
        continue

    if user_text.lower() in ["/exit", "exit", "quit"]:
        print("Agent: Goodbye!")
        break

    if user_text.lower().startswith("/switch"):
        # Switch session (still same DB)
        current_session_id = input("Enter NEW session id or tutor_session or assignment_session").strip()
        current_use_case = input("Choose use case (tutor / assignment): ").strip()
        session = SQLiteSession(current_session_id, db_path=DB_PATH) 
    # The value stored as [USE_CASE=assignment] or [USE_CASE=tutor]
        first_turn_prefix = f"[USE_CASE={current_use_case}] " 
        print(f"(Switched to session: {current_session_id} | use case: {current_use_case})")
        continue

    # Add the use case hint only for the first message in a fresh run.
    # (Simple approach: we add the prefix every time—safe and easy.)
    # first_turn_prefix = [USE_CASE=assignment] or [USE_CASE=tutor]
    prompt = first_turn_prefix + user_text
    result = Runner.run_sync(agent, prompt, session=session)
    print("Agent:", result.final_output)
