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

MIDI_FILE = '' # relative or absolute path for .mid file. Make sure to transpose it to B major
ATTEMPT_CHORD = False   # when this is enabled, the program will attempt to play chords by playing the notes 70ms apart (this is the fastest possible)
                        # when disabled, the program will only play the top note of any given chord
MODIFY_HALF = True      # when enabled, sharps or flats (black keys) will be rounded up. When disabled, they will be skipped over entirely.
                        # Try to avoid as many sharps and flats as possible, and put the score in B major.
file = mido.MidiFile(MIDI_FILE)
track = file.tracks[0]  # Only track 1 of the midi file will be played

def play_note(note, next_note):
    # max range is 59-83
    if note != -1:
        while note > 83: note-=12
        while note < 59: note+=12
    if next_note != -1:
        while next_note > 83: next_note-=12
        while next_note < 59: next_note+=12

    if note != -1:
        if note not in input_table and MODIFY_HALF:
            note -= 1
        if note in input_table:
            pyautogui.keyDown('z')
            time.sleep(0.034)
            pyautogui.keyUp('z')
            pyautogui.keyUp(input_table[note][0])
            pyautogui.keyUp(input_table[note][1])
            pyautogui.keyUp(input_table[note][2])
    if next_note != -1:
        if next_note not in input_table and MODIFY_HALF:
            next_note -= 1
        if next_note in input_table:
            time.sleep(0.034)
            pyautogui.keyDown(input_table[next_note][0])
            pyautogui.keyDown(input_table[next_note][1])
            pyautogui.keyDown(input_table[next_note][2])

def compile_track(track): # i know its awful and slow but it runs before any notes are played so i dont care.
    play_data = []
    time_sum = 0
    for msg in track:
        time_sum += msg.time
        if msg.velocity > 0:
            if msg.time == 0 and play_data:
                prev = play_data.pop()
                if ATTEMPT_CHORD:
                    if prev[1] == 0:
                        vel = 0
                        prev_list = []
                        while prev[1] == 0 and play_data:
                            prev = play_data.pop()
                            prev_list.append((prev[0], 0))
                        prev_list.append((msg.note, 0))
                        prev_list.sort(key=lambda x: x[0], reverse=True)
                        prev_list[0] = (prev_list[0][0], prev[1])
                        play_data.extend(prev_list)
                    else:
                        if msg.note > prev[0]:
                            play_data.append((msg.note, prev[1]))
                            play_data.append((prev[0], 0))
                        else:
                            play_data.append((prev[0], prev[1]))
                            play_data.append((msg.note, 0))
                else:
                    play_data.append((msg.note if msg.note > prev[0] else prev[0], prev[1]))
            else:
                play_data.append((msg.note, time_sum))
                time_sum = 0
    play_data.append((-1,0))
    return play_data

tempo = 0
ticks_per_beat = file.ticks_per_beat

for msg in track:
    if msg.is_meta and msg.time == 0:
        if msg.type == "set_tempo":
            tempo = msg.tempo

play_data = compile_track([msg for msg in track if msg.type == 'note_on'])
curr_note = -1
next_note = -1
time.sleep(3)
start_time = time.time()
tick_sum = 0
pyautogui.keyUp('left') # release keys from previous run
pyautogui.keyUp('right')
pyautogui.keyUp('up')
pyautogui.keyUp('down')
pyautogui.keyUp('c')
pyautogui.keyUp('z')

for msg in play_data:
    total_time = mido.tick2second(tick_sum, ticks_per_beat, tempo)
    sleep_time = total_time-(time.time()-start_time)
    if sleep_time > 0: time.sleep(sleep_time)
    tick_sum += msg[1]
    curr_note = next_note
    next_note = msg[0]
    play_note(curr_note, next_note)