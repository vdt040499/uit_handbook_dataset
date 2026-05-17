import json
import time
import requests

RAG_API_URL = "http://localhost:3001/api/v1/workspace/uit-handbook/chat" 
RAG_API_KEY = "YOUR_API_KEY_HERE"

def query_rag_system(question: str) -> dict:
    headers = {
        "Authorization": f"Bearer {RAG_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "message": question,
        "mode": "chat" 
    }
    
    try:
        response = requests.post(RAG_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        answer = data.get("textResponse", data.get("response", ""))
        
        context = []
        if "sourceDocuments" in data:
            context = [doc.get("pageContent", "") for doc in data["sourceDocuments"]]
            
        return {
            "answer": answer,
            "retrieved_context": context,
            "raw_response": data
        }
    except Exception as e:
        print(f"Lỗi khi query RAG: {e}")
        return {"answer": "ERROR", "retrieved_context": [], "raw_response": {}}

def run_evaluation():
    input_file = "handbook_test.jsonl"
    output_file = "handbook_predictions.jsonl"
    
    with open(input_file, "r", encoding="utf-8") as f:
        test_data = [json.loads(line) for line in f if line.strip()]
        
    print(f"Bắt đầu chạy test cho {len(test_data)} mẫu...")
    
    results = []
    with open(output_file, "w", encoding="utf-8") as f_out:
        for idx, sample in enumerate(test_data):
            print(f"[{idx+1}/{len(test_data)}] Đang xử lý ID: {sample['id']}...")
            
            start_time = time.time()
            rag_output = query_rag_system(sample["question"])
            latency = time.time() - start_time
            
            result = {
                "id": sample["id"],
                "question": sample["question"],
                "expected_answer": sample["expected_answer"],
                "category": sample["category"],
                "expected_behavior": sample["expected_behavior"],
                "must_contain": sample["must_contain"],
                "must_not_contain": sample["must_not_contain"],
                "predicted_answer": rag_output["answer"],
                "retrieved_context": rag_output["retrieved_context"],
                "latency": latency
            }
            results.append(result)
            
            f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
            
            time.sleep(1)
            
    print(f"DONE! {output_file}")

if __name__ == "__main__":
    run_evaluation()
