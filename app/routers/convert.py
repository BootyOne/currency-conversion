from aiohttp import web


async def convert_handler(request):
    params = request.rel_url.query
    from_currency = params.get('from')
    to_currency = params.get('to')
    try:
        amount = float(params.get('amount', 0))
    except ValueError:
        response_data = {
            'success': 0,
            'error': 'Invalid amount, should be a number'
        }
        return web.json_response(response_data, status=400)

    if from_currency is None or to_currency is None:
        response_data = {
            'success': 0,
            'error': 'You did not specify currencies'
        }
        return web.json_response(response_data, status=400)

    redis_conn = request.app['redis_conn']
    from_rate = redis_conn.get(from_currency)
    to_rate = redis_conn.get(to_currency)

    if from_rate is None or to_rate is None:
        response_data = {
            'success': 0,
            'error': 'Invalid currency'
        }
        return web.json_response(response_data, status=400)

    from_rate = float(from_rate.decode())
    to_rate = float(to_rate.decode())

    result = amount * to_rate / from_rate

    response_data = {
        'success': 1,
        'data': {
            'from': from_currency,
            'to': to_currency,
            'amount': amount,
            'result': result
        }
    }

    return web.json_response(response_data)
