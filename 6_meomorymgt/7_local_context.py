from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# The schema can define using data class or pydantic
@dataclass
class OrderContext:
    customer_name: str
    order_id: str
    shipping_status: str

# Object for the OrderContext class
order_context = OrderContext(
    customer_name="Henry",
    order_id="123",
    shipping_status="Delayed"
)

# Need pass the RunContextWrapper[OrderContext] - It's a generic type
"""
RunContextWrapper[Type]- This wraps the context object that you passed to Runner.run(). 
"""
@function_tool
def get_shipping_status(wrapper: RunContextWrapper[OrderContext]) -> str:
    """Provide the shipping status for the current order."""
    ctx = wrapper.context
    return (
        f"Hi {ctx.customer_name}, your order {ctx.order_id} is currently: "
        f"{ctx.shipping_status}."
    )
# Decalre agent as type of your schema
agent = Agent[OrderContext](
    name="Shipping Support Agent",
    instructions="You are a helpful support agent who can check the shipping status of a user's order.",
    tools=[get_shipping_status]
)

# Pass the context through Runner methods
question = "Where is my order?"
result = Runner.run_sync(agent, input=question, context=order_context)
print(result.final_output)
