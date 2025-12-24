from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import socket

# ---------------- КОНФИГУРАЦИЯ ---------------- #
PORT = 25616

class SimpleHandler(BaseHTTPRequestHandler):
    def _serve_html(self, content: str):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_error(self, code, message=None):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(f"Error {code}: {message}".encode("utf-8"))

    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        path = self.path.rstrip("/") or "/"

        # ---------------- СТИЛИ (NEO-BRUTALISM) ---------------- #
        base_styles = """
        <style>
            *, *::before, *::after {
                margin: 0; padding: 0; box-sizing: border-box;
            }
            body {
                font-family: 'Courier New', monospace;
                background: #FFF;
                color: #000;
                line-height: 1.6;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            header {
                border-bottom: 6px solid #000;
                padding: 30px 0;
                margin-bottom: 40px;
                background: #FFE500;
            }
            h1 {
                font-size: 3rem;
                font-weight: 900;
                text-transform: uppercase;
                letter-spacing: 3px;
            }
            nav {
                margin-top: 20px;
            }
            nav a {
                display: inline-block;
                padding: 10px 20px;
                margin-right: 10px;
                background: #FFF;
                border: 4px solid #000;
                text-decoration: none;
                color: #000;
                font-weight: bold;
                text-transform: uppercase;
                box-shadow: 4px 4px 0 #000;
                transition: all 0.1s;
            }
            nav a:hover,
            nav a.active {
                background: #000;
                color: #FFE500;
                transform: translate(2px, 2px);
                box-shadow: 2px 2px 0 #000;
            }
            .hero {
                padding: 60px 40px;
                background: #4ECDC4;
                border: 6px solid #000;
                margin-bottom: 40px;
                box-shadow: 8px 8px 0 #000;
            }
            .hero h2 {
                font-size: 2.5rem;
                margin-bottom: 20px;
            }
            .card {
                background: #FFF;
                border: 5px solid #000;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 6px 6px 0 #000;
            }
            .card h3 {
                font-size: 1.8rem;
                margin-bottom: 15px;
                color: #FF6B6B;
            }
            .btn {
                display: inline-block;
                padding: 15px 30px;
                background: #FFE500;
                border: 4px solid #000;
                color: #000;
                text-decoration: none;
                font-weight: bold;
                text-transform: uppercase;
                box-shadow: 4px 4px 0 #000;
                transition: all 0.1s;
                margin-top: 15px;
            }
            .btn:hover {
                background: #FF6B6B;
                transform: translate(2px, 2px);
                box-shadow: 2px 2px 0 #000;
            }
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-top: 40px;
            }
            footer {
                margin-top: 60px;
                padding: 40px 0;
                border-top: 6px solid #000;
                background: #F0F0F0;
                text-align: center;
            }
            @media (max-width: 768px) {
                h1 { font-size: 2rem; }
                .hero h2 { font-size: 1.8rem; }
                nav a { margin-bottom: 10px; }
            }
        </style>
        """

        def get_nav(active_path):
            links = [
                ("/", "ГЛАВНАЯ"),
                ("/bots", "УСЛУГИ"),
                ("/hosting", "ХОСТИНГ"),
                ("https://t.me/krimexAI", "TELEGRAM"),
            ]
            desk_html = ""
            mob_html = ""
            for href, label in links:
                cls = "active" if href == active_path else ""
                desk_html += f'<a href="{href}" class="{cls}">{label}</a>'
                mob_html += f'<a href="{href}" class="{cls}">{label}</a>'
            return f"""
            <nav class="desktop-nav">{desk_html}</nav>
            <nav class="mobile-nav" style="display:none;">{mob_html}</nav>
            """

        # ---------------- ГЛАВНАЯ ---------------- #
        if path == "/":
            html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>KRIMEX DEVELOPMENT</title>
                {base_styles}
            </head>
            <body>
                <header>
                    <div class="container">
                        <h1>🔥 KRIMEX DEV</h1>
                        {get_nav("/")}
                    </div>
                </header>
                <main class="container">
                    <div class="hero">
                        <h2>Разработка Telegram/Discord ботов, OSINT инструменты и инфраструктура. Без лишних слов, только рабочий код.</h2>
                    </div>

                    <div class="grid">
                        <div class="card">
                            <h3>🤖 KRIMEX AI</h3>
                            <p>Мощный ассистент в Telegram. Пишет код, решает задачи, генерирует контент.</p>
                            <a href="https://t.me/krimexAI" class="btn">ЗАПУСТИТЬ</a>
                        </div>
                        <div class="card">
                            <h3>📊 CRYPTO ANALYST</h3>
                            <p>Анализ трендов и курсов криптовалют в реальном времени.</p>
                            <a href="https://t.me/krimexAI" class="btn">ПОДРОБНЕЕ</a>
                        </div>
                        <div class="card">
                            <h3>🔍 OSINT TOOLS</h3>
                            <p>Поиск и агрегация информации из открытых источников.</p>
                            <a href="https://t.me/krimexAI" class="btn">УЗНАТЬ</a>
                        </div>
                        <div class="card">
                            <h3>🎮 MINECRAFT SERVER</h3>
                            <p>Честный Minecraft сервер без доната и лишних плагинов.</p>
                            <a href="https://t.me/krimexAI" class="btn">ПОДКЛЮЧИТЬСЯ</a>
                        </div>
                    </div>
                </main>
                <footer>
                    <div class="container">
                        <p><strong>KRIMEX DEVELOPMENT</strong> | Связь: <a href="https://t.me/krimexAI">@krimexAI</a></p>
                    </div>
                </footer>
            </body>
            </html>
            """
            self._serve_html(html)

        # ---------------- УСЛУГИ ---------------- #
        elif path == "/bots":
            html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>УСЛУГИ | KRIMEX</title>
                {base_styles}
            </head>
            <body>
                <header>
                    <div class="container">
                        <h1>🔥 KRIMEX DEV</h1>
                        {get_nav("/bots")}
                    </div>
                </header>
                <main class="container">
                    <div class="hero">
                        <h2>НАШИ УСЛУГИ</h2>
                    </div>

                    <div class="card">
                        <h3>🤖 TELEGRAM БОТЫ</h3>
                        <p>Магазины, Web Apps, Платежки, Админки</p>
                        <a href="https://t.me/krimexAI" class="btn">ЗАКАЗАТЬ</a>
                    </div>

                    <div class="card">
                        <h3>🤖 DISCORD БОТЫ</h3>
                        <p>Экономика, Модерация, Игры, Тикеты</p>
                        <a href="https://t.me/krimexAI" class="btn">ЗАКАЗАТЬ</a>
                    </div>

                    <div class="card">
                        <h3>🎨 ДИЗАЙН</h3>
                        <p>Красивые сайты, обложки, сервисы</p>
                        <a href="https://t.me/krimexAI" class="btn">ЗАКАЗАТЬ</a>
                    </div>
                </main>
                <footer>
                    <div class="container">
                        <p><strong>KRIMEX DEVELOPMENT</strong> | Связь: <a href="https://t.me/krimexAI">@krimexAI</a></p>
                    </div>
                </footer>
            </body>
            </html>
            """
            self._serve_html(html)

        # ---------------- ХОСТИНГ ---------------- #
        elif path == "/hosting":
            html = f"""
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>ХОСТИНГ | KRIMEX</title>
                {base_styles}
            </head>
            <body>
                <header>
                    <div class="container">
                        <h1>🔥 KRIMEX DEV</h1>
                        {get_nav("/hosting")}
                    </div>
                </header>
                <main class="container">
                    <div class="hero">
                        <h2>ПАРТНЕРСКИЙ ХОСТИНГ. ЧЕСТНЫЕ РЕСУРСЫ.</h2>
                        <p>Никакого оверселлинга. Только выделенные ядра Ryzen 9 5900X для максимального FPS и скорости работы ботов.</p>
                        <a href="https://t.me/krimexAI" class="btn">ВЫБРАТЬ ТАРИФ</a>
                    </div>
                </main>
                <footer>
                    <div class="container">
                        <p><strong>KRIMEX DEVELOPMENT</strong> | Связь: <a href="https://t.me/krimexAI">@krimexAI</a></p>
                    </div>
                </footer>
            </body>
            </html>
            """
            self._serve_html(html)

        else:
            self.send_error(404, "Page not found")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    server = ThreadingHTTPServer(("", PORT), SimpleHandler)
    local_ip = get_local_ip()
    print(f"🚀 Server started on:")
    print(f"   Local:   http://127.0.0.1:{PORT}")
    print(f"   Network: http://{local_ip}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⚠️  Server stopped")
        server.shutdown()
