from __future__ import print_function, unicode_literals

import timeit
from builtins import str
from pathlib import Path
from signal import pause
from subprocess import check_output

from snips_nlu import SnipsNLUEngine


def speak(text, engine=None, record=True):
    if engine is None:
        # TODO: support different engines..
        import pyttsx3

        # TODO: cache engine init?
        engine = pyttsx3.init()

    if record:
        print("[spoken]", text)

    engine.say(text)
    engine.runAndWait()


def transcribe(source, recognizer=None, retries=5, **kwargs):
    if recognizer is None:
        import speech_recognition as sr

        # TODO: cache recognizer init?
        recognizer = sr.Recognizer()

    kwargs.setdefault("language", "en-US-ptm")

    # TODO: should we adjust for ambient noise?
    recognizer.adjust_for_ambient_noise(source)

    for _ in range(retries):
        print("Say something!")
        start = timeit.default_timer()
        try:
            audio = recognizer.listen(source)
            return str(recognizer.recognize_sphinx(audio, **kwargs))
        except sr.UnknownValueError:
            speak("Sorry, I couldn't hear you.")
        except sr.RequestError as e:
            print(e)
            speak("uh oh")
        finally:
            print("{:.4f}".format(timeit.default_timer() - start))


def action_from(intent=None, slots=None, input=None):
    if intent is None:
        intent = {}
    if slots is None:
        slots = []
    if input is None:
        input = ""

    entities = {slot["slotName"]: slot for slot in slots}

    def change_led_state(state, led=None):
        import gpiozero
        from gpiozero import LED

        if led is None:
            # TODO: get default led arg from argparse
            led = 26

        try:
            led = LED(led)
        except gpiozero.exc.GPIOPinInUse:
            pass

        speak("Okay, turning the LED {}".format(state))
        getattr(led, state)()

    def change_light_state(state, room=None):
        room = "in the {}".format(room) if room is not None else ""
        speak("Okay, turning the light {} {}".format(state, room))

    if intent.get("intentName") == "turnLedOn":
        led = entities.get("led", {}).get("value")
        return lambda: change_led_state("on", led)

    if intent.get("intentName") == "turnLedOff":
        led = entities.get("led", {}).get("value")
        return lambda: change_led_state("off", led)

    if intent.get("intentName") == "turnLightOn":
        room = entities.get("room", {}).get("value")
        return lambda: change_light_state("on", room)

    if intent.get("intentName") == "turnLightOff":
        room = entities.get("room", {}).get("value")
        return lambda: change_light_state("off", room)

    if intent.get("intentName") == "getWeather":
        location = entities.get("location", {}).get("value")
        loc = "in {}".format(location) if location else "here"
        d = entities.get("dateTime", {}).get("rawValue", "")
        # TODO: use actual weather API
        return lambda: speak("It will be 32 degrees {} {}".format(loc, d))

    if intent.get("intentName") == "setTemperature":
        room = entities.get("room", {}).get("value")
        r = "in the {}".format(room) if room else ""
        t = entities.get("temperature", {}).get("rawValue", "")
        # TODO: use actual thermostat API
        return lambda: speak("OK setting the thermostat {} to {}".format(r, t))

    if intent.get("intentName") == "searchFlight":
        # TODO: use actual flight API
        return lambda: speak("I found a flight for 350 dollars")

    return lambda: speak("I didn't understand. Try saying it differently?")


if __name__ == "__main__":
    import speech_recognition as sr
    from gpiozero import Button

    # hacky but it works
    project_root = Path(
        check_output(["git", "rev-parse", "--show-toplevel"]).rstrip()
    )
    model_dir = Path(project_root, "models/nlu/engine")

    nlu_engine = SnipsNLUEngine().from_path(model_dir)

    with sr.Microphone(sample_rate=16000) as source:
        button = Button(6)

        def handle_button_press():
            # keyword_entries=[("light", 0.2), ("turn", 0.1), ("on", 0.05)],
            transcript = nlu_engine.parse(transcribe(source))

            print(transcript)

            action_from(**transcript)()

            button.when_pressed = handle_button_press

        pause()
