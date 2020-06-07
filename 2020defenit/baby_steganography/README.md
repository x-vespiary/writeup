# Baby Steganography

## Writeup

We are given a [file](problem.wav) named "problem". From `file` command, this is a wav audio file.

```bash
$ file problem
problem: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, stereo 48000 Hz
```

### Structure of wav

Top 44 bytes of wav file are magic number and metadata of `fmt` and `data` chunk. Wave data starts from the next byte.

Wave data is constructed by frame data. One frame data has bytes that shows wave amplitude of channels. Amplitude is integer whose size is equals to bit size of wav (in this challenge, bit size is 16).  
For example, at 16 bit stereo(2 channel) wav file, frame data has such bytes: `ad de ef be`. That means amplitude of channel 1 is 0xdead and of channel 2 is 0xbeef on this frame. If wav is 8 bit, amplitude is 8 bit integer. If wav is monoral (1 channel), the length of bytes is equal to bit size of wav.

I observed top bytes of wave data and found they are constructed by `01` or `00`. This means amplitude of frames are 0x0101, 0x0100, 0x0001 or 0x0000. In 16 bit wav, maximum amplitude is 0x7fff (`ff 7f`). So amplitudes of these frames seems to be too small to listen. This feature may be used by this steganography.

### Steganography

The Extraction of data is very simple and almost same LSB steganography of image.  
Top 8 bytes of wave data is `00 01 00 00 00 01 00 00`. I converted this bytes to a number: `01000100` (= 0x44). This number is ASCII code of "D" that is top charactor of flag format. This method can be applied to other bytes.

Finaly, I concatenate charactors and got a flag!!

## Code

[here](exploit.py)

## Flag

`Defenit{Y0u_knOw_tH3_@uD10_5t39@No9rAphy?!}`
