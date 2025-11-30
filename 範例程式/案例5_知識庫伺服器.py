# knowledge_server.py
# 個人知識庫後端伺服器
#
# 使用說明：
# 1. 安裝必要套件：pip install chromadb flask flask-cors requests
# 2. 下載 Embedding 模型：ollama pull nomic-embed-text
# 3. 確認 Ollama 已啟動：ollama serve
# 4. 執行此程式：python 案例5_知識庫伺服器.py
# 5. 用瀏覽器開啟：案例5_知識庫前端_進階版.html
#
# 注意：必須下載 nomic-embed-text 模型，一般對話模型不支援 embedding 功能

from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
import requests
import os

app = Flask(__name__)
CORS(app)  # 允許前端跨域請求

# 建立本地向量資料庫
# 資料會儲存在 ./my_knowledge_base 資料夾中
client = chromadb.PersistentClient(path="./my_knowledge_base")

# 取得或建立 collection
try:
    collection = client.get_collection(name="my_notes")
    print("✅ 載入現有知識庫")
except:
    collection = client.create_collection(
        name="my_notes",
        metadata={"description": "個人知識庫"}
    )
    print("✅ 建立新知識庫")


def get_embedding(text):
    """使用 Ollama 產生向量（Embedding）
    注意：必須使用專門的 embedding 模型（如 nomic-embed-text）
    一般對話模型（如 llama3、qwen）不支援此功能
    """
    try:
        response = requests.post('http://localhost:11434/api/embeddings', json={
            'model': 'nomic-embed-text',  # 專門的 embedding 模型
            'prompt': text
        })
        result = response.json()
        if 'embedding' in result:
            return result['embedding']
        else:
            print(f"Embedding 回應異常：{result}")
            print("請確認已執行：ollama pull nomic-embed-text")
            return None
    except Exception as e:
        print(f"Embedding 錯誤：{e}")
        return None


@app.route('/add_note', methods=['POST'])
def add_note():
    """API：新增筆記"""
    data = request.json
    title = data.get('title', '未命名')
    content = data.get('content', '')
    tags = data.get('tags', '')

    if not content:
        return jsonify({'error': '內容不能為空'}), 400

    # 產生向量
    embedding = get_embedding(content)
    if not embedding:
        return jsonify({'error': '無法產生向量，請確認 Ollama 已啟動'}), 500

    # 儲存到資料庫
    note_id = f"note_{collection.count() + 1}"
    collection.add(
        documents=[content],
        embeddings=[embedding],
        metadatas=[{"title": title, "tags": tags}],
        ids=[note_id]
    )

    return jsonify({'message': f'已儲存筆記：{title}', 'id': note_id})


@app.route('/ask', methods=['POST'])
def ask_question():
    """API：查詢知識庫"""
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({'error': '請輸入問題'}), 400

    # 搜尋相關筆記
    query_embedding = get_embedding(question)
    if not query_embedding:
        return jsonify({'error': '無法處理問題'}), 500

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # 如果沒有筆記
    if not results['documents'][0]:
        return jsonify({
            'answer': '知識庫中還沒有筆記，請先新增一些筆記。',
            'sources': []
        })

    # 組合上下文
    context = "\n\n---\n\n".join(results['documents'][0])
    sources = [meta['title'] for meta in results['metadatas'][0]]

    # 呼叫 Ollama 生成答案
    prompt = f"""基於以下我的筆記內容，回答問題。如果筆記中沒有相關資訊，請誠實說「筆記中沒有相關內容」。

我的筆記：
{context}

問題：{question}

請用繁體中文回答："""

    try:
        # 使用對話模型生成答案
        # 請根據你下載的模型修改此處，例如：llama3、qwen、mistral 等
        response = requests.post('http://localhost:11434/api/generate', json={
            'model': 'qwen:latest',  # 修改為你下載的對話模型
            'prompt': prompt,
            'stream': False
        })
        answer = response.json()['response']
    except Exception as e:
        answer = f"AI 回應錯誤：{e}"

    return jsonify({
        'answer': answer,
        'sources': sources
    })


@app.route('/notes', methods=['GET'])
def list_notes():
    """API：列出所有筆記"""
    all_notes = collection.get()
    notes = []
    for i, doc in enumerate(all_notes['documents']):
        notes.append({
            'id': all_notes['ids'][i],
            'title': all_notes['metadatas'][i].get('title', '未命名'),
            'preview': doc[:100] + '...' if len(doc) > 100 else doc
        })
    return jsonify({'notes': notes, 'total': len(notes)})


@app.route('/delete_note/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """API：刪除筆記"""
    try:
        collection.delete(ids=[note_id])
        return jsonify({'message': f'已刪除筆記：{note_id}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clear_all', methods=['DELETE'])
def clear_all():
    """API：清除所有筆記"""
    try:
        # 刪除並重建 collection
        client.delete_collection(name="my_notes")
        global collection
        collection = client.create_collection(
            name="my_notes",
            metadata={"description": "個人知識庫"}
        )
        return jsonify({'message': '已清除所有筆記'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """API：健康檢查"""
    return jsonify({
        'status': 'ok',
        'notes_count': collection.count()
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🧠 個人知識庫伺服器")
    print("=" * 50)
    print("📍 API 網址：http://localhost:5000")
    print("💡 請確認 Ollama 已啟動（ollama serve）")
    print("💡 請確認已下載 embedding 模型（ollama pull nomic-embed-text）")
    print("")
    print("可用的 API 端點：")
    print("  POST /add_note     - 新增筆記")
    print("  POST /ask          - 詢問知識庫")
    print("  GET  /notes        - 列出所有筆記")
    print("  DELETE /delete_note/<id> - 刪除筆記")
    print("  DELETE /clear_all  - 清除所有筆記")
    print("  GET  /health       - 健康檢查")
    print("=" * 50)

    app.run(port=5000, debug=True)
