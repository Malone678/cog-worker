from cog import BasePredictor, Input, Path
import requests
import base64
from typing import Any

class Predictor(BasePredictor):
    def setup(self):
        self.tts_url = "http://localhost:8880/v1/audio/speech"

    def predict(self, text: str = Input(description="Text for TTS"),
                voice: str = Input(default="af_bella", description="Voice ID"),
                speed: float = Input(default=1.0, description="Speed")) -> Path:
        payload = {
            "model": "kokoro",
            "input": text,
            "voice": voice,
            "speed": speed,
            "response_format": "mp3"
        }
        response = requests.post(self.tts_url, json=payload)
        response.raise_for_status()
        audio_bytes = response.content
        # Save to temp file
        output_path = Path(self.output_path / "audio.mp3")
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
        return output_path
