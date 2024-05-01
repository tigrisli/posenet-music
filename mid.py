import mido
from mido import Message
import time
import threading

# Open the MIDI port once
port = mido.open_output(mido.get_output_names()[0])

def play_midi_notes(midi_note):
    """Plays a given MIDI note in a separate thread, allowing dynamic note playing."""
    def play_note():
        with lock:  # Locking only the sending of messages
            port.send(Message('note_on', note=midi_note, velocity=64))
        time.sleep(1)  # Duration the note is held outside the lock
        with lock:
            port.send(Message('note_off', note=midi_note, velocity=64))
    
    # Start a new thread each time the function is called
    threading.Thread(target=play_note).start()

# Create a lock for thread-safe port access
lock = threading.Lock()

# Example dynamic invocation based on some external triggers


for i in range(60,80):
    play_midi_notes(i)
    time.sleep(0.1)
    
for i in range(79, 59, -1):
    play_midi_notes(i)
    time.sleep(0.1)  # Brief pause between starting each thread


# Assuming some mechanism to end the program cleanly
# Keep the main thread running while background threads are playing notes
while threading.active_count() > 1:
    time.sleep(1)

# Close the port after all threads are done
port.close()


import mido
from mido import Message
import time
import threading

# Open the MIDI port once
port = mido.open_output(mido.get_output_names()[0])

def set_instrument_to_guitar():
    # Program change to Acoustic Guitar (nylon), which is program number 24
    # Note: MIDI programs are zero-indexed in messages, so program 24 is sent as 23
    port.send(Message('program_change', program=28))

def play_midi_notes(midi_note):
    """Plays a given MIDI note in a separate thread, allowing dynamic note playing."""
    def play_note():
        with lock:  # Locking only the sending of messages
            port.send(Message('note_on', note=midi_note, velocity=64))
        time.sleep(1)  # Duration the note is held outside the lock
        with lock:
            port.send(Message('note_off', note=midi_note, velocity=64))
    
    # Start a new thread each time the function is called
    threading.Thread(target=play_note).start()

# Create a lock for thread-safe port access
lock = threading.Lock()

# Set MIDI instrument to guitar before playing notes
set_instrument_to_guitar()

# Example dynamic invocation based on some external triggers
for i in range(60, 100):
    play_midi_notes(i)
    time.sleep(0.1)
    
for i in range(99, 59, -1):
    play_midi_notes(i)
    time.sleep(0.1)  # Brief pause between starting each thread

# Assuming some mechanism to end the program cleanly
# Keep the main thread running while background threads are playing notes
#while threading.active_count() > 1:
#    time.sleep(1)

# Close the port after all threads are done
#port.close()

