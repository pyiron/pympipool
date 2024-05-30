import inspect
from typing import List, Optional
from concurrent.futures import Executor


def check_oversubscribe(oversubscribe: bool):
    if oversubscribe:
        raise ValueError(
            "Oversubscribing is not supported for the pympipool.flux.PyFLuxExecutor backend."
            "Please use oversubscribe=False instead of oversubscribe=True."
        )


def check_command_line_argument_lst(command_line_argument_lst: List[str]):
    if len(command_line_argument_lst) > 0:
        raise ValueError(
            "The command_line_argument_lst parameter is not supported for the SLURM backend."
        )


def check_gpus_per_worker(gpus_per_worker: int):
    if gpus_per_worker != 0:
        raise TypeError(
            "GPU assignment is not supported for the pympipool.mpi.PyMPIExecutor backend."
            "Please use gpus_per_worker=0 instead of gpus_per_worker="
            + str(gpus_per_worker)
            + "."
        )


def check_threads_per_core(threads_per_core: int):
    if threads_per_core != 1:
        raise TypeError(
            "Thread based parallelism is not supported for the pympipool.mpi.PyMPIExecutor backend."
            "Please use threads_per_core=1 instead of threads_per_core="
            + str(threads_per_core)
            + "."
        )


def check_executor(executor: Executor):
    if executor is not None:
        raise ValueError(
            "The executor parameter is only supported for the flux framework backend."
        )


def check_resource_dict(function: callable):
    if "resource_dict" in inspect.signature(function).parameters.keys():
        raise ValueError(
            "The parameter resource_dict is used internally in pympipool, "
            "so it cannot be used as parameter in the submitted functions."
        )


def check_resource_dict_is_empty(resource_dict: dict):
    if len(resource_dict) > 0:
        raise ValueError(
            "When block_allocation is enabled, the resource requirements have to be defined on the executor level."
        )


def check_refresh_rate(refresh_rate: float):
    if refresh_rate != 0.01:
        raise ValueError(
            "The sleep_interval parameter is only used when disable_dependencies=False."
        )


def validate_backend(
    backend: str, flux_installed: bool = False, slurm_installed: bool = False
) -> str:
    if backend not in ["auto", "mpi", "slurm", "flux"]:
        raise ValueError(
            'The currently implemented backends are ["flux", "mpi", "slurm"]. '
            'Alternatively, you can select "auto", the default option, to automatically determine the backend. But '
            + backend
            + " is not a valid choice."
        )
    elif backend == "flux" and not flux_installed:
        raise ImportError("'import flux.job' failed.")
    elif backend == "slurm" and not slurm_installed:
        raise RuntimeError("SLURM command not found.")
    elif backend == "flux" or (backend == "auto" and flux_installed):
        return "flux"
    elif backend == "slurm" or (backend == "auto" and slurm_installed):
        return "slurm"
    else:
        return "mpi"


def check_pmi(backend: str, pmi: Optional[str]):
    if backend != "flux" and pmi is not None:
        raise ValueError("The pmi parameter is currently only implemented for flux.")
    elif backend == "flux" and pmi not in ["pmix", "pmi1", "pmi2", None]:
        raise ValueError(
            "The pmi parameter supports [pmix, pmi1, pmi2], but not: " + pmi
        )


def check_init_function(block_allocation: bool, init_function: callable):
    if not block_allocation and init_function is not None:
        raise ValueError("")


def validate_number_of_cores(max_cores: int, max_workers: int) -> int:
    # only overwrite max_cores when it is set to 1
    if max_workers != 1 and max_cores == 1:
        return max_workers
    return max_cores
