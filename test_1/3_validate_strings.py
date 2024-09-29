def validate_string(s):
    stack = []
    
    matching_brackets = {
        '<': '>',
        '{': '}',
        '[': ']',
        '(': ')'
    }

    for char in s:
        if char in matching_brackets:
            if stack and (stack[-1] in matching_brackets and char in matching_brackets):
                return False
            stack.append(char)
        elif char in matching_brackets.values():  
            if not stack or matching_brackets[stack.pop()] != char:
                return False
    return len(stack) == 0

# Example usage
test_cases_true = [
    "{{[<<>[{{}}]]}}",
    "<<<<<<[{[{ [{{<{[[<{<[]<<{<{[<>]}>}>>>}>]]}>}}]}]}]>>>>>",
    "{<{[[{{<<>{{[{<>[]}]}}>[]}}]]}>}",
    "{{[{<[[{<{<<<[{{{[]{<{[<[[<{{[[[[[<{[{<[<<[[<<{[[{[<<",
    "[<> { } ]"
]

test_cases_false = [
    "]",
    "] [",
    "[ >]",
    "[>",
    "{{[<<>[{{ }}]]}}",
    "{<{[[{{[]<{[{[]<}]}}<>>}}]]}>}",
    "{{[{<[[{<<<<[{{{[]{<{[<[[<{{[[[[<{[{<[<<[[<<{[[[[<<<",
    "{[[<<[]<<<{[<>]}>}>>>>]]}>}}]}]}]>>>>",
    ">}}]}]}]>>>>>>] }]] }>>]]>>]>}]}>]]]]]}}>]]>]}>}}}} ]>>> }}]]>}]}}",
    "[<]>{}]"
]

# Testing valid strings
for test in test_cases_true:
    result = validate_string(test)
    print(f"Input: {test} => Output: {result}")

# Testing invalid strings
for test in test_cases_false:
    result = validate_string(test)
    print(f"Input: {test} => Output: {result}")
