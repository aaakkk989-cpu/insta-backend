from fastapi import FastAPI
from pydantic import BaseModel
from instagrapi import Client
from instagrapi.exceptions import BadPassword, TwoFactorRequired, ChallengeRequired

app = FastAPI()

class WorkerAuth(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return {"message": "Server is Running"}

@app.post("/api/verify-worker")
def verify_worker(data: WorkerAuth):
    cl = Client()
    try:
        cl.login(data.username, data.password)
        return {"status": "SUCCESS", "message": "Account Active"}
    except BadPassword:
        return {"status": "FAILED", "message": "Invalid Username or Password"}
    except (TwoFactorRequired, ChallengeRequired):
        return {"status": "OTP_REQUIRED", "message": "Please enter OTP code"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
                
