import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import tempfile

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def text_to_speech(text):
    if not text or not text.strip():
        return None, "Please enter some text."

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio_path = temp_audio.name

        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        ) as response:
            response.stream_to_file(temp_audio_path)

        return temp_audio_path, "Speech generated successfully."

    except Exception as e:
        return None, f"Error: {str(e)}"


with gr.Blocks() as demo:
    gr.Markdown("# Text to Speech Converter Demo")
    gr.Markdown("Enter text and convert it into speech.")

    text_input = gr.Textbox(
        label="Enter text",
        placeholder="Type your text here...",
        lines=6
    )

    convert_btn = gr.Button("Convert to Speech")

    audio_output = gr.Audio(label="Generated Audio", type="filepath")
    status_output = gr.Textbox(label="Status", interactive=False)

    convert_btn.click(
        fn=text_to_speech,
        inputs=text_input,
        outputs=[audio_output, status_output]
    )

demo.launch()