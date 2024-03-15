
import os
import time
import wavio
import numpy as np
import sounddevice as sd


def main(word_list):
    
    sr = 16000
    
    dir = input("Who is this User? What is your name? : ")
    if not os.path.isdir(dir):
        os.mkdir(dir)
        print(f"Created directory: {dir}\n")
    else:
        print(f"Found existing directory: {dir}\n")
    
    recordCounter = 0
    
    cmd = input("Press 'enter' to Continue, Anything else to quit: ")
    if cmd == "":
        for n, word in enumerate(word_list):
            cmd = input(f"[Enter] to start recording,  [q] to quit => Next Word - `{word}`:")
            if cmd == "":
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
                
                # if not filename.endswith(".wav"):
                filename = os.path.join(dir, word.replace(" ", "_") + ".wav")
                    
                    
                wavio.write(filename, myrecording, sr, sampwidth=2)
                recordCounter += 1
                print(f"Saved Recording - {recordCounter}, Filename -  {filename}")
            

            elif cmd == "q":
                print("Recording Suspended!")
                break
            else:
                print(f"{word} Skipped!")
                
    print(f"Total {recordCounter} recordings saved, Bye!")


        
        
if __name__ == '__main__':
    word_list = ["some medicine", "Other medicine"]
    main(word_list)