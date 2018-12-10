from __future__ import print_function

import timeit
from signal import pause

import pyttsx3
import speech_recognition as sr

from gpiozero import LED, Button


# TODO: support different engines..
def speak(text, engine=pyttsx3.init()):
    engine.say(text)
    engine.runAndWait()


def transcribe(source, recognizer=sr.Recognizer(), retries=5, **kwargs):
    kwargs.setdefault("language", "en-US-ptm")

    # TODO: should we adjust for ambient noise?
    recognizer.adjust_for_ambient_noise(source)

    for _ in range(retries):
        print("Say something!")
        start = timeit.default_timer()
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_sphinx(audio, **kwargs)
        except sr.UnknownValueError:
            txt = "Sorry, I couldn't hear you."
            print(txt)
            speak(txt)
        except sr.RequestError as e:
            print("uh oh; {0}".format(e))
            speak("uh oh")
        finally:
            print("{:.4f}".format(timeit.default_timer() - start))


if __name__ == "__main__":
    with sr.Microphone(sample_rate=16000) as source:
        led = LED(26)
        button = Button(6)

        def handle_button_press():
            txt = transcribe(
                source,
                # keyword_entries=[("light", 0.2), ("turn", 0.1), ("on", 0.05)],
            )

            print(txt)

            if "turn on" in txt:
                speak("Okay, turning the light on")
                led.on()
            elif "turn off" in txt:
                speak("Okay, turning the light off")
                led.off()

        button.when_pressed = handle_button_press

        pause()
