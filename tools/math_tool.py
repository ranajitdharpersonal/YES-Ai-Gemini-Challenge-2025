import sympy

def solve_math(expression: str) -> str:
    """
    Calculates the result of a mathematical expression and returns a precise decimal answer.
    Use this tool for ANY math calculation, like addition, subtraction, multiplication, division, etc.
    """
    try:
        # User-er deoa text theke shudhu math expression'ta ber kore ana hocche
        # Jemon "solve this 2+2" theke shudhu "2+2" neoya hobe
        # Eta ekta simple approach, kintu onek kaaj korbe
        allowed_chars = "0123456789.+-*/() "
        clean_expression = "".join(filter(lambda char: char in allowed_chars, expression))

        if not clean_expression:
            return "Sorry, I couldn't find a valid math expression in your message."

        result = sympy.sympify(clean_expression)
        
        # .evalf() function'ta result'take decimal number'e convert kore dey
        final_answer = result.evalf() 
        
        return f"The answer to '{clean_expression.strip()}' is: {final_answer}"
        
    except Exception as e:
        print(f"Math tool error: {e}")
        return "Sorry, I couldn't solve that math problem. Please provide a valid expression like '5 * 10' or '100 / 4'."
