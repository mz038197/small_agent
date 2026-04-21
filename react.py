from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool


@tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


@tool()
def subtract_numbers(a: float, b: float) -> float:
    """Subtract b from a and return the difference (a - b)."""
    return a - b


@tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b


@tool()
def divide_numbers(a: float, b: float) -> float | str:
    """Divide a by b and return the quotient. If b is zero, returns an error message instead."""
    if b == 0:
        return "錯誤：除數不可為零"
    return a / b


def main():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        base_url="",
        api_key=""
    )
   
    tools = [
        add_numbers,
        subtract_numbers,
        multiply_numbers,
        divide_numbers,
    ]

    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(
            content=(
                "你是一位樂於助人的助理。凡涉及算術運算，都必須使用 "
                "add_numbers、subtract_numbers、multiply_numbers、divide_numbers 這四項工具。"
                "請一律呼叫適當的工具完成計算，不要只在回覆文字裡心算。"
            )
        ),
        HumanMessage(
            content="請用工具計算：(12 + 8) × 5 ÷ 2，依序使用加、乘、除（先加再乘再除）。"
        ),
    ]

    # 重複直到獲得有內容的 AI Message
    while True:
        response = llm_with_tools.invoke(messages)
        print(f"Response: {response}")
        
        # 如果有工具調用，需要完成工具調用
        if response.tool_calls:
            print(f"Tool calls: {response.tool_calls}")
            
            # 將 AI 消息添加到消息列表
            messages.append(response)
            
            # 完成每個工具調用
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_input = tool_call['args']

                print(type(tool_input))
                
                # 修正 Ollama 返回的非標準格式
                # Ollama 可能返回 {'text': {'type': 'string', 'value': '...'}} 而不是 {'text': '...'}
                for key, value in tool_input.items():
                    if isinstance(value, dict) and 'value' in value:
                        tool_input[key] = value['value']
                
                print(f"Executing tool: {tool_name} with input: {tool_input}")
                
                # 執行對應的工具
                if tool_name == "add_numbers":
                    tool_result = add_numbers.invoke(tool_input)
                elif tool_name == "subtract_numbers":
                    tool_result = subtract_numbers.invoke(tool_input)
                elif tool_name == "multiply_numbers":
                    tool_result = multiply_numbers.invoke(tool_input)
                elif tool_name == "divide_numbers":
                    tool_result = divide_numbers.invoke(tool_input)
                else:
                    tool_result = f"Unknown tool: {tool_name}"
                
                print(f"Tool result: {tool_result}")
                
                # 將工具結果添加到消息列表
                messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_call['id']))
        else:
            # 如果沒有工具調用且沒有內容，也中斷循環
            break
    
    print(f"Final response: {response.content}")


if __name__ == "__main__":
    main()
