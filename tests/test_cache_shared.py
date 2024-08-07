from concurrent.futures import Future
import os
import shutil
import unittest


try:
    from executorlib.cache.hdf import dump
    from executorlib.cache.shared import (
        FutureItem,
        _check_task_output,
        _serialize_funct_h5,
    )
    from executorlib.cache.shared import execute_task_in_file

    skip_h5io_test = False
except ImportError:
    skip_h5io_test = True


def my_funct(a, b):
    return a + b


@unittest.skipIf(
    skip_h5io_test, "h5io is not installed, so the h5io tests are skipped."
)
class TestSharedFunctions(unittest.TestCase):
    def test_execute_function_mixed(self):
        cache_directory = os.path.abspath("cache")
        os.makedirs(cache_directory, exist_ok=True)
        task_key, data_dict = _serialize_funct_h5(
            my_funct,
            1,
            b=2,
        )
        file_name = os.path.join(cache_directory, task_key + ".h5in")
        dump(file_name=file_name, data_dict=data_dict)
        execute_task_in_file(file_name=file_name)
        future_obj = Future()
        _check_task_output(
            task_key=task_key, future_obj=future_obj, cache_directory=cache_directory
        )
        self.assertTrue(future_obj.done())
        self.assertEqual(future_obj.result(), 3)
        future_file_obj = FutureItem(
            file_name=os.path.join(cache_directory, task_key + ".h5out")
        )
        self.assertTrue(future_file_obj.done())
        self.assertEqual(future_file_obj.result(), 3)

    def test_execute_function_args(self):
        cache_directory = os.path.abspath("cache")
        os.makedirs(cache_directory, exist_ok=True)
        task_key, data_dict = _serialize_funct_h5(
            my_funct,
            1,
            2,
        )
        file_name = os.path.join(cache_directory, task_key + ".h5in")
        dump(file_name=file_name, data_dict=data_dict)
        execute_task_in_file(file_name=file_name)
        future_obj = Future()
        _check_task_output(
            task_key=task_key, future_obj=future_obj, cache_directory=cache_directory
        )
        self.assertTrue(future_obj.done())
        self.assertEqual(future_obj.result(), 3)
        future_file_obj = FutureItem(
            file_name=os.path.join(cache_directory, task_key + ".h5out")
        )
        self.assertTrue(future_file_obj.done())
        self.assertEqual(future_file_obj.result(), 3)

    def test_execute_function_kwargs(self):
        cache_directory = os.path.abspath("cache")
        os.makedirs(cache_directory, exist_ok=True)
        task_key, data_dict = _serialize_funct_h5(
            my_funct,
            a=1,
            b=2,
        )
        file_name = os.path.join(cache_directory, task_key + ".h5in")
        dump(file_name=file_name, data_dict=data_dict)
        execute_task_in_file(file_name=file_name)
        future_obj = Future()
        _check_task_output(
            task_key=task_key, future_obj=future_obj, cache_directory=cache_directory
        )
        self.assertTrue(future_obj.done())
        self.assertEqual(future_obj.result(), 3)
        future_file_obj = FutureItem(
            file_name=os.path.join(cache_directory, task_key + ".h5out")
        )
        self.assertTrue(future_file_obj.done())
        self.assertEqual(future_file_obj.result(), 3)

    def tearDown(self):
        if os.path.exists("cache"):
            shutil.rmtree("cache")
