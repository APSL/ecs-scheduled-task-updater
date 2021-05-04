# ecs-scheduled-task-updater
The main purpose of this script is to be used at Jenkins to update ECS Scheduled Tasks with the latest task definition available for a service.  

## Usage

**Installation** : 
```
sudo mv ecs-scheduled-task-updater.py /usr/local/bin/ecs-scheduled-task-updater 
```

**Args** :

* ```--scheduled-task```: Name of the scheduled task that we want to update
* ```--task-definition```: Name of the task definition associated to the scheduled task. (It always puts the latest task definition available) 

**Command** : 

```ecs-scheduled-task-updater --scheduled-task <scheduled_task_name> --task-definition <task_definition_name>```