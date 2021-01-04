import pyaudio
import wave


def sound_recorder(hertz_rate):
    format = pyaudio.paInt16
    channels = 1
    hertz_rate = hertz_rate
    chunk = 1024
    time_recording = 8
    wave_filename = "file.wav"

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format, channels=channels,
                        rate=hertz_rate, input=True,
                        frames_per_buffer=chunk)

    print("Proszę wydać komendę...")
    frames = []

    for i in range(0, int(hertz_rate / chunk * time_recording)):
        data = stream.read(chunk)
        frames.append(data)

    print("Przetwarzam ...")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(wave_filename, 'wb')
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(format))
    waveFile.setframerate(hertz_rate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
