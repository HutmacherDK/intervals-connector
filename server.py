from fastapi import FastAPI, Request
import requests, base64, os

app = FastAPI()

INTERVALS_KEY = os.getenv("INTERVALS_KEY")  # your API_KEY:<token>
ATHLETE_ID = os.getenv("ATHLETE_ID", "i113739")

@app.post("/intervals")
async def proxy(request: Request):
    data = await request.json()
    method = data.get("method", "GET")
    path = data.get("path", "")
    body = data.get("body", None)

    b64 = base64.b64encode(INTERVALS_KEY.encode()).decode()
    headers = {"Authorization": f"Basic {b64}", "Content-Type": "application/json"}

    url = f"https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/{path.lstrip('/')}"
    r = requests.request(method, url, headers=headers, json=body)

    try:
        return {"status": r.status_code, "data": r.json()}
    except:
        return {"status": r.status_code, "data": r.text}
