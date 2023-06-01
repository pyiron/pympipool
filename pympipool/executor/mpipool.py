import pickle
import cloudpickle
import sys
from pympipool.share.parallel import (
    parse_arguments,
    parse_socket_communication,
    initialize_zmq,
)


def main():
    from mpi4py import MPI

    MPI.pickle.__init__(
        cloudpickle.dumps,
        cloudpickle.loads,
        pickle.HIGHEST_PROTOCOL,
    )
    from mpi4py.futures import MPIPoolExecutor

    future_dict = {}
    argument_dict = parse_arguments(argument_lst=sys.argv)
    with MPIPoolExecutor(int(argument_dict["total_cores"])) as executor:
        if executor is not None:
            context, socket = initialize_zmq(
                host=argument_dict["host"], port=argument_dict["zmqport"]
            )
            while True:
                output = parse_socket_communication(
                    executor=executor,
                    input_dict=cloudpickle.loads(socket.recv()),
                    future_dict=future_dict,
                    cores_per_task=int(argument_dict["cores_per_task"]),
                )
                if isinstance(output, str) and output == "exit":
                    socket.close()
                    context.term()
                    break
                elif isinstance(output, dict):
                    socket.send(cloudpickle.dumps(output))


if __name__ == "__main__":
    main()