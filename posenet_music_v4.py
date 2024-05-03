import cv2
from PoseNet.pose import detect_pose
import mido
from mido import Message
import time
import threading

# Open the MIDI port once
port = mido.open_output(mido.get_output_names()[1])
global left_wrist_previous_x
global left_hip_previous_x
global left_knee_previous_x
global last_time
left_wrist_previous_x = 0
left_hip_previous_x=0
left_knee_previous_x=0
last_time = 0

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


def main():
  
  detect_pose(display_in_cv_image, quit_on_key=True)

def display_in_cv_image(image,poses):
  global left_wrist_previous_x
  global left_hip_previous_x
  global left_knee_previous_x
  global last_time
  current_time = time.time()
  r = random.randint(36, 59)
  pr = random.randint(60, 127)
  cv2.imshow('Pose detector', image)
  for pose in poses:
    #print(f"Pose Score: {pose.score: .2f}")
    for label, keypoint in pose.keypoints.items():
      if label.name == "LEFT_KNEE" and keypoint.score > 0.1:
        #print(f"(x={keypoint.point.x:.2f}, y={keypoint.point.y: .2f}), Score: {keypoint.score:.2f}")
        #print(f"{label.name}:    Score: {keypoint.score:.2f}")
        #print(f"(x={keypoint.point.x:.2f}, y={keypoint.point.y: .2f}) ")
         
        left_knee_current_x = int(keypoint.point.x)
        if left_knee_current_x > left_knee_previous_x+20:
          play_drum_beats(r)
          left_knee_previous_x = left_knee_current_x
          last_time=current_time
        if left_knee_current_x < left_knee_previous_x-20:
          left_knee_previous_x = left_knee_current_x  
          last_time=current_time          
          play_drum_beats(r)
        
      if label.name == "LEFT_HIP" and keypoint.score > 0.1:
        left_hip_current_x = int(keypoint.point.x) 
        if left_hip_current_x > left_hip_previous_x+10:
          left_hip_previous_x = left_hip_current_x 
          last_time=current_time          
          play_midi_notes(pr)        
          
        if left_hip_current_x < left_hip_previous_x-10:
          left_hip_previous_x = left_hip_current_x 
          left_last_time=left_current_time
          play_midi_notes(pr)         
       
      if label.name == "LEFT_WRIST" and keypoint.score > 0.1:          
        left_wrist_current_x = int(keypoint.point.x) 
        if left_wrist_current_x > left_wrist_previous_x+10:
          left_wrist_previous_x = left_wrist_current_x  
          play_random_guitar_note_threaded()  
          last_time=current_time          
          
        if left_wrist_current_x < left_wrist_previous_x-10:
          left_wrist_previous_x = left_wrist_current_x 
          play_random_guitar_note_threaded()
          last_time=current_time       
          
        #print("last_time: ",last_time, ", current_time: ",current_time )
        if current_time > last_time+10:
           play_drum_beats(36)
           time.sleep(0.25)
           play_drum_beats(36)
           time.sleep(0.25)
           play_drum_beats(38)
           time.sleep(0.25)
        
        
if __name__ == '__main__':
  main()