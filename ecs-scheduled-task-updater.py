#!/usr/bin/env python3
""" ecs-scheduled-task-updater """

import boto3
import argparse

def get_target_info(rule):
    client = session.client('events')
    response = client.list_targets_by_rule(
        Rule=rule,
    )
    target = response['Targets'][0]
    return target

def fetch_latest_task_definition(prefix):
    client = session.client('ecs')
    response = client.list_task_definitions(
        familyPrefix=prefix,
        status='ACTIVE',
        sort='DESC',
        maxResults=1
    )
    task = response['taskDefinitionArns'][0]
    return task

def update(st, t_id, t_arn, t_rolearn, t_tdarn):
    print("Trying to update scheduled task event with {} task definition".format(t_tdarn))
    client = session.client('events')
    response = client.put_targets(
        Rule=st,
        Targets=[
            {
                'Id': t_id,
                'Arn': t_arn,
                'RoleArn': t_rolearn,
                'EcsParameters': {
                    'TaskDefinitionArn': t_tdarn
                },
            }
        ]
    )
    
    if response["FailedEntryCount"] == 0:
        print("Event updated successfully!")
    else:
        print("Error updating event :(")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scheduled-task",
        help="Scheduled task to modify",
        required=True
    )
    parser.add_argument(
        "--task-definition",
        help="Task definition to fetch",
        required=True
    )    
    args = parser.parse_args()

    session = boto3.Session()
    info = get_target_info(args.scheduled_task)
    task_definition = fetch_latest_task_definition(args.task_definition)

    target_id = info['Id']
    target_arn = info['Arn']
    target_role_arn = info['RoleArn']

    update(args.scheduled_task, target_id, target_arn, target_role_arn, task_definition)
