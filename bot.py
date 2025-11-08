from flask import Flask, render_template_string, request, jsonify, Response
import os
import json
import time
import hashlib
import re
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Rate limiting için basit bir decorator
def rate_limit(requests_per_minute=60):
    def decorator(f):
        requests = []
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time.time()
            requests[:] = [req for req in requests if now - req < 60]
            if len(requests) >= requests_per_minute:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            requests.append(now)
            return f(*args, **kwargs)
        return wrapped
    return decorator

# XSS koruması
def sanitize_input(input_str):
    if not input_str:
        return ""
    # HTML tag'lerini temizle
    clean = re.compile('<.*?>')
    return re.sub(clean, '', input_str)

# TÜM API VERİLERİ - YENİ API'LER
ALL_APIS = [
    # YABANCI SORGULARI
    {"id": "yabanci", "title": "Yabancı Sorgu", "icon": "🌐", "category": "yabanci",
     "url": "https://nabi-api.trr.gt.tc/yabanci?ad=JOHN&soyad=DOE", "desc": "Yabancı kimlik sorgulama"},

    # TC DETAY SORGULARI
    {"id": "cinsiyet", "title": "Cinsiyet Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/cinsiyet?tc=11111111111", "desc": "TC cinsiyet sorgulama"},
    {"id": "din", "title": "Din Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/din?tc=11111111111", "desc": "TC din sorgulama"},
    {"id": "vergino", "title": "Vergi No Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/vergino?tc=11111111111", "desc": "TC vergi no sorgulama"},
    {"id": "medenihal", "title": "Medeni Hal Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/medenihal?tc=11111111111", "desc": "TC medeni hal sorgulama"},
    {"id": "koy", "title": "Köy Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/koy?tc=11111111111", "desc": "TC köy bilgisi sorgulama"},
    {"id": "burc", "title": "Burç Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/burc?tc=11111111111", "desc": "TC burç sorgulama"},
    {"id": "kimlikkayit", "title": "Kimlik Kayıt Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/kimlikkayit?tc=11111111111", "desc": "TC kimlik kayıt sorgulama"},
    {"id": "dogumyeri", "title": "Doğum Yeri Sorgu", "icon": "🔹", "category": "tc",
     "url": "https://nabi-api.trr.gt.tc/dogumyeri?tc=11111111111", "desc": "TC doğum yeri sorgulama"},

    # YETİMLİK SORGUSU
    {"id": "yetimlik", "title": "Yetimlik Sorgu", "icon": "🔹", "category": "yetimlik",
     "url": "https://nabi-api.trr.gt.tc/yetimlik?babatc=11111111111", "desc": "Yetimlik durumu sorgulama"},

    # AİLE SORGULARI
    {"id": "kardes", "title": "Kardeş Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/kardes?tc=11111111111", "desc": "Kardeş bilgileri sorgulama"},
    {"id": "anne", "title": "Anne Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/anne?tc=11111111111", "desc": "Anne bilgisi sorgulama"},
    {"id": "baba", "title": "Baba Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/baba?tc=11111111111", "desc": "Baba bilgisi sorgulama"},
    {"id": "cocuklar", "title": "Çocuklar Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/cocuklar?tc=11111111111", "desc": "Çocuk bilgileri sorgulama"},
    {"id": "amca", "title": "Amca Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/amca?tc=11111111111", "desc": "Amca bilgisi sorgulama"},
    {"id": "dayi", "title": "Dayı Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/dayi?tc=11111111111", "desc": "Dayı bilgisi sorgulama"},
    {"id": "hala", "title": "Hala Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/hala?tc=11111111111", "desc": "Hala bilgisi sorgulama"},
    {"id": "teyze", "title": "Teyze Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/teyze?tc=11111111111", "desc": "Teyze bilgisi sorgulama"},
    {"id": "kuzen", "title": "Kuzen Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/kuzen?tc=11111111111", "desc": "Kuzen bilgileri sorgulama"},
    {"id": "dede", "title": "Dede Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/dede?tc=11111111111", "desc": "Dede bilgisi sorgulama"},
    {"id": "nine", "title": "Nine Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/nine?tc=11111111111", "desc": "Nine bilgisi sorgulama"},
    {"id": "yeniden", "title": "Yeniden Sorgu", "icon": "🔹", "category": "aile",
     "url": "https://nabi-api.trr.gt.tc/yeniden?tc=11111111111", "desc": "Yeniden sorgulama"},

    # SAHMARAN BOTU SORGULARI
    {"id": "sorgu", "title": "Sahmaran Sorgu", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/sorgu?ad=AHMET&soyad=YILMAZ", "desc": "Ad soyad ile sorgulama"},
    {"id": "aile", "title": "Sahmaran Aile", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/aile?tc=11111111111", "desc": "Aile bilgileri sorgulama"},
    {"id": "adres", "title": "Sahmaran Adres", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/adres?tc=11111111111", "desc": "Adres bilgisi sorgulama"},
    {"id": "tc", "title": "Sahmaran TC", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/tc?tc=11111111111", "desc": "TC sorgulama"},
    {"id": "gsmtc", "title": "Sahmaran GSM TC", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/gsmtc?gsm=5551112233", "desc": "GSM'den TC sorgulama"},
    {"id": "tcgsm", "title": "Sahmaran TC GSM", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/tcgsm?tc=11111111111", "desc": "TC'den GSM sorgulama"},
    {"id": "olumtarihi", "title": "Sahmaran Ölüm Tarihi", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/olumtarihi?tc=11111111111", "desc": "Ölüm tarihi sorgulama"},
    {"id": "sulale", "title": "Sahmaran Sülale", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/sulale?tc=11111111111", "desc": "Sülale bilgisi sorgulama"},
    {"id": "sms", "title": "Sahmaran SMS", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/sms?gsm=5551112233", "desc": "SMS sorgulama"},
    {"id": "kizliksoyad", "title": "Sahmaran Kızlık Soyad", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/kizliksoyad?tc=11111111111", "desc": "Kızlık soyadı sorgulama"},
    {"id": "yas", "title": "Sahmaran Yaş", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/yas?tc=11111111111", "desc": "Yaş sorgulama"},
    {"id": "hikaye", "title": "Sahmaran Hikaye", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/hikaye?tc=11111111111", "desc": "Hayat hikayesi sorgulama"},
    {"id": "sirano", "title": "Sahmaran Sıra No", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/sirano?tc=11111111111", "desc": "Sıra no sorgulama"},
    {"id": "ayakno", "title": "Sahmaran Ayak No", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/ayakno?tc=11111111111", "desc": "Ayak no sorgulama"},
    {"id": "operator", "title": "Sahmaran Operatör", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/operator?gsm=5551112233", "desc": "Operatör sorgulama"},
    {"id": "yegen", "title": "Sahmaran Yeğen", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/yegen?tc=11111111111", "desc": "Yeğen bilgisi sorgulama"},
    {"id": "cocuk", "title": "Sahmaran Çocuk", "icon": "🔹", "category": "sahmaran",
     "url": "https://nabi-api.trr.gt.tc/cocuk?tc=11111111111", "desc": "Çocuk bilgisi sorgulama"},

    # MİYAVREM BOTU SORGULARI
    {"id": "vesika", "title": "Miyavrem Vesika", "icon": "🔹", "category": "miyavrem",
     "url": "https://nabi-api.trr.gt.tc/vesika?tc=11111111111", "desc": "Vesika sorgulama"},
    {"id": "plaka", "title": "Miyavrem Plaka", "icon": "🔹", "category": "miyavrem",
     "url": "https://nabi-api.trr.gt.tc/plaka?plaka=34ABC123", "desc": "Plaka sorgulama"},
    {"id": "tcplaka", "title": "Miyavrem TC Plaka", "icon": "🔹", "category": "miyavrem",
     "url": "https://nabi-api.trr.gt.tc/tcplaka?tc=11111111111", "desc": "TC'den plaka sorgulama"}
]

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nabi API - Türkiye'nin En İyi Ücretsiz API Servisi</title>
    <style>
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f3460;
            --highlight: #e94560;
            --text: #ffffff;
            --text-muted: #b8b8b8;
            --success: #00b894;
            --warning: #fdcb6e;
            --danger: #e74c3c;
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-border: rgba(255, 255, 255, 0.1);
            --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            color: var(--text);
            line-height: 1.6;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(233, 69, 96, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(15, 52, 96, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(22, 33, 62, 0.2) 0%, transparent 50%);
            z-index: -1;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            padding: 40px 0;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 20px;
            margin-bottom: 30px;
            border: 1px solid var(--card-border);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }
        
        header::before {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .logo {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(45deg, var(--highlight), var(--warning));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: var(--text-muted);
            font-size: 1.2rem;
            margin-bottom: 20px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid var(--card-border);
            backdrop-filter: blur(10px);
            transition: var(--transition);
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: var(--highlight);
            margin-bottom: 5px;
        }
        
        .api-categories {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .category {
            background: var(--card-bg);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid var(--card-border);
            backdrop-filter: blur(10px);
            transition: var(--transition);
        }
        
        .category:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow);
            border-color: var(--highlight);
        }
        
        .category h3 {
            color: var(--highlight);
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .api-list {
            list-style: none;
        }
        
        .api-item {
            background: rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
            border-radius: 10px;
            overflow: hidden;
            transition: var(--transition);
            border: 1px solid transparent;
        }
        
        .api-item:hover {
            background: rgba(0, 0, 0, 0.3);
            border-color: var(--card-border);
        }
        
        .api-header {
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        
        .api-name {
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .api-actions {
            display: flex;
            gap: 8px;
        }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: var(--transition);
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .btn-primary {
            background: var(--accent);
            color: white;
        }
        
        .btn-primary:hover {
            background: var(--highlight);
            transform: translateY(-2px);
        }
        
        .btn-success {
            background: var(--success);
            color: white;
        }
        
        .btn-success:hover {
            background: #00a085;
            transform: translateY(-2px);
        }
        
        .api-content {
            padding: 0 15px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out;
        }
        
        .api-content.active {
            padding: 0 15px 15px;
            max-height: 500px;
        }
        
        .api-result {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid var(--card-border);
        }
        
        .api-url {
            background: rgba(0, 0, 0, 0.5);
            padding: 12px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            word-break: break-all;
            margin-top: 10px;
            font-size: 0.9rem;
            color: var(--text-muted);
            border: 1px solid var(--card-border);
            display: none;
        }
        
        .api-params {
            margin-top: 15px;
        }
        
        .param-group {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }
        
        .param-input {
            flex: 1;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 10px;
            color: var(--text);
            transition: var(--transition);
        }
        
        .param-input:focus {
            outline: none;
            border-color: var(--highlight);
        }
        
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--success);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: var(--shadow);
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }
        
        .security-badge {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            z-index: 100;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .api-categories {
                grid-template-columns: 1fr;
            }
            
            .param-group {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="security-badge">
        🔒 Güvenli Bağlantı
    </div>
    
    <div class="container">
        <header>
            <div class="logo">🔮</div>
            <h1>Nabi API Servisi</h1>
            <div class="subtitle">Türkiye'nin En İyi Ücretsiz API Servisi</div>
            <p>🌐 Tüm API URL'leri - nabi-api.trr.gt.tc</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ total_apis }}</div>
                <div>Toplam API</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">7/24</div>
                <div>Aktif Hizmet</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">%99.9</div>
                <div>Uptime</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0₺</div>
                <div>Tamamen Ücretsiz</div>
            </div>
        </div>
        
        <div class="api-categories">
            <!-- Yabancı Sorguları -->
            <div class="category">
                <h3><span>🌐</span> Yabancı Sorguları</h3>
                <ul class="api-list">
                    {% for api in apis if api.category == 'yabanci' %}
                    <li class="api-item">
                        <div class="api-header" onclick="toggleApiContent('{{ api.id }}')">
                            <span class="api-name">
                                <span>{{ api.icon }}</span>
                                {{ api.title }}
                            </span>
                            <div class="api-actions">
                                <button class="btn btn-success" onclick="event.stopPropagation(); copyApiUrl('{{ api.url }}')">
                                    📋 Kopyala
                                </button>
                                <button class="btn btn-primary" onclick="event.stopPropagation(); toggleApiContent('{{ api.id }}')">
                                    🔍 Aç
                                </button>
                            </div>
                        </div>
                        <div class="api-content" id="{{ api.id }}-content">
                            <div class="api-params">
                                {% if 'ad=' in api.url and 'soyad=' in api.url %}
                                <div class="param-group">
                                    <input type="text" class="param-input" id="{{ api.id }}-ad" placeholder="Ad (Örn: JOHN)">
                                    <input type="text" class="param-input" id="{{ api.id }}-soyad" placeholder="Soyad (Örn: DOE)">
                                </div>
                                {% elif 'tc=' in api.url %}
                                <div class="param-group">
                                    <input type="text" class="param-input" id="{{ api.id }}-tc" placeholder="TC Kimlik No">
                                </div>
                                {% elif 'gsm=' in api.url %}
                                <div class="param-group">
                                    <input type="text" class="param-input" id="{{ api.id }}-gsm" placeholder="GSM No (Örn: 5551112233)">
                                </div>
                                {% elif 'plaka=' in api.url %}
                                <div class="param-group">
                                    <input type="text" class="param-input" id="{{ api.id }}-plaka" placeholder="Plaka (Örn: 34ABC123)">
                                </div>
                                {% elif 'babatc=' in api.url %}
                                <div class="param-group">
                                    <input type="text" class="param-input" id="{{ api.id }}-babatc" placeholder="Baba TC Kimlik No">
                                </div>
                                {% endif %}
                                <button class="btn btn-primary" onclick="executeApi('{{ api.id }}', '{{ api.url }}')">
                                    🚀 Sorgula
                                </button>
                            </div>
                            <div class="api-url" id="{{ api.id }}-url">{{ api.url }}</div>
                            <div class="api-result" id="{{ api.id }}-result"></div>
                        </div>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            
            <!-- TC Detay Sorguları -->
            <div class="category">
                <h3><span>🔹</span> TC Detay Sorguları</h3>
                <ul class="api-list">
                    {% for api in apis if api.category == 'tc' %}
                    <li class="api-item">
                        <div class="api-header" onclick="toggleApiContent('{{ api.id }}')">
                            <span class="api-name">
                                <span>{{ api.icon }}</span>
                                {{ api.title }}
                            </span>
                            <div class="api-actions">
                                <button class="btn btn-success" onclick="event.stopPropagation(); copyApiUrl('{{ api.url }}')">
                                    📋 Kopyala
                                </button>
                                <button class="btn btn-primary" onclick="event.stopPropagation(); toggleApiContent('{{ api.id }}')">
                                    🔍 Aç
                                </button>
                            </div>
                        </div>
                        <div class="api-content" id="{{ api.id }}-content">
                            <div class="api-params">
                                <div class="param-group">
                                    <input type="text" class="param-input" id="{{ api.id }}-tc" placeholder="TC Kimlik No">
                                </div>
                                <button class="btn btn-primary" onclick="executeApi('{{ api.id }}', '{{ api.url }}')">
                                    🚀 Sorgula
                                </button>
                            </div>
                            <div class="api-url" id="{{ api.id }}-url">{{ api.url }}</div>
                            <div class="api-result" id="{{ api.id }}-result"></div>
                        </div>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            
            <!-- Diğer kategoriler buraya eklenebilir -->
        </div>
    </div>
    
    <div class="toast" id="toast"></div>

    <script>
        function toggleApiContent(apiId) {
            const content = document.getElementById(apiId + '-content');
            content.classList.toggle('active');
        }
        
        function copyApiUrl(url) {
            navigator.clipboard.writeText(url).then(() => {
                showToast('API URL kopyalandı!');
            }).catch(err => {
                showToast('Kopyalama başarısız: ' + err);
            });
        }
        
        function executeApi(apiId, baseUrl) {
            const resultElement = document.getElementById(apiId + '-result');
            resultElement.textContent = 'Sorgulanıyor...';
            
            let url = baseUrl;
            
            // Parametreleri değiştir
            if (baseUrl.includes('ad=') && baseUrl.includes('soyad=')) {
                const ad = document.getElementById(apiId + '-ad')?.value || 'JOHN';
                const soyad = document.getElementById(apiId + '-soyad')?.value || 'DOE';
                url = baseUrl.replace('ad=JOHN', 'ad=' + ad).replace('soyad=DOE', 'soyad=' + soyad);
            } else if (baseUrl.includes('tc=')) {
                const tc = document.getElementById(apiId + '-tc')?.value || '11111111111';
                url = baseUrl.replace('tc=11111111111', 'tc=' + tc);
            } else if (baseUrl.includes('gsm=')) {
                const gsm = document.getElementById(apiId + '-gsm')?.value || '5551112233';
                url = baseUrl.replace('gsm=5551112233', 'gsm=' + gsm);
            } else if (baseUrl.includes('plaka=')) {
                const plaka = document.getElementById(apiId + '-plaka')?.value || '34ABC123';
                url = baseUrl.replace('plaka=34ABC123', 'plaka=' + plaka);
            } else if (baseUrl.includes('babatc=')) {
                const babatc = document.getElementById(apiId + '-babatc')?.value || '11111111111';
                url = baseUrl.replace('babatc=11111111111', 'babatc=' + babatc);
            }
            
            // API'yi çağır (simülasyon)
            setTimeout(() => {
                const responses = {
                    'success': true,
                    'data': {
                        'api': apiId,
                        'url': url,
                        'timestamp': new Date().toISOString(),
                        'status': 'success'
                    }
                };
                resultElement.textContent = JSON.stringify(responses, null, 2);
            }, 1000);
        }
        
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
        
        // Sayfa yüklendiğinde ilk API'yi aç
        document.addEventListener('DOMContentLoaded', function() {
            // İlk API'yi açık göster
            const firstApi = document.querySelector('.api-item');
            if (firstApi) {
                const firstApiId = firstApi.querySelector('.api-header').getAttribute('onclick').match(/'([^']+)'/)[1];
                toggleApiContent(firstApiId);
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
@rate_limit(30)  # Dakikada 30 istek
def home():
    total_apis = len(ALL_APIS)
    return render_template_string(HTML_TEMPLATE, apis=ALL_APIS, total_apis=total_apis)

@app.route('/api-list')
@rate_limit(60)
def api_list():
    return jsonify({
        'total': len(ALL_APIS),
        'apis': ALL_APIS
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

# Güvenlik headers'ı ekle
@app.after_request
def apply_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # Production için debug=False yapın
    app.run(host='0.0.0.0', port=port, debug=False)
