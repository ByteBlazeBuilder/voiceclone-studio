import uuid
import json
import threading
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
import psutil

app = Flask(__name__, static_folder='static')

VOICES_DIR = Path("voices")
OUTPUT_DIR = Path("outputs")
VOICES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

jobs = {}
tts_instance = None

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "tr": "Turkish",
    "pl": "Polish",
    "nl": "Dutch",
    "ar": "Arabic",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
}

def get_tts():
    global tts_instance
    if tts_instance is not None:
        return tts_instance
    import torch
    from TTS.api import TTS
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts_instance = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    return tts_instance

def generate_audio(job_id, text, voice_path, language):
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 10
        tts = get_tts()
        jobs[job_id]["progress"] = 50
        output_path = OUTPUT_DIR / f"{job_id}.wav"
        tts.tts_to_file(
            text=text,
            speaker_wav=str(voice_path),
            language=language,
            file_path=str(output_path)
        )
        jobs[job_id]["progress"] = 100
        jobs[job_id]["status"] = "done"
        jobs[job_id]["output"] = str(output_path)
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/system")
def system_info():
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ram = psutil.virtual_memory()
    return jsonify({
        "device": device,
        "ram_total": round(ram.total / (1024**3), 1),
        "ram_used": round(ram.used / (1024**3), 1),
        "ram_percent": ram.percent
    })

@app.route("/api/voices", methods=["GET"])
def list_voices():
    meta_file = VOICES_DIR / "meta.json"
    if not meta_file.exists():
        return jsonify([])
    with open(meta_file) as f:
        return jsonify(json.load(f))

@app.route("/api/voices", methods=["POST"])
def upload_voice():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files["file"]
    name = request.form.get("name", "Voice").strip() or "Voice"
    vid = str(uuid.uuid4())[:8]
    ext = Path(file.filename).suffix
    save_path = VOICES_DIR / f"{vid}{ext}"
    file.save(str(save_path))
    meta_file = VOICES_DIR / "meta.json"
    voices = []
    if meta_file.exists():
        with open(meta_file) as f:
            voices = json.load(f)
    voices.append({"id": vid, "name": name, "file": str(save_path)})
    with open(meta_file, "w") as f:
        json.dump(voices, f)
    return jsonify({"id": vid, "name": name})

@app.route("/api/voices/<vid>", methods=["DELETE"])
def delete_voice(vid):
    meta_file = VOICES_DIR / "meta.json"
    if not meta_file.exists():
        return jsonify({"ok": True})
    with open(meta_file) as f:
        voices = json.load(f)
    voice = next((v for v in voices if v["id"] == vid), None)
    if voice:
        try:
            Path(voice["file"]).unlink()
        except:
            pass
        voices = [v for v in voices if v["id"] != vid]
        with open(meta_file, "w") as f:
            json.dump(voices, f)
    return jsonify({"ok": True})

@app.route("/api/languages")
def list_languages():
    return jsonify([{"id": k, "name": v} for k, v in LANGUAGES.items()])

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    text = data.get("text", "").strip()
    voice_id = data.get("voice_id")
    language = data.get("language", "en")
    if not text:
        return jsonify({"error": "No text"}), 400
    if not voice_id:
        return jsonify({"error": "Select a voice profile"}), 400
    meta_file = VOICES_DIR / "meta.json"
    voices = []
    if meta_file.exists():
        with open(meta_file) as f:
            voices = json.load(f)
    voice = next((v for v in voices if v["id"] == voice_id), None)
    if not voice:
        return jsonify({"error": "Voice not found"}), 404
    job_id = str(uuid.uuid4())[:12]
    jobs[job_id] = {"status": "queued", "progress": 0}
    t = threading.Thread(target=generate_audio, args=(job_id, text, voice["file"], language))
    t.daemon = True
    t.start()
    return jsonify({"job_id": job_id})

@app.route("/api/job/<job_id>")
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Not found"}), 404
    return jsonify(job)

@app.route("/api/download/<job_id>")
def download(job_id):
    job = jobs.get(job_id)
    if not job or job["status"] != "done":
        return jsonify({"error": "Not ready"}), 404
    return send_file(job["output"], as_attachment=True, download_name=f"cloned_{job_id}.wav")

if __name__ == "__main__":
    print("\n VoiceClone Studio — XTTS-v2")
    print("   Open http://localhost:5000\n")
    app.run(debug=False, port=5000)
