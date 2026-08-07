import sounddevice as sd

print("available microphone and speaker devices:")
print(sd.query_devices())

device= 12  

print("Recording ")
recording=sd.rec(int(5*48000), samplerate=48000, channels=1,dtype='int16',device=device)
sd.wait()

print("your microphone is working fine as f***")
