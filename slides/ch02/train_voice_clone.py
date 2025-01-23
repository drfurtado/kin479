import os
import torch
from TTS.trainer import Trainer, TrainerArgs
from TTS.tts.configs.yourtts_config import YourTTSConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.utils.audio import AudioProcessor
from TTS.tts.models.yourtts import YourTTS

# Define training parameters
config = YourTTSConfig(
    batch_size=8,
    eval_batch_size=8,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    text_cleaner="phoneme_cleaners",
    use_phonemes=True,
    phoneme_language="en-us",
    phoneme_cache_path=os.path.join("data", "phoneme_cache"),
    precompute_num_workers=4,
    print_step=25,
    print_eval=True,
    mixed_precision=True,
    output_path=os.path.join("data", "output"),
    datasets=[
        BaseDatasetConfig(
            name="kin479",
            meta_file_train="metadata.csv",
            path="data/kin479_dataset/",
            language="en"
        ),
    ]
)

# Create dataset directory
os.makedirs("data/kin479_dataset", exist_ok=True)

# Create metadata file
voice_samples = [
    "../ch01/audio/479-ch01-1_8_primary_focus.mp3",
    "../ch01/audio/479-ch01-1_8_introduction.mp3",
    "../ch01/audio/479-ch01-1_8_overview.mp3",
    "../ch01/audio/479-ch01-1_8_welcome.mp3",
    "../ch01/audio/479-ch01-1_8_conclusion.mp3"
]

# Convert MP3s to WAV and create metadata
import librosa
import soundfile as sf
from pydub import AudioSegment

print("Preparing dataset...")
with open("data/kin479_dataset/metadata.csv", "w") as f:
    f.write("audio_file|text|speaker_name|language\n")
    for i, sample in enumerate(voice_samples):
        # Load MP3 and convert to WAV
        audio = AudioSegment.from_mp3(sample)
        wav_path = f"data/kin479_dataset/sample_{i}.wav"
        audio.export(wav_path, format="wav")
        
        # Get the duration
        y, sr = librosa.load(wav_path)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Use filename as placeholder text since we don't have transcriptions
        text = os.path.splitext(os.path.basename(sample))[0]
        
        # Write to metadata
        f.write(f"sample_{i}.wav|{text}|speaker1|en\n")

print("Dataset prepared. Starting training...")

# Initialize the model
model = YourTTS.init_from_config(config)

# Initialize the trainer
trainer = Trainer(
    TrainerArgs(
        restore_path=None,  # Path to a checkpoint to restore from
        checkpoint_path="data/output",  # Where to save checkpoints
        skip_train_epoch=False,
    ),
    config,
    output_path="data/output",
    model=model,
    train_samples=load_tts_samples(
        "data/kin479_dataset/metadata.csv",
        eval_split=True
    ),
    eval_samples=load_tts_samples(
        "data/kin479_dataset/metadata.csv",
        eval_split=True
    ),
)

# Start training
trainer.fit()
