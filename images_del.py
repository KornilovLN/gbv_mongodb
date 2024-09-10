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

def list_docker_images():
    '''Получение списка имеющихся образов в нужном формате'''
    result = subprocess.run(['docker', 'images', '--format', '{{.ID}} {{.Repository}}:{{.Tag}}'],
                            capture_output=True, text=True)
    images = result.stdout.strip().split('\n')
    for i, image in enumerate(images):
        print(f"{i+1}. {image}")
    return images

def delete_docker_images(images, selection):
    '''Удаление выбранных образов из хранилища'''
    for sel in selection:
        if '-' in sel:
            start, end = sel.split('-')
            start = int(start) if start else 1
            end = int(end) if end else len(images)
            for i in range(start-1, end):
                image_id = images[i].split()[0]
                subprocess.run(['docker', 'rmi', image_id])
        else:
            idx = int(sel) - 1
            image_id = images[idx].split()[0]
            subprocess.run(['docker', 'rmi', image_id])

def main():
    about()
    
    print("Docker Images:")
    images = list_docker_images()
    
    selection = input("Enter numbers or ranges of images to delete (e.g., 1; 2-4; 5-): ").split(';')
    selection = [s.strip() for s in selection if s.strip()]
    
    delete_docker_images(images, selection)
    
if __name__ == "__main__":
    main()

