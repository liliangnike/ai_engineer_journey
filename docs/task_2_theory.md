# 任务2.1 RAG(Retrieval-Augmented Generation，检索增强生成)

将一段文本转化为一串高维空间的数字(向量), 这些数字代表着语义，意思相近的文本距离很近，意思完全不同的文本距离很远。
RAG三大逻辑步骤：
  1. 分块(Chunking): 把1000页的PDF切分成几千个“小段落”，比如每500个字一段。

  2. 向量化(Embedding & Storing): 用Embedding模型把这些段落变成向量，存入向量数据库(Vectoring Database)。

  3. 检索(Retrieval): 当你问问题时，系统会将你的问题向量化，然后去数据库里查找距离最近的段落。把这几个段落和你的问题一起送给LLM。

