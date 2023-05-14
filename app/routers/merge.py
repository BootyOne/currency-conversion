import json
from aiohttp import web


async def database_handler(request):
    params = request.rel_url.query
    merge = params.get('merge')

    if merge == 0:
        redis_conn = request.app['redis_conn']
        redis_conn.flushall()
        response_data = {
            'success': 1,
            'data': 'Data was handicapped'
        }
        return web.json_response(response_data, status=400)

    try:
        data = await request.json()
    except json.decoder.JSONDecodeError:
        response_data = {
            'success': 0,
            'error': 'Invalid JSON data'
        }
        return web.json_response(response_data, status=400)

    redis_conn = request.app['redis_conn']
    with redis_conn.pipeline() as pipe:
        for currency, rate in data.items():
            pipe.set(currency, rate)
        pipe.execute()

    response_data = {
        'success': 1,
        'data': 'Data stored successfully'
    }
    return web.json_response(response_data, status=200)
