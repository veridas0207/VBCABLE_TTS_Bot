
import asyncio
import os
import uuid
import pyttsx3
import edge_tts
import numpy as np
import sounddevice as sd
import soundfile as sf
from colorama import init, Fore, Style

# --- 設定 ---
TTS_CACHE_DIR = "tts_cache"
VBCABLE_DEVICE_NAME = "CABLE Input"
# --- ---

VBCABLE_DEVICE_ID = None
TTS_MODE = "edge"  # 'edge' 或 'pytts'

# 初始化 colorama
init(autoreset=True)

def find_vb_cable_device():
    """尋找並設定 VB-CABLE 的裝置 ID"""
    global VBCABLE_DEVICE_ID
    try:
        devices = sd.query_devices()
        for i, device in enumerate(devices):
            if VBCABLE_DEVICE_NAME in device['name'] and device['max_output_channels'] > 0:
                VBCABLE_DEVICE_ID = i
                print(Fore.GREEN + f"✅ 成功找到虛擬音源裝置: {device['name']} (ID: {i})")
                return
        print(Fore.RED + f"❌ 錯誤: 找不到指定的虛擬音源裝置 '{VBCABLE_DEVICE_NAME}'。")
        print(Fore.YELLOW + "請確認 VB-CABLE 已正確安裝，或修改腳本中的 VBCABLE_DEVICE_NAME ويع")
        VBCABLE_DEVICE_ID = None
    except Exception as e:
        print(Fore.RED + f"❌ 尋找音訊裝置時發生錯誤: {e}")
        VBCABLE_DEVICE_ID = None

def play_audio_on_device(filename: str):
    """在指定的裝置上播放音訊檔案"""
    if VBCABLE_DEVICE_ID is None:
        print(Fore.RED + "沒有可用的播放裝置，已略過播放。")
        return

    try:
        data, fs = sf.read(filename, dtype='float32')
        sd.play(data, fs, device=VBCABLE_DEVICE_ID)
        sd.wait()  # 等待播放完成
    except Exception as e:
        print(Fore.RED + f"❌ 播放音訊時發生錯誤: {e}")

async def generate_edge_tts(text: str, filename: str):
    """使用 edge-tts 產生語音"""
    try:
        communicate = edge_tts.Communicate(text=text, voice="zh-TW-HsiaoChenNeural", rate="+10%")
        await communicate.save(filename)
        return True
    except Exception as e:
        print(Fore.RED + f"❌ edge-tts 產生語音失敗: {e}")
        return False

def generate_pyttsx3_tts(text: str, filename: str, engine):
    """使用 pyttsx3 產生語音"""
    try:
        engine.save_to_file(text, filename)
        engine.runAndWait()
        return True
    except Exception as e:
        print(Fore.RED + f"❌ pyttsx3 產生語音失敗: {e}")
        return False

def print_help():
    """顯示幫助訊息"""
    print(Fore.CYAN + "\n--- TTS to Meet 幫助 ---")
    print("直接輸入文字後按 Enter 即可轉換為語音。")
    print("支援以下指令:")
    print(f"  {Fore.GREEN}/tts edge{Style.RESET_ALL}   - 切換到 Edge-TTS 引擎 (預設，聲音自然)")
    print(f"  {Fore.GREEN}/tts pytts{Style.RESET_ALL}   - 切換到 pyttsx3 引擎 (離線，速度快)")
    print(f"  {Fore.GREEN}/help{Style.RESET_ALL}        - 顯示此幫助訊息")
    print(f"  {Fore.GREEN}/exit{Style.RESET_ALL}        - 結束程式")
    print("--------------------------\n")

async def main():
    """主應用程式迴圈"""
    global TTS_MODE
    
    os.makedirs(TTS_CACHE_DIR, exist_ok=True)
    find_vb_cable_device()

    # 初始化 pyttsx3 引擎
    pytts_engine = pyttsx3.init()
    pytts_engine.setProperty('rate', 175)

    print(Fore.MAGENTA + "\n==============================================")
    print(Fore.MAGENTA + "===      TTS to Google Meet 啟動成功      ===")
    print(Fore.MAGENTA + "==============================================")
    print_help()

    while True:
        try:
            text = await asyncio.to_thread(input, Fore.WHITE + "請輸入要轉換的文字 (或輸入 /help) > ")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 正在結束程式...")
            break

        if not text.strip():
            continue

        # 指令處理
        if text.lower().strip() == '/exit':
            print("👋 正在結束程式...")
            break
        
        if text.lower().strip() == '/help':
            print_help()
            continue

        if text.lower().strip().startswith('/tts'):
            parts = text.strip().split()
            if len(parts) > 1:
                new_mode = parts[1].lower()
                if new_mode in ['edge', 'pytts']:
                    TTS_MODE = new_mode
                    print(Fore.GREEN + f"✅ TTS 引擎已切換為: {TTS_MODE}")
                else:
                    print(Fore.RED + f"❌ 無效的 TTS 模式: {new_mode}。請使用 'edge' 或 'pytts'。")
            else:
                print(Fore.YELLOW + f"目前 TTS 引擎為: {TTS_MODE}。可使用 /tts edge 或 /tts pytts 切換。")
            continue

        # 產生唯一的檔案名稱
        filename = os.path.join(TTS_CACHE_DIR, f"meet_{uuid.uuid4().hex}.mp3")
        
        print(f"\n{Fore.CYAN}正在轉換: '{text}' (使用 {TTS_MODE} 引擎)")
        
        success = False
        if TTS_MODE == 'edge':
            success = await generate_edge_tts(text, filename)
        else: # pytts
            # pyttsx3 的操作不是非同步的，所以我們在主迴圈中直接執行
            success = await asyncio.to_thread(generate_pyttsx3_tts, text, filename, pytts_engine)

        if success and os.path.exists(filename):
            print(f"{Fore.GREEN}🔊 轉換成功，正在播放...")
            play_audio_on_device(filename)
            # 播放後可以選擇刪除檔案以節省空間
            try:
                os.remove(filename)
            except OSError as e:
                print(Fore.RED + f"❌ 刪除快取檔案失敗: {e}")
        else:
            print(Fore.RED + "轉換失敗，請檢查錯誤訊息。")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 程式已由使用者中斷。")
