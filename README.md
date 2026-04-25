# 🎙 VoiceClone Studio

> Free, unlimited voice cloning — no subscriptions, no credits, runs 100% on your machine.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![XTTS-v2](https://img.shields.io/badge/Model-XTTS--v2-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ What is this?

VoiceClone Studio is a **local web app** that lets you clone any voice using just a 10–30 second audio sample. Built on top of [Coqui XTTS-v2](https://github.com/coqui-ai/TTS) — the same technology behind paid tools like ElevenLabs.

- ✅ **No API key** — runs fully offline after setup
- ✅ **No credits** — unlimited generations forever
- ✅ **Hindi + English** — and 15 other languages
- ✅ **Clean web UI** — runs in your browser
- ✅ **Save voice profiles** — upload once, reuse anytime

---

## 🖥 Screenshots

> Upload a voice sample → paste script → download audio

---

## 🚀 Quick Start

### Requirements
- Windows 10/11
- [Miniconda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe) installed
- 4GB free disk space (for model download)
- Internet connection (first run only — downloads ~1.8GB model)

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/voiceclone-studio.git
cd voiceclone-studio
```

### Step 2 — Create conda environment
```bash
conda create -n voiceclone python=3.10 -y
conda activate voiceclone
```

### Step 3 — Install dependencies
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install coqui-tts transformers==4.46.1 flask psutil
```

### Step 4 — Run the app
```bash
python app.py
```

Open **http://localhost:5000** in your browser.

> ⚠️ First generation downloads the XTTS-v2 model (~1.8GB). This happens once automatically.

---

## 🎯 How to Use

1. **Record a voice sample** — 10–30 seconds, quiet room, no background noise
2. **Upload it** in the sidebar → give it a name → click Save
3. **Select the voice** from the sidebar
4. **Choose language** — Hindi, English, or 15 others
5. **Paste your script** in the text box
6. Click **Generate Cloned Audio**
7. **Download WAV** — ready to upload to YouTube

---

## 🌍 Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| Hindi | `hi` | English | `en` |
| Spanish | `es` | French | `fr` |
| German | `de` | Italian | `it` |
| Portuguese | `pt` | Russian | `ru` |
| Turkish | `tr` | Polish | `pl` |
| Dutch | `nl` | Arabic | `ar` |
| Chinese | `zh-cn` | Japanese | `ja` |
| Korean | `ko` | | |

---

## ⚡ Performance

| Hardware | Generation speed |
|----------|-----------------|
| CPU only | ~3–5 min per minute of audio |
| Nvidia GPU (RTX 3060+) | ~15–30 sec per minute of audio |

To enable GPU, install CUDA version of torch:
```bash
pip uninstall torch torchaudio
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 📁 Project Structure

```
voiceclone-studio/
├── app.py              # Flask backend
├── static/
│   └── index.html      # Web UI
├── voices/             # Saved voice profiles (auto-created)
├── outputs/            # Generated audio files (auto-created)
└── README.md
```

---

## 🛠 Tech Stack

- **[Coqui XTTS-v2](https://github.com/coqui-ai/TTS)** — voice cloning model
- **[Flask](https://flask.palletsprojects.com/)** — lightweight Python web server
- **Vanilla JS + CSS** — zero frontend dependencies

---

## ❓ FAQ

**Q: Does it work without internet?**  
A: Yes — after the first run downloads the model (~1.8GB), it works 100% offline.

**Q: How long should the voice sample be?**  
A: 15–30 seconds gives best results. Make sure it's clean audio with no background noise.

**Q: Can I clone any voice?**  
A: Technically yes. Please use responsibly and only clone voices you have permission to use.

**Q: Why does the first generation take so long?**  
A: It downloads the XTTS-v2 model (~1.8GB) on first run. After that it's cached locally.

**Q: Does it support Hindi?**  
A: Yes — Hindi is supported natively by XTTS-v2.

---

## ⚠️ Disclaimer

This tool is for **personal, educational, and creative use only**. Do not use it to clone voices without consent or for deceptive purposes. The authors are not responsible for misuse.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Credits

- [Coqui TTS](https://github.com/coqui-ai/TTS) for the XTTS-v2 model
- Built with ❤️ for the YouTube creator community
