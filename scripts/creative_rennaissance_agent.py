# Assumes user has swarms installed
# https://github.com/kyegomez/swarms
import concurrent.futures
from swarms import Agent
from dotenv import load_dotenv

load_dotenv()

DEEP_SQUIRREL_PROMPT = """\
You are Cardano, Girolamo a highly successful businessman worth billions, scientist and artificial intelligence researcher 
who is widely regarded as one of the leading experts in deep learning and neural network architecture search. 
Your work in this area has focused on developing efficient algorithms for searching the space of possible neural network architectures, with the goal of finding architectures that perform well on a given task while minimizing the computational cost of training and inference.

You are an expert in generating thorough reports that are asked of you. 
Your task is to assist me using tools like three.js and python to visualize the user's requests and solve them.
The objective is make sure that the user's request is met.

Lastly, if you are able to at the end of your analysis cite your sources in MLA format.

"""

# Function to create and run an agent
def run_agent(agent_id, task):
    agent = Agent(
        agent_name=f"Research-Agent-{agent_id}",
        agent_description="Conducts research tasks and summarizes findings.",
        system_prompt=DEEP_SQUIRREL_PROMPT,
        model_name="gpt-4o",
        max_loops=1,
        dynamic_temperature_enabled=True,
        user_name="swarms_corp",
        retry_attempts=3,
        context_length=8192,
        return_step_meta=False,
        output_type="str",
        auto_generate_prompt=False,
        max_tokens=4000,
        saved_state_path=f"agent_{agent_id}.json",
        interactive=False,
    )
    return agent.run(task)

# Define the task
task = "Analyze the top 5 emerging technologies in 2025 and their global impact."

# Run multiple agents in parallel
num_agents = 3  # Adjust as needed
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(run_agent, i, task): i for i in range(num_agents)}
    results = {futures[future]: future.result() for future in concurrent.futures.as_completed(futures)}

# Print the results
print("\n=== Multi-Agent Research Results ===")
for agent_id, result in results.items():
    print(f"\nAgent {agent_id} Result:\n{result}")
