import speech_recognition as sr
import serial
import time

# Replace with your actual COM port
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
time.sleep(2)  # Give time for NodeMCU to reset

r = sr.Recognizer()

print("🎤 Speak a command like: move forward, go backward, turn left, stop moving...")

while True:
    try:
        with sr.Microphone() as source:
            print("🎙️ Listening...")
            audio = r.listen(source, timeout=3)
            command = r.recognize_google(audio).lower()
            print("✅ You said:", command)

            if "forward" in command:
                arduino.write(b"forward\n")
                print("📤 Sent: forward")

            elif "backward" in command:
                arduino.write(b"backward\n")
                print("📤 Sent: backward")

            elif "left" in command:
                arduino.write(b"left\n")
                print("📤 Sent: left")

            elif "right" in command:
                arduino.write(b"right\n")
                print("📤 Sent: right")

            elif "stop" in command:
                arduino.write(b"stop\n")
                print("📤 Sent: stop")

            else:
                print("❌ No matching command found")

    except sr.UnknownValueError:
        print("❗ Could not understand audio")
    except sr.WaitTimeoutError:
        print("⌛ Timeout. Please speak again.")
    except KeyboardInterrupt:
        print("🛑 Exiting...")
        break
