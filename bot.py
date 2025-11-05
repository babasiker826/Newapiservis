# app.py
from flask import Flask, render_template_string, Response
import os
import json

app = Flask(__name__)

# TÜM API VERİLERİ - 62 API
# NOT: Tümü doğru domain ile ayarlandı. (Sorgulama/TC/AdSoyad/IBAN vs -> api2-nabi.trr.gt.tc)
ALL_APIS = [
    # Checker API'leri (8)
    {"id": "instagram_login", "title": "Instagram Login Check", "icon": "📷",
     "url": "https://nabi-check.trr.gt.tc/api/instagram/login?username=KULLANICI&password=SIFRE", "desc": "Instagram giriş kontrolü."},
    {"id": "tiktok_reset", "title": "TikTok Reset Check", "icon": "🎵",
     "url": "https://nabi-check.trr.gt.tc/api/tiktok/reset?email=email@gmail.com", "desc": "TikTok reset kontrolü."},
    {"id": "cramly_check", "title": "Cramly Check", "icon": "📚",
     "url": "https://nabi-check.trr.gt.tc/api/cramly/check?email=email@mail.com&password=sifre", "desc": "Cramly hesap kontrolü."},
    {"id": "tgoyemek_check", "title": "Tgoyemek Check", "icon": "🍔",
     "url": "https://nabi-check.trr.gt.tc/api/tgoyemek/check?username=kullanici&password=sifre", "desc": "Tgoyemek hesap kontrolü."},
    {"id": "oyundinar_check", "title": "OyunDinar Check", "icon": "🎮",
     "url": "https://nabi-check.trr.gt.tc/api/oyundinar/check?email=email@mail.com&password=sifre", "desc": "OyunDinar hesap kontrolü."},
    {"id": "mullvad_check", "title": "Mullvad Check", "icon": "🔒",
     "url": "https://nabi-check.trr.gt.tc/api/mullvad/check?username=kullanici&password=sifre", "desc": "Mullvad VPN kontrolü."},
    {"id": "supercell_check", "title": "Supercell Check", "icon": "📱",
     "url": "https://nabi-check.trr.gt.tc/api/supercell/check?email=email@mail.com&password=sifre", "desc": "Supercell hesap kontrolü."},
    {"id": "checker_stats", "title": "Checker İstatistikler", "icon": "📊",
     "url": "https://nabi-check.trr.gt.tc/api/stats", "desc": "Checker API istatistikleri."},

    # Rato API'leri (3)
    {"id": "rato_check_domain", "title": "Rato Domain Kontrol", "icon": "🔍",
     "url": "https://ratoekes.onrender.com/api/check_domain/test-domain", "desc": "Domain kayıt kontrolü."},
    {"id": "rato_register", "title": "Rato Kayıt İşlemi", "icon": "📝",
     "url": "curl -X POST \"https://ratoekes.onrender.com/api/register\" -H \"Content-Type: application/json\" -d '{\"domain\": \"test-domain\", \"client_id\": \"test-client\", \"info\": {\"os\": \"Windows\"}}'",
     "desc": "Yeni istemci kaydı."},
    {"id": "rato_check_commands", "title": "Rato Komut Kontrol", "icon": "⚡",
     "url": "https://ratoekes.onrender.com/api/check_commands/test-domain/test-client", "desc": "Komut sorgulama."},

    # Sosyal Medya API'leri (13)
    {"id": "instagram_likes", "title": "Instagram Beğeni (75)", "icon": "❤️",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_likes&link=https://instagram.com/p/CXXXXXXXXXX/", "desc": "Instagram beğeni gönderimi."},
    {"id": "tiktok_likes", "title": "TikTok Beğeni (30)", "icon": "👍",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=tiktok_likes&link=https://tiktok.com/@user/video/7XXXXXXXXXXXXXXX/", "desc": "TikTok beğeni gönderimi."},
    {"id": "instagram_followers", "title": "Instagram Takipçi (10)", "icon": "👥",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_followers&link=https://instagram.com/takipedilecek_username/", "desc": "Instagram takipçi gönderimi."},
    {"id": "instagram_views", "title": "Instagram Görüntüleme (2500)", "icon": "👀",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_views&link=https://instagram.com/p/CXXXXXXXXXX/", "desc": "Instagram görüntüleme gönderimi."},
    {"id": "instagram_saves", "title": "Instagram Kaydetme (150)", "icon": "💾",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_saves&link=https://instagram.com/p/CXXXXXXXXXX/", "desc": "Instagram kaydetme gönderimi."},
    {"id": "instagram_shares", "title": "Instagram Paylaşım (300)", "icon": "🔄",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_shares&link=https://instagram.com/p/CXXXXXXXXXX/", "desc": "Instagram paylaşım gönderimi."},
    {"id": "instagram_story_views", "title": "Instagram Story Görüntüleme", "icon": "📱",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=instagram_story_views&link=https://instagram.com/stories/username/XXXXXXXXXX/", "desc": "Instagram story görüntüleme."},
    {"id": "tiktok_views", "title": "TikTok Görüntüleme (400)", "icon": "🎬",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=tiktok_views&link=https://tiktok.com/@user/video/7XXXXXXXXXXXXXXX/", "desc": "TikTok görüntüleme gönderimi."},
    {"id": "tiktok_followers", "title": "TikTok Takipçi (20)", "icon": "👥",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=tiktok_followers&link=https://tiktok.com/@takipedilecek_user/", "desc": "TikTok takipçi gönderimi."},
    {"id": "youtube_likes", "title": "YouTube Beğeni", "icon": "▶️",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=youtube_likes&link=https://youtube.com/watch?v=XXXXXXXXXXX", "desc": "YouTube beğeni gönderimi."},
    {"id": "spotify_saves", "title": "Spotify Kaydetme", "icon": "🎵",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/send?service=spotify_saves&link=https://open.spotify.com/track/XXXXXXXXX", "desc": "Spotify kaydetme gönderimi."},
    {"id": "services_list", "title": "Servis Listesi", "icon": "📋",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/services", "desc": "Tüm servislerin listesi."},
    {"id": "api_status", "title": "API Durumu", "icon": "🟢",
     "url": "https://api-nabi-sosyalmedya.trr.gt.tc/api/status", "desc": "API durum kontrolü."},

    # AI API'leri (5)
    {"id": "gpt5mini", "title": "CHAT GPT 5 MINI MODEL", "icon": "🤖",
     "url": "https://ai.nabi.22web.org/gpt5model?message=merhaba", "desc": "Genel sohbet modeli."},
    {"id": "gpt4mini", "title": "CHAT GPT 4 MODEL", "icon": "🧠",
     "url": "https://ai.nabi.22web.org/gpt4mini?message=merhaba", "desc": "GPT-4 benzeri model."},
    {"id": "deepseek", "title": "DEEPSEEK MODEL", "icon": "🔍",
     "url": "https://ai.nabi.22web.org/deepseek?message=merhaba", "desc": "Arama/analiz odaklı."},
    {"id": "gemini", "title": "GEMINI 1.5 PRO MODEL", "icon": "💎",
     "url": "https://ai.nabi.22web.org/gemini1.5pro?message=merhaba", "desc": "Google Gemini benzeri."},
    {"id": "unknown", "title": "BİLİNMEYEN MODEL", "icon": "❓",
     "url": "https://ai.nabi.22web.org/chat?message=merhaba", "desc": "Belirsiz model."},

    # TC Sorgulama API'leri (hepsi api2-nabi.trr.gt.tc)
    {"id": "tc", "title": "TC SORGULAMA", "icon": "🆔",
     "url": "https://api2-nabi.trr.gt.tc/tc?tc=12345678901", "desc": "TC kimlik no sorgulama."},
    {"id": "tc_pro", "title": "TC PRO SORGULAMA", "icon": "🔍",
     "url": "https://api2-nabi.trr.gt.tc/tcpro?tc=12345678901", "desc": "Detaylı TC sorgulama."},
    {"id": "aile", "title": "AILE SORGULAMA", "icon": "👨‍👩‍👧‍👦",
     "url": "https://api2-nabi.trr.gt.tc/aile?tc=12345678901", "desc": "Aile bireylerini sorgulama."},
    {"id": "aile_pro", "title": "AILE PRO SORGULAMA", "icon": "🏠",
     "url": "https://api2-nabi.trr.gt.tc/ailepro?tc=12345678901", "desc": "Detaylı aile sorgulama."},
    {"id": "sulale", "title": "SÜLALE SORGULAMA", "icon": "🌳",
     "url": "https://api2-nabi.trr.gt.tc/sulale?tc=12345678901", "desc": "Sülale/soy ağacı sorgulama."},
    {"id": "hayat_hikayesi", "title": "HAYAT HİKAYESİ", "icon": "📖",
     "url": "https://api2-nabi.trr.gt.tc/hayathikayesi?tc=12345678901", "desc": "Kişisel hayat hikayesi."},

    # Ad Soyad Sorgulama (api2-nabi.trr.gt.tc)
    {"id": "adsoyad", "title": "AD SOYAD SORGULAMA", "icon": "👤",
     "url": "https://api2-nabi.trr.gt.tc/adsoyad?ad=ali&soyad=yilmaz", "desc": "Ad soyad ile sorgulama."},
    {"id": "ad_soyad", "title": "AD SOYAD SORGULAMA 2", "icon": "🔎",
     "url": "https://api2-nabi.trr.gt.tc/adsoyad?ad=mehmet&soyad=demir", "desc": "Alternatif ad soyad sorgu."},
    {"id": "ad_soyad_pro", "title": "AD SOYAD PRO", "icon": "💼",
     "url": "https://api2-nabi.trr.gt.tc/adsoyadpro?ad=ahmet&soyad=kaya", "desc": "Profesyonel ad soyad sorgu."},
    {"id": "adi_il_ilce", "title": "AD İL İLÇE SORGULAMA", "icon": "📍",
     "url": "https://api2-nabi.trr.gt.tc/adiililce?ad=ayse&il=istanbul&ilce=kadikoy", "desc": "Ad, il ve ilçe ile sorgu."},

    # İş ve Vergi Sorgulama (api2-nabi.trr.gt.tc)
    {"id": "is_yeri", "title": "İŞ YERİ SORGULAMA", "icon": "🏢",
     "url": "https://api2-nabi.trr.gt.tc/isyeri?vergino=1234567890", "desc": "Vergi no ile iş yeri sorgu."},
    {"id": "vergi_no", "title": "VERGİ NO SORGULAMA", "icon": "💰",
     "url": "https://api2-nabi.trr.gt.tc/vergino?vergino=1234567890", "desc": "Vergi numarası sorgulama."},
    {"id": "yas", "title": "YAŞ SORGULAMA", "icon": "🎂",
     "url": "https://api2-nabi.trr.gt.tc/yas?yas=25", "desc": "Yaş bazlı sorgulama."},

    # TC-GSM Sorgulama (api2-nabi.trr.gt.tc)
    {"id": "tc_gsm", "title": "TC GSM SORGULAMA", "icon": "📱",
     "url": "https://api2-nabi.trr.gt.tc/tcgsm?tc=12345678901", "desc": "TC den GSM sorgulama."},
    {"id": "gsm_tc", "title": "GSM TC SORGULAMA", "icon": "📞",
     "url": "https://api2-nabi.trr.gt.tc/gsmtc?gsm=5551234567", "desc": "GSM den TC sorgulama."},

    # Adres ve Konum Sorgulama (api2-nabi.trr.gt.tc)
    {"id": "adres", "title": "ADRES SORGULAMA", "icon": "🏠",
     "url": "https://api2-nabi.trr.gt.tc/adres?tc=12345678901", "desc": "TC ile adres sorgulama."},
    {"id": "hane", "title": "HANE SORGULAMA", "icon": "👨‍👩‍👧‍👦",
     "url": "https://api2-nabi.trr.gt.tc/hane?tc=12345678901", "desc": "Hane bilgisi sorgulama."},
    {"id": "apartman", "title": "APARTMAN SORGULAMA", "icon": "🏢",
     "url": "https://api2-nabi.trr.gt.tc/apartman?apartman=abc123", "desc": "Apartman bilgisi sorgu."},
    {"id": "ada_parsel", "title": "ADA PARSEL SORGULAMA", "icon": "🗺️",
     "url": "https://api2-nabi.trr.gt.tc/adaparsel?ada=1&parsel=25", "desc": "Ada ve parsel sorgulama."},

    # Eş ve Aile Sorgulama (api2-nabi.trr.gt.tc)
    {"id": "es", "title": "EŞ SORGULAMA", "icon": "💑",
     "url": "https://api2-nabi.trr.gt.tc/es?tc=12345678901", "desc": "Eş bilgisi sorgulama."},

    # Eğitim Sorgulama (api2-nabi.trr.gt.tc)
    {"id": "lgs", "title": "LGS SORGULAMA", "icon": "🎓",
     "url": "https://api2-nabi.trr.gt.tc/lgs?tc=12345678901", "desc": "LGS sonuçları sorgulama."},
    {"id": "e_kurs", "title": "E-KURS SORGULAMA", "icon": "📚",
     "url": "https://api2-nabi.trr.gt.tc/ekurs?tc=12345678901", "desc": "E-kurs bilgileri sorgu."},

    # Network Sorgulama (api2-nabi.trr.gt.tc)
    {"id": "ip", "title": "IP SORGULAMA", "icon": "🌐",
     "url": "https://api2-nabi.trr.gt.tc/ip?ip=192.168.1.1", "desc": "IP adresi sorgulama."},
    {"id": "dns", "title": "DNS SORGULAMA", "icon": "🔗",
     "url": "https://api2-nabi.trr.gt.tc/dns?domain=example.com", "desc": "DNS kayıtları sorgulama."},
    {"id": "whois", "title": "WHOIS SORGULAMA", "icon": "🔍",
     "url": "https://api2-nabi.trr.gt.tc/whois?domain=example.com", "desc": "Domain whois sorgulama."},
    {"id": "subdomain", "title": "SUBDOMAIN SORGULAMA", "icon": "🔎",
     "url": "https://api2-nabi.trr.gt.tc/subdomain?domain=example.com", "desc": "Subdomain bulma."},

    # Leak ve Telegram (api2-nabi.trr.gt.tc)
    {"id": "leak", "title": "LEAK SORGULAMA", "icon": "🔓",
     "url": "https://api2-nabi.trr.gt.tc/leak?email=ornek@gmail.com", "desc": "Email leak kontrolü."},
    {"id": "telegram", "title": "TELEGRAM SORGULAMA", "icon": "📱",
     "url": "https://api2-nabi.trr.gt.tc/telegram?username=ornekkullanici", "desc": "Telegram kullanıcı sorgu."},

    # IBAN API'leri (api2-nabi.trr.gt.tc - düzeltilmiş)
    {"id": "iban_verify", "title": "IBAN DOĞRULAMA", "icon": "✅",
     "url": "https://api-nabi.trr.gt.tc/ibanverify?iban=TR330006100519786457841326", "desc": "IBAN doğrulama endpointi."},
    {"id": "iban_query", "title": "IBAN SORGULAMA", "icon": "🔎",
     "url": "https://api-nabi.trr.gt.tc/ibanquery?iban=TR330006100519786457841326", "desc": "IBAN ile banka bilgisi."},

    # Şifre Encrypt (api2-nabi.trr.gt.tc)
    {"id": "sifre_encrypt", "title": "ŞİFRE ENCRYPT", "icon": "🔒",
     "url": "https://api2-nabi.trr.gt.tc/sifreencrypt?sifre=mypassword123", "desc": "Şifre encrypt işlemi."},

    # Ödeme API'leri (örnek)
    {"id": "iyzico", "title": "IYZICO API", "icon": "💳",
     "url": "https://api-nabi.trr.gt.tc/iyzico?cc=1234567890123456&ay=12&yil=2025&cvv=123", "desc": "Ödeme/giriş örneği (demo)."}
]

# HTML template (arka plan, çalışma butonları, JSON indir)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nabi System API Servisi — v2</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root{--bg-1:#0f1724;--bg-2:#0b1220;--accent-1:#4cc9f0;--accent-2:#ff8a00;--glass:rgba(255,255,255,0.06);--card-border:rgba(255,255,255,0.06);--muted:#cbd5e1;--glass-blur:10px;--radius:14px}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:Inter,system-ui,Arial;background:radial-gradient(1200px 600px at 10% 10%, rgba(76,201,240,0.06), transparent), linear-gradient(135deg,var(--bg-1) 0%,var(--bg-2) 100%);color:#fff;min-height:100vh;padding:16px;position:relative}
.bg-image{position:fixed;inset:0;background-image:url('https://i.ibb.co/wNDn84h0/file-00000000ffc061f4bacedf89d0e6a130.png');background-size:cover;background-position:center;opacity:0.55;z-index:-3;filter:grayscale(10%);transition:filter .35s ease, opacity .35s ease}
.bg-image.blurred{filter:blur(6px) saturate(0.75);opacity:0.46}
.gradient-overlay{position:fixed;inset:0;z-index:-2;background:linear-gradient(90deg, rgba(255,140,0,0.06), rgba(76,201,240,0.04));mix-blend-mode:overlay;pointer-events:none}
.wrapper{max-width:1200px;margin:0 auto}
.header-top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.controls{display:flex;gap:10px;align-items:center}
.search{display:flex;align-items:center;background:var(--glass);padding:8px 12px;border-radius:12px;border:1px solid var(--card-border);gap:8px;flex:1;min-width:200px;max-width:400px}
.search input{background:transparent;border:0;outline:0;color:inherit;font-size:14px;width:100%}
.api-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:12px}
.api-card{background:var(--glass);padding:14px;border-radius:var(--radius);border:1px solid var(--card-border);backdrop-filter:blur(var(--glass-blur));display:flex;flex-direction:column;gap:10px}
.api-head{display:flex;align-items:flex-start;gap:10px}
.api-icon{width:42px;height:42px;border-radius:8px;display:grid;place-items:center;font-size:18px;background:linear-gradient(135deg,#4361ee,#3a0ca3)}
.api-title{font-weight:700;color:#ff6aa2;font-size:14px;cursor:pointer}
.api-desc{font-size:12px;color:var(--muted)}
.api-url{background:rgba(0,0,0,0.3);padding:8px 10px;border-radius:8px;font-family:monospace;font-size:11px;color:var(--accent-1);word-break:break-all;border:1px solid rgba(255,255,255,0.04);cursor:pointer}
.card-actions{display:flex;gap:6px;flex-wrap:wrap}
.btn{padding:6px 8px;border-radius:8px;border:1px solid var(--card-border);background:transparent;color:#fff;cursor:pointer}
.badge{padding:4px 8px;border-radius:999px;background:rgba(40,167,69,0.18);color:#b7f0c1;font-weight:700;font-size:11px}
.toast{position:fixed;right:12px;bottom:12px;background:#0b1220;padding:8px 12px;border-radius:8px;border:1px solid var(--card-border);display:none;z-index:50;font-size:13px}
@media (max-width:768px){.api-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="bg-image" id="bgImage"></div>
<div class="gradient-overlay"></div>
<div class="wrapper">
  <header>
    <div class="header-top">
      <div>
        <h1>Nabi System</h1>
        <div style="color:var(--muted);font-size:13px">API Service • Mobile Uyumlu</div>
      </div>
      <div class="controls">
        <div style="margin-right:8px"><strong>{{ total }}</strong> API</div>
      </div>
    </div>

    <div style="display:flex;gap:8px;margin-top:10px;align-items:center">
      <div class="search"><i class="fa fa-search" style="opacity:0.7;margin-right:8px"></i><input id="q" placeholder="API ara..." onkeyup="searchApis()" /></div>
      <button class="btn" onclick="toggleBackground()">BG</button>
      <button class="btn" onclick="downloadAll()"><i class="fa fa-download"></i> Tüm API'leri JSON indir</button>
    </div>
  </header>

  <main>
    <div style="background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));padding:10px;border-radius:10px;border:1px solid rgba(255,255,255,0.04);color:var(--muted);margin-bottom:12px">
      <i class="fa fa-exclamation-triangle" style="color:#ffb4b4;margin-right:8px"></i>
      Apiler bize aittir. Lütfen verileri paylaşırken gizlilik ve yasalara dikkat ediniz.
    </div>

    <h2 style="color:var(--accent-1);margin-bottom:8px">🚀 TÜM API LİSTESİ ({{ total }} API)</h2>

    <div class="api-grid" id="allApisGrid">
      {% for api in apis %}
      <div class="api-card" data-text="{{ (api.id ~ ' ' ~ api.title ~ ' ' ~ api.desc ~ ' ' ~ api.url)|lower|e }}" data-url="{{ api.url|e }}">
        <div class="api-head">
          <div class="api-icon">{{ api.icon }}</div>
          <div style="flex:1">
            <div class="api-title" onclick="copyToClipboard(this.closest('.api-card').dataset.url)">{{ api.title }}</div>
            <div class="api-desc">{{ api.desc }}</div>
          </div>
          <div style="display:flex;align-items:center;gap:8px"><div class="badge">Aktif</div></div>
        </div>

        <div class="api-url" onclick="copyToClipboard(this.closest('.api-card').dataset.url)">{{ api.url }}</div>

        <div class="card-actions">
          <button class="btn" onclick="copyToClipboard(this.closest('.api-card').dataset.url)"><i class="fa fa-copy"></i> Kopyala</button>
          <button class="btn" onclick="openUrl(this.closest('.api-card').dataset.url)"><i class="fa fa-arrow-up-right-from-square"></i> Aç</button>
        </div>
      </div>
      {% endfor %}
    </div>
  </main>

  <footer style="margin-top:20px;text-align:center;color:var(--muted);font-size:12px">
    NABI SYSTEM SUNAR — v2 • {{ total }} API • Mobile Uyumlu<br>© 2025 Nabi System • Telegram: @sukazatkinis
  </footer>
</div>

<div class="toast" id="toast">Kopyalandı!</div>

<script>
function searchApis(){
  const q=document.getElementById('q').value.toLowerCase();
  document.querySelectorAll('[data-text]').forEach(el=>el.style.display = el.dataset.text.includes(q) ? '' : 'none');
}
async function copyToClipboard(text){
  if(!text) return showToast('Kopyalanacak metin yok');
  try{
    if(navigator.clipboard && navigator.clipboard.writeText){ await navigator.clipboard.writeText(text); }
    else { const ta=document.createElement('textarea'); ta.value=text; ta.style.position='fixed'; ta.style.left='-9999px'; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta); }
    showToast('URL kopyalandı!');
  }catch(e){ console.error(e); showToast('Kopyalama başarısız'); }
}
function openUrl(url){
  if(!url) return showToast('Açılacak adres yok');
  if(url.trim().toLowerCase().startsWith('curl ')){
    const filename='command.txt'; const blob=new Blob([url],{type:'text/plain;charset=utf-8'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=filename; document.body.appendChild(a); a.click(); URL.revokeObjectURL(a.href); a.remove(); showToast('Komut indiriliyor...'); return;
  }
  try{ window.open(url,'_blank'); }catch(e){
    const a=document.createElement('a'); a.href='data:text/plain;charset=utf-8,'+encodeURIComponent(url); a.target='_blank'; document.body.appendChild(a); a.click(); a.remove();
  }
}
async function downloadAll(){
  try{
    const resp=await fetch('/api-list'); if(!resp.ok) throw new Error('İndirilemedi');
    const blob=await resp.blob(); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='apis.json'; document.body.appendChild(a); a.click(); URL.revokeObjectURL(a.href); a.remove();
    showToast('apis.json indiriliyor...');
  }catch(e){ console.error(e); showToast('İndirme başarısız'); }
}
function toggleBackground(){ document.getElementById('bgImage').classList.toggle('blurred'); }
function showToast(msg){ const t=document.getElementById('toast'); t.innerText=msg; t.style.display='block'; clearTimeout(window._toastTimer); window._toastTimer=setTimeout(()=>{ t.style.display='none'; },1500); }
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, apis=ALL_APIS, total=len(ALL_APIS))

@app.route("/api-list")
def api_list():
    return Response(json.dumps({"total": len(ALL_APIS), "apis": ALL_APIS}, ensure_ascii=False, indent=2),
                    content_type="application/json; charset=utf-8")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # production: use gunicorn/nginx; geliştirme için debug True
    app.run(host="0.0.0.0", port=port, debug=True)
