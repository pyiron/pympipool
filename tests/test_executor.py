import unittest
from concurrent.futures import ThreadPoolExecutor
from pympipool.common import exec_funct, parse_socket_communication


# def get_ranks(input_parameter, comm=None):
#     from mpi4py import MPI
#     size = MPI.COMM_WORLD.Get_size()
#     rank = MPI.COMM_WORLD.Get_rank()
#     if comm is not None:
#         size_new = comm.Get_size()
#         rank_new = comm.Get_rank()
#     else:
#         size_new = 0
#         rank_new = 0
#     return size, rank, size_new, rank_new, input_parameter


class TestExecutor(unittest.TestCase):
    def test_exec_funct_single_core(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            output = exec_funct(
                executor=executor,
                funct=sum,
                lst=[[1, 1], [2, 2]],
                cores_per_task=1
            )
        self.assertEqual(output, [2, 4])

    # def test_exec_funct_multi_core(self):
    #     with ThreadPoolExecutor(max_workers=1) as executor:
    #         output = exec_funct(
    #             executor=executor,
    #             funct=get_ranks,
    #             lst=[1],
    #             cores_per_task=2
    #         )
    #     self.assertEqual(output, [(1, 0, 1, 0, 1)])

    def test_parse_socket_communication_close(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            output = parse_socket_communication(
                executor=executor,
                input_dict={"c": "close"},
                future_dict={},
                cores_per_task=1
            )
        self.assertEqual(output, "exit")

    def test_parse_socket_communication_execute(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            output = parse_socket_communication(
                executor=executor,
                input_dict={"f": sum, "l": [[1, 1]]},
                future_dict={},
                cores_per_task=1
            )
        self.assertEqual(output, {"r": [2]})

    def test_parse_socket_communication_submit(self):
        future_dict = {}
        with ThreadPoolExecutor(max_workers=1) as executor:
            output = parse_socket_communication(
                executor=executor,
                input_dict={"f": sum, "a": [[1, 1]]},
                future_dict=future_dict,
                cores_per_task=1
            )
        future = future_dict[output['r']]
        self.assertEqual(future.result(), 2)

    def test_parse_socket_communication_update(self):
        future_dict = {}
        with ThreadPoolExecutor(max_workers=1) as executor:
            output = parse_socket_communication(
                executor=executor,
                input_dict={"f": sum, "a": [[1, 1]]},
                future_dict=future_dict,
                cores_per_task=1
            )
            future_hash = output["r"]
            result = parse_socket_communication(
                executor=executor,
                input_dict={"u": [future_hash]},
                future_dict=future_dict,
                cores_per_task=1
            )
        self.assertEqual(result, {"r": {future_hash: 2}})
