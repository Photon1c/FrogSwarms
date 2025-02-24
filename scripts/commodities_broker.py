import concurrent.futures
from swarms import Agent
from swarms.prompts.deep_research_team import PAPER_IMPLEMENTOR_AGENT_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Define the research task for commodity demand trends
task = """
Analyze the top 15 most in-demand global commodities for 2025 and rank them based on their expected directional momentum. 
For each commodity, provide:
- Current demand drivers
- Future demand projections
- Key geopolitical/economic factors
- Whether demand is increasing or decreasing (momentum direction)
Return results as a ranked list from highest to lowest momentum.
"""

# Function to create and run an agent for analysis
def run_agent(agent_id, task):
    agent = Agent(
        agent_name=f"Commodity-Research-Agent-{agent_id}",
        agent_description="Analyzes commodity demand trends and ranks them by momentum.",
        system_prompt=PAPER_IMPLEMENTOR_AGENT_PROMPT,
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
        saved_state_path=f"commodity_agent_{agent_id}.json",
        interactive=False,
    )
    return agent.run(task)

# Run multiple agents in parallel for robust analysis
num_agents = 3  # Adjust as needed for deeper validation
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(run_agent, i, task): i for i in range(num_agents)}
    results = {futures[future]: future.result() for future in concurrent.futures.as_completed(futures)}

# Print the final commodity ranking results
print("\n=== 📊 Commodity Demand Report: Ranked by Momentum ===")
for agent_id, result in results.items():
    print(f"\n🔍 Agent {agent_id} Report:\n{result}")
