# Deltarune Organ Player

This code, you guessed it, plays the organ in Deltarune Chapter 4.
Running `main.py` plays the midi file set with `MIDI_FILE`.
Running `live.py` checks for attached midi devices and lets you connect a midi keyboard to use to play the organ live.

Limitations:
- You must transpose your midi file to B major first. (Yes, it would be trivial to make the code do this automatically, sue me.)
- The Deltarune piano can only play one note at a time, and one note every other frame. Because Deltarune runs at 30fps, this means one note every 70ms. Playing chords is impossible. (although there is an option to make chord notes play in rapid succession.)
- The Deltarune piano is limited to two octaves and white keys only.

How to use:
Install the python libraries `mido` and `pyautogui`:
```
pip install -r requirements.txt
```
If running the midi player (`main.py`), you will have 3 seconds after running the code to bring up the Deltarune window before PyAutoGUI starts hitting keys.
If running the live keyboard translator (`live.py`), just switch to Deltarune before you start playing.
