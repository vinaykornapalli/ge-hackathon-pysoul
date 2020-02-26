import click
from pysoul.extract import extract_content
from pysoul.detect import DetectPHI
from pysoul.generatepdf import generate_pdf
from pysoul.generatetext import generate_text
from pysoul.api.server import run_server
from pysoul.filter import filter_content



@click.group()
def cli():
    click.echo('Hello, Welcome to Pysoul')

@click.command()
def extract():
    click.echo('Extracting the content...')
    extract_content('input',1)
    click.echo('Content Extracted...')

@click.command()
def detect():
    click.echo('started detecting phi...')
    obj = DetectPHI()
    obj.detect_phi()
    click.echo('Personal Information detected...')

@click.command()
def generatepdf():
    click.echo('Started Generating Output PDFs...')
    generate_pdf('input',1)
    filter_content()
    click.echo('Output PDFs generated...')

@click.command()
def generatetext():
    click.echo('Started Generating Output txts...')
    generate_text()
    click.echo('Output txts generated...')

@click.command()
def start():
    click.echo('Extracting the content...')
    extract_content('input',1)
    click.echo('Content Extracted...')
    click.echo('started detecting phi...')
    obj = DetectPHI()
    obj.detect_phi()
    click.echo('Personal Information detected...')
    click.echo('Started Generating Output PDFs...')
    generate_pdf('input',1)
    click.echo('Output PDFs generated...')
    click.echo('Started Generating Output txts...')
    generate_text()
    filter_content()
    click.echo('Output txts generated...')

@click.command()
def run():
    run_server()



cli.add_command(extract)
cli.add_command(detect)
cli.add_command(generatepdf)
cli.add_command(generatetext)
cli.add_command(start)
cli.add_command(run)




















