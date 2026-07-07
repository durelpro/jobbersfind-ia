# 🧠 JobbersFind Intelligent Trust & Skill Engine (JITSE)

Bienvenue dans le dépôt du cerveau IA de JobbersFind. 
Ce projet est un système Multi-Agents d'évaluation de la crédibilité professionnelle spécifiquement taillé pour le marché du Cameroun (prenant en compte le dynamisme du secteur informel).

---

## 🏗️ Architecture
Il est constitué de **7 moteurs IA spécialisés** (Vision, Video, NLP, OCR, Cross-Validation, Scoring, Explainable AI) orchestrés par un **Decision Engine**. Le tout se déploie via une API FastAPI.

Retrouvez toute l'évolution du projet et l'état des Volumes architecturaux dans le `PROGRESS.md`.

## 🚀 Démarrage Rapide (Développement Sous Windows)

1. **Pré-requis :** Avoir `python` (3.9+) installé.
2. **Créer l'environnement virtuel :**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configurer l'environnement :**
   Copiez `.env.example` en `.env` à la racine pour ajouter vos clés.
5. **Lancer le serveur :**
   Double-cliquez sur `start.bat` 
   Ou exécutez la commande : `uvicorn src.api.main:app --reload`
   
L'API Swagger UI documentée sera accessible sur : http://127.0.0.1:8000/docs
