# LLM Agent

A framework that enables Language Models to autonomously execute functions while maintaining natural conversations with users. This project bridges the gap between LLM's natural language understanding and actual task execution capabilities.

## Overview

LLM Agent is designed to:
- Enable autonomous function execution by LLMs
- Maintain natural conversations with users
- Handle multiple function calls in sequence
- Manage execution flow and resources
- Provide detailed logging for debugging

## Architecture

### Core Components

1. **LLM Executor**
   - Manages communication with the Language Model (GPT-4)
   - Handles function discovery and registration
   - Controls execution flow and iteration limits
   - Provides logging and error handling

2. **Function Registry**
   - Automatically discovers available functions
   - Generates function descriptions for LLM
   - Manages function signatures and documentation

3. **Resource Management**
   - Handles generated resources (e.g., images)
   - Provides cleanup and organization
   - Maintains execution history

## Features

- **Natural Conversation**: Maintains context and provides natural responses while executing tasks
- **Multi-step Execution**: Can execute multiple functions in sequence to complete complex tasks
- **Automatic Function Discovery**: New functions are automatically discovered and made available to the LLM
- **Resource Management**: Generated files are automatically saved and organized
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Safety Limits**: Configurable iteration limits to prevent infinite loops

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key"
```

3. Run the agent:
```bash
python main.py
```

## Example Interaction

```
User: Can you analyze this text and create a visual representation of its statistics?

Agent: I'll analyze the text and create a visualization for you. Let me break this down into steps:
1. First, I'll analyze the text statistics
2. Then, I'll create a visual representation of the results
[Executes functions and provides results with explanation]

User: Can you modify the visualization to be more colorful?
[Agent proceeds to adjust the visualization while maintaining conversation]
```

## Extending Functionality

The agent can be extended by adding new functions to `utils.py`. Each function should:
- Include clear docstrings describing functionality and parameters
- Return well-defined outputs
- Handle errors gracefully

Example function template:
```python
def new_function(param1: type, param2: type) -> return_type:
    """
    Clear description of what the function does
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    Returns:
        Description of return value
    """
    # Function implementation
```

## Technical Details

- **Language Model**: GPT-4-Turbo (gpt-4o-mini)
- **Maximum Iterations**: 5 (configurable)
- **Supported Function Types**: Python functions with proper type hints and docstrings
- **Resource Management**: Automatic file handling and cleanup

## Logging

The system provides comprehensive logging at different levels:
- INFO: High-level operations
- DEBUG: Detailed execution information
- ERROR: Error conditions and exceptions

## Future Improvements

- Support for async function execution
- Memory management for long conversations
- Function result caching
- More sophisticated error recovery
- Web interface for interaction

## Note

This project is designed for research and development purposes. When using in production:
- Implement appropriate security measures
- Add rate limiting and error handling
- Monitor resource usage
- Add appropriate authentication 