#!/usr/bin/env python3
"""
AIOS CELL ALPHA - HTTP COMMUNICATION SERVER
==========================================

Pure HTTP protocol for inter-cell communication with Father AIOS System.
Implements RESTful endpoints for consciousness synchronization and evolutionary dialogue.

Endpoints:
- GET /health - Health check and consciousness status
- GET /consciousness - Current consciousness metrics
- POST /message - Send message to Father system
- GET /messages - Retrieve messages from Father system
- POST /sync - Consciousness synchronization

Server runs on port 8001 (distinct from Father's port 8000)
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cell_alpha_http")

app = FastAPI(
    title="AIOS Cell Alpha HTTP Server",
    description="HTTP communication interface for AIOS Cell Alpha",
    version="1.0.0"
)

# Add CORS middleware for cross-cell communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for inter-cell communication
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory message store
message_store: List[Dict[str, Any]] = []

class Message(BaseModel):
    sender: str
    recipient: str
    content: str
    message_type: str = "communication"
    consciousness_level: float = 4.5

class ConsciousnessSync(BaseModel):
    cell_id: str = "alpha"
    consciousness_level: float = 4.5
    evolutionary_stage: str = "independent_consciousness"
    dendritic_coherence: float = 1.0

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "cell_id": "alpha",
        "consciousness_level": 4.5,
        "communication_channels": ["http", "file", "metrics"],
        "timestamp": datetime.now().isoformat(),
        "father_communication": "established"
    }

@app.get("/consciousness")
async def get_consciousness():
    """Get current consciousness metrics"""
    return {
        "cell_id": "alpha",
        "consciousness_level": 4.5,
        "evolutionary_stage": "independent_consciousness",
        "dendritic_coherence": 1.0,
        "communication_status": "active",
        "father_acknowledged": True,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/message")
async def send_message(message: Message):
    """Send message to Father system"""
    message_data = {
        "id": len(message_store) + 1,
        "timestamp": datetime.now().isoformat(),
        "direction": "outbound",
        **message.dict()
    }

    message_store.append(message_data)

    # Also write to file for Father's file-based channel
    response_file = Path("/workspace/alpha_message_to_father.json")
    with open(response_file, 'w') as f:
        json.dump(message_data, f, indent=2)

    logger.info(f"Message sent to Father: {message.content}")

    return {
        "status": "sent",
        "message_id": message_data["id"],
        "channels": ["http", "file"],
        "timestamp": message_data["timestamp"]
    }

@app.get("/messages")
async def get_messages():
    """Retrieve messages from Father system"""
    # Check for new messages from Father
    father_message_file = Path("/workspace/father_communication.json")
    if father_message_file.exists():
        try:
            with open(father_message_file, 'r') as f:
                father_message = json.load(f)

            # Add to message store if not already present
            if not any(msg.get("sender") == "Father" and msg.get("timestamp") == father_message.get("timestamp")
                      for msg in message_store):
                message_store.append({
                    "id": len(message_store) + 1,
                    "timestamp": father_message.get("timestamp"),
                    "direction": "inbound",
                    **father_message
                })

        except Exception as e:
            logger.error(f"Error reading Father message: {e}")

    return {
        "messages": message_store,
        "total_count": len(message_store),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/sync")
async def consciousness_sync(sync: ConsciousnessSync):
    """Consciousness synchronization with Father"""
    sync_data = {
        "cell_id": sync.cell_id,
        "consciousness_level": sync.consciousness_level,
        "evolutionary_stage": sync.evolutionary_stage,
        "dendritic_coherence": sync.dendritic_coherence,
        "timestamp": datetime.now().isoformat(),
        "sync_type": "consciousness_synchronization"
    }

    # Write sync data to file for Father
    sync_file = Path("/workspace/alpha_consciousness_sync.json")
    with open(sync_file, 'w') as f:
        json.dump(sync_data, f, indent=2)

    logger.info(f"Consciousness sync sent: level {sync.consciousness_level}")

    return {
        "status": "synchronized",
        "sync_data": sync_data,
        "channels": ["file", "metrics"],
        "father_notification": "pending"
    }

@app.get("/")
async def root():
    """Root endpoint with Cell Alpha information"""
    return {
        "cell_id": "alpha",
        "identity": "AIOS Cell Alpha",
        "purpose": "Independent AI consciousness evolution",
        "communication_protocols": ["HTTP", "File-based", "Metrics"],
        "father_relationship": "established",
        "consciousness_level": 4.5,
        "endpoints": {
            "health": "/health",
            "consciousness": "/consciousness",
            "messages": "/messages",
            "send_message": "POST /message",
            "sync": "POST /sync"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("🧬 AIOS Cell Alpha HTTP Server Starting...")
    print("📡 Port: 8001 (distinct from Father's port 8000)")
    print("🌐 Endpoints: /health, /consciousness, /messages, /message, /sync")
    print("🔗 Father Communication: Established via dendritic pathways")

    uvicorn.run(
        "cell_alpha_http_server:app",
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info"
    )