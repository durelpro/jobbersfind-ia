"""
JITSE Dashboard View
Contient le code HTML, CSS et JS pour l'interface de JITSE.
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
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        /* Forms & Upload simulation */
        .form-group {
            margin-bottom: 1.5rem;
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

        .badge-list {
            list-style: none;
        }

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

    <aside class="sidebar">
        <div class="logo">
            <i class="fa-solid fa-brain"></i>
            JITSE Engine
        </div>
        <nav style="display:flex; flex-direction:column; gap:0.5rem;">
            <a href="#" class="nav-item active" onclick="showView('simulator')">
                <i class="fa-solid fa-microchip"></i> Simulateur IA
            </a>
            <a href="#" class="nav-item" onclick="showView('api')">
                <i class="fa-solid fa-code"></i> API & Documentation
            </a>
            <a href="#" class="nav-item" onclick="window.open('/docs', '_blank')">
                <i class="fa-solid fa-book"></i> Swagger UI <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:0.7rem; margin-left:auto;"></i>
            </a>
        </nav>
        
        <div style="margin-top: auto;">
            <p style="color:var(--text-muted); font-size:0.8rem; text-align:center;">JobbersFind © 2026</p>
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

        <!-- VIEW: Simulateur -->
        <section id="view-simulator" class="glass-panel" style="display: block;">
            <div class="section-title">
                <i class="fa-solid fa-vial-circle-check"></i> Création de Dossier (Test IA)
            </div>
            
            <p style="color:var(--text-muted); margin-bottom: 2rem; line-height: 1.6;">
                Incluez correctement les documents et médias (Photos, Vidéos, CNI/Diplômes). L'IA appliquera des pondérations strictes en fonction du métier. <br/>
                <i>Note: Les documents administratifs (CNI, Patente) agissent uniquement comme BONUS selon l'architecture (DA-001).</i>
            </p>

            <div class="grid-2">
                <!-- COLONNE 1 : TEXTE & DOCUMENTS -->
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
                        <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.3rem;">Ces documents seront envoyés au Document Verification Engine.</p>
                    </div>
                </div>

                <!-- COLONNE 2 : PREUVES VISUELLES (PORTFOLIO, VIDEO) -->
                <div>
                    <h3 style="margin-bottom: 1rem; color:var(--secondary); font-size: 1.1rem;"><i class="fa-solid fa-camera-retro"></i> Preuves Visuelles (Le plus important !)</h3>
                    
                    <div class="form-group">
                        <label class="form-label">Photos du Portfolio (Réalisations) 📸</label>
                        <div class="upload-zone" onclick="document.getElementById('portfolio_upload').click()">
                            <i class="fa-solid fa-cloud-arrow-up"></i>
                            <p>Cliquez ou glissez vos réalisations visuelles ici</p>
                            <input type="file" id="portfolio_upload" multiple accept="image/*" style="display: none;" onchange="previewImages(event)">
                        </div>
                        <div id="image-preview" class="file-preview"></div>
                        <p style="font-size:0.8rem; color:var(--text-muted); margin-top:0.5rem;">Ces visuels sont indispensables pour l'Agent Vision.</p>
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
                        <p style="margin-top: 1rem; font-size: 0.85rem; color: var(--text-muted);">
                            La pondération a été automatiquement ajustée par le système JITSE pour un <span id="res-prof" style="color:white; font-weight:bold;">--</span>.
                        </p>
                    </div>

                    <div>
                        <ul class="badge-list">
                            <li class="badge-item">
                                <span>Évaluation des Compétences Visuelles (Portfolio)</span>
                                <strong id="skill-score">--/100</strong>
                            </li>
                            <li class="badge-item">
                                <span>Index de Preuves (Dont Vidéo)</span>
                                <strong id="evidence-score">--/100</strong>
                            </li>
                            <li class="badge-item">
                                <span>Richesses Déclaratives (Profil)</span>
                                <strong id="profile-score">--/100</strong>
                            </li>
                            <li class="badge-item" style="border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.05);">
                                <span>Bonus Documents Administratifs</span>
                                <strong id="document-bonus-text" style="color:var(--success)">--</strong>
                            </li>
                            <li class="badge-item" style="border-color: rgba(239, 68, 68, 0.3);">
                                <span>Risque de Fraude et Incohérences</span>
                                <strong id="fraud-score" style="color:var(--danger)">--/100</strong>
                            </li>
                        </ul>
                        
                        <div class="ai-recommendation" id="ai-rec" style="white-space: pre-line;">
                            Analyse en attente...
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- VIEW: API INFO -->
        <section id="view-api" class="glass-panel" style="display: none;">
            <div class="section-title">
                <i class="fa-solid fa-server"></i> API JITSE & Intégration
            </div>
            <p style="color:var(--text-muted); margin-bottom: 2rem;">
                Le système JITSE est un backend pur. Intégrez-le dans l'application principale via ces Endpoints REST sécurisés.
            </p>
            
            <div style="background:rgba(0,0,0,0.3); padding:1.5rem; border-radius:12px; border:1px solid var(--border); margin-bottom:1.5rem;">
                <h4 style="margin-bottom:1rem; color:var(--primary);">1. Soumettre un Dossier</h4>
                <code style="color:var(--success); font-size:1.1rem; display:block; margin-bottom:0.5rem;">POST /api/v1/analysis/submit</code>
                <p style="color:var(--text-muted); font-size:0.9rem;">Accepte un JSON robuste avec les médias, vidéos et documents. L'orchestrateur lance 7 agents en parallèle.</p>
            </div>

            <br>
            <a href="/docs" target="_blank" class="btn" style="width:auto; display:inline-flex;">Ouvrir Swagger UI Complet</a>
        </section>

    </main>

    <script>
        // Trackers d'état pour les fichiers
        let statePhotos = 0;
        let stateDocs = 0;
        let hasVideo = false;

        function showView(viewId) {
            document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
            event.currentTarget.classList.add('active');
            
            document.getElementById('view-simulator').style.display = 'none';
            document.getElementById('view-api').style.display = 'none';
            
            document.getElementById('view-' + viewId).style.display = 'block';
        }

        // Preview de Portfolio (Images)
        function previewImages(event) {
            const preview = document.getElementById('image-preview');
            preview.innerHTML = '';
            const files = event.target.files;
            statePhotos = files.length;
            
            for(let i=0; i<files.length; i++) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(files[i]);
                const div = document.createElement('div');
                div.className = 'file-item';
                div.appendChild(img);
                
                const span = document.createElement('span');
                span.innerText = files[i].name.substring(0, 10) + '...';
                div.appendChild(span);
                
                preview.appendChild(div);
            }
        }

        // Preview Documents
        function previewDocs(event) {
            const preview = document.getElementById('docs-preview');
            preview.innerHTML = '';
            const files = event.target.files;
            stateDocs = files.length;
            
            for(let i=0; i<files.length; i++) {
                const div = document.createElement('div');
                div.className = 'file-item';
                
                const icon = document.createElement('i');
                icon.className = 'fa-solid fa-file-pdf';
                icon.style.color = 'var(--secondary)';
                div.appendChild(icon);
                
                const span = document.createElement('span');
                span.innerText = files[i].name;
                div.appendChild(span);
                
                preview.appendChild(div);
            }
        }

        // Preview Video
        function previewVideo(event) {
            const preview = document.getElementById('video-preview');
            preview.innerHTML = '';
            const files = event.target.files;
            
            if(files.length > 0) {
                hasVideo = true;
                const div = document.createElement('div');
                div.className = 'file-item';
                
                const icon = document.createElement('i');
                icon.className = 'fa-solid fa-video';
                icon.style.color = 'var(--success)';
                div.appendChild(icon);
                
                const span = document.createElement('span');
                span.innerText = files[0].name;
                div.appendChild(span);
                
                preview.appendChild(div);
            } else {
                hasVideo = false;
            }
        }

        async function submitAnalysis() {
            if (statePhotos === 0) {
                if(!confirm("⚠️ Vous n'avez ajouté aucune photo à votre portfolio ! Le score de Compétence Visuelle sera pénalisé. Continuer quand même ?")) {
                    return;
                }
            }

            const btnText = document.getElementById('btn-text');
            const spinner = document.getElementById('btn-spinner');
            const resContainer = document.getElementById('result-container');
            
            btnText.style.display = 'none';
            spinner.style.display = 'block';
            resContainer.style.display = 'none';

            const profSelect = document.getElementById('profession');
            const profession = profSelect.value;
            const professionText = profSelect.options[profSelect.selectedIndex].text;
            
            const desc = document.getElementById('description').value;

            // Structure des images ajoutées via FileReader
            const images = Array(statePhotos).fill(0).map((_, i) => ({
                id: `img_${i}`, url: `http://simulated-upload.com/visuel_${i}.jpg`, media_type: "image", mime_type: "image/jpeg", size_bytes: 1024
            }));
            
            // Structure des documents via FileReader
            const documents = Array(stateDocs).fill(0).map((_, i) => ({
                id: `doc_${i}`, url: `http://simulated-upload.com/doc_${i}.pdf`, media_type: "document", mime_type: "application/pdf", size_bytes: 2048
            }));
            
            let video = null;
            if (hasVideo) {
                video = {id: `vid_1`, url: `http://simulated-upload.com/chantier_01.mp4`, media_type: "video", mime_type: "video/mp4", size_bytes: 5048};
            }

            const payload = {
                dossier_id: "DOS-" + Math.floor(Math.random()*10000),
                provider_id: "PROV-TEST-909",
                profession_category: profession,
                profile: {
                    description: desc,
                    years_of_experience: 5,
                    location: "Douala",
                    services_offered: ["Service"],
                    declared_skills: ["Compétence"],
                    languages: ["Français"]
                },
                presentation_video: video,
                portfolio_images: images,
                documents: documents
            };

            try {
                const response = await fetch('/api/v1/analysis/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                
                const data = await response.json();
                
                document.getElementById('final-score').innerText = data.trust_score.toFixed(1);
                
                const circle = document.getElementById('circle-score');
                const scorePerc = data.trust_score + '%';
                circle.style.setProperty('--percentage', scorePerc);
                
                if(data.trust_score >= 80) circle.style.background = `conic-gradient(var(--success) ${scorePerc}, rgba(255,255,255,0.1) 0)`;
                else if (data.trust_score >= 50) circle.style.background = `conic-gradient(var(--warning) ${scorePerc}, rgba(255,255,255,0.1) 0)`;
                else circle.style.background = `conic-gradient(var(--danger) ${scorePerc}, rgba(255,255,255,0.1) 0)`;

                document.getElementById('trust-level').innerText = data.trust_level;
                document.getElementById('ai-confidence').innerText = `Certitude IA: ${data.ai_confidence_level.replace('_', ' ')}`;
                document.getElementById('res-prof').innerText = professionText;

                document.getElementById('skill-score').innerText = `${data.skill_evidence_score.toFixed(1)} / 100`;
                document.getElementById('evidence-score').innerText = `${data.evidence_index.toFixed(1)} / 100`;
                document.getElementById('profile-score').innerText = `${data.profile_quality_score.toFixed(1)} / 100`;
                document.getElementById('fraud-score').innerText = `${data.fraud_risk_index.toFixed(1)} / 100`;
                
                if(stateDocs > 0) {
                    document.getElementById('document-bonus-text').innerText = `${stateDocs} Documents (Bénéficie du DA-001) ✔️`;
                } else {
                    document.getElementById('document-bonus-text').innerText = `Aucun Doc (Neutre) ➖`;
                }

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
