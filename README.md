# 🍌 Banana Game – Distributed Service Architecture Project

A Python based educational game developed using Tkinter, SQLite, and an external REST API, designed to demonstrate event-driven architecture, distributed services, and software design principles.

This project was developed as part of the CIS045-3 Distributed Service Architectures module.
## 🛠️ Tech Stack

 - Language: Python 3

 - GUI: Tkinter

 - Database: SQLite

 - Image Processing: Pillow (PIL)

 - Audio: pygame.mixer

 - Architecture: Event-Driven, Modular Design

 - API: Banana Puzzle API (JSON)

## 🎮 Game Overview

Banana Game is a puzzle-based desktop game where players must solve visual math challenges fetched dynamically from an external API. The game includes:

 - User authentication (Sign Up / Login)

 - Timed gameplay with bonus-time challenges

 - Profile management

 - Sound effects and background music

 - Custom-designed UI with image-based components

## 🧠 Key Features
### 🔐 User Authentication (Virtual Identity)

 - Username & password-based login system

 - Secure credential storage using SQLite

 - Session-based identity handling during gameplay

### ⏱️ Timer & Bonus Time System

 - Countdown timer during gameplay

 - “Get More Time” feature (limited to 3 uses)

 - Bonus time awarded by solving API-based challenges

 - Timer pauses while bonus challenge window is open

### 🌐 Distributed Service (Interoperability)

 - Integrates with Banana API
https://marcconrad.com/uob/banana/api.php

 - Fetches puzzle images and solutions via HTTP (REST / JSON)

 - Demonstrates real-world service interoperability

### 🖼️ Custom UI & UX

 - Image-based buttons and backgrounds

 - Custom modal message boxes (success, error, warning, win/lose)

 - Fullscreen, borderless windows for immersive gameplay

### 🔊 Audio System

 - Background music

 - Click / success / error sound effects

 - Independent mute controls for music and SFX
