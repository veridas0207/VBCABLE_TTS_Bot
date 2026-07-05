# VBCABLE_TTS_Bot

把輸入的文字轉成語音，並播放到 VB-CABLE 的 `CABLE Input` 裝置，方便在 Google Meet、Discord、OBS 或其他軟體中當作麥克風音訊使用。

## 功能

- 支援 Edge TTS，預設使用 `zh-TW-HsiaoChenNeural`。
- 支援本機 `pyttsx3` TTS，可在沒有 Edge TTS 網路服務時切換使用。
- 自動尋找名稱包含 `CABLE Input` 的 VB-CABLE 輸出裝置。
- 每次輸入文字後會產生暫存音檔、播放到 VB-CABLE，播放完後自動刪除。

## 需求

- Windows
- Python 3.8 或更新版本
- VB-CABLE Virtual Audio Device
- 可連線到 Edge TTS 服務的網路環境，若要使用預設 `edge` 模式

## 安裝 VB-CABLE

官方下載頁：

- https://vb-audio.com/Cable/

安裝步驟：

1. 到官方頁下載 `VBCABLE_Driver_Pack45.zip`。
2. 解壓縮檔案。
3. 以系統管理員身分執行安裝程式。
4. 安裝完成後重新啟動電腦。
5. 打開 Windows 音效設定，確認出現 `CABLE Input` 與 `CABLE Output`。

程式會把語音播放到 `CABLE Input`。在 Google Meet、Discord 或其他軟體中，請把麥克風選成 `CABLE Output`。

## 安裝 Python 套件

可以直接執行：

```bat
setup.bat
```

或手動安裝：

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 啟動

在專案資料夾執行：

```powershell
python bot.py
```

看到提示文字後，直接輸入要播放的文字並按 Enter。

## 使用方式

一般播放：

```text
你好，這是一段測試語音
```

切換 TTS 模式：

```text
/tts edge
/tts pytts
```

其他指令：

```text
/help
/exit
```

## 在 Google Meet 使用

1. 先啟動 `python bot.py`。
2. 開啟 Google Meet。
3. 進入「設定」>「音訊」。
4. 將麥克風選成 `CABLE Output`。
5. 回到終端機輸入文字，語音就會送進 Meet。

如果你還需要聽到語音，可以在 Windows 音效控制台或 VB-CABLE 相關設定中啟用監聽，或用 OBS / Voicemeeter 之類的工具做音訊路由。

## 常見問題

### 找不到 `CABLE Input`

- 確認 VB-CABLE 已安裝。
- 重新啟動電腦後再試。
- 檢查 Windows 音訊裝置名稱是否包含 `CABLE Input`。
- 如果你的裝置名稱不同，請修改 `bot.py` 裡的 `VBCABLE_DEVICE_NAME`。

### Edge TTS 失敗

- 確認網路連線正常。
- 可先切換成本機 TTS：

```text
/tts pytts
```

### 沒有聲音進到 Meet 或 Discord

- 程式端要找到並播放到 `CABLE Input`。
- Meet / Discord 的麥克風要選 `CABLE Output`。
- 確認應用程式沒有靜音，也沒有選到實體麥克風。

### 中文顯示亂碼

如果終端機顯示亂碼，可先在 PowerShell 執行：

```powershell
chcp 65001
```

再重新啟動程式。
