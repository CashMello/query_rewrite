from langchain_community.chat_models import ChatOllama
from query_rewriter import QueryRewriter
from prompt import PROMPTS

sys_prompt = PROMPTS["query_rewrite"]
model = ChatOllama(model="llama3.1:latest")
rewriter = QueryRewriter(
    model,
    system_prompt=sys_prompt
)

queries = rewriter.rewrite(
    "What are the health benefits of green tea?",
    max_variations=3
)
print(queries)
# 输出示例(包含改写query和原query): 
#['Benefits of drinking green tea for overall health', 'Health advantages of consuming green tea regularly', 'How does green tea contribute to physical and mental well-being', 'What are the health benefits of green tea?']

