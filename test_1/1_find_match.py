def find_match(N, strings):
    match = []
    strings_lower = []
    for i in range(N):
        strings_lower.append(strings[i].lower())
    for i in range(N):
        for j in range(i + 1, N):
            if strings_lower[i] == strings_lower[j]:
                match.append((i + 1, j + 1))
                return f"{match[0][0]} {match[0][1]}"
    return "false"

# examples Usage
N1 = 4
strings1 = ["abcd", "acbd", "11", "Satu"]
print(find_match(N1, strings1))  # Output: 2 4

N2 = 5
strings2 = ["Tusuk", "Sate", "aaab", "Tujuh", "Tujuh"]
print(find_match(N2, strings2))  # Output: 4 5

N3 = 3
strings3 = ["enak", "sekali", "rasanya"]
print(find_match(N3, strings3))  # Output: false