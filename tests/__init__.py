from asyncio import Future


def setup_future(result=None):
    future = Future()
    future.set_result(result)
    return future
