import cv2
from PoseNet.pose import detect_pose
import time
import threading
import random
import pygame
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pydub import AudioSegment

# Open the MIDI port once

global left_wrist_previous_x
global right_wrist_previous_x
global left_hip_previous_x
global right_hip_previous_x
global left_knee_previous_x
global right_knee_previous_x
global left_shoulder_previous_x
global right_shoulder_previous_x
global left_elbow_previous_x
global right_elbow_previous_x
global left_shoulder_previous_x
global right_ankle_previous_x
global left_ankle_previous_x
global file_map
global last_time

left_wrist_previous_x = 0
right_wrist_previous_x = 0
left_hip_previous_x = 0
right_hip_previous_x = 0
left_knee_previous_x = 0
right_knee_previous_x = 0
left_shoulder_previous_x = 0
right_shoulder_previous_x = 0
left_elbow_previous_x = 0
right_elbow_previous_x = 0
left_ankle_previous_x = 0
right_ankle_previous_x = 0
last_time = 0

pygame.mixer.init()
pool = ThreadPoolExecutor(max_workers=5)
play_records = {}  # This dictionary will store datetime objects as keys and dicts of file paths and counts as values.

def play_ogg_file(file_path):
    """ Play a single .ogg file and record the play time. """
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    # Record the time and file played
    timestamp = datetime.now()
    if timestamp in play_records:
        if file_path in play_records[timestamp]:
            play_records[timestamp][file_path] += 1
        else:
            play_records[timestamp][file_path] = 1
    else:
        play_records[timestamp] = {file_path: 1}

def thread_play(file_path):
    """ Submit play task to the thread pool. """
    pool.submit(play_ogg_file, file_path)

