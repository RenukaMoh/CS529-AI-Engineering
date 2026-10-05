import os
import csv
import json
from datetime import datetime

import gradio as gr
from dotenv import load_dotenv

from agents import Agent, Runner
from agents.decorators import tool


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not found in the .env file.")


# ============================================================
# 2. CSV FILE
# ============================================================

CSV_FILE = "leave_requests.csv"


def save_leave_decision(
    student_name: str,
    start_date: str,
    end_date: str,
    reason: str,
    status: str,
    rejection_reason: str = ""
):
    """
    Purpose: Save the faculty's final decision in a CSV file.
    Input:   Leave details, approval status, and optional rejection reason.
    Process: Creates the CSV header if needed and appends one record.
    Output:  No return value; the decision is stored in leave_requests.csv.
    """

    file_exists = os.path.exists(CSV_FILE)

# newline="" lets the csv module handle row endings correctly
# and helps prevent extra blank lines in the CSV file.
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Student Name",
                "Start Date",
                "End Date",
                "Reason",
                "Status",
                "Rejection Reason",
                "Reviewed At"
            ])

        writer.writerow([
            student_name,
            start_date,
            end_date,
            reason,
            status,
            rejection_reason,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])


# ============================================================
# 3. READ TOOL ARGUMENTS FROM THE INTERRUPTION
# ============================================================

def get_request_details(interruption):
    """
    Purpose: Read the leave details proposed by the agent.
    Input:   HITL interruption containing the approve_leave arguments.
    Process: Converts JSON-string arguments to a Python dictionary if needed.
    Output:  Dictionary containing student name, dates, and reason.
    """

    args = interruption.arguments

    # Tool arguments may arrive as a JSON string.
    # Convert the string to a Python dictionary for easy access.
    if isinstance(args, str):
        return json.loads(args)

    return args


# ============================================================
# 4. PROTECTED LEAVE APPROVAL TOOL
# ============================================================

@tool(needs_approval=True)
def approve_leave(
    student_name: str,
    start_date: str,
    end_date: str,
    reason: str
) -> str:
    """
    Purpose: Complete an approved leave request.
    Input:   Student name, start date, end date, and leave reason.
    Process: Executes ONLY after the faculty approves the HITL request.
    Output:  Returns the approval result to the agent workflow.

    If faculty rejects the request, this function does NOT execute.
    """

    return (
        f"Leave request for {student_name} from "
        f"{start_date} to {end_date} has been approved."
    )


# ============================================================
# 5. CREATE THE LEAVE APPROVAL AGENT
# ============================================================

agent = Agent(
    name="Leave Approval Agent",

    instructions="""
    You are a student leave request assistant.

    A complete leave request must contain:
    1. Student name
    2. Start date
    3. End date
    4. Reason for leave

    DATE RULES:
    - For a one-day leave, the start date and end date are the same.
    - For a multi-day leave, identify both the start date and end date.
    - If the student provides one date for a one-day request,
      use that date for both start_date and end_date.
    - If a multi-day request is missing the start date or end date,
      ask the student to provide the missing information.

    When all required information is available,
    use the approve_leave tool.

    Do not say that leave has been approved unless the human reviewer
    approves the tool request and the workflow successfully resumes.

    If the human reviewer rejects the request,
    clearly tell the student that the request was not approved.
    """,

    tools=[approve_leave],
    model="gpt-6-astra"
)


# ============================================================
# 6. SUBMIT LEAVE REQUEST
# ============================================================

