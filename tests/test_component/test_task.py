# pylint: disable=protected-access, unused-argument
# pylint: disable=no-value-for-parameter

__copyright__ = "Copyright 2020, http://radical.rutgers.edu"
__license__   = "MIT"

from unittest import TestCase

import pytest

from radical.entk.task import Task
from radical.entk import states

import radical.entk.exceptions as ree

try:
    import mock
except ImportError:
    from unittest import mock


# ------------------------------------------------------------------------------
#
class TestTask(TestCase):


    # --------------------------------------------------------------------------
    #
    @mock.patch('radical.utils.generate_id', return_value='test.0000')
    def test_task_initialization(self, mocked_generate_id):
        '''
        **Purpose**: Test if the task attributes have, thus expect, the correct 
        data types
        '''

        t = Task()

        self.assertEqual(t._uid, 'test.0000')
        self.assertEqual(t.name, '')
        self.assertEqual(t.state, states.INITIAL)
        self.assertEqual(t.state_history, [states.INITIAL])
        self.assertEqual(t.executable, '')
        self.assertIsInstance(t.arguments, list)
        self.assertIsInstance(t.pre_exec, list)
        self.assertIsInstance(t.post_exec, list)

        self.assertEqual(t._cpu_reqs['processes'], 1)
        self.assertIsNone(t._cpu_reqs['process_type'])
        self.assertEqual(t._cpu_reqs['threads_per_process'], 1)
        self.assertIsNone(t._cpu_reqs['thread_type'])
        self.assertEqual(t._gpu_reqs['processes'], 0)
        self.assertIsNone(t._gpu_reqs['process_type'])
        self.assertEqual(t._gpu_reqs['threads_per_process'], 0)
        self.assertIsNone(t._gpu_reqs['thread_type'])

        self.assertEqual(t.lfs_per_process, 0)
        self.assertEqual(t.sandbox, '')
        self.assertIsInstance(t.upload_input_data, list)
        self.assertIsInstance(t.copy_input_data, list)
        self.assertIsInstance(t.link_input_data, list)
        self.assertIsInstance(t.move_input_data, list)
        self.assertIsInstance(t.copy_output_data, list)
        self.assertIsInstance(t.link_output_data, list)
        self.assertIsInstance(t.move_output_data, list)
        self.assertIsInstance(t.download_output_data, list)
        self.assertEqual(t.stdout, '')
        self.assertEqual(t.stderr, '')
        self.assertIsNone(t.exit_code)
        self.assertIsNone(t.tag)
        self.assertIsNone(t.path)
        self.assertIsNone(t.parent_pipeline['uid'])
        self.assertIsNone(t.parent_pipeline['name'])
        self.assertIsNone(t.parent_stage['name'])
        self.assertIsNone(t.parent_stage['uid'])


    # --------------------------------------------------------------------------
    #
    @mock.patch('radical.utils.generate_id', return_value='test.0000')
    @mock.patch.object(Task, '__init__',   return_value=None)
    def test_cpu_reqs(self, mocked_generate_id, mocked_init):
        task = Task()
        task._cpu_reqs = {'processes'           : 1,
                          'process_type'        : None,
                          'threads_per_process' : 1,
                          'thread_type'         : None}
        cpu_reqs = {'processes' : 2, 
                    'process_type' : None, 
                    'threads_per_process' : 1, 
                    'thread_type' : 'OpenMP'}
        task.cpu_reqs = {'processes' : 2, 
                         'process_type' : None, 
                         'threads_per_process' : 1, 
                         'thread_type' : 'OpenMP'}

        self.assertEqual(task._cpu_reqs, cpu_reqs)
        self.assertEqual(task.cpu_reqs, {'cpu_processes' : 2, 
                                         'cpu_process_type' : None, 
                                         'cpu_threads' : 1, 
                                         'cpu_thread_type' : 'OpenMP'})

        with self.assertRaises(ree.MissingError):
            task.cpu_reqs = {'cpu_processes' : 2, 
                             'cpu_process_type' : None, 
                             'cpu_thread_type' : 'OpenMP'}

        with self.assertRaises(ree.TypeError):
            task.cpu_reqs = {'cpu_processes' : 'a', 
                             'cpu_process_type' : None, 
                             'cpu_threads' : 1,
                             'cpu_thread_type' : 'OpenMP'}

        with self.assertRaises(ree.TypeError):
            task.cpu_reqs = {'cpu_processes' : 1, 
                             'cpu_process_type' : None, 
                             'cpu_threads' : 'a',
                             'cpu_thread_type' : 'OpenMP'}

        with self.assertRaises(ree.TypeError):
            task.cpu_reqs = list()

        with self.assertRaises(ree.ValueError):
            task.cpu_reqs = {'cpu_processes' : 1, 
                             'cpu_process_type' : None, 
                             'cpu_threads' : 1,
                             'cpu_thread_type' : 'MPI'}

        with self.assertRaises(ree.ValueError):
            task.cpu_reqs = {'cpu_processes' : 1, 
                             'cpu_process_type' : 'test', 
                             'cpu_threads' : 1,
                             'cpu_thread_type' : 'OpenMP'}


    # --------------------------------------------------------------------------
    #
    @mock.patch('radical.utils.generate_id', return_value='test.0000')
    @mock.patch.object(Task, '__init__',   return_value=None)
    def test_gpu_reqs(self, mocked_generate_id, mocked_init):
        task = Task()
        task._gpu_reqs = {'processes'           : 1,
                          'process_type'        : None,
                          'threads_per_process' : 1,
                          'thread_type'         : None}
        gpu_reqs = {'processes' : 2, 
                    'process_type' : None, 
                    'threads_per_process' : 1, 
                    'thread_type' : 'OpenMP'}
        task.gpu_reqs = {'processes' : 2, 
                         'process_type' : None, 
                         'threads_per_process' : 1, 
                         'thread_type' : 'OpenMP'}

        self.assertEqual(task._gpu_reqs, gpu_reqs)
        self.assertEqual(task.gpu_reqs, {'gpu_processes' : 2, 
                                         'gpu_process_type' : None, 
                                         'gpu_threads' : 1, 
                                         'gpu_thread_type' : 'OpenMP'})

        with self.assertRaises(ree.TypeError):
            task.gpu_reqs = list()

        with self.assertRaises(ree.MissingError):
            task.gpu_reqs = {'gpu_processes' : 2, 
                             'gpu_process_type' : None, 
                             'gpu_thread_type' : 'OpenMP'}

        with self.assertRaises(ree.TypeError):
            task.gpu_reqs = {'gpu_processes' : 'a', 
                             'gpu_process_type' : None, 
                             'gpu_threads' : 1,
                             'gpu_thread_type' : 'OpenMP'}

        with self.assertRaises(ree.TypeError):
            task.gpu_reqs = {'gpu_processes' : 1, 
                             'gpu_process_type' : None, 
                             'gpu_threads' : 'a',
                             'gpu_thread_type' : 'OpenMP'}

        with self.assertRaises(ree.ValueError):
            task.gpu_reqs = {'gpu_processes' : 1, 
                             'gpu_process_type' : None, 
                             'gpu_threads' : 1,
                             'gpu_thread_type' : 'MPI'}

        with self.assertRaises(ree.ValueError):
            task.gpu_reqs = {'gpu_processes' : 1, 
                             'gpu_process_type' : 'test', 
                             'gpu_threads' : 1,
                             'gpu_thread_type' : 'OpenMP'}

    # --------------------------------------------------------------------------
    #
    @mock.patch.object(Task, '__init__',   return_value=None)
    def test_uid(self, mocked_init):

        task = Task()
        task._uid = 'test.0000'
        self.assertEqual(task.uid, 'test.0000')

        task.uid = 'test.0001'
        self.assertEqual(task._uid, 'test.0001')

        with self.assertRaises(ree.TypeError):
            task.uid = 1

    # --------------------------------------------------------------------------
    #
    @mock.patch.object(Task, '__init__',   return_value=None)
    def test_luid(self, mocked_init):

        task = Task()
        task._name = ""
        task.parent_pipeline = {'name':'p0'}
        task.parent_stage = {'name':'s0'}
        task.name = 'test.0000'
        self.assertEqual(task.luid, 'p0.s0.test.0000')

        task = Task()
        task._name = ""
        task.parent_pipeline = {'uid':'p0'}
        task.parent_stage = {'uid':'s0'}
        task.uid = 'test.0000'
        self.assertEqual(task.luid, 'p0.s0.test.0000')

    # --------------------------------------------------------------------------
    #
    def test_dict_to_task(self):

        d = {'name'      : 'foo',
            'pre_exec'  : ['bar'],
            'executable': 'buz',
            'arguments' : ['baz', 'fiz'],
            'cpu_reqs'  : {'processes'          : 1,
                            'process_type'       : None,
                            'threads_per_process': 1,
                            'thread_type'        : None},
            'gpu_reqs'  : {'processes'          : 0,
                            'process_type'       : None,
                            'threads_per_process': 0,
                            'thread_type'        : None}}
        t = Task(from_dict=d)

        for k,v in d.items():
            self.assertEqual(t.__getattribute__(k), v, msg='%s != %s'
                % (t.__getattribute__(k), v))

        d = {'name'      : 'foo',
            'pre_exec'  : ['bar'],
            'executable': 'buz',
            'arguments' : ['baz', 'fiz'],
            'cpu_reqs'  : {'processes'          : 1,
                            'process_type'       : None,
                            'threads_per_process': 1,
                            'thread_type'        : None},
            'gpu_reqs'  : {'processes'          : 0,
                            'process_type'       : None,
                            'threads_per_process': 0,
                            'thread_type'        : None}}
        t = Task()
        t.from_dict(d)

        for k,v in d.items():
            self.assertEqual(t.__getattribute__(k), v, msg='%s != %s'
                % (t.__getattribute__(k), v))

        # make sure the type checks kick in
        d = 'test'
        with pytest.raises(ree.TypeError):
            t = Task(from_dict=d)
