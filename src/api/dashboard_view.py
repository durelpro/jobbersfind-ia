"""
JITSE Dashboard View
Contient le code HTML, CSS et JS pour l'interface de JITSE.
Intègre le système d'authentification IAM avec workflow de validation Admin.
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JITSE - JobbersFind Intelligent Trust Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.5);
            --secondary: #ec4899;
            --secondary-glow: rgba(236, 72, 153, 0.5);
            --bg: #0f111a;
            --bg-panel: rgba(255, 255, 255, 0.03);
            --bg-panel-hover: rgba(255, 255, 255, 0.06);
            --border: rgba(255, 255, 255, 0.08);
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Outfit', sans-serif;
        }

        body {
            background-color: var(--bg);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(236, 72, 153, 0.15), transparent 25%);
            background-size: 100% 100%;
            background-attachment: fixed;
        }

        /* --- AUTHENTICATION SCREEN --- */
        #auth-screen {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(15, 17, 26, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .auth-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 3rem;
            width: 100%;
            max-width: 450px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            text-align: center;
        }
        .auth-tabs {
            display: flex;
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
        }
        .auth-tab {
            flex: 1;
            padding: 1rem;
            cursor: pointer;
            color: var(--text-muted);
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .auth-tab.active {
            color: var(--primary);
            border-bottom: 3px solid var(--primary);
        }
        #login-error, #reg-msg, #pwd-msg {
            margin-bottom: 1rem;
            font-size: 0.9rem;
            font-weight: 500;
        }

        /* --- LAYOUT COMPONENT --- */
        #app-layout {
            display: none; /* Hidden until logged in */
            width: 100%;
            
        }

        .sidebar {
            width: 280px;
            background: rgba(15, 17, 26, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid var(--border);
            padding: 2rem 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            z-index: 10;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-item {
            padding: 1rem 1.25rem;
            border-radius: 12px;
            color: var(--text-muted);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .nav-item:hover, .nav-item.active {
            background: var(--bg-panel-hover);
            color: var(--text);
            transform: translateX(5px);
        }

        .nav-item.active {
            border: 1px solid var(--border);
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 20px rgba(0,0,0,0.2), inset 0 0 0 1px var(--border);
        }

        .main-content {
            flex: 1;
            padding: 2rem 3rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            height: 100vh;
            overflow-y: auto;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            font-size: 2rem;
            font-weight: 700;
        }

        .status-badge {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .glass-panel {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 2.5rem;
            backdrop-filter: blur(12px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            display: none; /* All sections hidden by default */
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        /* --- FORMS & UPLOADS --- */
        .form-group {
            margin-bottom: 1.5rem;
            text-align: left;
        }
        
        .upload-zone {
            border: 2px dashed var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            background: rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: pointer;
            margin-bottom: 0.5rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .upload-zone:hover {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.05);
        }
        .upload-zone i {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }
        .upload-zone p {
            color: var(--text-muted);
            font-size: 0.9rem;
        }
        
        .form-label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
            color: var(--text-muted);
            font-weight: 500;
            font-size: 0.9rem;
        }

        .form-label .badge-bonus {
            background: rgba(16, 185, 129, 0.2);
            color: var(--success);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-weight: bold;
        }

        .form-control {
            width: 100%;
            background: rgba(0,0,0,0.2);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 1rem 1.25rem;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
            outline: none;
        }
        .form-control:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
        }

        .btn {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px var(--primary-glow);
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.75rem;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px var(--primary-glow);
        }
        .btn-small {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
            width: auto;
            border-radius: 8px;
        }

        /* --- ADMIN LIST --- */
        .admin-list {
            list-style: none;
            margin-top: 1rem;
        }
        .admin-list li {
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .btn-approve {
            background: rgba(16, 185, 129, 0.15);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }
        .btn-approve:hover {
            background: var(--success);
            color: white;
        }

        /* --- PORTFOLIO RESULTS --- */
        .passport-result {
            display: none;
            margin-top: 2rem;
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .score-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: conic-gradient(var(--success) var(--percentage), rgba(255,255,255,0.1) 0);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            margin: 0 auto 2rem;
        }
        .score-circle::before {
            content: '';
            position: absolute;
            width: 120px;
            height: 120px;
            background: var(--bg);
            border-radius: 50%;
        }
        .score-value {
            position: relative;
            font-size: 2.5rem;
            font-weight: 800;
            z-index: 1;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        .badge-list { list-style: none; }
        .badge-item {
            padding: 1rem;
            background: rgba(255,255,255,0.03);
            border-radius: 12px;
            margin-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid var(--border);
        }

        .ai-recommendation {
            margin-top: 2rem;
            padding: 1.5rem;
            background: rgba(99, 102, 241, 0.1);
            border-left: 4px solid var(--primary);
            border-radius: 0 12px 12px 0;
            font-style: italic;
            line-height: 1.6;
        }

        .spinner {
            display: none;
            width: 24px;
            height: 24px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        .file-preview {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }
        .file-item {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border);
            padding: 0.5rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
        }
        .file-item img {
            width: 40px;
            height: 40px;
            object-fit: cover;
            border-radius: 4px;
        }
    </style>
</head>
<body>

    <!-- AUTHENTICATION SCREEN -->
    <div id="auth-screen">
        <div class="auth-box">
            <div class="logo" style="justify-content:center; margin-bottom: 2rem;">
                <i class="fa-solid fa-shield-halved"></i>
                JITSE Auth Portal
            </div>
            
            <div class="auth-tabs">
                <div class="auth-tab active" id="tab-login" onclick="switchAuthTab('login')">Se connecter</div>
                <div class="auth-tab" id="tab-register" onclick="switchAuthTab('register')">Demander Accès</div>
            </div>

            <!-- Login Form -->
            <div id="form-login">
                <div id="login-error" style="color: var(--danger); display: none;"></div>
                <div class="form-group">
                    <input type="email" id="login-email" class="form-control" placeholder="Email (ex: admin@jobbersfind.com)">
                </div>
                <div class="form-group">
                    <input type="password" id="login-pwd" class="form-control" placeholder="Mot de passe">
                </div>
                <button class="btn" onclick="doLogin()">Connexion</button>
            </div>

            <!-- Register Form -->
            <div id="form-register" style="display: none;">
                <div id="reg-msg" style="display: none;"></div>
                <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom:1.5rem;">
                    La création de compte nécessite la validation d'un administrateur.
                </p>
                <div class="form-group">
                    <input type="email" id="reg-email" class="form-control" placeholder="Votre Email">
                </div>
                <div class="form-group">
                    <input type="password" id="reg-pwd" class="form-control" placeholder="Mot de passe">
                </div>
                <button class="btn" style="background: var(--bg-panel); border: 1px solid var(--border);" onclick="doRegister()">Créer le compte</button>
            </div>
            
            <p style="margin-top:2rem; font-size:0.8rem; color:var(--text-muted)">Security powered by JITSE</p>
        </div>
    </div>


    <!-- APP LAYOUT -->
    <div id="app-layout">
        <aside class="sidebar">
            <div class="logo">
                <i class="fa-solid fa-brain"></i> JITSE Engine
            </div>
            <div style="font-size:0.8rem; color:var(--text-muted); margin-top:-1.5rem; text-align:center;">
                Connecté en tant que: <span id="current-user-email" style="color:white; font-weight:bold;"></span>
            </div>

            <nav style="display:flex; flex-direction:column; gap:0.5rem; margin-top:2rem;">
                <!-- ADMIN ONLY -->
                <a href="#" class="nav-item" id="nav-admin" onclick="showView('admin')" style="display:none;">
                    <i class="fa-solid fa-user-shield"></i> Modération Accès
                </a>
                
                <a href="#" class="nav-item active" onclick="showView('simulator')">
                    <i class="fa-solid fa-vial-circle-check"></i> Simulateur IA
                </a>
                <a href="#" class="nav-item" onclick="showView('account')">
                    <i class="fa-solid fa-user-lock"></i> Mon Compte
                </a>
                <a href="#" class="nav-item" onclick="showView('api')">
                    <i class="fa-solid fa-code"></i> API & Doc
                </a>
            </nav>
            
            <div style="margin-top: auto;">
                <button onclick="logout()" class="btn" style="background:transparent; border:1px solid var(--border); box-shadow:none; font-size:0.9rem;">
                    <i class="fa-solid fa-arrow-right-from-bracket"></i> Déconnexion
                </button>
            </div>
        </aside>

        <main class="main-content">
            <header class="header">
                <div>
                    <h1>Dashboard de Supervision</h1>
                    <p style="color:var(--text-muted); margin-top:0.5rem;">JobbersFind Intelligent Trust & Skill Engine</p>
                </div>
                <div class="status-badge">
                    <i class="fa-solid fa-circle"></i> Système en Ligne & Actif
                </div>
            </header>

            <!-- VIEW: ADMIN MODERATION -->
            <section id="view-admin" class="glass-panel">
                <div class="section-title" style="color:var(--primary);">
                    <i class="fa-solid fa-user-shield"></i> Approbation des nouveaux utilisateurs
                </div>
                <p style="color:var(--text-muted); margin-bottom: 2rem;">
                    En tant qu'administrateur, vous devez approuver toute nouvelle demande d'accès.<br/>
                    <b>(Une seule fois requise par utilisateur).</b>
                </p>
                
                <button class="btn btn-small" onclick="loadPendingUsers()" style="margin-bottom: 2rem; width:auto; border-radius:8px;">
                    <i class="fa-solid fa-rotate-right"></i> Rafraîchir la liste
                </button>

                <ul class="admin-list" id="pending-users-list">
                    <li><span style="color:var(--text-muted);">Chargement...</span></li>
                </ul>
            </section>
            
            
            <!-- VIEW: ACCOUNT CONFIG -->
            <section id="view-account" class="glass-panel">
                <div class="section-title">
                    <i class="fa-solid fa-user-lock"></i> Paramètres de Sécurité
                </div>
                <p style="color:var(--text-muted); margin-bottom: 2rem;">Modifiez votre mot de passe d'accès.</p>
                
                <div style="max-width:400px;">
                    <div id="pwd-msg"></div>
                    <div class="form-group">
                        <label class="form-label">Nouveau mot de passe</label>
                        <input type="password" id="new-pwd" class="form-control">
                    </div>
                    <button class="btn" onclick="changePassword()">Mettre à jour</button>
                </div>
            </section>


            <!-- VIEW: Simulateur -->
            <section id="view-simulator" class="glass-panel" style="display: block;">
                <div class="section-title">
                    <i class="fa-solid fa-vial-circle-check"></i> Création de Dossier (Test IA)
                </div>
                
                <p style="color:var(--text-muted); margin-bottom: 2rem; line-height: 1.6;">
                    Incluez correctement les documents et médias (Photos, Vidéos, CNI/Diplômes). L'IA appliquera des pondérations strictes en fonction du métier. <br/>
                    <i>💡 <b>Détection IA:</b> Renommez une image avec "ia" ou "stock" pour simuler un blocage pour Fraude visuelle !</i>
                </p>

                <div class="grid-2">
                    <div>
                        <h3 style="margin-bottom: 1rem; color:var(--primary); font-size: 1.1rem;"><i class="fa-solid fa-address-card"></i> Profil & Identité</h3>
                        
                        <div class="form-group">
                            <label class="form-label">Profession / Métier</label>
                            <select id="profession" class="form-control">
                                <option value="mason">Maçon (Construction)</option>
                                <option value="web_developer">Développeur Web (Tech)</option>
                                <option value="photographer">Photographe (Média)</option>
                                <option value="teacher">Professeur (Services)</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Description du profil 📝</label>
                            <textarea id="description" class="form-control" rows="3">Spécialiste de mon domaine, garantissant un travail propre, rapide et aux normes en vigueur pour toute la clientèle.</textarea>
                        </div>

                        <h3 style="margin-bottom: 1rem; color:var(--primary); font-size: 1.1rem; margin-top: 2rem;"><i class="fa-solid fa-file-contract"></i> Documents Administratifs</h3>
                        
                        <div class="form-group">
                            <label class="form-label">Documents Approuvés (CNI, Patente) <span class="badge-bonus">+ BONUS</span></label>
                            <div class="upload-zone" onclick="document.getElementById('docs_upload').click()">
                                <i class="fa-solid fa-file-pdf"></i>
                                <p>Cliquez pour rajouter vos documents</p>
                                <input type="file" id="docs_upload" multiple accept=".pdf,.doc,.docx,image/*" style="display: none;" onchange="previewDocs(event)">
                            </div>
                            <div id="docs-preview" class="file-preview"></div>
                        </div>
                    </div>

                    <div>
                        <h3 style="margin-bottom: 1rem; color:var(--secondary); font-size: 1.1rem;"><i class="fa-solid fa-camera-retro"></i> Preuves Visuelles </h3>
                        
                        <div class="form-group">
                            <label class="form-label">Photos du Portfolio (Réalisations) 📸</label>
                            <div class="upload-zone" onclick="document.getElementById('portfolio_upload').click()">
                                <i class="fa-solid fa-cloud-arrow-up"></i>
                                <p>Cliquez ou glissez vos réalisations visuelles ici</p>
                                <input type="file" id="portfolio_upload" multiple accept="image/*" style="display: none;" onchange="previewImages(event)">
                            </div>
                            <div id="image-preview" class="file-preview"></div>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Vidéo de présentation / Chantier 🎥</label>
                            <div class="upload-zone" onclick="document.getElementById('video_upload').click()">
                                <i class="fa-solid fa-video"></i>
                                <p>Cliquez pour ajouter une vidéo MP4</p>
                                <input type="file" id="video_upload" accept="video/mp4,video/webm" style="display: none;" onchange="previewVideo(event)">
                            </div>
                            <div id="video-preview" class="file-preview"></div>
                        </div>
                        
                        <button class="btn" id="analyze-btn" onclick="submitAnalysis()" style="margin-top: 2rem;">
                            <span id="btn-text">Envoyer le Dossier à l'IA JITSE</span>
                            <div class="spinner" id="btn-spinner"></div>
                        </button>
                    </div>
                </div>

                <!-- RESULTATS -->
                <div id="result-container" class="passport-result">
                    <hr style="border:0; border-top:1px solid var(--border); margin: 3rem 0;">
                    <div class="section-title" style="color:var(--success);">
                        <i class="fa-solid fa-passport"></i> JobbersFind Trust Passport™
                    </div>

                    <div class="grid-2">
                        <div style="text-align: center;">
                            <p style="color:var(--text-muted); margin-bottom:1rem; font-weight:600;">TRUST SCORE FINAL</p>
                            <div class="score-circle" id="circle-score" style="--percentage: 0%;">
                                <div class="score-value" id="final-score">0</div>
                            </div>
                            <h3 id="trust-level" style="text-transform:uppercase; letter-spacing:2px; color:var(--success);">---</h3>
                            <p style="color:var(--text-muted); font-size:0.9rem; margin-top:0.5rem;" id="ai-confidence">Certitude IA : Haut</p>
                        </div>

                        <div>
                            <ul class="badge-list">
                                <li class="badge-item">
                                    <span>Compétences Visuelles (Portfolio)</span>
                                    <strong id="skill-score">--/100</strong>
                                </li>
                                <li class="badge-item">
                                    <span>Index de Preuves Diverses</span>
                                    <strong id="evidence-score">--/100</strong>
                                </li>
                                <li class="badge-item">
                                    <span>Qualité Déclarative (Profil)</span>
                                    <strong id="profile-score">--/100</strong>
                                </li>
                                <li class="badge-item" style="border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.05);">
                                    <span>Documents Administratifs</span>
                                    <strong id="document-bonus-text" style="color:var(--success)">--</strong>
                                </li>
                                <li class="badge-item" style="border-color: rgba(239, 68, 68, 0.3);">
                                    <span>Risque de Fraude (Détection Fakes)</span>
                                    <strong id="fraud-score" style="color:var(--danger)">--/100</strong>
                                </li>
                            </ul>
                            
                            <div class="ai-recommendation" id="ai-rec" style="white-space: pre-line;"></div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- VIEW: API INFO -->
            <section id="view-api" class="glass-panel">
                <div class="section-title">
                    <i class="fa-solid fa-server"></i> API JITSE & Intégration
                </div>
                <p style="color:var(--text-muted); margin-bottom: 2rem;">Le backend JITSE 1.0 est prêt et sécurisé.</p>
                <div style="background:rgba(0,0,0,0.3); padding:1.5rem; border-radius:12px; border:1px solid var(--border); margin-bottom:1.5rem;">
                    <code style="color:var(--success); font-size:1.1rem;">POST /api/v1/auth/login</code><br><br>
                    <code style="color:var(--success); font-size:1.1rem;">POST /api/v1/analysis/submit</code>
                </div>
                <a href="/docs" target="_blank" class="btn" style="width:auto; display:inline-flex;">Ouvrir Swagger UI</a>
            </section>
        </main>
    </div>

   <script>
    // --- IAM & AUTH LOGIC ---
    let session = null; // { email, role, token }

    function switchAuthTab(tab) {
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        const activeTab = document.getElementById('tab-' + tab);
        if (activeTab) activeTab.classList.add('active');
        
        document.getElementById('form-login').style.display = tab === 'login' ? 'block' : 'none';
        document.getElementById('form-register').style.display = tab === 'register' ? 'block' : 'none';
    }

    async function doLogin() {
        const email = document.getElementById('login-email').value;
        const pwd = document.getElementById('login-pwd').value;
        const errDiv = document.getElementById('login-error');
        
        try {
            const res = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: pwd })
            });
            const data = await res.json();
            
            if (!res.ok) {
                errDiv.innerText = data.detail || "Échec de connexion.";
                errDiv.style.display = 'block';
            } else {
                session = data.session; // Contient email, role et optionnellement token
                initApp();
            }
        } catch (e) {
            errDiv.innerText = "Erreur serveur.";
            errDiv.style.display = 'block';
        }
    }

    async function doRegister() {
        const email = document.getElementById('reg-email').value;
        const pwd = document.getElementById('reg-pwd').value;
        const msgDiv = document.getElementById('reg-msg');
        
        try {
            const res = await fetch('/api/v1/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email, password: pwd })
            });
            const data = await res.json();
            
            if (!res.ok) {
                msgDiv.innerHTML = `<span style="color:var(--danger)">${data.detail || 'Erreur lors de l\'inscription'}</span>`;
            } else {
                msgDiv.innerHTML = `<span style="color:var(--success)">${data.message || 'Inscription réussie !'}</span>`;
            }
            msgDiv.style.display = 'block';
        } catch (e) {
            msgDiv.innerHTML = `<span style="color:var(--danger)">Erreur serveur.</span>`;
            msgDiv.style.display = 'block';
        }
    }

    function logout() {
        session = null;
        document.getElementById('app-layout').style.display = 'none';
        document.getElementById('auth-screen').style.display = 'flex';
        
        document.getElementById('login-email').value = '';
        document.getElementById('login-pwd').value = '';
        document.getElementById('login-error').style.display = 'none';
    }

    async function changePassword() {
        const newPwd = document.getElementById('new-pwd').value;
        const msgDiv = document.getElementById('pwd-msg');
        
        if (!newPwd || newPwd.length < 4) {
            return alert('Mot de passe trop court (4 caractères minimum).');
        }
        
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (session && session.token) {
                headers['Authorization'] = `Bearer ${session.token}`;
            }

            const res = await fetch('/api/v1/auth/users/change-password', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ email: session.email, password: newPwd })
            });
            
            if (res.ok) {
                msgDiv.innerHTML = `<span style="color:var(--success)">Mot de passe changé !</span>`;
                document.getElementById('new-pwd').value = '';
            } else {
                const data = await res.json();
                msgDiv.innerHTML = `<span style="color:var(--danger)">${data.detail || 'Erreur.'}</span>`;
            }
        } catch (e) {
            msgDiv.innerHTML = `<span style="color:var(--danger)">Erreur réseau.</span>`;
        }
    }

    async function loadPendingUsers() {
        const list = document.getElementById('pending-users-list');
        list.innerHTML = '<li><span style="color:var(--text-muted);">Chargement...</span></li>';
        
        try {
            const headers = {};
            if (session && session.token) {
                headers['Authorization'] = `Bearer ${session.token}`;
            }

            const res = await fetch('/api/v1/auth/users/pending', { headers });
            const data = await res.json();
            
            if (!data.pending_users || data.pending_users.length === 0) {
                list.innerHTML = '<li><span style="color:var(--success);"><i class="fa-solid fa-check"></i> Aucun utilisateur en attente d\'approbation.</span></li>';
                return;
            }
            
            list.innerHTML = '';
            data.pending_users.forEach(user => {
                const li = document.createElement('li');
                
                const bold = document.createElement('b');
                bold.style.fontSize = '1.1rem';
                bold.textContent = user.email;
                
                const btn = document.createElement('button');
                btn.className = 'btn-approve';
                btn.innerHTML = '<i class="fa-solid fa-check-double"></i> Approuver';
                btn.onclick = () => approveUser(user.email);
                
                li.appendChild(bold);
                li.appendChild(btn);
                list.appendChild(li);
            });
        } catch (e) {
            list.innerHTML = '<li><span style="color:var(--danger);">Erreur lors du chargement.</span></li>';
        }
    }
    
    async function approveUser(email) {
        try {
            const headers = { 'Content-Type': 'application/json' };
            if (session && session.token) {
                headers['Authorization'] = `Bearer ${session.token}`;
            }

            const res = await fetch(`/api/v1/auth/users/approve/${encodeURIComponent(email)}`, { 
                method: 'POST',
                headers: headers 
            });

            if (res.ok) {
                alert(`Utilisateur ${email} approuvé ! Il peut désormais se connecter.`);
                loadPendingUsers();
            } else {
                alert(`Impossible d'approuver l'utilisateur.`);
            }
        } catch (e) {
            alert(`Erreur réseau lors de l'approbation.`);
        }
    }

    // --- UI LOGIC ---
    function initApp() {
        document.getElementById('auth-screen').style.display = 'none';
        document.getElementById('app-layout').style.display = 'flex';
        document.getElementById('current-user-email').innerText = session.email;
        
        if (session.role === 'admin') {
            document.getElementById('nav-admin').style.display = 'flex';
            showView('admin');
            loadPendingUsers();
        } else {
            document.getElementById('nav-admin').style.display = 'none';
            showView('simulator');
        }
    }

    function showView(viewId) {
        document.querySelectorAll('.glass-panel').forEach(p => p.style.display = 'none');
        
        const targetView = document.getElementById('view-' + viewId);
        if (targetView) targetView.style.display = 'block';
        
        document.querySelectorAll('nav .nav-item').forEach(a => a.classList.remove('active'));
        const activeNav = document.getElementById('nav-' + viewId);
        if (activeNav) activeNav.classList.add('active');
    }

    // --- SIMULATOR LOGIC (File Reading) ---
    let statePhotos = 0, stateDocs = 0, hasVideo = false;
    let globalPhotosFiles = [], globalDocsFiles = [], globalVideoFile = null;

    function previewImages(event) {
        const preview = document.getElementById('image-preview');
        preview.innerHTML = '';
        globalPhotosFiles = Array.from(event.target.files);
        statePhotos = globalPhotosFiles.length;
        
        globalPhotosFiles.forEach(f => {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(f);
            img.onload = () => URL.revokeObjectURL(img.src);
            
            const div = document.createElement('div');
            div.className = 'file-item';
            div.appendChild(img);
            
            const span = document.createElement('span');
            span.textContent = f.name.length > 15 ? f.name.substring(0, 15) + '...' : f.name;
            
            div.appendChild(span);
            preview.appendChild(div);
        });
    }

    function previewDocs(event) {
        const preview = document.getElementById('docs-preview');
        preview.innerHTML = '';
        globalDocsFiles = Array.from(event.target.files);
        stateDocs = globalDocsFiles.length;
        
        globalDocsFiles.forEach(f => {
            const div = document.createElement('div');
            div.className = 'file-item';
            
            const icon = document.createElement('i');
            icon.className = 'fa-solid fa-file-pdf';
            icon.style.color = 'var(--secondary)';
            
            const span = document.createElement('span');
            span.textContent = f.name;
            
            div.appendChild(icon);
            div.appendChild(span);
            preview.appendChild(div);
        });
    }

    function previewVideo(event) {
        const preview = document.getElementById('video-preview');
        preview.innerHTML = '';
        const files = event.target.files;
        
        if (files.length > 0) {
            hasVideo = true;
            globalVideoFile = files[0];
            
            const div = document.createElement('div');
            div.className = 'file-item';
            
            const icon = document.createElement('i');
            icon.className = 'fa-solid fa-video';
            icon.style.color = 'var(--success)';
            
            const span = document.createElement('span');
            span.textContent = files[0].name;
            
            div.appendChild(icon);
            div.appendChild(span);
            preview.appendChild(div);
        } else {
            hasVideo = false;
            globalVideoFile = null;
        }
    }

    async function submitAnalysis() {
        if (statePhotos === 0) {
            if (!confirm("⚠️ Vous n'avez ajouté aucune photo à votre portfolio ! Continuer quand même ?")) return;
        }

        const btnText = document.getElementById('btn-text');
        const spinner = document.getElementById('btn-spinner');
        const resContainer = document.getElementById('result-container');
        
        btnText.style.display = 'none';
        spinner.style.display = 'inline-block';
        resContainer.style.display = 'none';

        const profession = document.getElementById('profession').value;
        const desc = document.getElementById('description').value;

        // Fichiers encodés pour simuler le comportement Multimodal Backend
        const images = globalPhotosFiles.map((file, i) => ({
            id: `img_${i}`, 
            url: `http://simulated-upload.com/${encodeURIComponent(file.name)}`, 
            media_type: "image", 
            mime_type: file.type || "image/jpeg", 
            size_bytes: file.size || 1024
        }));
        
        const documents = globalDocsFiles.map((file, i) => ({
            id: `doc_${i}`, 
            url: `http://simulated-upload.com/${encodeURIComponent(file.name)}`, 
            media_type: "document", 
            mime_type: file.type || "application/pdf", 
            size_bytes: file.size || 2048
        }));
        
        let video = null;
        if (hasVideo && globalVideoFile) {
            video = { 
                id: `vid_1`, 
                url: `http://simulated-upload.com/${encodeURIComponent(globalVideoFile.name)}`, 
                media_type: "video", 
                mime_type: globalVideoFile.type || "video/mp4", 
                size_bytes: globalVideoFile.size || 5048 
            };
        }

        const payload = {
            dossier_id: "DOS-" + Math.floor(Math.random() * 10000), 
            provider_id: session ? session.email : "guest",
            profession_category: profession, 
            profile: { 
                description: desc, 
                years_of_experience: 5, 
                location: "Douala", 
                services_offered: ["Service"], 
                declared_skills: [], 
                languages: ["FR"] 
            },
            presentation_video: video, 
            portfolio_images: images, 
            documents: documents
        };

        try {
            const headers = { 'Content-Type': 'application/json' };
            if (session && session.token) {
                headers['Authorization'] = `Bearer ${session.token}`;
            }

            const response = await fetch('/api/v1/analysis/submit', { 
                method: 'POST', 
                headers: headers, 
                body: JSON.stringify(payload) 
            });
            
            if (!response.ok) throw new Error(`Erreur serveur (${response.status})`);
            
            const data = await response.json();
            
            document.getElementById('final-score').innerText = data.trust_score.toFixed(1);
            
            const circleScore = document.getElementById('circle-score');
            circleScore.style.setProperty('--percentage', data.trust_score + '%');
            
            if (data.trust_score >= 80) {
                circleScore.style.background = `conic-gradient(var(--success) ${data.trust_score}%, rgba(255,255,255,0.1) 0)`;
            } else if (data.trust_score >= 50) {
                circleScore.style.background = `conic-gradient(var(--warning) ${data.trust_score}%, rgba(255,255,255,0.1) 0)`;
            } else {
                circleScore.style.background = `conic-gradient(var(--danger) ${data.trust_score}%, rgba(255,255,255,0.1) 0)`;
            }

            document.getElementById('trust-level').innerText = data.trust_level;
            document.getElementById('ai-confidence').innerText = `Certitude IA: ${(data.ai_confidence_level || '').replace('_', ' ')}`;

            document.getElementById('skill-score').innerText = `${data.skill_evidence_score.toFixed(1)} / 100`;
            document.getElementById('evidence-score').innerText = `${data.evidence_index.toFixed(1)} / 100`;
            document.getElementById('profile-score').innerText = `${data.profile_quality_score.toFixed(1)} / 100`;
            document.getElementById('fraud-score').innerText = `${data.fraud_risk_index.toFixed(1)} / 100`;
            
            document.getElementById('document-bonus-text').innerText = stateDocs > 0 ? `${stateDocs} Documents Approuvés ✔️` : `Aucun (Neutre) ➖`;
            document.getElementById('ai-rec').innerText = `🤖 EXPLICATION IA:\n\n${data.ai_recommendation}`;
            
            resContainer.style.display = 'block';
        } catch (err) { 
            alert("Erreur: " + err.message); 
        } finally { 
            btnText.style.display = 'inline'; 
            spinner.style.display = 'none'; 
        }
    }
</script>
</body>
</html>
"""
