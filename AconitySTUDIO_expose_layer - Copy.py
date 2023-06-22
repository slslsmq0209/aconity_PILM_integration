import asyncio
import aiohttp
import json
import sys, os
import time
import logging
from datetime import datetime
from pytz import timezone, utc

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from AconitySTUDIO_client import AconitySTUDIOPythonClient
from AconitySTUDIOpy.AconitySTUDIO_client import AconitySTUDIO_client as AconitySTUDIOPythonClient
from AconitySTUDIO_client import utils
           

async def pauser(pause, message):
    '''helper function to put messages on the console'''
    print('')
    for i in range(pause):
        sys.stdout.write(f'\rWaiting for {pause-i} seconds {message}')
        sys.stdout.flush()
        await asyncio.sleep(1) #simulating waiting time
    print('')

async def main(login_data, info):
    '''
    Example Code to illustrate on how a parameter can be changed during a job.
    The code does the folllowing things:
    * Gather necessary information about the machine and setup.
    * Start a job.
    * Wait for some database input (simulated by waiting)
    * Pause the job (after that, wait until state of machine is paused).
    * Change one global and two part specific parameters.
    * Resume the job.
    * After a little while, we stop the job.
    '''

    #create client with factory method
    client = await AconitySTUDIOPythonClient.create(login_data)
    client.studio_version = info['studio_version']
    
    # IMPORTANT:
    # the following convenience functions (get_job_id etc) only work if the job_name, machine_name or config_name are unique.
    # If this is not the case, set the attributes job_name, config_name, machine_name manually
    await client.get_job_id(info['job_name'])
    await client.get_machine_id(info['machine_name'])
    await client.get_config_id(info['config_name'])
        

    # Subscribe to "run" report. We do this in order to know when the
    # machine has truly paused, i.e finished the current layer.
    # (Note that this is different from the time we send the pause command)
    # Only if the machine is in state paused can new parameters be injected.
    #await client.subscribe_report('run')
    
    # Start a job. 
    await client.task.on(machine_id, "light")
    await asyncio.sleep(5) 
    await client.task.off(machine_id, "light")

    # Pause the job.
    #print('\n\t***soon pausing***')
    # (The pauser coroutine does a simple asyncio.sleep,
    # but with a countdown printed on the console.)
    #await pauser(10, message='until we initiate a pause ...') 

    #print('\n\t***initiating pause! (machine will be paused when the current layer is finished, which may take a few moments.)***')
    #await client.pause_job()
    await asyncio.sleep(5)
    #print('\n\t***machine is in state paused. Changing some parameters next!***')
    
    
    # Next, we change one global parameter and two part specific parameters.
    # (To see the changed parameters in the GUI please reload the tab.)
    #await client.change_global_parameter('return_velocity', 113)

    # Note: for the (first) argument of change_part_parameter, please read the documentation.
    #part_id = 1
    #param = 'mark_speed'
    #value = 4
    #await client.change_part_parameter(part_id = part_id, param=param, value=value)

    #await client.change_part_parameter(*change_2)
    #change_2 = (2, 'mark_speed', 456)
    #print('\n\t***Parameters were changed. (To see the result in in the GUI, please reload the tab.)***\n\n')


    # Resume the Job. We want to start at a different layer now, depending on how many layers we already built.
    #print('\n\t***Next, we calculate the new starting layer and resume the job.***\n\n')
    #new_starting_layer = client.job_info['start_layer'] + client.job_info['AddLayerCommands']

    #await asyncio.sleep(5)
    #await client.resume_job(layers=[new_starting_layer, end_layer], parts=build_parts)

    #After a little while, we stop the job and exit.
    #print('\n\t***We soon stop the job and exit***')
    #await pauser(20, message = 'until we exit ...')
    
    #await client.pause_job()
    await client.stop_job() # use this line instead of pause_job to initiate a hard stop
    print('\n\t***we are done***\n\n')

if __name__ == '__main__':
    '''
    Example script on how to use the AconitySCRIPT to control the flow of a job.
    While job is paused, we show how to change its parameters.
    '''

    #Create a logfile for this session in the example folder.
    #The logfile contains the name of this script with a timestamp.
    #Note: This is just one possible way to log. 
    #Logging configuration should be configured by the user, if any logging is to be used at all.
    utils.log_setup(sys.argv[0], directory_path='')
    
    #change login_data to your needs
    login_data = {
        'rest_url' : f'http://192.168.2.201:9000',
        'ws_url' : f'ws://192.168.2.201:9000',
        'email' : 'mshuai@stanford.edu',
        'password' : 'aconity'
    }

    #change info to your needs
    info = {
        'machine_name' : '1.4404',
        'config_name': 'LinearizedPower_AlignedAxisToChamber',
        'job_name': 'testScan',
    }
    info_test_server = {
        'machine_name' : '1.4404',
        'config_name': 'LinearizedPower_AlignedAxisToChamber',
        'job_name': 'testScan',
    }

    info = {
        'machine_name' : '1.4404',
        'config_name': 'LinearizedPower_AlignedAxisToChamber',
        'job_name': 'testScan',
        'studio_version' : 1
    }
    
    #info = info_test_server

    result = asyncio.run(main(login_data, info), debug=True)