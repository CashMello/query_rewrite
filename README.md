# Query Rewriter Module

## Overview

This module provides a query rewriting service using the Ollama LLM (Language Learning Model) to generate multiple variations of a search query for improved document retrieval.

## Features

- Generates multiple query variations based on a single input query
- Handles synonyms and different phrasings of the same question
- Includes the original query in the results

## Installation

1. Ensure you have Python 3.9+ installed
2. Install the required dependencies:
   ```
   pip install -r requirements.min
   ```
3. Make sure you have Ollama installed and running with the desired model (default: "llama3.1:latest")

## Usage

### Basic Usage

```python
from langchain_community.chat_models import ChatOllama
from query_rewriter import QueryRewriter
from prompt import PROMPTS

# Initialize the model and rewriter
model = ChatOllama(model="llama3.1:latest")
rewriter = QueryRewriter(model, system_prompt=PROMPTS["query_rewrite"])

# Rewrite a query
queries = rewriter.rewrite(
    "What are the health benefits of green tea?",
    max_variations=3
)
print(queries)
```

### Expected Output

The output will be a list of query variations including the original query:

```python
[
    "Benefits of drinking green tea for overall health",
    "Health advantages of consuming green tea regularly",
    "How does green tea contribute to physical and mental well-being",
    "What are the health benefits of green tea?"
]
```

## Configuration

### Model Selection

You can specify different Ollama models by changing the model parameter:

```python
model = ChatOllama(model="your-preferred-model")
```

### Prompt Customization

The system prompt can be customized by modifying the `PROMPTS["query_rewrite"]` in `prompt.py` or passing a different string when initializing the `QueryRewriter`.

## Error Handling

The module includes built-in error handling:

- If JSON parsing fails, it falls back to line-based parsing
- If all parsing fails and `fallback_on_error=True` (default), it returns the original query
- Errors are logged with a warning message

## Methods

### `QueryRewriter.rewrite(query: str, max_variations: int = 3, fallback_on_error: bool = True) -> List[str]`

Generates alternative query formulations.

**Parameters:**
- `query`: Original user query
- `max_variations`: Maximum number of variations to return (default: 3)
- `fallback_on_error`: Whether to return original query on failure (default: True)

**Returns:**
List of rewritten queries (always includes original as last element)

## Requirements

- Python 3.7+
- `langchain-community`
- `langchain-core`
- Ollama with at least one LLM model installed

## Example Use Cases

1. Improving search engine results by submitting multiple query variations
2. Data augmentation for training NLP models
3. Generating test cases for search functionality
4. Enhancing chatbot responses by understanding multiple phrasings of questions

## Troubleshooting

If you encounter issues:
1. Verify Ollama is running (`ollama serve`)
2. Check that the specified model is downloaded (`ollama pull llama3.1:latest`)
3. Review the error logs for specific messages
4. Try reducing `max_variations` if responses are being truncated

## License

[MIT License] - Include your actual license here if applicable