def compile_audio():
    """Compile the audio tracks played during the simulation into a single file."""
    if not play_records:
        print("No audio has been recorded.")
        return
    
    # Find the earliest and latest times to set the initial duration of the silent segment
    start_time = min(play_records.keys())
    end_time = max(play_records.keys())
    total_duration = int((end_time - start_time).total_seconds() * 1000)
    compiled_audio = AudioSegment.silent(duration=total_duration)

    print("Starting audio compilation...")
    for timestamp in sorted(play_records.keys()):
        elapsed_time = (timestamp - start_time).total_seconds()
        offset = int(elapsed_time * 1000)  # Ensure offset is an integer number of milliseconds
        print(f"Processing sounds at {timestamp} (elapsed {elapsed_time} seconds, offset {offset}ms)")

        for file_path, count in play_records[timestamp].items():
            if count > 0:
                try:
                    print(f"Adding {file_path} {count} times...")
                    # Load the sound file, potentially handling any specific audio properties here
                    sound = AudioSegment.from_file(file_path) * count
                    compiled_audio = compiled_audio.overlay(sound, position=offset)
                    print(f"Current compiled audio length: {len(compiled_audio)} ms after adding {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            else:
                print(f"Skipping {file_path} as count is zero.")

    # Attempt to export the compiled audio
    try:
        compiled_audio.export("compiled_audio.wav", format="wav")
        print(f"Audio compiled and saved to 'compiled_audio.wav', duration: {compiled_audio.duration_seconds} seconds.")
    except Exception as e:
        print(f"Error exporting audio: {e}")



file_map = {
    '1': 'drum_base_a.ogg',
    '2': 'drum_base_b.ogg',
    '3': 'drum_base_c.ogg',
    '4': 'drum_base_d.ogg',
    '5': 'drum_base_e.ogg',
    '6': 'drum_base_f.ogg',
    '7': 'drum_base_g.ogg',
    '8': 'drum_base_h.ogg',
    '9': 'drum_base_i.ogg',
    '10': 'drum_base_j.ogg',
    '11': 'drum_base_k.ogg',
    '12': 'drum_base_l.ogg',
    '13': 'drum_base_m.ogg',
    '14': 'drum_base_n.ogg',
    '15': 'guitar_a.ogg',
    '16': 'guitar_b.ogg',
    '17': 'guitar_c.ogg',
    '18': 'guitar_d.ogg',
    '19': 'guitar_e.ogg',
    '20': 'guitar_f.ogg',
    '21': 'guitar_g.ogg',
    '22': 'guitar_h.ogg',
    '23': 'guitar_i.ogg',
    '24': 'guitar_j.ogg',
    '25': 'guitar_k.ogg',
    '26': 'guitar_l.ogg',
    '27': 'guitar_m.ogg',
    '28': 'guitar_n.ogg',
    '29': 'analog_synth_a.ogg',
    '30': 'analog_synth_b.ogg',
    '31': 'analog_synth_c.ogg',
    '32': 'analog_synth_d.ogg',
    '33': 'analog_synth_e.ogg',
    '34': 'analog_synth_f.ogg',
    '35': 'analog_synth_g.ogg',
    '36': 'analog_synth_h.ogg',
    '37': 'analog_synth_i.ogg',
    '38': 'analog_synth_j.ogg',
    '39': 'analog_synth_k.ogg',
    '40': 'analog_synth_l.ogg',
    '41': 'analog_synth_m.ogg',
    '42': 'analog_synth_n.ogg',
    '43': 'clap_a.ogg',
    '44': 'string_a.ogg',
    '45': 'string_b.ogg',
    '46': 'string_c.ogg',
    '47': 'string_d.ogg',
    '48': 'string_e.ogg',
    '49': 'string_f.ogg',
    '50': 'string_g.ogg',
    '51': 'string_h.ogg',
    '52': 'string_i.ogg',
    '53': 'string_j.ogg',
    '54': 'string_k.ogg',
    '55': 'string_l.ogg',
    '56': 'string_m.ogg',
    '57': 'string_n.ogg',
}



def main():
  
  detect_pose(display_in_cv_image, quit_on_key=True)
  compile_audio()
def display_in_cv_image(image,poses):
  global left_wrist_previous_x
  global right_wrist_previous_x
  global left_hip_previous_x
  global right_hip_previous_x
  global left_knee_previous_x
  global right_knee_previous_x
  global left_shoulder_previous_x
  global right_shoulder_previous_x
  global left_elbow_previous_x
  global right_elbow_previous_x
  global left_shoulder_previous_x
  global right_ankle_previous_x
  global left_ankle_previous_x
  global last_time
  global file_map
  current_time = time.time()
  drum_base = random.randint(1, 14)
  guitar = random.randint(15, 28)
  analog_synth = random.randint(29, 42)
  string = random.randint(44, 57)
  cv2.imshow('Pose detector', image)
  for pose in poses:
    #print(f"Pose Score: {pose.score: .2f}")
    for label, keypoint in pose.keypoints.items():
      if label.name == "LEFT_KNEE" and keypoint.score > 0.1:
        #print(f"(x={keypoint.point.x:.2f}, y={keypoint.point.y: .2f}), Score: {keypoint.score:.2f}")
        #print(f"{label.name}:    Score: {keypoint.score:.2f}")
        #print(f"(x={keypoint.point.x:.2f}, y={keypoint.point.y: .2f}) ")
         
        left_knee_current_x = int(keypoint.point.x)
        if left_knee_current_x > left_knee_previous_x+10:
          thread_play(file_map[str(drum_base)])
          left_knee_previous_x = left_knee_current_x
          last_time=current_time
        if left_knee_current_x < left_knee_previous_x-10:
          left_knee_previous_x = left_knee_current_x  
          last_time=current_time          
          thread_play(file_map[str(drum_base)])
        
      if label.name == "RIGHT_KNEE" and keypoint.score > 0.1:     
        right_knee_current_x = int(keypoint.point.x)
        if right_knee_current_x > right_knee_previous_x+10:
          thread_play(file_map[str(string)])
          right_knee_previous_x = right_knee_current_x
          last_time=current_time
        if right_knee_current_x < right_knee_previous_x-10:
          right_knee_previous_x = right_knee_current_x  
          last_time=current_time          
          thread_play(file_map[str(string)])

      if label.name == "LEFT_WRIST" and keypoint.score > 0.1:     
        left_wrist_current_x = int(keypoint.point.x)
        if left_wrist_current_x > left_wrist_previous_x+10:
          left_wrist_previous_x = left_wrist_current_x  
          thread_play(file_map[str(analog_synth)])   
          last_time=current_time          
          
        if left_wrist_current_x < left_wrist_previous_x-10:
          left_wrist_previous_x = left_wrist_current_x 
          thread_play(file_map[str(analog_synth)]) 
          last_time=current_time          

       
       
      if label.name == "RIGHT_WRIST" and keypoint.score > 0.1:          
        right_wrist_current_x = int(keypoint.point.x) 
        if right_wrist_current_x > right_wrist_previous_x+30:
          right_wrist_previous_x = right_wrist_current_x  
          thread_play(file_map[str(43)])   
          last_time=current_time          
          
        if right_wrist_current_x < right_wrist_previous_x-30:
          right_wrist_previous_x = right_wrist_current_x 
          thread_play(file_map[str(43)]) 
          last_time=current_time            
          
      if label.name == "RIGHT_ELBOW" and keypoint.score > 0.1:          
        right_elbow_current_x = int(keypoint.point.x) 
        if right_elbow_current_x > right_elbow_previous_x+30:
          right_elbow_previous_x = right_elbow_current_x  
          thread_play(file_map[str(guitar)])   
          last_time=current_time          
          
        if right_elbow_current_x < right_elbow_previous_x-30:
          right_elbow_previous_x = right_elbow_current_x 
          thread_play(file_map[str(guitar)]) 
          last_time=current_time            
          
      # if label.name == "LEFT_ELBOW" and keypoint.score > 0.1:          
        # left_elbow_current_x = int(keypoint.point.x) 
        # if left_elbow_current_x > left_elbow_previous_x+30:
          # left_elbow_previous_x = left_elbow_current_x  
          # thread_play(file_map[str(43)])   
          # last_time=current_time          
          
        # if left_elbow_current_x < left_elbow_previous_x-30:
          # left_elbow_previous_x = left_elbow_current_x 
          # thread_play(file_map[str(43)]) 
          # last_time=current_time                   

      # if label.name == "RIGHT_SHOULDER" and keypoint.score > 0.1:          
        # right_shoulder_current_x = int(keypoint.point.x) 
        # if right_shoulder_current_x > right_shoulder_previous_x+30:
          # right_shoulder_previous_x = right_shoulder_current_x  
          # thread_play(file_map[str(43)])   
          # last_time=current_time          
          
        # if right_shoulder_current_x < right_shoulder_previous_x-30:
          # right_shoulder_previous_x = right_shoulder_current_x 
          # thread_play(file_map[str(43)]) 
          # last_time=current_time            
          
      # if label.name == "LEFT_SHOULDER" and keypoint.score > 0.1:          
        # left_shoulder_current_x = int(keypoint.point.x) 
        # if left_shoulder_current_x > left_shoulder_previous_x+30:
          # left_shoulder_previous_x = left_shoulder_current_x  
          # thread_play(file_map[str(43)])   
          # last_time=current_time          
          
        # if left_shoulder_current_x < left_shoulder_previous_x-30:
          # left_shoulder_previous_x = left_shoulder_current_x 
          # thread_play(file_map[str(43)]) 
          # last_time=current_time   
      # if label.name == "RIGHT_ANKLE" and keypoint.score > 0.1:          
        # right_ankle_current_x = int(keypoint.point.x) 
        # if right_ankle_current_x > right_ankle_previous_x+30:
          # right_ankle_previous_x = right_ankle_current_x  
          # thread_play(file_map[str(43)])   
          # last_time=current_time          
          
        # if right_ankle_current_x < right_ankle_previous_x-30:
          # right_ankle_previous_x = right_ankle_current_x 
          # thread_play(file_map[str(43)]) 
          # last_time=current_time            
          
      # if label.name == "LEFT_ANKLE" and keypoint.score > 0.1:          
        # left_ankle_current_x = int(keypoint.point.x) 
        # if left_ankle_current_x > left_ankle_previous_x+30:
          # left_ankle_previous_x = left_ankle_current_x  
          # thread_play(file_map[str(43)])   
          # last_time=current_time          
          
        # if left_ankle_current_x < left_ankle_previous_x-30:
          # left_ankle_previous_x = left_ankle_current_x 
          # thread_play(file_map[str(43)]) 
          # last_time=current_time      
          
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
