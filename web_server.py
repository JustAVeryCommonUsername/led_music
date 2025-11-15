import os
import threading
from aiohttp import web

class LEDWebServer:
    def __init__(self, led_interface, host='0.0.0.0', port=5000, static_dir='static'):
        self.led_interface = led_interface
        self.host = host
        self.port = port
        if not os.path.isabs(static_dir):
            static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), static_dir))
        self.static_dir = static_dir
        self.app = web.Application()
        self._setup_routes()

    def _setup_routes(self):
        self.app.router.add_get('/', self.index)
        self.app.router.add_get('/ws', self.ws_handler)
        self.app.router.add_static('/static/', self.static_dir, show_index=False)

    async def index(self, request):
        return web.FileResponse(os.path.join(self.static_dir, 'index.html'))

    async def ws_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == web.WSMsgType.BINARY:
                data = msg.data
                if len(data) >= 3 and self.led_interface:
                    r, g, b = data[0], data[1], data[2]
                    self.led_interface.send_rgb(r, g, b)
            elif msg.type == web.WSMsgType.ERROR:
                print(f'WebSocket error: {ws.exception()}')
        return ws

    def run(self):
        web.run_app(self.app, host=self.host, port=self.port, handle_signals=False)

def start_led_web_server(led_interface, host='0.0.0.0', port=5000, static_dir='static'):
    server = LEDWebServer(led_interface, host=host, port=port, static_dir=static_dir)
    server.run()

def start_server_in_thread(led_interface, host='0.0.0.0', port=5000, static_dir='static'):
    t = threading.Thread(target=start_led_web_server, args=(led_interface, host, port, static_dir), daemon=True)
    t.start()
    return t