async def submit_request(user_request):
    """
    Purpose: Process the student's leave request.
    Input:   Leave request text entered in the Gradio textbox.
    Process: Runs the agent. If approve_leave is proposed,
             HITL pauses the workflow.
    Output:  Returns 3 values to Gradio:
             (status message, run_state, interruption_state)
    """

    # Check whether the user entered meaningful text.
    if not user_request.strip():
        return (
            "### Please enter a leave request.",
            None, # No Input
            None # No Output
        )

    result = await Runner.run(agent, user_request)

    # If HITL is triggered, preserve the paused workflow.
    if result.interruptions:

        state = result.to_state()
        interruption = result.interruptions[0]

        details = get_request_details(interruption)

        message = f"""
### ⚠️ Faculty Approval Required

Please review the leave request.

**Student:** {details.get("student_name", "")}  
**Start Date:** {details.get("start_date", "")}  
**End Date:** {details.get("end_date", "")}  
**Reason:** {details.get("reason", "")}

Choose **Approve** or enter a rejection reason and choose **Reject**.
"""

        return message, state, interruption

    # Used when the agent needs more information from the student.
    return (
        f"### Agent Response\n\n{result.final_output}",
        None,
        None
    )


# ============================================================
# 7. APPROVE REQUEST
# ============================================================

async def approve_request(state, interruption):
    """
    Purpose: Process the faculty's approval decision.
    Input:   Paused RunState and pending HITL interruption.
    Process: Approves the tool call, resumes the agent,
             and saves the approved decision to CSV.
    Output:  Returns 4 values to the Gradio UI:
             (status message, run_state, interruption_state,
              rejection textbox value)
    """

    # Prevent approval when no request is waiting.
    if state is None or interruption is None:
        return (
            "### No request is currently waiting for approval.",
            None,
            None,
            ""
        )

    details = get_request_details(interruption)

    # Approve the pending protected tool call.
    state.approve(interruption)

    # Resume the SAME paused workflow.
    # The approve_leave tool can now execute.
    result = await Runner.run(agent, state)

    # Store the final faculty decision.
    save_leave_decision(
        student_name=details.get("student_name", ""),
        start_date=details.get("start_date", ""),
        end_date=details.get("end_date", ""),
        reason=details.get("reason", ""),
        status="APPROVED"
    )

    return (
        "### ✅ Leave Request Approved\n\n"
        f"{result.final_output}\n\n"
        f"**Status:** APPROVED  \n"
        f"The decision has been saved to `{CSV_FILE}`.",
        None,   # Clear run_state
        None,   # Clear interruption_state
        ""      # Clear rejection reason textbox
    )


# ============================================================
# 8. REJECT REQUEST
# ============================================================

async def reject_request(state, interruption, rejection_reason):
    """
    Purpose: Process the faculty's rejection decision.
    Input:   Paused RunState, HITL interruption, and rejection reason.
    Process: Rejects the tool call, resumes the agent,
             and saves the rejected decision to CSV.
    Output:  Returns 4 values to the Gradio UI:
             (status message, run_state, interruption_state,
              rejection textbox value)
    """

    # Prevent rejection when no request is waiting.
    if state is None or interruption is None:
        return (
            "### No request is currently waiting for approval.",
            None,
            None,
            ""
        )

    # Faculty must provide a reason before rejecting.
    if not rejection_reason.strip():
        return (
            "### ⚠️ Please enter a reason before rejecting the request.",
            state,
            interruption,
            rejection_reason
        )

    details = get_request_details(interruption)

    # Reject the pending protected tool call.
    # approve_leave will NOT execute.
    state.reject(
        interruption,
        rejection_message=(
            "The leave request was rejected by the faculty reviewer. "
            f"Reason: {rejection_reason.strip()}"
        )
    )

    # Resume the workflow so the agent receives the rejection.
    result = await Runner.run(agent, state)

    # Store the rejected decision and faculty reason.
    save_leave_decision(
        student_name=details.get("student_name", ""),
        start_date=details.get("start_date", ""),
        end_date=details.get("end_date", ""),
        reason=details.get("reason", ""),
        status="REJECTED",
        rejection_reason=rejection_reason.strip()
    )

    return (
        "### ❌ Leave Request Rejected\n\n"
        f"**Status:** REJECTED  \n"
        f"**Faculty Reason:** {rejection_reason.strip()}  \n\n"
        f"{result.final_output}\n\n"
        f"The decision has been saved to `{CSV_FILE}`.",
        None,   # Clear run_state
        None,   # Clear interruption_state
        ""      # Clear rejection reason textbox
    )

