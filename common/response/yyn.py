def return_fail(errorcode: int = 1, msg: str = "失败"):
    return {
        'errorcode': errorcode,
        'ret'      : errorcode,
        'msg'      : msg
    }


def return_ok(data):
    return {
        'errorcode': 0,
        'ret'      : 0,
        'msg'      : "ok",
        'traceid'  : '',
        'data'     : data
    }