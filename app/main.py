from aiohttp import web
import redis

from app.routers.convert import convert_handler
from app.routers.merge import database_handler


async def on_startup(app):
    app['redis_conn'] = redis.Redis(host='127.0.0.1', port=6379, db=0)


app = web.Application()
app.on_startup.append(on_startup)
app.add_routes([
    web.get('/convert', convert_handler),
    web.post('/database', database_handler),
])


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)
