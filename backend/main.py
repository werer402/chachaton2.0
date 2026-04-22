from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import User, Building, Company
from datetime import datetime
from typing import Dict, List
import uvicorn

app = FastAPI(title="MTB City Pro API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Хранилище данных (In-memory)
users: Dict[str, User] = {}
buildings: Dict[str, Building] = {}

COMPANIES = {
    "mtb_bank": Company("mtb_bank", "МТБ Банк", "🏦", 0, ""),
    "wildberries": Company("wildberries", "Wildberries", "🟣", 200, "PROMO-WB-15"),
    "steam": Company("steam", "Steam", "🎮", 100, "MTB-GABEN-2024"),
    "yandex_go": Company("yandex_go", "Яндекс Go", "🚕", 50, "GO-MTB-FREE"),
    "burger_king": Company("burger_king", "Burger King", "🍔", 30, "BK-MTB-COIN"),
    "mak_by": Company("mak_by", "Mak.by", "🍟", 30, "MAK-BY-PROMO"),
}

def sync_user_data(user_id: str):
    """Ядро пассивного дохода: считаем всё с момента последнего входа"""
    user = users[user_id]
    now = datetime.now()
    seconds_passed = (now - user.last_sync).total_seconds()
    hours = seconds_passed / 3600
    
    user_b = [b for b in buildings.values() if b.building_id.startswith(user_id)]
    for b in user_b:
        reward = b.get_current_income() * hours
        if b.income_type == "mt_coins":
            user.mt_coins += reward
        else:
            b.promo_progress += reward
            if b.promo_progress >= 100:
                user.inventory.append(f"{COMPANIES[b.company_id].name}: {COMPANIES[b.company_id].promo_text}")
                b.promo_progress %= 100
    user.last_sync = now

@app.get("/health")
def health(): return {"status": "ok"}

@app.post("/user/register")
def register(user_id: str, username: str):
    if user_id not in users:
        users[user_id] = User(user_id=user_id, username=username)
        # Банк строится сразу
        b_id = f"{user_id}_mtb_bank"
        buildings[b_id] = Building(b_id, "mtb_bank", income_rate=100, income_type="mt_coins")
    return users[user_id]

@app.get("/user/{user_id}")
def get_user(user_id: str):
    sync_user_data(user_id)
    return users[user_id]

@app.post("/farm/add-spending")
def add_spending(user_id: str, company_id: str, amount: float):
    user = users[user_id]
    user.total_spent += amount
    comp = COMPANIES[company_id]
    
    if user.total_spent >= comp.unlock_threshold:
        b_id = f"{user_id}_{company_id}"
        if b_id not in buildings:
            buildings[b_id] = Building(b_id, company_id, income_rate=10, income_type="promo_percent")
        elif amount >= 150: # Сильная транзакция апает уровень
            buildings[b_id].level += 1
    return {"status": "success"}

@app.get("/farm/buildings/{user_id}")
def get_farm(user_id: str):
    sync_user_data(user_id)
    # Возвращаем и построенные здания, и список всех компаний для 3D-рендера
    all_data = []
    for c_id, info in COMPANIES.items():
        b_id = f"{user_id}_{c_id}"
        is_built = b_id in buildings
        all_data.append({
            "info": info,
            "state": buildings[b_id].__dict__ if is_built else None
        })
    return all_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)