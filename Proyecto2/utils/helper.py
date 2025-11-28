def count_operators(expr):
    return sum(1 for c in expr if c in "+-*/%")

def count_parentheses_depth(expr):
    depth = 0
    max_depth = 0
    for c in expr:
        if c == "(":
            depth += 1
            max_depth = max(max_depth, depth)
        elif c == ")":
            depth -= 1
    return max_depth
