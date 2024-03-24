import json
import shutil
import random
import numpy as np
import gradio as gr

def get_a_product_name(recorder_dir, json_data_path = 'data_gen_list.json', middle_part_prob = 0.75, packsize_prob = 0.5):
    with open(json_data_path, 'r') as f:
        data = json.load(f)
    
    first_part = random.choice(data['first_part'])
    middle_part = random.choice(data['middle_part'])
    final_part = random.choice(data['final_part'])
    pack_size = random.choice(data['pack_size'])
    
    if np.random.rand(1) >= middle_part_prob:
        single_product_name = f'{first_part.strip()} {middle_part.strip()} {final_part.strip()}'
    else:
        single_product_name = f'{first_part} {final_part}'
    
    if np.random.rand(1) >= packsize_prob:
        single_product_name = f'{single_product_name} {pack_size}'
    
    word = single_product_name[1:] if single_product_name.startswith(' ') else single_product_name
    
    list_of_audios = os.listdir(recorder_dir)
            
    if word.replace(" ", "_") + ".wav" in list_of_audios:
        print(f'{word} already exists, conitnuing to next one.')
        return get_a_product_name(recorder_dir, json_data_path = 'data_gen_list.json', middle_part_prob = 0.75, packsize_prob = 0.5)
    
    return word, gr.Microphone(value = None, label="Record Here", type="filepath", interactive=True)

import os

def create_folder_and_offer_product_name(recorder_name):
    # Sanitize the input text to avoid issues with folder names.
    folder_name = "".join(x for x in recorder_name if x.isalnum() or x in " _-")
    try:
        # Create the folder if it doesn't already exist.
        os.makedirs(folder_name, exist_ok=True)
        response = f"Folder '{folder_name}' created successfully."
    except Exception as e:
        response = f"Failed to create folder '{folder_name}': {str(e)}"
        print(response)
    
    product_name, audio_recorder = get_a_product_name(folder_name, json_data_path = 'data_gen_list.json', middle_part_prob = 0.75, packsize_prob = 0.5)

    # This function now also attempts to create a folder based on the input text.
    # Customize further as needed.
    return product_name, audio_recorder

def save_audio_and_offer_product_name(recorder_name, product_name, recorded_aud_path):
    # Sanitize the input text to avoid issues with folder names.
    folder_name = "".join(x for x in recorder_name if x.isalnum() or x in " _-")
    try:
        # Create the folder if it doesn't already exist.
        os.makedirs(folder_name, exist_ok=True)
        response = f"Folder '{folder_name}' created successfully."
    except Exception as e:
        response = f"Failed to create folder '{folder_name}': {str(e)}"
        print(response)
    
    shutil.copyfile(recorded_aud_path, 
                    os.path.join(folder_name, product_name.strip().replace(" ", "-") + ".wav"))

    product_name, audio_recorder = get_a_product_name(folder_name, json_data_path = 'data_gen_list.json', middle_part_prob = 0.75, packsize_prob = 0.5)

    # This function now also attempts to create a folder based on the input text.
    # Customize further as needed.
    return product_name, audio_recorder

with gr.Blocks() as app:
    gr.HTML("""
        <h2 style="color: green; text-align: center;">Product Data Collector</h2>
    """)
    with gr.Row():
        text_input = gr.Textbox(label="Who is recording? Enter you Name.")
    with gr.Column(variant="panel"):
        with gr.Row():
            output_text = gr.Textbox(label="Product Name to Read", interactive=False)
            audio_recorder = gr.Microphone(label="Record Here", type="filepath", interactive=True)
        with gr.Row():
            submit_button = gr.Button("Submit")
    
    text_input.submit(create_folder_and_offer_product_name, 
                      text_input, 
                      outputs=[output_text, audio_recorder])
    # audio_recorder.stop_recording(lambda : gr.Button("Submit", interactive=True), None, submit_button)
    submit_button.click(save_audio_and_offer_product_name, 
                        inputs=[text_input, output_text, audio_recorder], 
                        outputs=[output_text, audio_recorder])

# To run the app, use the following command in your Python environment:
app.queue()
app.launch(server_name="0.0.0.0",
           server_port=9989)
