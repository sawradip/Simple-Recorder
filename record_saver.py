
import os
import time
import wavio
import numpy as np
import sounddevice as sd


def main():
    
    sr = 16000
    
    dir = input("Which directory you want to store the recordings? : ")
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print(f"Created directory: {dir}\n\n")
    else:
        print(f"Found existing directory: {dir}\n\n")
    
    recordCounter = 0
    while True:
        
        cmd = input("Press 'enter' to start recording, q to quit: ")
        if cmd == "":
            print("Recording... Press 'enter' to stop.")

            recording = []
            def callback(indata, frames, time, status):
                recording.append(indata.copy())
                
            # Create a stream object with callback
            with sd.InputStream(samplerate=sr, channels=1, callback=callback):
                while True:
                    time.sleep(0.1)
                    if input() == "":  # Stop recording when 'q' is pressed
                        break

            # Convert list of numpy arrays into a single numpy array
            myrecording = np.concatenate(recording, axis=0)
            print(myrecording.shape)

            filename = ""
            if filename == "":
                filename = input("Enter filename to save (with .wav extension): ")

            # if not filename.endswith(".wav"):
            filename = os.path.join(dir, filename + ".wav")
                
                
            wavio.write(filename, myrecording, sr, sampwidth=2)
            recordCounter += 1
            print(f"Saved Recording - {recordCounter}, Filename -  {filename}")
            
            
        elif cmd == "q":
            print(f"Total {recordCounter} recordings saved, Bye!")
            break
        else:
            print(f"You pressed - {cmd}")

        
        
if __name__ == '__main__':
    
    main()