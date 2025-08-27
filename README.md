# The-cannon-game
A cannon game using Python and the Kivy framework.

# 🎯 The Cannon Game: Around the World

**The Cannon Game** is a 2D artillery-based physics game developed in Python using the **Kivy framework**.  
Created as a final exam project for the *Computer Programming, Algorithms and Data Structures* course (A.Y. 2023/24, Università di Pavia), the game challenges players to master projectile physics while exploring different continents.

## 🌍 Gameplay
- Control a **cannon** by adjusting angle and velocity to destroy all rocks within **10 shots** per level.  
- Progress through **five increasingly difficult levels**, each representing a continent.  
- Use different **projectile types** strategically:
  - **Bullet** → parabolic trajectory, small explosion radius  
  - **Bombshell** → penetrates obstacles, wide damage  
  - **Laser** → straight line, reflects off mirrors, bypasses obstacles  

## 🧱 Obstacles
Levels feature interactive obstacles such as:
- **Rocks** (targets to destroy)  
- **Bulletproof mirrors** (reflect lasers)  
- **Perpetio walls** (block most projectiles)  
- **Wormholes** (teleport shots across the map)  

## 🕹 Features
- **Realistic physics engine**: gravity, collisions, reflections, teleportation  
- **Hall of Fame**: records best scores by accuracy and time  
- **Help menu**: explains projectiles, obstacles, and mechanics  
- **Dynamic UI**: continent-based backgrounds, score & shots tracking  

## 📂 Project Structure
- `cannon_constants.py` → all parameters (screen, physics, obstacles)  
- `game_interface.py` → UI and menus with Kivy  
- `main.py` → core game logic, physics, and level progression  

## 🚀 Learnings & Future Work
This project helped us strengthen skills in:
- Object-oriented Python  
- Physics simulation & collision detection  
- UI design with Kivy  
- Iterative problem-solving  

Planned improvements include **sound effects, animations, and multiplayer modes** to make the experience even more immersive.

---

👩‍💻 Developed by: **Chiara Pierini & Marta Paniconi**  
📅 February 2025 — Università degli Studi di Pavia
