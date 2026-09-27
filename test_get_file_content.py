from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")

tests = [
    get_file_content("calculator", "main.py"),
    get_file_content("calculator", "pkg/calculator.py"),
    get_file_content("calculator", "/bin/cat"), # (this should return an error string)
    get_file_content("calculator", "pkg/does_not_exist.py"), # (this should return an error string)
]

print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")

for t in tests:
    print(t)

