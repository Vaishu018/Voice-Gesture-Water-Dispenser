import time
import RPi.GPIO as GPIO
import speech_recognition as sr

# -----------------------------
# GPIO Pin Configuration
# -----------------------------
HOT_WATER_RELAY = 17      # Relay for Hot Water
COLD_WATER_RELAY = 27     # Relay for Cold Water
GESTURE_SENSOR = 22       # IR / Gesture Sensor Input

GPIO.setmode(GPIO.BCM)
GPIO.setup(HOT_WATER_RELAY, GPIO.OUT)
GPIO.setup(COLD_WATER_RELAY, GPIO.OUT)
GPIO.setup(GESTURE_SENSOR, GPIO.IN)

# Turn OFF relays initially
GPIO.output(HOT_WATER_RELAY, GPIO.LOW)
GPIO.output(COLD_WATER_RELAY, GPIO.LOW)

# -----------------------------
# Functions
# -----------------------------
def dispense_hot_water():
    print("Dispensing Hot Water...")
    GPIO.output(HOT_WATER_RELAY, GPIO.HIGH)
    time.sleep(3)   # dispense for 3 seconds
    GPIO.output(HOT_WATER_RELAY, GPIO.LOW)
    print("Hot Water Stopped.")

def dispense_cold_water():
    print("Dispensing Cold Water...")
    GPIO.output(COLD_WATER_RELAY, GPIO.HIGH)
    time.sleep(3)   # dispense for 3 seconds
    GPIO.output(COLD_WATER_RELAY, GPIO.LOW)
    print("Cold Water Stopped.")

def stop_all():
    GPIO.output(HOT_WATER_RELAY, GPIO.LOW)
    GPIO.output(COLD_WATER_RELAY, GPIO.LOW)
    print("All Water Flow Stopped.")

def detect_voice_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for voice command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("Voice Command:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand voice.")
        return ""
    except sr.RequestError:
        print("Speech recognition service unavailable.")
        return ""

# -----------------------------
# Main Program
# -----------------------------
try:
    print("Smart Water Dispenser Started")
    print("Say: hot water / cold water / stop")

    while True:
        # Gesture Detection
        if GPIO.input(GESTURE_SENSOR) == GPIO.HIGH:
            print("Gesture Detected! Dispensing default Cold Water...")
            dispense_cold_water()
            time.sleep(1)

        # Voice Command Detection
        command = detect_voice_command()

        if "hot" in command:
            dispense_hot_water()

        elif "cold" in command:
            dispense_cold_water()

        elif "stop" in command:
            stop_all()

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting Program...")

finally:
    stop_all()
    GPIO.cleanup()