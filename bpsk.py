from __future__ import division
import pyttsx3
import speech_recognition as sr
import numpy as np
import scipy
import matplotlib.pylab as plt
import time

#unipolar_arr = np.array([1, 0, 1, 1, 0, 1])


def Speak(audio):
    # initializing pyttsx3 module
    engine = pyttsx3.init()
    # anything we pass inside engine.say(),
    # will be spoken by our voice assistant
    engine.say(audio)
    engine.runAndWait()
def take_commands():
    # initializing speech_recognition
    r = sr.Recognizer()
    # opening physical microphone of computer
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 0.7
        # storing audio/sound to audio variable
        audio = r.listen(source)
        try:
            print("Recognizing")
            # Recognizing audio using google api
            Query = r.recognize_google(audio)
            print("the sequence is printed=",Query)
        except Exception as e:
            print(e)
            print("Say that again sir")
            # returning none if there are errors
            return "None"
    # returning audio as text
    import time
    time.sleep(1)
    return Query
Speak("Tell me the input binary sequence")
while True:
    sequence = take_commands()
    if len(sequence)>=6:
        Speak("thankyou for providing the sequence , the BPSK signal will be provided soon")
        break
    else:
        Speak("Sequence length insufficient,please tell the sequence again")
input = ""
for i in sequence:
    if type(i) == int:
        input = input + i
sequence = sequence.replace(" ","")
unipolar_arr = np.array([list(map(int, str(sequence)))])
#bin_seq = [int(x) for x in str(num)]  
#unipolar_arr = np.array([list(map(int, str(sequence)))])
#result = [a if ' ' not in a.split(',')[0] else a.replace(' ','',1) for a in sequence]
#result = sequence.replace(" ","")
#unipolar_arr = list(filter(str.strip, result))
#unipolar_arr = [int(i) for i in unipolar_arr] 
#int(x) for x in str(sequence)
bipolar = 2*unipolar_arr - 1
bit_duration = 1
amplitude_scaling_factor = bit_duration/2  # This will result in unit amplitude waveforms
freq = 3/bit_duration  # carrier frequency
n_samples = 1200
time = np.linspace(0, 6, n_samples)

samples_per_bit = n_samples/unipolar_arr.size  # no need for np.divide. Also, use size rather than shape if you want something similar to Matlab's "length"
# 1. Use repeat rather than tile (read the docs)
# 2. No need for conjugate transpose
dd = np.repeat(unipolar_arr, samples_per_bit)  # replicate each bit Nsb times
bb = np.repeat(bipolar, samples_per_bit)  # Transpose the rows and columns
dw = dd
# no idea why this is here
#dw = dw.flatten(0).conj()
bw = bb  # one again, no need for conjugate transpose
# no idea why this is here
#bw = bw.flatten(0).conj()
waveform = np.sqrt(2*amplitude_scaling_factor/bit_duration) * np.cos(2*np.pi * freq * time)  # no need for np.dot to perform scalar-scalar multiplication or scalar-array multiplication
bpsk_w = bw*waveform

f, ax = plt.subplots(4,1, sharex=True, sharey=True, squeeze=True)
ax[0].plot(time, dw)
ax[1].plot(time, bw)
ax[2].plot(time, waveform)
ax[3].plot(time, bpsk_w, '.')
ax[0].axis([0, 6, -1.5, 1.5])
ax[0].set_xlabel('time')
Speak('here is your BPSK modulated signal for the binary sequence provided by you')
plt.show()
Speak('the first figure shows the square waveform of binary input sequence provided by you')
Speak('the second figure shows the bipolar NRZ form of the input sequence')
Speak('the third figure shows the carrier signal with frequency fc')
Speak('the final figure gives us the BPSK modulated signal')