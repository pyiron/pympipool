import pickle
import sys

import cloudpickle

from pympipool.cache.shared import backend_load_file, backend_write_file


def main():
    from mpi4py import MPI

    MPI.pickle.__init__(
        cloudpickle.dumps,
        cloudpickle.loads,
        pickle.HIGHEST_PROTOCOL,
    )
    mpi_rank_zero = MPI.COMM_WORLD.Get_rank() == 0
    mpi_size_larger_one = MPI.COMM_WORLD.Get_size() > 1
    file_name = sys.argv[1]

    if mpi_rank_zero:
        apply_dict = backend_load_file(file_name=file_name)
    else:
        apply_dict = None
    apply_dict = MPI.COMM_WORLD.bcast(apply_dict, root=0)
    output = apply_dict["fn"].__call__(*apply_dict["args"], **apply_dict["kwargs"])
    if mpi_size_larger_one:
        result = MPI.COMM_WORLD.gather(output, root=0)
    else:
        result = output
    if mpi_rank_zero:
        backend_write_file(
            file_name=file_name,
            output=result,
        )
    MPI.COMM_WORLD.Barrier()


if __name__ == "__main__":
    main()