def show_processing():
    """Display a status message while the agent processes the request."""
    return "### ⏳ Processing leave request..."

# ============================================================
# 9. GRADIO USER INTERFACE
# ============================================================

with gr.Blocks(title="Student Leave Approval Agent") as demo:

    gr.Markdown(
        """
# 📋 Student Leave Approval Agent

Enter the student's **name, leave date(s), and reason**.

**One-day example:**  
`My name is David. I need leave on October 10, 2026 for a family event.`

**Multi-day example:**  
`My name is David. I need leave from October 10, 2026 to October 12, 2026 for a family event.`

The agent prepares the leave request, but **faculty approval is required**
before the request can be completed.
"""
    )

    user_input = gr.Textbox(
        label="Student Leave Request",
        placeholder=(
            "Example: My name is David. I need leave from "
            "October 10, 2026 to October 12, 2026 "
            "because of a family event."
        ),
        lines=4
    )

    submit_button = gr.Button(
        "Submit Request",
        variant="primary"  # Visual style: emphasizes the main action
    )

    gr.Markdown("## Request Status")

    status_output = gr.Markdown(
        "No request submitted yet."
    )

    # Gradio states preserve values between separate button clicks:
    # run_state -> paused agent workflow
    # interruption_state -> specific tool call waiting for approval
    # Intial values are None
    run_state = gr.State()
    interruption_state = gr.State()

    rejection_reason = gr.Textbox(
        label="Faculty Rejection Reason",
        placeholder="Required only when rejecting the request.",
        lines=2
    )

    with gr.Row():

        approve_button = gr.Button(
            "✅ Approve",
            variant="primary"  # Visual style: emphasizes approval
        )

        reject_button = gr.Button(
            "❌ Reject",
            variant="stop"  # Visual style: indicates reject/stop action
        )


    # --------------------------------------------------------
    # SUBMIT BUTTON
    #
    # Input:
    #   user_input
    #
    # Outputs:
    #   status_output
    #   run_state
    #   interruption_state
    # --------------------------------------------------------


    submit_button.click(
        fn=show_processing,
        outputs=status_output
    ).then(
        fn=submit_request,
        inputs=[user_input],
        outputs=[
            status_output,
            run_state, # Paused Run State object
            interruption_state # ToolApprovalItem for approve_leave
         ]
    )


    # --------------------------------------------------------
    # APPROVE BUTTON
    #
    # Inputs from Gradio State:
    #   run_state -> paused workflow
    #   interruption_state -> pending approval action
    #
    # Outputs:
    #   status message
    #   cleared run_state
    #   cleared interruption_state
    #   cleared rejection textbox
    # --------------------------------------------------------

    approve_event = approve_button.click(
        fn=approve_request,
        inputs=[
            run_state,
            interruption_state
        ],
        outputs=[
            status_output,
            run_state, # After approval, Component state becomes None
            interruption_state, # Tool Executed and component state becomes None
            rejection_reason
        ]
    )


    # --------------------------------------------------------
    # REJECT BUTTON
    #
    # Inputs:
    #   run_state
    #   interruption_state
    #   faculty rejection reason
    #
    # Outputs:
    #   status message
    #   cleared run_state
    #   cleared interruption_state
    #   cleared rejection textbox
    # --------------------------------------------------------

    reject_event = reject_button.click(
        fn=reject_request,
        inputs=[
            run_state,
            interruption_state,
            rejection_reason
        ],
        outputs=[
            status_output,
            run_state,
            interruption_state,
            rejection_reason
        ]
    )


# ============================================================
# 10. START GRADIO
# ============================================================

if __name__ == "__main__":
    demo.launch(inbrowser=True)