# -*- coding: utf-8 -*-

import uuid
import click
import datetime
import random
import importlib.resources as pkg_resources
from . import notebook_deploy
from . import templates


@click.group()
def main():
    pass


def gen_ukey():
    return uuid.uuid4()


@main.command()
def ukey():
    click.echo(gen_ukey())


def random_year():
    return random.randint(2016, 2019)


def random_month():
    return random.randint(1, 12)


def random_day():
    return random.randint(1, 29)


def notebook_date(date):
    if date == 'no':
        return ''
    l = len(date)
    if l < 4:
        d = datetime.date(random_year(), random_month(), random_day())
    elif l < 6:
        d = datetime.date(int(date[0:4]), random_month(), random_day())
    else:
        d = datetime.date(int(date[0:4]), int(l[4:6]), int(l[6:8]))
    return d.strftime('%Y-%m-%d')


@main.command()
@click.argument('title')
@click.option('--layout', default='article')
@click.option('--date', default='')
@click.option('--out', default='.')
def new(title, layout, date, out):
    date = notebook_date(date)
    if date:
        filename = date + ' ' + title + '.md'
    else:
        filename = title + '.md'
    ukey = gen_ukey()
    tpl = pkg_resources.read_text(templates, 'notebook.md')
    content = str.format(tpl, title=title, layout=layout, ukey=ukey)
    with open(out + '/' + filename, 'w') as w:
        w.write(content)
    click.echo('Successfully create ' + filename)


@main.command()
@click.option('--notebook_dir', default='/Users/albert/vscode/notebook')
@click.option('--blog_dir', default='/Users/albert/vscode/blog')
def deploy(notebook_dir, blog_dir):
    notebook_deploy.deploy(notebook_dir, blog_dir)
    click.echo('Successfully deploy ' + blog_dir)
