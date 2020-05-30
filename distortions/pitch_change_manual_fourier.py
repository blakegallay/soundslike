import wave
import numpy as np

wr = wave.open('../audio/post/mark.wav', 'r')
# Set the parameters for the output file.
par = list(wr.getparams())
par[3] = 0  # The number of samples will be set by writeframes.
par = tuple(par)
ww = wave.open('../audio/post/mark-2.wav', 'w')
ww.setparams(par)

fr = 1
sz = wr.getframerate()//fr  # Read and process 1/fr second at a time.
# A larger number for fr means less reverb.
c = int(wr.getnframes()/sz)  # count of the whole file
# shift = 1000//fr  # shifting 100 Hz
shift = 1000//fr

for num in range(c):

    da = np.fromstring(wr.readframes(sz), dtype=np.int16)
    left, right = da[0:: 2], da[1:: 2]  # left and right channel

    # print(left)

    lf, rf = np.fft.rfft(left), np.fft.rfft(right)

    print(np.append(lf, [0 for i in range(100)]))

    lf = np.append(lf, [0 for i in range(1000)])
    rf = np.append(rf, [0 for i in range(1000)])

    #lf = np.insert(lf, 0, [0 for i in range(shift)])
    #rf = np.insert(rf, 0, [0 for i in range(shift)])

    lf, rf = np.roll(lf, shift), np.roll(rf, shift)
# The highest frequencies roll over to the lowest ones. That's not what we want, so zero them.

    #lf[0: shift], rf[0: shift] = 0, 0
# Now use the inverse Fourier transform to convert the signal back into amplitude.

    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
# Combine the two channels.

    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)
# Write the output data.

    ww.writeframes(ns.tostring())
# Close the files when all frames are processed.

wr.close()
ww.close()
