import base64
import datetime
import tempfile
import traceback

import whisper

model = whisper.load_model('large')


def process_fragments(fragments, ws):
    for fragment in fragments:
        audio = whisper.load_audio(fragment, sr=16000)
        audio = whisper.pad_or_trim(audio)
        transcription = whisper.transcribe(
            model,
            audio
        )
        print(transcription['text'])
        ws.send(transcription['text'])


def process_wav_bytes(webm_bytes: bytes, sample_rate: int = 16000):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as temp_file:
        temp_file.write(webm_bytes)
        temp_file.flush()
        waveform = whisper.load_audio(temp_file.name, sr=sample_rate)
        return waveform


def transcribe_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message:
            print('message received', len(message), type(message))
            try:
                if isinstance(message, str):
                    message = base64.b64decode(message)
                audio = process_wav_bytes(bytes(message)).reshape(1, -1)
                audio = whisper.pad_or_trim(audio)
                transcription = whisper.transcribe(
                    model,
                    audio
                )
            except Exception as e:
                traceback.print_exc()


def video_to_text(file_path):
    # save a timestamp before transcription
    t1 = datetime.datetime.now()
    print(f"started at {t1}")

    # do the transcription
    output = model.transcribe(file_path)
    print(output)
    # show time elapsed after transcription is complete.
    t2 = datetime.datetime.now()
    print(f"ended at {t2}")
    print(f"time elapsed: {t2 - t1}")
    segments = output['segments']

    text = ''
    for i in range(0, len(segments)):
      segment = segments[i]
      text += segment["text"] + '\n\n'

    # Specify the file path and name where you want to save the string
    file_path = "transcribed.txt"

    # Open the file in write mode ('w')
    with open(file_path, 'w') as file:
        file.write(text)

    print(f'Transcribed text saved to {file_path}')
    return text
