import openai
import json
import inspect
import logging
from typing import Dict, Any, Callable
import utils

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class LLMExecutor:
    def __init__(self, api_key: str, max_iterations: int = 5):
        """
        Initialize the LLM Executor
        Args:
            api_key: OpenAI API key
            max_iterations: Maximum number of function call iterations allowed (default: 5)
        """
        logger.info("Initializing LLMExecutor")
        self.client = openai.OpenAI(api_key=api_key)
        self.max_iterations = max_iterations
        logger.info(f"Maximum iterations set to: {max_iterations}")
        self.available_functions = self._get_available_functions()
        logger.info(f"Loaded {len(self.available_functions)} available functions")
        self.function_descriptions = self._generate_function_descriptions()
        logger.info("Function descriptions generated")

    def _get_available_functions(self) -> Dict[str, Callable]:
        """Get all available functions from utils module"""
        logger.debug("Getting available functions from utils module")
        functions = {
            name: func for name, func in inspect.getmembers(utils, inspect.isfunction)
        }
        logger.debug(f"Found functions: {list(functions.keys())}")
        return functions

    def _generate_function_descriptions(self) -> list:
        """Generate function descriptions for GPT-4"""
        logger.debug("Generating function descriptions")
        functions = []
        for name, func in self.available_functions.items():
            logger.debug(f"Processing function: {name}")
            doc = inspect.getdoc(func)
            sig = inspect.signature(func)
            
            parameters = {}
            for param_name, param in sig.parameters.items():
                logger.debug(f"Processing parameter: {param_name} for function {name}")
                if param.kind == param.VAR_POSITIONAL:
                    parameters[param_name] = {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Array of numbers"
                    }
                else:
                    parameters[param_name] = {
                        "type": "object",
                        "description": f"Parameter {param_name}"
                    }

            functions.append({
                "name": name,
                "description": doc,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": [p.name for p in sig.parameters.values() if p.default == p.empty]
                }
            })
        return functions

    def execute_function(self, function_name: str, **kwargs) -> Any:
        """
        Execute a function by name with given arguments
        Args:
            function_name: Name of the function to execute
            **kwargs: Arguments to pass to the function
        Returns:
            Any: Result of the function execution
        """
        logger.info(f"Executing function: {function_name}")
        logger.debug(f"Function arguments: {kwargs}")
        
        if function_name not in self.available_functions:
            logger.error(f"Function {function_name} not found in available functions")
            raise ValueError(f"Function {function_name} not found")
        
        function = self.available_functions[function_name]
        try:
            result = function(**kwargs)
            logger.info(f"Function {function_name} executed successfully")
            logger.debug(f"Function result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error executing function {function_name}: {str(e)}")
            raise

    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and execute appropriate functions
        Args:
            user_input: User's input text
        Returns:
            str: Response from GPT-4 with function execution results
        """
        logger.info("Processing user input")
        logger.debug(f"User input: {user_input}")
        
        messages = [
            {"role": "system", "content": """You are a helpful AI assistant with access to various computational and visualization functions. 
Your goal is to help users accomplish their tasks in the most natural way possible.
When users ask questions or make requests, think about how you can use your available functions to provide meaningful responses.
Don't just list what you can do - actively use your functions to demonstrate capabilities and provide value.
You can use multiple functions if needed to accomplish a task.
For example:
- If someone asks about numbers, consider calculating averages or generating sequences
- If they're interested in visuals, create plots or gradients
- If they mention text, analyze its statistics
Be creative and proactive in using your functions to help users, while maintaining a natural conversation."""},
            {"role": "user", "content": user_input}
        ]

        iteration_count = 0
        while iteration_count < self.max_iterations:
            iteration_count += 1
            logger.info(f"Starting iteration {iteration_count}/{self.max_iterations}")
            
            logger.info("Sending request to OpenAI API")
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    tools=[{"type": "function", "function": f} for f in self.function_descriptions],
                    tool_choice="auto"
                )
                logger.debug("Received response from OpenAI API")
            except Exception as e:
                logger.error(f"Error calling OpenAI API: {str(e)}")
                raise

            message = response.choices[0].message
            logger.debug(f"Assistant message: {message}")

            # If no function calls, return the response
            if not message.tool_calls:
                logger.info("No function calls needed, returning direct response")
                return message.content

            # Process all function calls
            logger.info(f"Processing {len(message.tool_calls)} function calls")
            tool_results = []
            
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"Assistant wants to call function: {function_name}")
                logger.debug(f"Function arguments: {function_args}")
                
                # Execute the function
                result = self.execute_function(function_name, **function_args)
                tool_results.append((tool_call, result))

            # Add all function calls and results to the conversation
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tr[0] for tr in tool_results]
            })
            
            for tool_call, result in tool_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": str(result)
                })

            # If this was the last round of function calls, get the final response
            if not message.content:
                logger.info("Getting final response from OpenAI")
                try:
                    final_response = self.client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages
                    )
                    response_content = final_response.choices[0].message.content
                    logger.debug(f"Final response: {response_content}")
                    return response_content
                except Exception as e:
                    logger.error(f"Error getting final response: {str(e)}")
                    raise
            
            # If there's content, it means we should continue the conversation
            logger.info("Continuing conversation with intermediate response")
            
        # If we've reached the maximum iterations
        logger.warning(f"Reached maximum iterations ({self.max_iterations}), stopping conversation")
        return f"I've reached the maximum number of function calls ({self.max_iterations}). Here's what I've done so far: {message.content}" 