#Sample working script
# Import necessary libraries and modules
import tinytroupe
from openai import OpenAI
from swarms import Agent
from swarms.prompts.finance_agent_sys_prompt import FINANCIAL_AGENT_SYS_PROMPT
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_image(image):
    """Process a single image and return insights"""
    # Using the correct OpenAI client instance method for image analysis
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze this image and provide insights:"},
                    {"type": "image_url", "image_url": {"url": image.url if hasattr(image, 'url') else image}}
                ]
            }
        ],
        max_tokens=300
    )
    
    # Extract and summarize the response
    summary = response.choices[0].message.content
    return summary

def main():
    # Step 1: Collect and preprocess images with error handling
    try:
        images = tinytroupe.capture_images(source='source_identifier')
        preprocessed_images = tinytroupe.preprocess_images(images)
    except Exception as e:
        print(f"Error in image collection/preprocessing: {e}")
        return
    
    # Step 2: Analyze images using OpenAI Vision Model with parallel processing
    insights = []
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            insights = list(executor.map(analyze_image, preprocessed_images))
    except Exception as e:
        print(f"Error in image analysis: {e}")
        return
    
    # Step 3: Manage and aggregate tasks using Swarms with proper parameters
    try:
        tasks = [(i, img) for i, img in enumerate(preprocessed_images)]
        swarm = Swarms.Swarm()  # Create a Swarm instance
        swarm.manage_tasks(tasks, concurrency=3)  # Set appropriate concurrency
        final_results = swarm.aggregate_results(insights)
    except Exception as e:
        print(f"Error in task management: {e}")
        return
    
    # Output results with better formatting
    for i, result in enumerate(final_results):
        print(f"Result {i+1}:\n{result}\n{'-'*50}")

    # Step 4: Initialize and run the Financial Analysis Agent
    financial_agent = Agent(
        agent_name="Financial-Analysis-Agent",
        system_prompt=FINANCIAL_AGENT_SYS_PROMPT,
        model_name="gpt-4o-mini",
        max_loops=1,
        autosave=True,
        dashboard=False,
        verbose=True,
        dynamic_temperature_enabled=True,
        saved_state_path="finance_agent.json",
        user_name="swarms_corp",
        retry_attempts=1,
        context_length=200000,
        return_step_meta=False,
        output_type="string",
        streaming_on=False,
    )

    # Run the financial agent with a specific query
    financial_agent.run(
        "How can I establish a ROTH IRA to buy stocks and get a tax break? What are the criteria"
    )

if __name__ == "__main__":
    main()
