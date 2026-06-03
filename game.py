

Copy code
import requests, random


API_URL = "https:6a1f89a2b79eec0d6cf0d53a.mockapi.io/players"

# Weapons & gear
weapon_pool = [
    {"name": "Combat Knife", "type": "Melee", "rarity": "Common", "damage": 15, "weight": 50},
    {"name": "Pistol", "type": "Gun", "rarity": "Common", "damage": 25, "ammo": 12, "weight": 40},
    {"name": "Shotgun", "type": "Gun", "rarity": "Uncommon", "damage": 50, "ammo": 6, "weight": 25},
    {"name": "Assault Rifle", "type": "Gun", "rarity": "Rare", "damage": 35, "ammo": 30, "weight": 20},
    {"name": "Sniper Rifle", "type": "Gun", "rarity": "Legendary", "damage": 90, "ammo": 5, "weight": 5},
    {"name": "Grenade", "type": "Explosive", "rarity": "Uncommon", "damage": 70, "blast_radius": 5, "weight": 15},
    {"name": "Riot Shield", "type": "Defense", "rarity": "Rare", "defense": 80, "weight": 10}
]

def spin_wheel():
    total = sum(w["weight"] for w in weapon_pool)
    pick = random.randint(1, total)
    current = 0
    for w in weapon_pool:
        current += w["weight"]
        if pick <= current:
            return w

def register(username):
    return requests.post(API_URL, json={"username": username, "level": 1, "rank": "Bronze", "inventory": []}).json()

def get_player(username):
    for p in requests.get(API_URL).json():
        if p["username"] == username:
            return p

def update_player(player):
    requests.put(f"{API_URL}/{player['id']}", json=player)

def spin(username):
    player = get_player(username)
    if not player: return
    weapon = spin_wheel()
    player["inventory"].append(weapon)
    player["level"] += 1
    if player["level"] >= 10: player["rank"] = "Silver"
    if player["level"] >= 20: player["rank"] = "Gold"
    update_player(player)
    print(f"🎯 {weapon['name']} ({weapon['rarity']}) - {weapon.get('damage','')} dmg")

if __name__ == "__main__":
    name = input("Username: ")
    if not get_player(name): register(name)
    while True:
        cmd = input("spin / quit: ").lower()
        if cmd == "quit": break
        if cmd == "spin": spin(name)
