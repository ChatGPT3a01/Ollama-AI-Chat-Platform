# Ollama 本地 AI 模型對話平台

本專案為「自己架設 AI - 零基礎到大師」課程教學資源，涵蓋如何使用 Ollama 在本機部署 AI 模型，並自建網頁對話平台。

## 下載專案

### 方法一：使用 Git Clone
```bash
git clone https://github.com/YOUR_USERNAME/Ollama-AI-Chat-Platform.git
cd Ollama-AI-Chat-Platform
```

### 方法二：下載 ZIP
1. 點擊頁面上方的綠色 **Code** 按鈕
2. 選擇 **Download ZIP**
3. 解壓縮到想要的位置

## 環境準備

### 步驟一：安裝 Ollama

**Windows / Mac：**
1. 前往 https://ollama.com
2. 點擊 Download 下載安裝檔
3. 執行安裝程式，按照指示完成安裝

**Linux：**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 步驟二：下載 AI 模型

開啟終端機/命令提示字元，執行以下指令：

```bash
# 推薦：Llama 3（效能佳，約 4.7GB）
ollama pull llama3

# 備選：Mistral（較小，約 4.1GB）
ollama pull mistral

# 中文優化：Qwen（阿里通義千問）
ollama pull qwen2
```

### 步驟三：確認 Ollama 運行中

1. 確保 Ollama 在背景執行（系統托盤應有 Ollama 圖示）
2. 開啟瀏覽器，輸入 http://localhost:11434
3. 如果顯示 `Ollama is running` 即表示成功

## 使用教學

### 基礎使用

1. 用瀏覽器開啟 `範例程式/10.2_基礎對話平台.html`
2. 在輸入框輸入問題，按送出即可與 AI 對話

### 案例 1：合約審查助手

1. 開啟 `範例程式/案例1_合約審查助手.html`
2. 上傳 PDF / DOCX / TXT 合約檔案
3. AI 會自動分析合約內容並提供建議

### 案例 2：蘇格拉底式教學助手

1. 開啟 `範例程式/案例2_蘇格拉底式教學助手.html`
2. 輸入學習問題，AI 會用引導式教學法回答
3. 教師可開啟 `案例2_教師監控面板.html` 查看學習統計

### 案例 3：程式碼審查工具

1. 開啟 `範例程式/案例3_程式碼審查工具.html`
2. 貼上程式碼
3. 選擇功能：程式碼審查、測試生成、重構建議

### 案例 4：寫作工作台

1. 開啟 `範例程式/案例4_寫作工作台.html`
2. 輸入文章內容
3. 可進行改寫、風格轉換、標題發想、SEO 優化等

### 案例 5：個人知識庫

**簡易版（無需後端）：**
1. 直接開啟 `範例程式/案例5_知識庫前端.html`
2. 資料儲存在瀏覽器 localStorage

**進階版（需要 Python 後端）：**
```bash
# 安裝相依套件
pip install chromadb flask flask-cors requests

# 啟動後端伺服器
python 範例程式/案例5_知識庫伺服器.py

# 然後開啟 案例5_知識庫前端_進階版.html
```

## 專案內容

### 簡報（5 個 Part）

| Part | 標題 | 重點內容 |
|------|------|---------|
| Part 1 | 本地 AI 入門與價值 | 雲端 vs 本地比較、10 大應用情境 |
| Part 2 | 快速上手 Ollama | 安裝、下載模型、GUI 對話測試 |
| Part 3 | 自建網頁對話平台 | HTML/CSS/JS 實作、串接 Ollama API |
| Part 4 | 系統架構與模型選擇 | 三層架構、模型比較、硬體需求 |
| Part 5 | 實戰案例與延伸 | 5 大案例展示、進階應用方向 |

### 範例程式清單

| 檔案名稱 | 說明 |
|---------|------|
| `10.2_基礎對話平台.html` | 基本的 AI 對話介面 |
| `案例1_合約審查助手.html` | 上傳文件進行 AI 法律分析 |
| `案例2_蘇格拉底式教學助手.html` | AI 引導式教學法 |
| `案例2_教師監控面板.html` | 查看學生學習統計 |
| `案例3_程式碼審查工具.html` | 程式碼審查、測試生成 |
| `案例4_寫作工作台.html` | 改寫、風格轉換、SEO 優化 |
| `案例5_知識庫前端.html` | 純前端版本知識庫 |
| `案例5_知識庫伺服器.py` | Python 後端 (ChromaDB) |
| `案例5_知識庫前端_進階版.html` | 搭配後端的進階版本 |

## 常見問題

**Q: 網頁無法連接 AI？**
A: 請確認：
   - Ollama 已啟動（系統托盤有圖示）
   - 已下載模型（`ollama list` 可查看已安裝模型）
   - 瀏覽器可以訪問 http://localhost:11434

**Q: 模型回應很慢？**
A:
   - 首次載入模型需要時間（會載入到記憶體）
   - 可嘗試使用較小的模型如 `mistral` 或 `phi3`
   - 確保電腦有足夠的 RAM（建議 8GB 以上）

**Q: 中文顯示亂碼？**
A: 確保瀏覽器編碼設定為 UTF-8

**Q: 如何切換不同的模型？**
A: 在網頁介面中通常有模型選擇下拉選單，或修改程式碼中的 `model` 參數

## 硬體需求

| 等級 | RAM | 適用模型 |
|------|-----|---------|
| 入門 | 8GB | phi3, gemma:2b |
| 推薦 | 16GB | llama3, mistral, qwen2 |
| 進階 | 32GB+ | llama3:70b, mixtral |

## 授權

本專案為教學用途。
