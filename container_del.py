#!/usr/bin/env python3

import os
import subprocess

def about():
    print(
    '''
    -----------------------------------------------------------
    Программа удаления не нужных образов, созданных для тестов
    сustomer: IVL Equipment & Engineering
    -----------------------------------------------------------
    author: Старых ЛН
    e-mail: ln.kornilovstar@gmail.com
    e-mail: ln.starmark@ekatra.io
    github: https://github.com/KornilovLN
    tel:    +380 66 9805661
    ------------------------------------------------------------
    ''')

def list_docker_containers():
    '''Получение списка имеющихся контейнеров в нужном формате'''
    result = subprocess.run(['docker', 'ps', '-a', '--format', '{{.ID}} {{.Names}} {{.Status}}'],
                             capture_output=True, text=True)
    containers = result.stdout.strip().split('\n')
    for i, container in enumerate(containers):
        print(f"{i+1}. {container}")
    return containers

def stop_and_remove_containers(containers, selection):
    for sel in selection:
        if '-' in sel:
            start, end = sel.split('-')
            start = int(start) if start else 1
            end = int(end) if end else len(containers)
            for i in range(start-1, end):
                container_id = containers[i].split()[0]
                stop_container(container_id)
                remove_container(container_id)
        else:
            idx = int(sel) - 1
            container_id = containers[idx].split()[0]
            stop_container(container_id)
            remove_container(container_id)

def stop_container(container_id):
    try:
        result = subprocess.run(['docker', 'stop', container_id], capture_output=True, text=True, check=True)
        print(f"Stopped container: {container_id}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop container {container_id}: {e.stderr.strip()}")

def remove_container(container_id):
    try:
        result = subprocess.run(['docker', 'rm', container_id], capture_output=True, text=True, check=True)
        print(f"Removed container: {container_id}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove container {container_id}: {e.stderr.strip()}")

def main():
    about()

    print("Docker Containers:")
    containers = list_docker_containers()
    
    selection = input("Enter numbers or ranges of containers to stop and delete (e.g., 1; 2-4; 5-): ").split(';')
    selection = [s.strip() for s in selection if s.strip()]
    
    stop_and_remove_containers(containers, selection)

if __name__ == "__main__":
    main()


