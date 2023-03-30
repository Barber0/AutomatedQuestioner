# AI问题生成器：基于T5预训练模型实现的问题生成脚本

## 项目结构
1. [Training.ipynb](./Training.ipynb): 训练脚本
2. [Validation.ipynb](./Validation.ipynb): 效果测试脚本
3. [Data provider](./data_provider/): 工具包(训练数据准备)

    + 语料准备
        + [docs](./data_provider/docs/): 训练语料目录
        + [question_answer_pair-example.csv](./data_provider/question_answer_pair-example.csv): 预处理语料(示例)
    + 预处理工具
        + [data_loader.py](./data_provider/data_loader.py): 详细上下文提取器，用于训练
        + [context_loader.py](./data_provider/context_loader.py): 上下文提取器的具体实现脚本，配合[data_loader.py](./data_provider/data_loader.py)
        + [keyword_extractor.py](./data_provider/keyword_extractor.py): 文章关键词提取器，用于实际生成

## 技术细节
1. Fine-tuned T5 Model: 微调后的T5预训练模型，根据输入的关键词与上下文，推导出语法正确、内容相关的问题。
    
    + 输入(字符串)："answer: <关键词> \<sep\> context: <上下文>"
    + 输出(字符串): 根据关键词与上下文生成的问题
2. [context_loader.py](./data_provider/context_loader.py): 上下文提取器，根据训练数据集中用于给AI对照的问题，在语料库中搜索出相应的段落，缩小推断范围，提高训练效率。具体原理借鉴了以下工具和算法：

    + ElasticSearch
    + BM25
    + TF-IDF
3. [keyword_extractor.py](./data_provider/keyword_extractor.py): 关键词提取器。用于在实际生成过程中，从外来文章中提取出用于推断的关键词。具体原理借鉴了一下算法:

    + Text-Rank Algorithm: 一种借鉴了Google PageRank算法的关键词提取算法，运用图结构，从长文本中选出具有概括性的关键词。
    + PageRank