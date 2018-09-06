from radical.entk import Pipeline, Stage, Task, AppManager
import os, sys
from random import shuffle

# ------------------------------------------------------------------------------
# Set default verbosity

if not os.environ.get('RADICAL_ENTK_VERBOSE'):
    os.environ['RADICAL_ENTK_VERBOSE'] = 'INFO'


CUR_NEW_STAGE=0
MAX_NEW_STAGE=4

def generate_pipeline():

    def func_condition():

        global CUR_NEW_STAGE, MAX_NEW_STAGE

        if CUR_NEW_STAGE <= MAX_NEW_STAGE:
            return True

        return False

    def func_on_true():

        global CUR_NEW_STAGE
        CUR_NEW_STAGE += 1

        shuffle(p.stages[CUR_NEW_STAGE:]):

    def func_on_false():
        print 'Done'

    # Create a Pipeline object
    p = Pipeline()

    for s in range(MAX_NEW_STAGE+1):

        # Create a Stage object
        s1 = Stage()

        for i in range(CUR_TASKS):

            t1 = Task()
            t1.executable = ['sleep']
            t1.arguments = [ '30']

            # Add the Task to the Stage
            s1.add_tasks(t1)

        # Add post-exec to the Stage
        s1.post_exec = {
                        condition': func_condition,
                        on_true': func_on_true,
                        on_false': func_on_false
                        }

        # Add Stage to the Pipeline
        p.add_stages(s1)

    return p

if __name__ == '__main__':

    # Create a dictionary describe four mandatory keys:
    # resource, walltime, cores and project
    # resource is 'local.localhost' to execute locally
    res_dict = {

        'resource': 'local.localhost',
        'walltime': 15,
        'cpus': 2,
    }

    # Create Application Manager
    appman = AppManager()
    appman.resource_desc = res_dict

    p = generate_pipeline()

    # Assign the workflow as a set of Pipelines to the Application Manager
    appman.workflow = [p]

    # Run the Application Manager
    appman.run()
