from flask import Flask, jsonify, request, render_template_string
import requests
import json
import os

app = Flask(__name__)

# Ana sayfa için HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nabi System API Servisi — v2</title>
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root{
            --bg-1: #0f1724;
            --bg-2: #0b1220;
            --accent-1: #4cc9f0;
            --accent-2: #ff8a00;
            --glass: rgba(255,255,255,0.06);
            --glass-2: rgba(255,255,255,0.08);
            --card-border: rgba(255,255,255,0.06);
            --muted: #cbd5e1;
            --glass-blur: 10px;
            --radius: 14px;
        }

        *{box-sizing:border-box;margin:0;padding:0}
        html,body{height:100%}
        body{
            font-family:'Inter',system-ui,-apple-system,"Segoe UI",Roboto,Arial,"Noto Sans",sans-serif;
            background: radial-gradient(1200px 600px at 10% 10%, rgba(76,201,240,0.06), transparent), linear-gradient(135deg,var(--bg-1) 0%,var(--bg-2) 100%);
            color:#fff;min-height:100vh;overflow-x:hidden;line-height:1.35;
            padding:16px;
        }

        /* Background image with controllable blur */
        .bg-image{
            position:fixed;inset:0;background-image: url('https://i.ibb.co/wNDn84h0/file-00000000ffc061f4bacedf89d0e6a130.png');
            background-size:cover;background-position:center;opacity:0.55;z-index:-3;filter:grayscale(10%);
            transition:filter .35s ease, opacity .35s ease;
        }
        .bg-image.blurred{filter:blur(6px) saturate(0.75);opacity:0.46}

        /* subtle animated gradient overlay */
        .gradient-overlay{position:fixed;inset:0;z-index:-2;background:linear-gradient(90deg, rgba(255,140,0,0.06), rgba(76,201,240,0.04));mix-blend-mode:overlay;pointer-events:none}

        /* container */
        .wrapper{max-width:1200px;margin:0 auto}

        header{display:flex;flex-direction:column;gap:16px;margin-bottom:20px}
        .brand{display:flex;align-items:center;gap:14px}
        .brand h1{font-size:24px;letter-spacing:0.5px;background:linear-gradient(90deg,var(--accent-2),#e52e71);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:800}
        .brand p{color:var(--muted);font-size:12px}

        /* top controls */
        .header-top{display:flex;justify-content:space-between;align-items:center;gap:12px}
        .controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
        .search{display:flex;align-items:center;background:var(--glass);padding:8px 12px;border-radius:12px;border:1px solid var(--card-border);gap:8px;flex:1;min-width:200px;max-width:300px}
        .search input{background:transparent;border:0;outline:0;color:inherit;font-size:14px;width:100%}
        .small-btn{background:transparent;border:1px solid var(--card-border);padding:8px 10px;border-radius:10px;font-size:13px;cursor:pointer;white-space:nowrap}
        .small-btn:active{transform:translateY(1px)}

        /* header stats */
        .stats{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
        .stat{background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));padding:8px 12px;border-radius:10px;border:1px solid var(--card-border);font-weight:600;min-width:80px}
        .stat .num{font-size:16px;color:var(--accent-2)}
        .stat .label{font-size:11px;color:var(--muted)}

        main{margin-top:6px}

        .section-title{font-size:18px;color:var(--accent-1);margin:16px 0 8px;font-weight:700}

        .api-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
        .api-card{background:var(--glass);padding:14px;border-radius:var(--radius);border:1px solid var(--card-border);backdrop-filter:blur(var(--glass-blur));box-shadow:0 8px 30px rgba(2,6,23,0.6);display:flex;flex-direction:column;gap:10px;transition:transform .18s ease,box-shadow .18s ease}
        .api-card:hover{transform:translateY(-4px);box-shadow:0 12px 30px rgba(0,0,0,0.6)}

        .api-head{display:flex;align-items:flex-start;gap:10px}
        .api-icon{width:42px;height:42px;border-radius:8px;display:grid;place-items:center;font-size:18px;background:linear-gradient(135deg,#4361ee,#3a0ca3);box-shadow:0 4px 12px rgba(0,0,0,0.4);flex-shrink:0}
        .api-title{font-weight:700;color:#ff6aa2;font-size:14px;line-height:1.3}
        .api-desc{font-size:12px;color:var(--muted);line-height:1.4}

        .api-url{background:rgba(0,0,0,0.3);padding:8px 10px;border-radius:8px;font-family:monospace;font-size:11px;color:var(--accent-1);word-break:break-all;border:1px solid rgba(255,255,255,0.04);line-height:1.4}

        .card-actions{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
        .btn{display:inline-flex;align-items:center;gap:6px;padding:6px 8px;border-radius:8px;border:1px solid var(--card-border);background:transparent;cursor:pointer;font-weight:600;font-size:12px;white-space:nowrap}
        .btn.copy{min-width:70px}
        .badge{padding:4px 8px;border-radius:999px;background:rgba(40,167,69,0.18);color:#b7f0c1;border:1px solid rgba(40,167,69,0.4);font-weight:700;font-size:11px;white-space:nowrap}

        /* warning / info */
        .notice{padding:10px;border-radius:10px;background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));border:1px solid rgba(255,255,255,0.04);color:var(--muted);display:flex;gap:10px;align-items:flex-start;font-size:12px;line-height:1.4}

        /* about section */
        .about-section{background:var(--glass);padding:20px;border-radius:var(--radius);border:1px solid var(--card-border);margin:20px 0}
        .about-section h2{color:var(--accent-1);margin-bottom:12px;font-size:20px}
        .about-content{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}
        .about-card{background:rgba(255,255,255,0.03);padding:16px;border-radius:10px;border:1px solid rgba(255,255,255,0.05)}
        .about-card h3{color:var(--accent-2);margin-bottom:8px;font-size:16px}
        .about-card p{color:var(--muted);font-size:13px;line-height:1.5}

        footer{margin-top:20px;text-align:center;color:var(--muted);font-size:12px;padding:10px 0}

        /* Mobile responsive */
        @media (max-width: 768px) {
            body{padding:12px}
            .header-top{flex-direction:column;align-items:stretch;gap:12px}
            .controls{justify-content:space-between}
            .search{max-width:none;min-width:auto}
            .stats{justify-content:center}
            .api-grid{grid-template-columns:1fr;gap:10px}
            .api-card{padding:12px}
            .brand h1{font-size:20px}
            .section-title{font-size:16px}
            .about-content{grid-template-columns:1fr}
        }

        @media (max-width: 480px) {
            body{padding:8px}
            .brand{flex-direction:column;align-items:flex-start;gap:8px}
            .brand h1{font-size:18px}
            .controls{gap:8px}
            .search{padding:6px 10px}
            .small-btn{padding:6px 8px;font-size:12px}
            .stat{padding:6px 10px;min-width:70px}
            .stat .num{font-size:14px}
        }

        /* small utility */
        .menu-dot{background:var(--glass-2);padding:8px;border-radius:8px;border:1px solid var(--card-border);cursor:pointer;display:grid;place-items:center;width:36px;height:36px}

        /* modal */
        .modal{position:fixed;right:12px;top:60px;background:rgba(6,8,20,0.95);padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.04);display:none;z-index:40;min-width:160px}
        .modal.show{display:block}
        .modal a{display:block;padding:8px 10px;border-radius:6px;color:var(--muted);text-decoration:none;font-size:13px}
        .modal a:hover{background:rgba(255,255,255,0.02);color:#fff}

        /* toast */
        .toast{position:fixed;right:12px;bottom:12px;background:#0b1220;padding:8px 12px;border-radius:8px;border:1px solid var(--card-border);display:none;z-index:50;font-size:13px}

        /* Mobile menu improvements */
        @media (max-width: 768px) {
            .modal{right:8px;top:56px;min-width:140px}
            .toast{right:8px;bottom:8px}
        }
    </style>
</head>
<body>
    <div class="bg-image" id="bgImage" aria-hidden="true"></div>
    <div class="gradient-overlay" aria-hidden="true"></div>

    <div class="wrapper">
        <header>
            <div class="header-top">
                <div class="brand">
                    <div style="display:flex;flex-direction:column">
                        <h1>Nabi System</h1>
                        <p>API Service • Mobile Uyumlu</p>
                    </div>
                </div>

                <div class="controls">
                    <div class="search" role="search" aria-label="API ara">
                        <i class="fa fa-search" style="opacity:.8"></i>
                        <input id="q" placeholder="API ara..." aria-label="API arama"/>
                    </div>

                    <button class="small-btn" id="toggleBg" title="Arka plan bulanıklaştır">BG</button>

                    <div class="menu-dot" id="menuDot" title="Ayarlar">
                        <i class="fa fa-ellipsis-v"></i>
                    </div>
                </div>
            </div>

            <div class="stats" aria-hidden="true">
                <div class="stat"><div class="num" id="totalApis">62</div><div class="label">Toplam API</div></div>
                <div class="stat"><div class="num" id="activeApis">62</div><div class="label">Aktif API</div></div>
            </div>
        </header>

        <div class="modal" id="menuModal" role="menu" aria-hidden="true">
            <a href="#" id="openEditor">Sayfa kaynağını düzenle</a>
            <a href="#" id="downloadJson">API listesini indir (.json)</a>
            <a href="#" id="about">Hakkında</a>
        </div>

        <main>
            <section>
                <div class="notice" role="status">
                    <i class="fa fa-exclamation-triangle" style="color:#ffb4b4"></i>
                    <div>
                        Apiler bize aittir. Lütfen verileri paylaşırken gizlilik ve yasalara dikkat ediniz.
                    </div>
                </div>
            </section>

            <!-- About Section -->
            <section class="about-section">
                <h2>🚀 Nabi System Hakkında</h2>
                <div class="about-content">
                    <div class="about-card">
                        <h3>📊 Servis İstatistikleri</h3>
                        <p>• Toplam 62+ Aktif API<br>• 12+ Farklı Kategori<br>• 7/24 Çalışır Durum<br>• Mobile Uyumlu Arayüz</p>
                    </div>
                    <div class="about-card">
                        <h3>🔧 Teknoloji Stack</h3>
                        <p>• Flask Backend API<br>• JavaScript Frontend<br>• RESTful Mimarisi<br>• JSON Formatı</p>
                    </div>
                    <div class="about-card">
                        <h3>🎯 Kullanım Alanları</h3>
                        <p>• Sosyal Medya Otomasyon<br>• Veri Sorgulama<br>• AI Destekli API'ler<br>• Account Checker</p>
                    </div>
                    <div class="about-card">
                        <h3>📞 İletişim & Destek</h3>
                        <p>• Telegram: @sukazatkinis<br>• Kanal: @nabisystem<br>• 7/24 Teknik Destek<br>• Hızlı Yanıt Süresi</p>
                    </div>
                </div>
            </section>

            <h2 class="section-title">🔐 Checker API'leri</h2>
            <div class="api-grid" id="checkerGrid"></div>

            <h2 class="section-title">🐀 Rato API'leri</h2>
            <div class="api-grid" id="ratoGrid"></div>

            <h2 class="section-title">📱 Sosyal Medya API'leri</h2>
            <div class="api-grid" id="sosyalGrid"></div>

            <h2 class="section-title">🤖 AI API'leri</h2>
            <div class="api-grid" id="aiGrid"></div>

            <h2 class="section-title">🆔 TC Sorgulama API'leri</h2>
            <div class="api-grid" id="tcGrid"></div>

            <h2 class="section-title">👤 Ad Soyad Sorgulama</h2>
            <div class="api-grid" id="adsoyadGrid"></div>

            <h2 class="section-title">💼 İş ve Vergi Sorgulama</h2>
            <div class="api-grid" id="isvergiGrid"></div>

            <h2 class="section-title">📱 TC-GSM Sorgulama</h2>
            <div class="api-grid" id="tcgsmGrid"></div>

            <h2 class="section-title">🏠 Adres ve Konum Sorgulama</h2>
            <div class="api-grid" id="adresGrid"></div>

            <h2 class="section-title">👨‍👩‍👧‍👦 Eş ve Aile Sorgulama</h2>
            <div class="api-grid" id="aileGrid"></div>

            <h2 class="section-title">🎓 Eğitim Sorgulama</h2>
            <div class="api-grid" id="egitimGrid"></div>

            <h2 class="section-title">🌐 Network Sorgulama</h2>
            <div class="api-grid" id="networkGrid"></div>

            <h2 class="section-title">🔓 Leak ve Telegram</h2>
            <div class="api-grid" id="leakGrid"></div>

            <h2 class="section-title">💰 IBAN API'leri</h2>
            <div class="api-grid" id="ibanGrid"></div>

            <h2 class="section-title">🔒 Şifre Encrypt</h2>
            <div class="api-grid" id="sifreGrid"></div>

            <h2 class="section-title">💳 Ödeme API'leri</h2>
            <div class="api-grid" id="payGrid"></div>
        </main>

        <footer>
            <div>NABI SYSTEM SUNAR — v2 • 62+ API • Mobile Uyumlu</div>
            <div style="margin-top:6px;color:var(--muted);font-size:11px">© 2025 Nabi System • Telegram: @sukazatkinis</div>
        </footer>
    </div>

    <div class="toast" id="toast">Kopyalandı!</div>

    <script>
        // API veri tanımı
        const apiData = {
            checker: [
                {id:'instagram_login',title:'Instagram Login Check',icon:'📷',url:'https://nabi-check.trr.gt.tc/api/instagram/login?username=KULLANICI&password=SIFRE',desc:'Instagram giriş kontrolü.'},
                {id:'tiktok_reset',title:'TikTok Reset Check',icon:'🎵',url:'https://nabi-check.trr.gt.tc/api/tiktok/reset?email=email@gmail.com',desc:'TikTok reset kontrolü.'},
                {id:'cramly_check',title:'Cramly Check',icon:'📚',url:'https://nabi-check.trr.gt.tc/api/cramly/check?email=email@mail.com&password=sifre',desc:'Cramly hesap kontrolü.'},
                {id:'tgoyemek_check',title:'Tgoyemek Check',icon:'🍔',url:'https://nabi-check.trr.gt.tc/api/tgoyemek/check?username=kullanici&password=sifre',desc:'Tgoyemek hesap kontrolü.'},
                {id:'oyundinar_check',title:'OyunDinar Check',icon:'🎮',url:'https://nabi-check.trr.gt.tc/api/oyundinar/check?email=email@mail.com&password=sifre',desc:'OyunDinar hesap kontrolü.'},
                {id:'mullvad_check',title:'Mullvad Check',icon:'🔒',url:'https://nabi-check.trr.gt.tc/api/mullvad/check?username=kullanici&password=sifre',desc:'Mullvad VPN kontrolü.'},
                {id:'supercell_check',title:'Supercell Check',icon:'📱',url:'https://nabi-check.trr.gt.tc/api/supercell/check?email=email@mail.com&password=sifre',desc:'Supercell hesap kontrolü.'},
                {id:'checker_stats',title:'Checker İstatistikler',icon:'📊',url:'https://nabi-check.trr.gt.tc/api/stats',desc:'Checker API istatistikleri.'}
            ],
            rato: [
                {id:'rato_check_domain',title:'Rato Domain Kontrol',icon:'🔍',url:'https://ratoekes.onrender.com/api/check_domain/test-domain',desc:'Domain kayıt kontrolü.'},
                {id:'rato_register',title:'Rato Kayıt İşlemi',icon:'📝',url:'curl -X POST "https://ratoekes.onrender.com/api/register" -H "Content-Type: application/json" -d \'{"domain": "test-domain", "client_id": "test-client", "info": {"os": "Windows"}}\'',desc:'Yeni istemci kaydı.'},
                {id:'rato_check_commands',title:'Rato Komut Kontrol',icon:'⚡',url:'https://ratoekes.onrender.com/api/check_commands/test-domain/test-client',desc:'Komut sorgulama.'}
            ],
            sosyal: [
                {id:'instagram_likes',title:'Instagram Beğeni (75)',icon:'❤️',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_likes&link=https://instagram.com/p/CXXXXXXXXXX/',desc:'Instagram beğeni gönderimi.'},
                {id:'tiktok_likes',title:'TikTok Beğeni (30)',icon:'👍',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=tiktok_likes&link=https://tiktok.com/@user/video/7XXXXXXXXXXXXXXX/',desc:'TikTok beğeni gönderimi.'},
                {id:'instagram_followers',title:'Instagram Takipçi (10)',icon:'👥',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_followers&link=https://instagram.com/takipedilecek_username/',desc:'Instagram takipçi gönderimi.'},
                {id:'instagram_views',title:'Instagram Görüntüleme (2500)',icon:'👀',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_views&link=https://instagram.com/p/CXXXXXXXXXX/',desc:'Instagram görüntüleme gönderimi.'},
                {id:'instagram_saves',title:'Instagram Kaydetme (150)',icon:'💾',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_saves&link=https://instagram.com/p/CXXXXXXXXXX/',desc:'Instagram kaydetme gönderimi.'},
                {id:'instagram_shares',title:'Instagram Paylaşım (300)',icon:'🔄',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_shares&link=https://instagram.com/p/CXXXXXXXXXX/',desc:'Instagram paylaşım gönderimi.'},
                {id:'instagram_story_views',title:'Instagram Story Görüntüleme',icon:'📱',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_story_views&link=https://instagram.com/stories/username/XXXXXXXXXX/',desc:'Instagram story görüntüleme.'},
                {id:'tiktok_views',title:'TikTok Görüntüleme (400)',icon:'🎬',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=tiktok_views&link=https://tiktok.com/@user/video/7XXXXXXXXXXXXXXX/',desc:'TikTok görüntüleme gönderimi.'},
                {id:'tiktok_followers',title:'TikTok Takipçi (20)',icon:'👥',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=tiktok_followers&link=https://tiktok.com/@takipedilecek_user/',desc:'TikTok takipçi gönderimi.'},
                {id:'youtube_likes',title:'YouTube Beğeni',icon:'▶️',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=youtube_likes&link=https://youtube.com/watch?v=XXXXXXXXXXX',desc:'YouTube beğeni gönderimi.'},
                {id:'spotify_saves',title:'Spotify Kaydetme',icon:'🎵',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=spotify_saves&link=https://open.spotify.com/track/XXXXXXXXX',desc:'Spotify kaydetme gönderimi.'},
                {id:'services_list',title:'Servis Listesi',icon:'📋',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/services',desc:'Tüm servislerin listesi.'},
                {id:'api_status',title:'API Durumu',icon:'🟢',url:'https://api-nabi-sosyalmedya.trr.gt.tc/api/status',desc:'API durum kontrolü.'}
            ],
            ai: [
                {id:'gpt5mini',title:'CHAT GPT 5 MINI MODEL',icon:'🤖',url:'https://ai.nabi.22web.org/gpt5model?message=merhaba',desc:'Genel sohbet modeli.'},
                {id:'gpt4mini',title:'CHAT GPT 4 MODEL',icon:'🧠',url:'https://ai.nabi.22web.org/gpt4mini?message=merhaba',desc:'GPT-4 benzeri model.'},
                {id:'deepseek',title:'DEEPSEEK MODEL',icon:'🔍',url:'https://ai.nabi.22web.org/deepseek?message=merhaba',desc:'Arama/analiz odaklı.'},
                {id:'gemini',title:'GEMINI 1.5 PRO MODEL',icon:'💎',url:'https://ai.nabi.22web.org/gemini1.5pro?message=merhaba',desc:'Google Gemini benzeri.'},
                {id:'unknown',title:'BİLİNMEYEN MODEL',icon:'❓',url:'https://ai.nabi.22web.org/chat?message=merhaba',desc:'Belirsiz model.'}
            ],
            tc: [
                {id:'tc',title:'TC SORGULAMA',icon:'🆔',url:'https://api-nabi.trr.gt.tc/tc?tc=12345678901',desc:'TC kimlik no sorgulama.'},
                {id:'tc_pro',title:'TC PRO SORGULAMA',icon:'🔍',url:'https://api-nabi.trr.gt.tc/tc_pro_sorgulama?tc=12345678901',desc:'Detaylı TC sorgulama.'},
                {id:'aile',title:'AILE SORGULAMA',icon:'👨‍👩‍👧‍👦',url:'https://api-nabi.trr.gt.tc/aile?tc=12345678901',desc:'Aile bireylerini sorgulama.'},
                {id:'aile_pro',title:'AILE PRO SORGULAMA',icon:'🏠',url:'https://api-nabi.trr.gt.tc/aile_pro?tc=12345678901',desc:'Detaylı aile sorgulama.'},
                {id:'sulale',title:'SÜLALE SORGULAMA',icon:'🌳',url:'https://api-nabi.trr.gt.tc/sulale?tc=12345678901',desc:'Sülale/soy ağacı sorgulama.'},
                {id:'hayat_hikayesi',title:'HAYAT HİKAYESİ',icon:'📖',url:'https://api-nabi.trr.gt.tc/hayat_hikayesi?tc=12345678901',desc:'Kişisel hayat hikayesi.'}
            ],
            adsoyad: [
                {id:'adsoyad',title:'AD SOYAD SORGULAMA',icon:'👤',url:'https://api-nabi.trr.gt.tc/adsoyad?ad=Ali&soyad=Yılmaz',desc:'Ad soyad ile sorgulama.'},
                {id:'ad_soyad',title:'AD SOYAD SORGULAMA 2',icon:'🔎',url:'https://api-nabi.trr.gt.tc/ad_soyad?ad=Mehmet&soyad=Demir',desc:'Alternatif ad soyad sorgu.'},
                {id:'ad_soyad_pro',title:'AD SOYAD PRO',icon:'💼',url:'https://api-nabi.trr.gt.tc/ad_soyad_pro?ad=Ahmet&soyad=Kaya',desc:'Profesyonel ad soyad sorgu.'},
                {id:'adi_il_ilce',title:'AD İL İLÇE SORGULAMA',icon:'📍',url:'https://api-nabi.trr.gt.tc/adi_il_ilce?ad=Ayşe&il=İstanbul&ilce=Kadıköy',desc:'Ad, il ve ilçe ile sorgu.'}
            ],
            isvergi: [
                {id:'is_yeri',title:'İŞ YERİ SORGULAMA',icon:'🏢',url:'https://api-nabi.trr.gt.tc/is_yeri?vergino=1234567890',desc:'Vergi no ile iş yeri sorgu.'},
                {id:'vergi_no',title:'VERGİ NO SORGULAMA',icon:'💰',url:'https://api-nabi.trr.gt.tc/vergi_no?vergino=1234567890',desc:'Vergi numarası sorgulama.'},
                {id:'yas',title:'YAŞ SORGULAMA',icon:'🎂',url:'https://api-nabi.trr.gt.tc/yas?yas=25',desc:'Yaş bazlı sorgulama.'}
            ],
            tcgsm: [
                {id:'tc_gsm',title:'TC GSM SORGULAMA',icon:'📱',url:'https://api-nabi.trr.gt.tc/tc_gsm?tc=12345678901',desc:'TC den GSM sorgulama.'},
                {id:'gsm_tc',title:'GSM TC SORGULAMA',icon:'📞',url:'https://api-nabi.trr.gt.tc/gsm_tc?gsm=5551234567',desc:'GSM den TC sorgulama.'}
            ],
            adres: [
                {id:'adres',title:'ADRES SORGULAMA',icon:'🏠',url:'https://api-nabi.trr.gt.tc/adres?tc=12345678901',desc:'TC ile adres sorgulama.'},
                {id:'hane',title:'HANE SORGULAMA',icon:'👨‍👩‍👧‍👦',url:'https://api-nabi.trr.gt.tc/hane?tc=12345678901',desc:'Hane bilgisi sorgulama.'},
                {id:'apartman',title:'APARTMAN SORGULAMA',icon:'🏢',url:'https://api-nabi.trr.gt.tc/apartman?apartman=ABC123',desc:'Apartman bilgisi sorgu.'},
                {id:'ada_parsel',title:'ADA PARSEL SORGULAMA',icon:'🗺️',url:'https://api-nabi.trr.gt.tc/ada_parsel?ada=1&parsel=25',desc:'Ada ve parsel sorgulama.'}
            ],
            aile: [
                {id:'es',title:'EŞ SORGULAMA',icon:'💑',url:'https://api-nabi.trr.gt.tc/es?tc=12345678901',desc:'Eş bilgisi sorgulama.'}
            ],
            egitim: [
                {id:'lgs',title:'LGS SORGULAMA',icon:'🎓',url:'https://api-nabi.trr.gt.tc/lgs?tc=12345678901',desc:'LGS sonuçları sorgulama.'},
                {id:'e_kurs',title:'E-KURS SORGULAMA',icon:'📚',url:'https://api-nabi.trr.gt.tc/e_kurs?tc=12345678901',desc:'E-kurs bilgileri sorgu.'}
            ],
            network: [
                {id:'ip',title:'IP SORGULAMA',icon:'🌐',url:'https://api-nabi.trr.gt.tc/ip?ip=192.168.1.1',desc:'IP adresi sorgulama.'},
                {id:'dns',title:'DNS SORGULAMA',icon:'🔗',url:'https://api-nabi.trr.gt.tc/dns?domain=example.com',desc:'DNS kayıtları sorgulama.'},
                {id:'whois',title:'WHOIS SORGULAMA',icon:'🔍',url:'https://api-nabi.trr.gt.tc/whois?domain=example.com',desc:'Domain whois sorgulama.'},
                {id:'subdomain',title:'SUBDOMAIN SORGULAMA',icon:'🔎',url:'https://api-nabi.trr.gt.tc/subdomain?domain=example.com',desc:'Subdomain bulma.'}
            ],
            leak: [
                {id:'leak',title:'LEAK SORGULAMA',icon:'🔓',url:'https://api-nabi.trr.gt.tc/leak?email=ornek@gmail.com',desc:'Email leak kontrolü.'},
                {id:'telegram',title:'TELEGRAM SORGULAMA',icon:'📱',url:'https://api-nabi.trr.gt.tc/telegram?username=ornekkullanici',desc:'Telegram kullanıcı sorgu.'}
            ],
            iban: [
                {id:'iban_verify',title:'IBAN DOĞRULAMA',icon:'✅',url:'https://api-nabi.trr.gt.tc/iban_verify?iban=TR330006100519786457841326',desc:'IBAN doğrulama endpointi.'},
                {id:'iban_query',title:'IBAN SORGULAMA',icon:'🔎',url:'https://api-nabi.trr.gt.tc/iban_query?iban=TR330006100519786457841326',desc:'IBAN ile banka bilgisi.'}
            ],
            sifre: [
                {id:'sifre_encrypt',title:'ŞİFRE ENCRYPT',icon:'🔒',url:'https://api-nabi.trr.gt.tc/sifre_encrypt?sifre=myPassword123',desc:'Şifre encrypt işlemi.'}
            ],
            pay: [
                {id:'iyzico',title:'IYZICO API',icon:'💳',url:'https://api-nabi.trr.gt.tc/iyzico?cc=KART_NUMARASI&ay=AA&yil=YYYY&cvv=CVV',desc:'Ödeme/giriş örneği (demo).'}
            ]
        };

        // Helper: create card element
        function makeCard(item){
            const card = document.createElement('article');
            card.className = 'api-card';
            card.innerHTML = `
                <div class="api-head">
                    <div class="api-icon">${item.icon}</div>
                    <div style="flex:1">
                        <div class="api-title">${item.title}</div>
                        <div class="api-desc">${item.desc || ''}</div>
                    </div>
                    <div class="badge">Aktif</div>
                </div>
                <div class="api-url" tabindex="0">${item.url}</div>
                <div class="card-actions">
                    <button class="btn copy" data-url="${item.url}" title="Kopyala"><i class="fa fa-copy"></i> Kopyala</button>
                    <button class="btn open" data-url="${item.url}" title="Yeni sekmede aç"><i class="fa fa-arrow-up-right-from-square"></i> Aç</button>
                    <button class="btn" onclick="navigator.clipboard.writeText('${item.id}')" title="ID kopyala">ID</button>
                </div>
            `;
            return card;
        }

        // Render initial lists
        function renderAll(){
            document.getElementById('checkerGrid').innerHTML=''; apiData.checker.forEach(i=>document.getElementById('checkerGrid').appendChild(makeCard(i)));
            document.getElementById('ratoGrid').innerHTML=''; apiData.rato.forEach(i=>document.getElementById('ratoGrid').appendChild(makeCard(i)));
            document.getElementById('sosyalGrid').innerHTML=''; apiData.sosyal.forEach(i=>document.getElementById('sosyalGrid').appendChild(makeCard(i)));
            document.getElementById('aiGrid').innerHTML=''; apiData.ai.forEach(i=>document.getElementById('aiGrid').appendChild(makeCard(i)));
            document.getElementById('tcGrid').innerHTML=''; apiData.tc.forEach(i=>document.getElementById('tcGrid').appendChild(makeCard(i)));
            document.getElementById('adsoyadGrid').innerHTML=''; apiData.adsoyad.forEach(i=>document.getElementById('adsoyadGrid').appendChild(makeCard(i)));
            document.getElementById('isvergiGrid').innerHTML=''; apiData.isvergi.forEach(i=>document.getElementById('isvergiGrid').appendChild(makeCard(i)));
            document.getElementById('tcgsmGrid').innerHTML=''; apiData.tcgsm.forEach(i=>document.getElementById('tcgsmGrid').appendChild(makeCard(i)));
            document.getElementById('adresGrid').innerHTML=''; apiData.adres.forEach(i=>document.getElementById('adresGrid').appendChild(makeCard(i)));
            document.getElementById('aileGrid').innerHTML=''; apiData.aile.forEach(i=>document.getElementById('aileGrid').appendChild(makeCard(i)));
            document.getElementById('egitimGrid').innerHTML=''; apiData.egitim.forEach(i=>document.getElementById('egitimGrid').appendChild(makeCard(i)));
            document.getElementById('networkGrid').innerHTML=''; apiData.network.forEach(i=>document.getElementById('networkGrid').appendChild(makeCard(i)));
            document.getElementById('leakGrid').innerHTML=''; apiData.leak.forEach(i=>document.getElementById('leakGrid').appendChild(makeCard(i)));
            document.getElementById('ibanGrid').innerHTML=''; apiData.iban.forEach(i=>document.getElementById('ibanGrid').appendChild(makeCard(i)));
            document.getElementById('sifreGrid').innerHTML=''; apiData.sifre.forEach(i=>document.getElementById('sifreGrid').appendChild(makeCard(i)));
            document.getElementById('payGrid').innerHTML=''; apiData.pay.forEach(i=>document.getElementById('payGrid').appendChild(makeCard(i)));
            
            // Calculate total APIs
            let total = 0;
            for(const category in apiData) {
                total += apiData[category].length;
            }
            document.getElementById('totalApis').innerText = total;
            document.getElementById('activeApis').innerText = document.querySelectorAll('.api-card .badge').length;
        }
        renderAll();

        // Delegated event listeners for copy/open
        document.addEventListener('click', (e)=>{
            if(e.target.closest('.copy')){
                const btn = e.target.closest('.copy'); const url = btn.dataset.url;
                navigator.clipboard.writeText(url).then(()=>showToast('Endpoint kopyalandı'));
            }
            if(e.target.closest('.open')){
                const btn = e.target.closest('.open'); const url = btn.dataset.url;
                window.open(url,'_blank');
            }
        });

        // Search filter
        document.getElementById('q').addEventListener('input', function(e){
            const q = e.target.value.toLowerCase().trim();
            document.querySelectorAll('.api-card').forEach(card=>{
                const text = card.innerText.toLowerCase();
                card.style.display = text.includes(q) ? '' : 'none';
            });
        });

        // Toggle background blur
        document.getElementById('toggleBg').addEventListener('click', ()=>{
            document.getElementById('bgImage').classList.toggle('blurred');
        });

        // Menu
        const menuDot = document.getElementById('menuDot'); const modal = document.getElementById('menuModal');
        menuDot.addEventListener('click', ()=>{ modal.classList.toggle('show'); modal.setAttribute('aria-hidden', modal.classList.contains('show') ? 'false' : 'true'); });
        document.addEventListener('click', (e)=>{ if(!e.target.closest('.menu-dot') && !e.target.closest('.modal')) modal.classList.remove('show'); });

        // Download JSON
        document.getElementById('downloadJson').addEventListener('click', (e)=>{
            e.preventDefault(); const blob = new Blob([JSON.stringify(apiData, null, 2)], {type:'application/json'}); const url = URL.createObjectURL(blob);
            const a = document.createElement('a'); a.href=url; a.download='api-list.json'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
            showToast('api-list.json indiriliyor...');
        });

        document.getElementById('about').addEventListener('click', (e)=>{ e.preventDefault(); alert('Nabi System — API servisi v2\\nMobile uyumlu, kopyala / aç / indir özellikleri eklendi.\\nToplam 62+ aktif API!'); });

        document.getElementById('openEditor').addEventListener('click', (e)=>{ e.preventDefault(); showToast('Bu buton örnektir — manuel düzenleyin.'); });

        // toast helper
        function showToast(msg){ const t = document.getElementById('toast'); t.innerText = msg; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'),1600); }

        // Mobile touch improvements
        document.addEventListener('touchstart', function(){}, {passive: true});
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Ana sayfa - API listesi"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/list')
def api_list():
    """Tüm API'leri JSON formatında döndür"""
    api_data = {
        "checker": [
            {"id": "instagram_login", "title": "Instagram Login Check", "url": "https://nabi-check.trr.gt.tc/api/instagram/login?username=KULLANICI&password=SIFRE", "desc": "Instagram giriş kontrolü."},
            # Diğer API'ler buraya eklenebilir
        ],
        # Diğer kategoriler...
    }
    return jsonify(api_data)

@app.route('/api/stats')
def api_stats():
    """API istatistiklerini döndür"""
    stats = {
        "total_apis": 62,
        "active_apis": 62,
        "categories": 16,
        "status": "online"
    }
    return jsonify(stats)

@app.route('/api/download')
def download_api_list():
    """API listesini JSON dosyası olarak indir"""
    api_data = {
        "checker": [
            {"id": "instagram_login", "title": "Instagram Login Check", "url": "https://nabi-check.trr.gt.tc/api/instagram/login?username=KULLANICI&password=SIFRE", "desc": "Instagram giriş kontrolü."},
            # Diğer API'ler...
        ],
        # Diğer kategoriler...
    }
    return jsonify(api_data)

@app.route('/health')
def health_check():
    """Sağlık kontrolü endpoint'i"""
    return jsonify({"status": "healthy", "service": "Nabi System API"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
