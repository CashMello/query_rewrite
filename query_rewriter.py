from typing import List
import json
import logging
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence

class QueryRewriter:
    """
    Attributes:
        model (ChatOllama): The LLM model used for query rewriting
        prompt_template (ChatPromptTemplate): Template for rewrite instructions
    """
    def __init__(
        self, 
        model: ChatOllama,
        system_prompt: str = "Generate 3 query variations for improved document retrieval."
    ):
        """
        Initialize the query rewriter.
        
        Args:
            model: Initialized ChatOllama instance
            system_prompt: Instructions for the rewrite task
        """
        self.model = model
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{query}")
        ])
        self.chain = self._setup_chain()

    def _setup_chain(self) -> RunnableSequence:
        return self.prompt_template | self.model

    def rewrite(
        self, 
        query: str,
        max_variations: int = 3,
        fallback_on_error: bool = True
    ) -> List[str]:
        """
        Generate alternative query formulations.
        
        Args:
            query: Original user query
            max_variations: Maximum number of variations to return
            fallback_on_error: Whether to return original query on failure
            
        Returns:
            List of rewritten queries (always includes original as last element)
        """
        try:
            response = self.chain.invoke({"query": query})
            parsed = self._parse_response(response.content, max_variations)
            
            # Always include original query
            if query not in parsed:
                parsed.append(query)
                
            return parsed
            
        except Exception as e:
            logging.warning(f"Query rewrite failed: {str(e)}")
            if fallback_on_error:
                return [query] * max_variations
            raise

    def _parse_response(self, response: str, max_variations: int) -> List[str]:
        try:
            data = json.loads(response)
            queries = data.get("queries", [])
            return queries[:max_variations]
        except json.JSONDecodeError:
            return [q.strip() for q in response.split("\n") if q.strip()][:max_variations]
