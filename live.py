import pyautogui
import mido
import time
pyautogui.PAUSE = 0

input_table = {
    59: ['', '', 'c'],
    61: ['', 'right', 'c'],
    63: ['down', 'right', 'c'],
    64: ['down', '', 'c'],
    66: ['down', 'left', 'c'],
    68: ['', 'left', 'c'],
    70: ['up', 'left', 'c'],
    71: ['', '', ''],
    73: ['', 'right', ''],
    75: ['down', 'right', ''],
    76: ['down', '', ''],
    78: ['down', 'left', ''],
    80: ['', 'left', ''],
    82: ['up', 'left', ''],
    83: ['up', '', '']
}

def play_note(note):
    # max range is 71-95
    note -= 12
    while note > 83: note-=12
    while note < 59: note+=12
    if note in input_table:
        pyautogui.keyDown(input_table[note][0])
        pyautogui.keyDown(input_table[note][1])
        pyautogui.keyDown(input_table[note][2])
        pyautogui.keyDown('z')
        time.sleep(0.034)
        pyautogui.keyUp('z')
        pyautogui.keyUp(input_table[note][0])
        pyautogui.keyUp(input_table[note][1])
        pyautogui.keyUp(input_table[note][2])
        time.sleep(0.034)

def midi_to_note_name(note_number):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    note = note_names[note_number % 12]
    octave = (note_number // 12) - 1
    return f"{note}{octave}"

devices = mido.get_input_names()
for i, name in enumerate(devices):
    print(f"{i}: {name}")
port = input("\nPick a device by number: ")

with mido.open_input(devices[int(port)]) as inport: # connect to a midi device. The range on your keyboard will be transposed in deltarune
    print("Please enter the lowest note on your keyboard to calibrate. (The pitches played in deltarune will be transposed.)")
    for msg in inport:
        if msg.type == 'note_on' and msg.velocity != 0:
            note = msg.note
            break

print("Captured note:", midi_to_note_name(note))
print(f"Keyboard range {midi_to_note_name(note)}-{midi_to_note_name(note+24)} transcribed to B4-B6 in Deltarune.")

with mido.open_input(devices[int(port)]) as inport:
    print('Device ready, begin playing!')
    for msg in inport:
        if msg.type == 'note_on' and msg.velocity > 0:
            play_note(msg.note-note+71) # If hitting a chord on the piano, the chord will be played in the order that the notes were pressed on the keyboard