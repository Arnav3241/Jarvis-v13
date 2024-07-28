
def ExecuteCode(code_str: str) -> None:
    try:
        exec(code_str)
    except Exception as e:
        print('Error in ExecuteCode function(Execute.py), code contained in input string has wrong syntax OR wrong datatype argument. Error:', e)


# Test cases
if __name__ == '__main__':
    ExecuteCode('a = input("Ji")')
    ExecuteCode('print("hi")\nprint("yo")')
    ExecuteCode('import math\nprint(math.sqrt(49))')
