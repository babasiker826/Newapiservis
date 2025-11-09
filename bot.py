# app.py
from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Güvenlik ayarları
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Yeni HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Bu İnternet Adresi Erişime Kapatılmıştır</title>
<style>
  @font-face { font-family:"Nexa"; src:url("./Nexa-ExtraLight.ttf") format("truetype"); }
  @font-face { font-family:"Nexa"; src:url("./Nexa-Heavy.ttf") format("truetype"); font-weight:bold; }

  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:100%;height:100%;}
  body{
    background-image:url("./Background.jpg");
    background-size:cover;
    display:flex;align-items:center;justify-content:center;
    font-family:"Nexa"; color:#fff;
  }

  main{ width:1200px; max-width:100%; padding:2vw; }
  main>h1{
    text-align:center;
    margin-bottom:clamp(16px,1.8vw,28px);
    font-size:clamp(22px,1.9vw,34px);
  }
  main>p{
    text-align:justify;
    font-size:clamp(15px,1.35vw,23px);
    line-height:1.55;
  }
  main>p:nth-child(2){ margin-bottom:clamp(16px,1.8vw,28px); }

  .logos{
    display:flex; flex-wrap:nowrap;
    justify-content:space-between; align-items:center;
    margin-top:clamp(24px,6vw,64px);
    gap:0;
  }
  .logos>img{ height:auto; display:block; object-fit:contain; }

  .logo-mit   { width:190px; height:auto; }
  .logo-jgk   { width:160px; height:auto; }
  .logo-usom  { width:240px; height:auto; }
  .logo-masak { width:140px; height:auto; }

  @media (max-width: 640px){
    main{ padding: 6vw; }
    main>h1{ font-size: clamp(20px,6vw,30px); margin-bottom: 5vw; }
    main>p{ font-size: clamp(14px,3.4vw,20px); line-height: 1.6; }
    main>p:nth-child(2){ margin-bottom: 5vw; }

    .logos{ margin-top: 6vw; gap: 4vw; justify-content: space-between; }
    .logo-mit   { max-height: 65px; width:auto; }
    .logo-jgk   { max-height: 57px; width:auto; }
    .logo-usom  { max-height: 57px; width:auto; }
    .logo-masak { max-height: 55px; width:auto; }
  }

  @media (min-width: 2000px){
    main{ max-width: 1600px; }
    .logos{ gap:0; }
  }
</style>
</head>
<body>
  <main>
    <h1>BU İNTERNET ADRESİ ERİŞİME KAPATILMIŞTIR</h1>

    <p>Bu internet adresi, Türkiye Cumhuriyeti'nin ulusal güvenliğine yönelik yasa dışı siber faaliyetlerde bulunması nedeniyle, Milli İstihbarat Teşkilatı (MİT), Jandarma Genel Komutanlığı (JGK), Ulusal Siber Olaylara Müdahale Merkezi (USOM) ve Mali Suçları Araştırma Kurulu (MASAK) tarafından yürütülen koordineli operasyonlar neticesinde ele geçirilmiş ve erişime kapatılmıştır.</p>

    <p>Yasa dışı faaliyetlerde bulunan siber teröristlere karşı önleyici ve caydırıcı tedbirler kararlılıkla sürdürülecektir.</p>

    <section class="logos">
      <img class="logo-mit"   src="./MİT.png"   alt="Milli İstihbarat Teşkilatı">
      <img class="logo-jgk"   src="./JGK.png"   alt="Jandarma Genel Komutanlığı">
      <img class="logo-usom"  src="./USOM.png"  alt="Ulusal Siber Olaylara Müdahale Merkezi">
      <img class="logo-masak" src="./MASAK.png" alt="Mali Suçları Araştırma Kurulu">
    </section>
  </main>
</body>
</html>"""

# Security headers middleware
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template_string(HTML_TEMPLATE), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template_string(HTML_TEMPLATE), 500

# Routes - tüm route'lar aynı sayfayı göstersin
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/<path:any_path>")
def catch_all(any_path):
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
