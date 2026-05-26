"""
最小 Demo：使用者輸入 → ChatGPT 串流印出 → TTS 串流播放。

執行：uv run stream_chat_tts.py
或：  uv run stream_chat_tts.py "今天天氣如何？"
"""

from __future__ import annotations

import os
import queue
import sys
import threading

import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
TTS_MODEL = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")
TTS_VOICE = os.getenv("TTS_VOICE", "nova")
PCM_SAMPLE_RATE = 24000


class PcmStreamPlayer:
    """把 PCM chunk 餵進 queue，背景 thread 連續寫入 sounddevice。"""

    def __init__(self, sample_rate: int = PCM_SAMPLE_RATE) -> None:
        self._sample_rate = sample_rate
        self._queue: queue.Queue[bytes | None] = queue.Queue()
        self._done = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        with sd.OutputStream(
            samplerate=self._sample_rate,
            channels=1,
            dtype="int16",
        ) as stream:
            while True:
                chunk = self._queue.get()
                if chunk is None:
                    break
                audio = np.frombuffer(chunk, dtype=np.int16)
                if audio.size:
                    stream.write(audio)
        self._done.set()

    def feed(self, data: bytes) -> None:
        if data:
            self._queue.put(data)

    def close(self) -> None:
        self._queue.put(None)
        self._done.wait(timeout=120)


def stream_chat(client: OpenAI, user_text: str) -> str:
    """串流 ChatGPT，邊收邊印，回傳完整文字。"""
    stream = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": user_text}],
        stream=True,
    )

    parts: list[str] = []
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        if delta:
            print(delta, end="", flush=True)
            parts.append(delta)

    reply = "".join(parts).strip()
    if not reply:
        raise RuntimeError("ChatGPT 沒有回傳任何文字")
    return reply


def stream_tts_play(client: OpenAI, text: str) -> None:
    """TTS 串流收 PCM，邊收邊播。"""
    player = PcmStreamPlayer()
    try:
        with client.audio.speech.with_streaming_response.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text,
            response_format="pcm",
            instructions="用自然、清晰的繁體中文語氣說話。",
        ) as response:
            for chunk in response.iter_bytes(chunk_size=4096):
                player.feed(chunk)
    finally:
        player.close()


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("請在 .env 或環境變數設定 OPENAI_API_KEY", file=sys.stderr)
        sys.exit(1)

    user_text = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else input("你：").strip()
    if not user_text:
        print("請輸入一段文字。", file=sys.stderr)
        sys.exit(1)

    client = OpenAI()

    print("\n助手：", end="", flush=True)
    reply = stream_chat(client, user_text)
    print("\n\n（ChatGPT 串流完成，開始 TTS 串流播放…）")

    stream_tts_play(client, reply)
    print("（播放完成）")


if __name__ == "__main__":
    main()
