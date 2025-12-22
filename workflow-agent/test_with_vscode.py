import asyncio
import os

from agent_framework.azure import AzureAIAgentClient
from agent_framework.observability import setup_observability
from azure.ai.agentserver.agentframework import from_agent_framework
from dotenv import load_dotenv
from src.workflow_core import start_workflow, get_credential

load_dotenv(override=True)


async def main() -> None:
    """
    The writer and reviewer multi-agent workflow.
    This module serves as the entry point for the containerized workflow application.

    Environment variables required:
    - AZURE_AI_PROJECT_ENDPOINT: Your Microsoft Foundry project endpoint
    - AZURE_AI_MODEL_DEPLOYMENT_NAME: Your Microsoft Foundry model deployment name
    """

    # Initialize observability for visualization.
    # Set enable_sensitive_data to True to include sensitive information such as prompts and responses.
    setup_observability(vs_code_extension_port=4319, enable_sensitive_data=False)

    async with get_credential() as credential:
        try: 
            async with AzureAIAgentClient(
                project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                model_deployment_name=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
                async_credential=credential
            ) as chat_client:
                agent = await start_workflow(chat_client)
                await from_agent_framework(agent).run_async()

        except Exception as e:
            print(f"❌ Error in container execution: {e}")
            print("you may nned to login using 'az login' if you have not already.")

if __name__ == "__main__":
    asyncio.run(main())
