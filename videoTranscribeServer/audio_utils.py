import os
os.environ["IMAGEIO_FFMPEG_EXE"] = '/usr/local/bin/ffmpeg'

from pydub import AudioSegment
from moviepy.editor import VideoFileClip


def convert_mp4_to_wav(mp4_file, wav_file):
    # Load the video clip
    video_clip = VideoFileClip(mp4_file)

    # Extract the audio from the video clip
    audio_clip = video_clip.audio

    # Write the audio to a WAV file
    audio_clip.write_audiofile(wav_file)


def slice_audio(input_file, output_folder="output_fragments", slice_duration_ms=5000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Calculate the total duration of the audio in milliseconds
    total_duration = len(audio)

    # Calculate the number of fragments based on the specified slice duration
    num_fragments = total_duration // slice_duration_ms
    fragments = []
    # Slice the audio into fragments
    for i in range(num_fragments):
        start_time = i * slice_duration_ms
        end_time = (i + 1) * slice_duration_ms
        fragment = audio[start_time:end_time]

        # Output file path for the current fragment
        output_file = f"{output_folder}/fragment_{i}.wav"
        # Export the fragment as a WAV file
        fragment.export(output_file, format="wav")
        fragments.append(output_file)
    return fragments


