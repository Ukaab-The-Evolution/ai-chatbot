"""
Simple speech utilities used by the Streamlit frontend (optional).
This provides two functions: record_and_transcribe() and speak_text().
They try to use available libraries but will gracefully degrade if missing.
"""

def record_and_transcribe(timeout=5):
    """
    Attempt to record from microphone and transcribe. If SpeechRecognition is not available,
    return an empty string so the UI can fallback to typing.
    """
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... (this runs on the server, not the browser)")
            audio = r.listen(source, timeout=timeout)
        try:
            text = r.recognize_google(audio)
            return text
        except Exception:
            return ""
    except Exception:
        return ""

def speak_text(text: str):
    """
    Speak text using pyttsx3 if available. Otherwise no-op.
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass
