from radical.entk import Pipeline, Stage, Task, AppManager
import pytest
from radical.entk.exceptions import *
import os

hostname = os.environ.get('RMQ_HOSTNAME','localhost')
port = int(os.environ.get('RMQ_PORT',5672))

def test_state_order():

    """
    **Purpose**: Test if the Pipeline, Stage and Task are assigned their states in the correct order
    """

    def create_single_task():

        t1 = Task()
        t1.name = 'simulation'
        t1.executable = ['/bin/date']
        t1.copy_input_data = []
        t1.copy_output_data = []

        return t1

    p1 = Pipeline()
    p1.name = 'p1'

    s = Stage()
    s.name = 's1'
    s.tasks = create_single_task()
    s.add_tasks(create_single_task())

    p1.add_stages(s)

    res_dict = {

            'resource': 'local.localhost',
            'walltime': 5,
            'cpus': 1,
            'project': ''

    }

    os.environ['RADICAL_PILOT_DBURL'] = 'mongodb://user:user@ds129013.mlab.com:29013/travis_tests'
    os.environ['RP_ENABLE_OLD_DEFINES'] = 'True'

    appman = AppManager(hostname=hostname, port=port)
    appman.resource_desc = res_dict

    appman.assign_workflow(set([p1]))
    appman.run()

    print p1.state

    p_state_hist = p1.state_history
    assert p_state_hist == ['DESCRIBED', 'SCHEDULING', 'DONE']

    s_state_hist = p1.stages[0].state_history
    assert s_state_hist == ['DESCRIBED', 'SCHEDULING', 'SCHEDULED', 'DONE']

    tasks = p1.stages[0].tasks

    for t in tasks:

        t_state_hist = t.state_history
        assert t_state_hist == ['DESCRIBED', 'SCHEDULING', 'SCHEDULED', 'SUBMITTING', 'SUBMITTED',
                            'EXECUTED', 'DEQUEUEING', 'DEQUEUED', 'DONE']

    