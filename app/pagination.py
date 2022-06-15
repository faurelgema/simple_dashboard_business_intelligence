from app.models import response_model

def get_list_pagination(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)

    if count < start or limit < 0:
        return response_model.BadRequest('404', "Something Wrong", [])
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    if start == 1:
        obj['previous'] = ''

    else:
        start_new = max(1, start - limit)
        limit_new =  start - 1
        obj['previous'] = url + "?start=%d" % (start_new, limit_new)
    obj['result'] = results[(start-1):(start-1 + limit)]
    return obj