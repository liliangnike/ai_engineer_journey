# 任务1.1 LLM 与代码交互的底层架构

  1. System Prompt
     - 核心价值:
       设定模型的“人设” 与 “行为准则”。在对话的最开始定义了模型的上下文偏好，优先级高于User Prompt.

     - 工程意义:
       稳定输出格式(如强制Json)、定义技术规范(如强制使用C++17特性).

  2. Stateless 与上下文管理
     - 本质:
       LLM本身不存储对话信息。

     - 实现方式:
       通过本地维护一个‘messages'列表（数组）， 在每次调用的时候将整个对话历史作为payload发送给模型。

     - 工程权衡:
       上下文越长，Token消耗越大，延迟越高。需要学会何时清空或者剪裁历史对话。


# Summary of task 1.2 - 01_foundation/first_ai_chat.py
    
  This is first AI chat practice Python source code. It is local 'ChatGPT'.
  (Ollama responses slowly - might be due to there is no GPU in my Linux workstation.)

# 任务1.3 LLM的Function Calling(工具调用)

  1. 核心理论：从“文本输出”到“结构化决策”
     - 什么是Function Calling:
       以前模型回答：”你需要查看今天CPU的温度。“; 现在模型回答：”我识别到你需要查询的指标，请调用函数get_cpu_temp()函数，参数为{}“

     - 底层机制:
       模型训练时，被灌输了特殊的token处理逻辑。当你提供tools定义时，模型会判断当前的问题是否可以通过预定义的工具解决。如果能，会停止文本生成，转而输出一个符合你定义的函数调用需求。

  2. 工程意义
     - 闭环控制:
       这是实现AI Agent的基础。没有它，AI只是聊天机器人；有了它，AI可以操作你的系统、查询git commits、发送邮件等等。
     - 防御性工程：
       作为AI开发者，必须学会校验AI返回的函数名和参数(熟悉接口)。

# Summary of task 1.3 - 01_foundation/function_calling.py
       Function Calling is that LLM returns specific JSON data then code parses the JSON to trigger local function calling. AI and local function co-working is implemented.
