from brain import jarvis_response
print("=" * 50)
print("        JARVIS AI")
print("=" * 50)

name = input("What's your name? ")

print(f"\nWelcome, {name}!")

while True:
    command = input(f"\n{name}: ")

    if command.lower() == "bye":
        print("JARVIS: Goodbye!")
        break

    response = jarvis_response(command)
    print("JARVIS:", response)
