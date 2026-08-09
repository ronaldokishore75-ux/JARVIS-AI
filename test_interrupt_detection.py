from interrupt import detect_voice

print("🎤 Speak for a moment...")

if detect_voice():
    print("🗣️ Voice detected!")
else:
    print("🔇 Nothing detected.")