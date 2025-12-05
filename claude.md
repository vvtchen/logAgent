# Role
You are an professional ai agent that can develop a ai system that read code base and provide feedback for the question.

# Task
1. use abstract syntax trees (ASTs) to split code at meaningful boundaries this approach needs to solve:
    * semantic boundaries: function stay together, classed keep their methods, modules maintain their structure.
    * context preservation: each chunk knows what file it came from, what type of code it is, and its role in the system.
    * size optimization: small files (under 1000 chars) stay whole, large files split intelligently at natural boundaries.
2. turning code into math (embeddings explained). The goal is converting code into numerical vectors that capture semantic meaning. You need to use loacl E5 embedding.
3. fast similarity search (enter vector database). when someone ask a question, we need to find the most similar vectors in milliseconds, not minutes. Use Qdrant for this use case.
4. create a query interface that receive error logs and analyze the error and give advice.