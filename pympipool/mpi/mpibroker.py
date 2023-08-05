from pympipool.shared.executorbase import (
    ExecutorBase,
    executor_broker,
    get_executor_dict,
)
from pympipool.shared.thread import RaisingThread
from pympipool.mpi.mpitask import PyMPISingleTaskExecutor


class PyMPIExecutor(ExecutorBase):
    def __init__(
        self,
        max_workers,
        cores_per_worker=1,
        threads_per_core=1,
        gpus_per_worker=0,
        oversubscribe=False,
        init_function=None,
        cwd=None,
        sleep_interval=0.1,
        enable_slurm_backend=False,
    ):
        super().__init__()
        if not enable_slurm_backend:
            if threads_per_core != 1:
                raise ValueError(
                    "The MPI backend only supports threads_per_core=1, "
                    + "to manage threads use the SLURM queuing system enable_slurm_backend=True ."
                )
            elif gpus_per_worker != 0:
                raise ValueError(
                    "The MPI backend only supports gpus_per_core=0, "
                    + "to manage GPUs use the SLURM queuing system enable_slurm_backend=True ."
                )
        self._process = RaisingThread(
            target=_mpi_executor_broker,
            kwargs={
                "future_queue": self._future_queue,
                "max_workers": max_workers,
                "cores_per_worker": cores_per_worker,
                "threads_per_core": threads_per_core,
                "gpus_per_worker": gpus_per_worker,
                "oversubscribe": oversubscribe,
                "init_function": init_function,
                "cwd": cwd,
                "sleep_interval": sleep_interval,
                "enable_slurm_backend": enable_slurm_backend,
            },
        )
        self._process.start()


def _mpi_executor_broker(
    future_queue,
    max_workers,
    cores_per_worker=1,
    threads_per_core=1,
    gpus_per_worker=0,
    oversubscribe=False,
    init_function=None,
    cwd=None,
    sleep_interval=0.1,
    enable_slurm_backend=False,
):
    executor_broker(
        future_queue=future_queue,
        meta_future_lst=get_executor_dict(
            max_workers=max_workers,
            executor_class=PyMPISingleTaskExecutor,
            cores=cores_per_worker,
            threads_per_core=threads_per_core,
            gpus_per_task=int(gpus_per_worker / cores_per_worker),
            oversubscribe=oversubscribe,
            init_function=init_function,
            cwd=cwd,
            enable_slurm_backend=enable_slurm_backend,
        ),
        sleep_interval=sleep_interval,
    )