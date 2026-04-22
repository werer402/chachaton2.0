from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class User:
    user_id: str
    username: str
    mt_coins: float = 1000.0  # Стартовый капитал
    total_spent: float = 0.0
    inventory: List[str] = field(default_factory=list)
    last_sync: datetime = field(default_factory=datetime.now)

@dataclass
class Building:
    building_id: str
    company_id: str
    level: int = 1
    income_rate: float = 0.0  # Коины или % в час
    income_type: str = "mt_coins"  # "mt_coins" или "promo_percent"
    promo_progress: float = 0.0
    
    def get_current_income(self):
        """Прогрессия дохода: +20% за каждый уровень выше первого"""
        return self.income_rate * (1 + (self.level - 1) * 0.2)

@dataclass
class Company:
    company_id: str
    name: str
    icon: str
    unlock_threshold: float
    promo_text: str