import asyncio

import sys

import time

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

from AconitySTUDIOpy.AconitySTUDIO_client import AconitySTUDIO_client as AconitySTUDIOPythonClient

def handle_task_event(topic, msg):

    log = f"{topic} {msg['id']} {msg['report']}"

    for event in msg['events']:

        log  +=  f" {event['state']}\n{event['t_state']}\n{event['msg']}"

    print(f"\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\nANALYSE TASK EVENTS\n(topic={topic})\n{log}\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n", flush=True)


def handle_cmds_event(topic, msg):

    log = f"{topic} {msg}"

    print(f"\n**********************************************************\n\nANALYSE CMDS EVENTS\n(topic={topic})\n{log}\n\n**********************************************************\n\n", flush=True)

def handle_positioning_data(topic, msg):

    log = f"{topic} {msg['id']}"

    for data_msg in msg['data']:

        log  +=  f" {data_msg['cid']}"
        log  +=  f" {data_msg['ts']}"
        # log  +=  f"{data['tag']}\n"

        for data in data_msg['data']:

            log  +=  f" {data['name']} {data['type']} {data['value']}\n"

    print(f"\n##########################################################\n\nPOS (topic={topic})\n{log}\n##########################################################\n", flush=True)

def handle_state_data(topic, msg):

    log = f"{topic} {msg['id']}"

    for data_msg in msg['data']:

        log  +=  f" {data_msg['cid']}"
        log  +=  f" {data_msg['ts']}"
        # log  +=  f"{data['tag']}\n"

        for data in data_msg['data']:

            log  +=  f" {data['name']} {data['type']} {data['value']}\n"

    print(f"\n##########################################################\n\nSTATE (topic={topic})\n{log}\n##########################################################\n", flush=True)





async def execute(login_data, info):

    '''
    Example code demonstrating simple usages of the Python client task api.

    1) asyncioTask object "lighter" turns lights on and off
    2) Move Slider, Supplier tasks are also available.
    '''

    print('\n\n ######## INIT CLIENT ########\n\n')

    #create client with factory method
    client = await AconitySTUDIOPythonClient.create(login_data, studio_version=info['studio_version'])

    #Create a logfile for this session in the example folder.
    #The logfile contains the name of this script with a timestamp.
    #Note: This is just one possible way to log.
    #Logging configuration should be configured by the user, if any logging is to be used at all.
    client.log_setup(sys.argv[0], directory_path='')

    # #### SESSION STATE #### #

    print('\n\n ######## SESSION STATE ########\n\n')

    # #### MACHINE #### #

    machine_name = info['machine_name']

    machine_id = await client.gateway.get_machine_id(machine_name)

    # #### (START) CONFIG #### #

    config_name = info['config_name']

    config_id = await client.gateway.get_config_id(config_name)

    if await client.gateway.config_state(config_id) == "inactive":

        await client.gateway.start_config(config_id)

    else:

        print("CONFIG IS ALREADY STARTED")

    # #### JOB #### #

    job_name = info['job_name']

    job_id = await client.job.get_job_id(job_name)

    # #### PROCESSORS #### #

    print('\n\n ######## ADD PROCESSORS ########\n\n')

    client.data.add_processor(['task'], handle_task_event)
    client.data.add_processor(['cmds'], handle_cmds_event)
    client.data.add_processor(['Positioning'], handle_positioning_data)
    client.data.add_processor(['State'], handle_state_data)

    print('\n\n ######## SUBSCRIBE TOPICS ########\n\n')

    await client.data.subscribe_event_topic('task')
    await client.data.subscribe_event_topic('cmds')

    await client.data.subscribe_data_topic('Positioning')
    await client.data.subscribe_data_topic('State')

    # #### TASK EXECUTION #### #

    print('\n\n ######## START TASK EXECUTION ... ########\n\n')
    


    await client.task.off(machine_id, "light")


    


    # #### EXPOSE #### #

    # await client.task.expose(machine_id, job_id, 100, [1,2,3,4], channel="manual")

    # # #### LIGHT #### #

    #print('\n\n ######## TRY on/off "light" ########\n\n')
    
    #if(await client.task.on(machine_id, "light")):

        #print('\n ######## on "light" => wait ########\n')

        #await asyncio.sleep(5)

        #if(await client.task.off(machine_id, "light")):

            #print('\n ######## off "light" ########\n')

    # #### GUIDE BEAM 1 #### #

    #print('\n\n ######## TRY on/off "guide_beam_1" ########\n\n')

    #if(await client.task.on(machine_id, "guide_beam_1")):

        #print('\n ######## on "guide_beam_1" => wait ########\n')

        #await asyncio.sleep(5)

        #if(await client.task.off(machine_id, "guide_beam_1")):

            #print('\n ######## off "guide_beam_1" ########\n')

    # # #### SUPPLIER #### #

    # print('\n\n ######## TRY move_rel "supplier_1" +3/-3 ######## \n\n')

    # if(await client.task.move_rel(machine_id, "supplier_1", 3)):

    #     print('\n ######## moved "supplier_1" +3 ########')

    #     if(await client.task.move_rel(machine_id, "supplier_1", -3)):

    #         print('\n ######## moved "supplier_1" -3 ########')

    # # #### SLIDER #### #

    # print('\n\n ######## TRY move_rel "slider" +10/-10 ######## \n\n')

    # if(await client.task.move_rel(machine_id, "slider", 10)):

    #     print('\n ######## moved "slider" +10 ########')

    #     if(await client.task.move_rel(machine_id, "slider", -10)):

    #         print('\n ######## moved "slider" -10 ########')

    # # #### OPTICAL AXIS #### #

    # print('\n\n ######## TRY move_rel "optical_axis" +30/-30 ######## \n\n')

    # if(await client.task.move_rel(machine_id, "optical_axis", 30)):

    #     print('\n ######## moved "optical_axis" +30 ########')

    #     if(await client.task.move_rel(machine_id, "optical_axis", -30)):

    #         print('\n ######## moved "optical_axis" -30 ########')

    #await asyncio.sleep(5)

    print('\n\n ######## ... TASKS EXECUTED ########\n\n')

#########################################################################################################################

if __name__ == '__main__':


    '''
    Example on how to use the python client for executing scripts.
    Please change login_data and info to your needs.
    '''
   

    # #### LOGIN DATA #### #

    login_data = {
        'rest_url' : f'http://192.168.2.201:9000',
        'ws_url' : f'ws://192.168.2.201:9000',
        'email' : 'mshuai@stanford.edu',
        'password' : 'aconity'
    }

    # #### SESSION STATE #### #

    info = {
        'machine_name' : '1.4404',
        'config_name': 'LinearizedPower_AlignedAxisToChamber',
        'job_name': '2023_05_04_FeBTest',
        'studio_version' : 1
    }

    result = asyncio.run(execute(login_data, info), debug=True)
