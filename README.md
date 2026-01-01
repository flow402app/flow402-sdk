## How to add it to your existing API (2 steps, < 2 minutes)

1. Install the SDK in your project terminal:
   ```bash
   pip install flow402-sdk

2. Open your main API file (e.g. main.py or app.py) and add these two lines:
   ```python
   from flow402 import Flow402Middleware   # add this import
   app = FastAPI()
   app.add_middleware(Flow402Middleware, api_key="your_key_here")  # add this line

Full example of what your file should look like:
  ```python
  from fastapi import FastAPI
from flow402 import Flow402Middleware   # ← new

app = FastAPI()

app.add_middleware(Flow402Middleware, api_key="fk_your_key_from_dashboard")  # ← new

@app.get("/")
def home():
    return {"message": "My x402 API"}

@app.post("/api/chat")
def chat():
    return {"response": "Paid response!"}
