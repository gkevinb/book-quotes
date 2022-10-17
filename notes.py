#!/usr/bin/env python

import click
import main
from bs4 import BeautifulSoup
import json


@click.group()
def notes():
    pass


@notes.command()
@click.option('--html', help='Source file')
@click.option('--source', help='source')
@click.option('--output',help='Output file')
@click.option('--author',help='Author')
@click.option('--book',help='Book')
def extract(html, source, output, author, book):
    """Command to start casting alchemy"""
    with open(html) as f:
        content = f.read()

    html_content = BeautifulSoup(content, "html.parser")
    if source == "kindle":
        q = main.extract_quotes_from_kindle(html_content)
    if source == "apple":
        q = main.extract_quotes_from_apple_book(html_content)

    q = main.format_quotes(q, author, book)

    with open(output, 'w') as file:
        file.write(json.dumps(q, indent=4))


if __name__ == '__main__':
    notes()