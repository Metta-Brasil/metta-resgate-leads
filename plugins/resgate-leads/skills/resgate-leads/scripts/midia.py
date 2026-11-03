#!/usr/bin/env python3
"""Lê o anúncio em vídeo. Precisa de ffmpeg e ffprobe; para transcrever, faster-whisper (pip install faster-whisper).

  video <arquivo> --id ID            transcrição da fala, quadros para ler o texto da tela e versão leve (até 16 MB)
  conferir <arquivos...>             confere tamanho contra os limites do WhatsApp

A saída vai para Metta-Resgate/criativos/arquivos/<ID>/ na pasta de trabalho.
Limites da Meta (Cloud API, mídia): vídeo MP4 H.264 + AAC até 16 MB; imagem JPEG/PNG até 5 MB, lado até 4.096 px.
"""
import argparse, json, os, shutil, subprocess, sys

RAIZ_PADRAO = os.path.join(os.getcwd(), "Metta-Resgate")
MAX_VIDEO = 16 * 1024 * 1024
MAX_IMG = 5 * 1024 * 1024
ALVO_VIDEO = int(15.0 * 1024 * 1024)  # folga sob o limite


def exige(prog):
    if not shutil.which(prog):
        sys.exit(f"Falta o programa '{prog}'. No Mac: brew install ffmpeg")


def pasta_saida(raiz, id_):
    p = os.path.join(os.path.expanduser(raiz), "criativos", "arquivos", id_)
    os.makedirs(p, exist_ok=True)
    return p


def duracao(arq):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", arq],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def ler_wav(wav):
    """Lê o WAV mono 16 kHz gerado pelo ffmpeg como float32, sem depender do PyAV."""
    import wave
    import numpy as np  # type: ignore
    with wave.open(wav, "rb") as w:
        bruto = w.readframes(w.getnframes())
    return np.frombuffer(bruto, dtype=np.int16).astype(np.float32) / 32768.0


def transcrever(wav, destino):
    """Tenta faster-whisper, depois openai-whisper. Sem nenhum dos dois, ou com erro, devolve None."""
    try:
        try:
            from faster_whisper import WhisperModel  # type: ignore
            modelo = WhisperModel("small", device="cpu", compute_type="int8")
            segs, _ = modelo.transcribe(ler_wav(wav), language="pt")
            texto = "\n".join(s.text.strip() for s in segs)
        except ImportError:
            import whisper  # type: ignore
            texto = whisper.load_model("small").transcribe(ler_wav(wav), language="pt")["text"]
    except ImportError:
        return None
    except Exception as e:  # transcrição falhou: segue sem ela, com o motivo
        print(f"transcrição falhou: {e}", file=sys.stderr)
        return None
    open(destino, "w", encoding="utf-8").write(texto.strip() + "\n")
    return destino


def cmd_video(a):
    exige("ffmpeg"); exige("ffprobe")
    out = pasta_saida(a.raiz, a.id)
    dur = duracao(a.arquivo)
    res = {"id": a.id, "origem": a.arquivo, "duracao_s": round(dur, 1), "quadros": []}
    # quadros: 1s, 3s, 6s e depois a cada 8s, para ler o texto da tela
    tempos = [t for t in [1, 3, 6] if t < dur] + list(range(14, int(dur), 8))
    for t in tempos:
        q = os.path.join(out, f"quadro_{t:03d}s.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", a.arquivo, "-frames:v", "1",
                        "-vf", "scale=720:-2", q], check=True)
        res["quadros"].append(q)
    wav = os.path.join(out, "audio.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.arquivo, "-vn", "-ac", "1", "-ar", "16000", wav],
                   check=True)
    t = transcrever(wav, os.path.join(out, "transcricao.txt"))
    res["transcricao"] = t or "SEM_TRANSCRICAO: instale faster-whisper (pip install faster-whisper) ou transcreva à mão"
    # versão leve: H.264 Main sem B-frames, AAC 96k, faststart, 720p, bitrate pela duração
    leve = os.path.join(out, f"{a.id}_envio.mp4")
    kbps = max(300, int((ALVO_VIDEO * 8 / dur) / 1000) - 96)
    for tentativa in range(3):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.arquivo,
                        "-vf", "scale='min(720,iw)':-2", "-c:v", "libx264", "-profile:v", "main", "-bf", "0",
                        "-pix_fmt", "yuv420p", "-b:v", f"{kbps}k", "-maxrate", f"{kbps}k", "-bufsize", f"{2*kbps}k",
                        "-c:a", "aac", "-b:a", "96k", "-ac", "2", "-movflags", "+faststart", leve], check=True)
        if os.path.getsize(leve) <= MAX_VIDEO:
            break
        kbps = int(kbps * 0.8)
    res["arquivo_envio"] = leve
    res["tamanho_envio_mb"] = round(os.path.getsize(leve) / 1024 / 1024, 2)
    res["dentro_do_limite"] = os.path.getsize(leve) <= MAX_VIDEO
    os.remove(wav)
    print(json.dumps(res, ensure_ascii=False, indent=1))


def cmd_conferir(a):
    ok = True
    for f in a.arquivos:
        ext = os.path.splitext(f)[1].lower()
        tam = os.path.getsize(f)
        lim = MAX_VIDEO if ext in {".mp4", ".3gp"} else MAX_IMG if ext in {".jpg", ".jpeg", ".png", ".webp"} else 100 * 1024 * 1024
        dentro = tam <= lim
        ok &= dentro
        print(f"{'OK ' if dentro else 'ACIMA'} {tam/1024/1024:7.2f} MB  {f}")
    sys.exit(0 if ok else 1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--raiz", default=os.environ.get("RESGATE_RAIZ", RAIZ_PADRAO))
    s = p.add_subparsers(dest="cmd", required=True)
    x = s.add_parser("video"); x.add_argument("arquivo"); x.add_argument("--id", required=True); x.set_defaults(f=cmd_video)
    x = s.add_parser("conferir"); x.add_argument("arquivos", nargs="+"); x.set_defaults(f=cmd_conferir)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
