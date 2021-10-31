#!/usr/bin/python3
import aiohttp_cors
import os

import aiohttp
import concurrent.futures
import asyncio

class EyesWebServer():

    def __init__(self):
        self.app_path="/opt/eyes"
        self.web_path="/opt/eyes/web/eyes"
        self.web_address="home.dayton.tech"
        self.web_port=8080
        self.sse_enabled = False
        self.loop = asyncio.get_event_loop()

    def start(self, beta=False):
        try:
            self.web_server = aiohttp.web.Application()
            self.web_server.router.add_get('/', self.root_handler)
            self.web_server.router.add_static('/eyes', path=self.web_path, append_version=True)

            if self.sse_enabled:
                self.web_server.router.add_get('/sse', self.sse_handler)

            self.cors = aiohttp_cors.setup(self.web_server, defaults={
                "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_methods='*', allow_headers="*") })
            for route in self.web_server.router.routes():
                self.cors.add(route)

            self.loop.run_until_complete(self.start_web_server())
            self.loop.run_forever()
            #else:
            #    self.error_state=True
        except KeyboardInterrupt:  # pragma: no cover
            pass
        except:
            logger.error('Loop terminated', exc_info=True)
        finally:
            self.server.shutdown()

    async def start_web_server(self):
        self.runner = aiohttp.web.AppRunner(self.web_server)
        await self.runner.setup()
        self.ssl_context = None
        self.site = aiohttp.web.TCPSite(self.runner, self.web_address, self.web_port, ssl_context=self.ssl_context)            
        await self.site.start()


    async def root_handler(self, request):
        return aiohttp.web.FileResponse('/opt/eyes/web/eyes/index.html')

    async def sse_handler(self, request):
        pass

if __name__ == '__main__':
    eyes = EyesWebServer()
    eyes.start()
        
 
