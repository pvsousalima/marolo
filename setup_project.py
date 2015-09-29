#!/usr/bin/env python
# -*- coding: utf-8 -*-
u"""Script para auxiliar instalação  e manutenção do projeto."""
import os
import glob
import argparse
from shutil import copy2


def repopulate_db():
    u"""Repovoa banco de dados."""
    delete_db()
    populate_db()


def populate_db():
    u"""Povoa banco de dados."""
    os.system(
        "../../web2py.py -S marolo -M -R ./applications/marolo/populate_db.py")


def delete_db():
    u"""Apaga banco de dados."""
    files = glob.glob('./databases/*')
    for f in files:
        os.remove(f)


def copy_requirements():
    u"""Cópia de requisitos (appconfig.ini e routes.py)."""
    if not os.path.exists('private/appconfig.ini'):
        try:
            copy2('./appconfig.ini', 'private/appconfig.ini')
        except:
            print('appconfig.ini not found')

    if not os.path.exists('../../routes.py'):
        try:
            copy2('routes.py', '../../routes.py')
        except:
            print('routes.py not found')


def install_requirements(sudo):
    u"""Instala ou atualiza bibliotecas necessárias."""
    if sudo and os.name == "posix":
        os.system(" sudo pip install -U -r requirements.txt")
    elif sudo:
        os.system(" sudo pip install -U -r requirements.txt")
    else:
        os.system("pip install -U -r requirements.txt")


def setup():
    u"""Adição de argumentos para interface do terminal."""
    if not os.path.exists('private'):
        os.mkdir('private')

    if not os.path.exists('databases'):
        os.mkdir('databases')

    parser = argparse.ArgumentParser(
        prog='setup_project.py',
        description='Automatização do projeto'
        ' importando configurações e banco de dados.'
    )
    parser.add_argument(
        '-p',
        help='povoar banco de dados',
        action="store_true"
    )
    parser.add_argument(
        '-d',
        help='apagar banco de dados',
        action="store_true"
    )
    parser.add_argument(
        '-rp',
        help='repovoar banco de dados',
        action="store_true"
    )
    parser.add_argument(
        '-cp',
        help='copiar dependências',
        action="store_true"
    )
    parser.add_argument(
        '-r',
        help='instalar dependências',
        action="store_true"
    )
    parser.add_argument(
        '--sudo',
        help='argumento utilizando em conjunto com -r para indicar'
        ' que comando será feito utilizando superusuário',
        action="store_true"
    )
    parser.add_argument(
        '--all',
        help='argumento utilizando para executar todas as opções'
        ' necessárias para execução do projeto',
        action="store_true"
    )

    # parse args
    args = parser.parse_args()

    if args.r:
        install_requirements(sudo=args.sudo)

    if args.cp:
        copy_requirements()
        print('Bibliotecas instaladas ou atualizadas com sucesso!')

    # testa argumentos
    if args.p:
        populate_db()
        print('Banco de dados esta preenchido.')

    if args.d:
        delete_db()
        print('O banco de dados foi deletado.')

    if args.rp:
        repopulate_db()
        print('O banco de dados foi repovoado.')

    if args.all:
        install_requirements(sudo=args.sudo)
        copy_requirements()
        repopulate_db()
        print('Todos requisitos instalados.')

if __name__ == '__main__':
    setup()
