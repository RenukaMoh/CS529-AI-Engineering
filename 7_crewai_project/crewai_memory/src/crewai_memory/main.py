#!/usr/bin/env python

from crewai_memory.crew import CrewaiMemory


def run():
    inputs = {
        "request": (
            "My name is Renuka. I am a Computer Science professor, "
            "and I prefer concise answers. Write a two-sentence "
            "professional introduction for me."
        )
    }

    CrewaiMemory().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()


# Run the crew:
# uv run crewai run
#
# Start interactive chat:
# uv run crewai chat
#
# If the project dependencies are not installed:
# uv sync