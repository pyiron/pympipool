from concurrent.futures import Executor as FutureExecutor, Future
from queue import Queue
from threading import Thread

from pympipool.share.serial import execute_tasks, _cloudpickle_update


class Executor(FutureExecutor):
    def __init__(
        self,
        cores,
        oversubscribe=False,
        enable_flux_backend=False,
        init_function=None,
        cwd=None,
    ):
        self._future_queue = Queue()
        self._process = Thread(
            target=execute_tasks,
            args=(self._future_queue, cores, oversubscribe, enable_flux_backend, cwd),
        )
        self._process.start()
        _cloudpickle_update(ind=2)
        if init_function is not None:
            self._future_queue.put({"i": True, "f": init_function, "a": (), "k": {}})

    def submit(self, fn, *args, **kwargs):
        f = Future()
        self._future_queue.put({"f": fn, "a": args, "k": kwargs, "l": f})
        return f

    def shutdown(self, wait=True, *, cancel_futures=False):
        self._future_queue.put({"c": "close"})
        self._process.join()

    def __len__(self):
        return self._future_queue.qsize()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        return False
