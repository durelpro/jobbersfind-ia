"""
JITSE Dashboard View
Contient le code HTML, CSS et JS pour l'interface de JITSE.
Intègre le système d'authentification IAM avec workflow de validation Admin.
"""

# dashbord_view.py

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JITSE AI - Simuler & Vérifier un Profil</title>
    <!-- FontAwesome & Fonts -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --secondary: #8b5cf6;
            --accent: #06b6d4;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --danger: #ef4444;
            --success: #10b981;
            --warning: #f59e0b;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.15) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* --- AUTH SCREEN --- */
        #auth-screen {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }

        .auth-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 40px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }

        .auth-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .auth-header i {
            font-size: 2.5rem;
            color: var(--primary);
            margin-bottom: 10px;
        }

        .auth-tabs {
            display: flex;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
            padding: 4px;
            margin-bottom: 24px;
        }

        .auth-tab {
            flex: 1;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--text-muted);
            transition: all 0.3s ease;
        }

        .auth-tab.active {
            background: var(--primary);
            color: white;
        }

        /* --- APP LAYOUT --- */
        #app-layout {
            display: none;
            flex: 1;
        }

        sidebar {
            width: 260px;
            background: rgba(15, 23, 42, 0.8);
            border-right: 1px solid var(--card-border);
            padding: 24px 16px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-main);
            padding: 0 12px;
        }

        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            border-radius: 12px;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
            font-weight: 500;
        }

        .nav-item:hover, .nav-item.active {
            background: rgba(255, 255, 255, 0.05);
            color: var(--primary);
        }

        main {
            flex: 1;
            padding: 32px;
            overflow-y: auto;
            max-width: 1200px;
            margin: 0 auto;
        }

        .glass-panel {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 24px;
        }

        /* --- FORMS & INPUTS --- */
        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        input[type="text"],
        input[type="email"],
        input[type="password"],
        select,
        textarea {
            width: 100%;
            padding: 12px 16px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            color: var(--text-main);
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, select:focus, textarea:focus {
            border-color: var(--primary);
        }

        .file-upload-box {
            border: 2px dashed var(--card-border);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            cursor: pointer;
            background: rgba(15, 23, 42, 0.3);
            transition: all 0.2s;
        }

        .file-upload-box:hover {
            border-color: var(--primary);
            background: rgba(59, 130, 246, 0.05);
        }

        .file-preview-container {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 10px;
        }

        .file-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .file-item img {
            width: 24px;
            height: 24px;
            object-fit: cover;
            border-radius: 4px;
        }

        .btn-primary {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: opacity 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }

        .btn-primary:hover {
            opacity: 0.9;
        }

        /* --- RESULTS DISPLAY --- */
        .score-display-card {
            display: flex;
            align-items: center;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }

        .circular-progress {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: conic-gradient(var(--primary) calc(var(--percentage) * 1%), rgba(255, 255, 255, 0.1) 0);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        .circular-progress::before {
            content: "";
            position: absolute;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: var(--bg-dark);
        }

        .score-value {
            position: relative;
            font-size: 1.8rem;
            font-weight: 700;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }

        .metric-card {
            background: rgba(15, 23, 42, 0.4);
            border: 1px solid var(--card-border);
            padding: 16px;
            border-radius: 12px;
        }

        .metric-title {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .metric-value {
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 4px;
        }

        /* --- ADMIN LIST --- */
        .admin-list {
            list-style: none;
        }

        .admin-list li {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: rgba(15, 23, 42, 0.4);
            border-radius: 8px;
            margin-bottom: 8px;
        }

        .btn-approve {
            background: var(--success);
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
        }

        /* Spinner */
        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top: 3px solid white;
            width: 18px;
            height: 18px;
            animation: spin 1s linear infinite;
            display: none;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>

    <!-- SECTION AUTHENTIFICATION -->
    <div id="auth-screen">
        <div class="auth-card">
            <div class="auth-header">
                <i class="fa-solid fa-brain"></i>
                <h2>JITSE AI Engine</h2>
                <p style="color:var(--text-muted); font-size:0.85rem;">Plateforme d'Analyse de Profils</p>
            </div>

            <div class="auth-tabs">
                <div class="auth-tab active" onclick="switchAuthTab('login')">Connexion</div>
                <div class="auth-tab" onclick="switchAuthTab('register')">Inscription</div>
            </div>

            <!-- LOGIN FORM -->
            <form id="login-form" onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label>Adresse Email</label>
                    <input type="email" id="login-email" required placeholder="nom@exemple.com">
                </div>
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" id="login-password" required placeholder="••••••••">
                </div>
                <button type="submit" class="btn-primary">
                    <span>Se Connecter</span>
                    <i class="fa-solid fa-arrow-right"></i>
                </button>
            </form>

            <!-- REGISTER FORM -->
            <form id="register-form" style="display:none;" onsubmit="handleRegister(event)">
                <div class="form-group">
                    <label>Adresse Email</label>
                    <input type="email" id="reg-email" required placeholder="nom@exemple.com">
                </div>
                <div class="form-group">
                    <label>Mot de passe</label>
                    <input type="password" id="reg-password" required placeholder="••••••••">
                </div>
                <div class="form-group">
                    <label>Rôle souhaité</label>
                    <select id="reg-role">
                        <option value="user">Utilisateur / Recruteur</option>
                        <option value="admin">Administrateur</option>
                    </select>
                </div>
                <button type="submit" class="btn-primary">
                    <span>S'inscrire</span>
                    <i class="fa-solid fa-user-plus"></i>
                </button>
            </form>
            
            <div id="auth-msg" style="margin-top:15px; font-size:0.85rem; text-align:center;"></div>
        </div>
    </div>

    <!-- APPLICATION LAYOUT (CACHE INITIALEMENT) -->
    <div id="app-layout">
        <sidebar>
            <div class="brand">
                <i class="fa-solid fa-shield-halved" style="color:var(--primary)"></i>
                <span>JITSE AI</span>
            </div>
            <div style="font-size:0.75rem; color:var(--text-muted); padding:0 12px;" id="current-user-email">
                --
            </div>

            <nav style="display:flex; flex-direction:column; gap:8px; margin-top:20px;">
                <div class="nav-item active" onclick="showView('simulator')">
                    <i class="fa-solid fa-sliders"></i>
                    <span>Simulateur IA</span>
                </div>
                <div class="nav-item" id="nav-admin" style="display:none;" onclick="showView('admin')">
                    <i class="fa-solid fa-user-shield"></i>
                    <span>Gestion Admin</span>
                </div>
            </nav>

            <div style="margin-top:auto;">
                <div class="nav-item" onclick="logout()">
                    <i class="fa-solid fa-right-from-bracket" style="color:var(--danger)"></i>
                    <span style="color:var(--danger)">Déconnexion</span>
                </div>
            </div>
        </sidebar>

        <main>
            <!-- VUE SIMULATEUR -->
            <div id="view-simulator" class="glass-panel">
                <h2 style="margin-bottom:8px;"><i class="fa-solid fa-wand-magic-sparkles" style="color:var(--secondary)"></i> Evaluation du Profil</h2>
                <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:24px;">Remplissez les informations ci-dessous pour lancer le moteur d'analyse multi-modal.</p>

                <div class="form-group">
                    <label>Métier / Domaine d'expertise</label>
                    <input type="text" id="profession" placeholder="Ex: Developpeur Fullstack React / Node.js">
                </div>

                <div class="form-group">
                    <label>Description des compétences & Expériences</label>
                    <textarea id="description" rows="4" placeholder="Décrivez le parcours, les projets réalisés, les frameworks maîtrisés..."></textarea>
                </div>

                <!-- SECTION FICHIERS -->
                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:16px; margin-bottom:20px;">
                    <!-- Photos / Portfolio -->
                    <div class="form-group">
                        <label>Portfolio / Captures (Images)</label>
                        <div class="file-upload-box" onclick="document.getElementById('portfolio_upload').click()">
                            <i class="fa-solid fa-images" style="font-size:1.5rem; color:var(--primary); margin-bottom:8px;"></i>
                            <p style="font-size:0.8rem;">Ajouter des images</p>
                        </div>
                        <input type="file" id="portfolio_upload" multiple accept="image/*" style="display:none;" onchange="previewImages(event)">
                        <div id="image-preview" class="file-preview-container"></div>
                    </div>

                    <!-- Documents PDF -->
                    <div class="form-group">
                        <label>Attestations / Diplômes (PDF)</label>
                        <div class="file-upload-box" onclick="document.getElementById('docs_upload').click()">
                            <i class="fa-solid fa-file-pdf" style="font-size:1.5rem; color:var(--secondary); margin-bottom:8px;"></i>
                            <p style="font-size:0.8rem;">Ajouter des PDFs</p>
                        </div>
                        <input type="file" id="docs_upload" multiple accept=".pdf" style="display:none;" onchange="previewDocs(event)">
                        <div id="docs-preview" class="file-preview-container"></div>
                    </div>

                    <!-- Vidéo -->
                    <div class="form-group">
                        <label>Vidéo de présentation (MP4/WebM)</label>
                        <div class="file-upload-box" onclick="document.getElementById('video_upload').click()">
                            <i class="fa-solid fa-video" style="font-size:1.5rem; color:var(--accent); margin-bottom:8px;"></i>
                            <p style="font-size:0.8rem;">Ajouter une vidéo</p>
                        </div>
                        <input type="file" id="video_upload" accept="video/*" style="display:none;" onchange="previewVideo(event)">
                        <div id="video-preview" class="file-preview-container"></div>
                    </div>
                </div>

                <button class="btn-primary" id="analyze-btn" onclick="submitAnalysis()">
                    <span id="btn-text">Envoyer le Dossier à l'IA JITSE</span>
                    <div class="spinner" id="btn-spinner"></div>
                </button>

                <!-- SECTION RESULTATS -->
                <div id="result-container" style="display:none; margin-top:32px; border-top:1px solid var(--card-border); padding-top:24px;">
                    <h3>Résultats de l'Analyse</h3>
                    
                    <div class="score-display-card">
                        <div class="circular-progress" id="circle-score" style="--percentage: 0;">
                            <span class="score-value" id="final-score">0</span>
                        </div>
                        <div>
                            <h4 id="trust-level" style="font-size:1.2rem; color:var(--primary);">Analyse en attente</h4>
                            <p style="color:var(--text-muted); font-size:0.85rem;" id="ai-confidence">Certitude IA : --</p>
                        </div>
                    </div>

                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-title">Score Compétences</div>
                            <div class="metric-value" id="skill-score">0/100</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-title">Cohérence Épreuves</div>
                            <div class="metric-value" id="evidence-score">0/100</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-title">Complétude Profil</div>
                            <div class="metric-value" id="profile-score">0/100</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-title">Indice de Fraude / Risque</div>
                            <div class="metric-value" id="fraud-score" style="color:var(--danger)">0/100</div>
                        </div>
                    </div>

                    <div style="margin-top:20px; background:rgba(15,23,42,0.4); padding:16px; border-radius:12px; border:1px solid var(--card-border);">
                        <strong>Certificats & Documents :</strong> <span id="document-bonus-text" style="color:var(--text-muted)">Non évalué</span>
                        <p id="ai-rec" style="margin-top:8px; font-size:0.9rem; color:var(--text-muted);"></p>
                    </div>
                </div>
            </div>

            <!-- VUE ADMIN -->
            <div id="view-admin" class="glass-panel" style="display:none;">
                <h2><i class="fa-solid fa-user-check" style="color:var(--success)"></i> Demandes d'Inscriptions en Attente</h2>
                <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:20px;">Approuvez les accès utilisateurs pour autoriser leur connexion.</p>

                <ul class="admin-list" id="pending-users-list">
                    <li><span style="color:var(--text-muted);">Chargement...</span></li>
                </ul>
            </div>
        </main>
    </div>

    <!-- SCRIPT FRONTEND -->
    <script>
        let session = {
            email: null,
            role: null
        };

        function switchAuthTab(tab) {
            document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
            if (tab === 'login') {
                document.querySelectorAll('.auth-tab')[0].classList.add('active');
                document.getElementById('login-form').style.display = 'block';
                document.getElementById('register-form').style.display = 'none';
            } else {
                document.querySelectorAll('.auth-tab')[1].classList.add('active');
                document.getElementById('login-form').style.display = 'none';
                document.getElementById('register-form').style.display = 'block';
            }
            document.getElementById('auth-msg').innerText = '';
        }

        async function handleLogin(e) {
            e.preventDefault();
            const msg = document.getElementById('auth-msg');
            msg.style.color = 'var(--text-muted)';
            msg.innerText = "Connexion en cours...";

            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const res = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ email, password })
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    session.email = data.email;
                    session.role = data.role;
                    initApp();
                } else {
                    msg.style.color = 'var(--danger)';
                    msg.innerText = data.detail || "Erreur lors de la connexion.";
                }
            } catch (err) {
                msg.style.color = 'var(--danger)';
                msg.innerText = "Impossible de contacter le serveur.";
            }
        }

        async function handleRegister(e) {
            e.preventDefault();
            const msg = document.getElementById('auth-msg');
            msg.style.color = 'var(--text-muted)';
            msg.innerText = "Traitement de l'inscription...";

            const email = document.getElementById('reg-email').value;
            const password = document.getElementById('reg-password').value;
            const role = document.getElementById('reg-role').value;

            try {
                const res = await fetch('/api/v1/auth/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ email, password, role })
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    msg.style.color = 'var(--success)';
                    msg.innerText = data.message || "Inscription enregistrée. En attente d'approbation.";
                } else {
                    msg.style.color = 'var(--danger)';
                    msg.innerText = data.detail || "Erreur lors de l'inscription.";
                }
            } catch (err) {
                msg.style.color = 'var(--danger)';
                msg.innerText = "Impossible de contacter le serveur.";
            }
        }

        function logout() {
            session = { email: null, role: null };
            document.getElementById('app-layout').style.display = 'none';
            document.getElementById('auth-screen').style.display = 'flex';
        }

        async function loadPendingUsers() {
            const list = document.getElementById('pending-users-list');
            list.innerHTML = '<li><span style="color:var(--text-muted);">Chargement...</span></li>';
            
            try {
                const res = await fetch(`/api/v1/auth/admin/pending?admin_email=${encodeURIComponent(session.email)}`);
                const data = await res.json();
                
                if (!res.ok) {
                    list.innerHTML = `<li><span style="color:var(--danger);">${data.detail || 'Erreur'}</span></li>`;
                    return;
                }
                
                if (data.pending_users.length === 0) {
                    list.innerHTML = '<li><span style="color:var(--text-muted);">Aucune demande en attente.</span></li>';
                    return;
                }
                
                list.innerHTML = '';
                data.pending_users.forEach(u => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        <div>
                            <strong>${u.email}</strong>
                            <div style="font-size:0.8rem; color:var(--text-muted)">Inscrit le : ${u.created_at}</div>
                        </div>
                        <button class="btn-approve" onclick="approveUser('${u.email}')">
                            <i class="fa-solid fa-check"></i> Approuver
                        </button>
                    `;
                    list.appendChild(li);
                });
            } catch (e) {
                list.innerHTML = '<li><span style="color:var(--danger);">Erreur de connexion serveur.</span></li>';
            }
        }

        async function approveUser(userEmail) {
            try {
                const res = await fetch('/api/v1/auth/admin/approve', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        admin_email: session.email,
                        target_email: userEmail
                    })
                });
                
                if (res.ok) {
                    loadPendingUsers();
                } else {
                    const data = await res.json();
                    alert("Erreur: " + data.detail);
                }
            } catch (e) {
                alert("Erreur lors de l'approbation.");
            }
        }

        function initApp() {
            document.getElementById('auth-screen').style.display = 'none';
            document.getElementById('app-layout').style.display = 'flex';
            document.getElementById('current-user-email').innerText = session.email;
            
            if (session.role === 'admin') {
                document.getElementById('nav-admin').style.display = 'flex';
                showView('admin');
            } else {
                document.getElementById('nav-admin').style.display = 'none';
                showView('simulator');
            }
        }

        function showView(viewName) {
            document.querySelectorAll('.glass-panel').forEach(p => p.style.display = 'none');
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            
            const target = document.getElementById('view-' + viewName);
            if (target) target.style.display = 'block';
            
            const navBtn = document.querySelector(`.nav-item[onclick*="'${viewName}'"]`);
            if (navBtn) navBtn.classList.add('active');
            
            if (viewName === 'admin') {
                loadPendingUsers();
            }
        }

        // --- PREVIEW FUNCTIONS ---
        function previewImages(event) {
            const container = document.getElementById('image-preview');
            container.innerHTML = '';
            Array.from(event.target.files).forEach(file => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const item = document.createElement('div');
                    item.className = 'file-item';
                    item.innerHTML = `<img src="${e.target.result}"/> <span>${file.name}</span>`;
                    container.appendChild(item);
                };
                reader.readAsDataURL(file);
            });
        }

        function previewDocs(event) {
            const container = document.getElementById('docs-preview');
            container.innerHTML = '';
            Array.from(event.target.files).forEach(file => {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.innerHTML = `<i class="fa-solid fa-file-pdf" style="color:var(--primary); font-size:1.2rem;"></i> <span>${file.name}</span>`;
                container.appendChild(item);
            });
        }

        function previewVideo(event) {
            const container = document.getElementById('video-preview');
            container.innerHTML = '';
            const file = event.target.files[0];
            if (file) {
                const item = document.createElement('div');
                item.className = 'file-item';
                item.innerHTML = `<i class="fa-solid fa-file-video" style="color:var(--secondary); font-size:1.2rem;"></i> <span>${file.name}</span>`;
                container.appendChild(item);
            }
        }

        // --- SUBMIT ANALYSIS ---
        async function submitAnalysis() {
            const btn = document.getElementById('analyze-btn');
            const btnText = document.getElementById('btn-text');
            const spinner = document.getElementById('btn-spinner');
            const resultDiv = document.getElementById('result-container');
            
            btnText.innerText = "Analyse IA en cours...";
            spinner.style.display = "inline-block";
            btn.disabled = true;

            const formData = new FormData();
            formData.append('profession', document.getElementById('profession').value);
            formData.append('description', document.getElementById('description').value);
            
            const portfolioFiles = document.getElementById('portfolio_upload').files;
            for (let i = 0; i < portfolioFiles.length; i++) {
                formData.append('portfolio', portfolioFiles[i]);
            }

            const docsFiles = document.getElementById('docs_upload').files;
            for (let i = 0; i < docsFiles.length; i++) {
                formData.append('documents', docsFiles[i]);
            }

            const videoFile = document.getElementById('video_upload').files[0];
            if (videoFile) {
                formData.append('video', videoFile);
            }

            try {
                const res = await fetch('/api/v1/analysis/submit', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    document.getElementById('circle-score').style.setProperty('--percentage', `${data.trust_score}%`);
                    document.getElementById('final-score').innerText = data.trust_score;
                    document.getElementById('trust-level').innerText = data.trust_level;
                    document.getElementById('ai-confidence').innerText = `Certitude IA : ${data.confidence || 'Haut'}`;
                    
                    document.getElementById('skill-score').innerText = `${data.skill_score}/100`;
                    document.getElementById('evidence-score').innerText = `${data.evidence_score}/100`;
                    document.getElementById('profile-score').innerText = `${data.profile_score}/100`;
                    document.getElementById('fraud-score').innerText = `${data.fraud_risk}/100`;
                    
                    document.getElementById('document-bonus-text').innerText = data.has_documents ? "+15 pts (Vérifié)" : "Non fourni";
                    document.getElementById('ai-rec').innerText = data.recommendations || "Aucune recommandation spécifique.";
                    
                    resultDiv.style.display = 'block';
                    resultDiv.scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert("Erreur lors de l'analyse : " + (data.detail || "Problème serveur"));
                }
            } catch (e) {
                alert("Erreur réseau lors de la soumission.");
            } finally {
                btnText.innerText = "Envoyer le Dossier à l'IA JITSE";
                spinner.style.display = "none";
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""