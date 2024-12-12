import sys
import whisper

def transcribe(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result['text']

if __name__ == "__main__":
    filename = sys.argv[1]
    transcription = transcribe(filename)
    print(transcription)
