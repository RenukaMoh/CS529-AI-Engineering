# src/ai_skill_researcher/main.py

import os
from aiskills_researcher.crew import AISkillResearchCrew

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)


def run():
    """Run the AI Skill Research crew."""
    inputs = {
        "role": "software developers",
        "year": "2026",
    }

    # Start the crew
    result = AISkillResearchCrew().crew().kickoff(inputs=inputs)

    # Print final output
    print("\n\n=== FINAL REPORT ===\n\n")
    print(result.raw)

    print(f"\n\nReport saved to: output/ai_skills_{inputs['year']}.md")


if __name__ == "__main__":
    run()
