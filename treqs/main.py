from email.policy import default
from treqs.create_elements import create_elements
from treqs.list_elements import list_elements
from treqs.check_elements import check_elements
from treqs.process_elements import process_elements
import logging
import click
import os
import sys
from pathlib import Path


@click.group()
def treqs():
   #initialise logger
   logger = logging.getLogger('treqs-on-git.treqs-ng')
   #We use level 10 for debug, level 20 for verbose, level 30 and higher for important
   #This corresponds to the macros 10 for DEBUG, 20 for INFO, and 30 for WARNING, but has different semantics
   logger.setLevel(10)
   console_handler = logging.StreamHandler()
   #NOTE: We could have different levels for different handlers as well.
   # console_handler.setLevel(10)
   #only display message for now.
   formatter = logging.Formatter('%(message)s')
   console_handler.setFormatter(formatter)
   logger.addHandler(console_handler)
   pass


@click.command(help='List treqs elements in this folder')
@click.option('--type', help='Limit action to specified treqs element type')
@click.option('--uid', help='Limit action to treqs element with specified id')
@click.option('--outlinks/--no-outlinks', default=False, help='Print outgoing tracelinks', show_default=True)
@click.option('--inlinks/--no-inlinks', default=False, help='Print incoming tracelinks', show_default=True)
@click.option('--recursive', type=bool, default=True, help='List treqs elements recursively in all subfolders.')
@click.option('--verbose/--no-verbose', type=bool, default=False,
              help='Print verbose output instead of only the most important messages.', show_default=True)
@click.option('--plantuml/--no-plantuml', type=bool, default=False,
              help='Generate a PlantUML diagram from the treqs elements', show_default=True)
@click.argument('filename', nargs=-1, )  # , help='Give a file or directory to list from.')
def list(filename, type, recursive, uid, outlinks, inlinks, verbose, plantuml):
   setVerbosity(verbose)
   le = list_elements()
   if plantuml:
      click.echo(le.list_elements_as_plantuml(filename=filename, type=type, outlinks=outlinks, inlinks=inlinks,
                                              recursive=recursive, uid=uid))
   else:
      click.echo(le.list_elements(filename, type, recursive, uid, outlinks, inlinks))


@click.command(help='Creates a treqs element and prints it on the command line.')
@click.option('--type', type=str, default='undefined', help='The treqs element type that the new element should have. If available, treqs will select a template for this type.')
@click.option('--label', type=str, default='', help='A short (less than one line) text describing this treqs element. Markdown (headings) encouraged.')
@click.option('--amount', type=int, default = 1,  help='The number of times the element should be created using the given template.')
@click.option('--templatefolder', type=click.Path(exists=True), default=Path(__file__).parent / "../templates", help='Location where the templates are stored. Default location is the template folder in the treqs homefolder. A path to any folder can be given here and it is recommended to maintain a template folder for each project in which treqs is used. In that case, consider a template folder in your local repository, e.g. as sub-folder of requirements.')
@click.option('--template', is_flag=False, default='treqs_element', help='A .md file that contains a template for specifying a requirement. This allows to choose a template independent from type.')
@click.option('--verbose', type=bool, default=False , help='Print verbose output instead of only the most important messages.')
@click.option('--interactive/--non-interactive', default=False, help='Choose between an interactive or a non-interactive interface.')
def create(type, amount, verbose, templatefolder, template, label, interactive):
   setVerbosity(verbose)
   
   if interactive:
      if type == 'undefined':
         type = click.prompt('Which type should the element have?',  type=str, default='undefined')
      if label == '':
         label = click.prompt('Enter the label for the element',  type=str, default='')  
   
   path = Path(os.path.join(templatefolder, type +".md")).exists()
   path2 = Path(os.path.join(templatefolder, template + ".md")).exists()

   if path==True :
      for i in range(amount):
         click.echo(create_elements.create_markdown_element(type,templatefolder,label))
   elif path==False and path2==True:
      for i in range(amount):
         click.echo(create_elements.create_markdown_new_template(type,templatefolder,template,label))
      if interactive or (not interactive and type != 'undefined'):
         print("Template not found for this type. Output generated with default template. Refer to treqs create --help.")
   else:
      print("No matching template found")


@click.command(help='Creates a link to a treqs element.')
@click.option('--linktype', prompt='Which type should the link have?', default='relatesto', help='The treqs link type, specifying the type of relationship to target .')
@click.option('--target', prompt='What UID does the target treqs element have?', default='UID missing', help='Use treqs list to find the right UID.')
@click.option('--verbose/--no-verbose', type=bool, default=False ,help='Print verbose output instead of only the most important messages.', show_default=True)
def createlink(linktype, target, verbose):
   setVerbosity(verbose)
   click.echo(create_elements.create_link(linktype, target))

@click.command(help='Checks for consistency of treqs elements.')
@click.option('--recursive', type=bool, default=True ,help='Check treqs elements recursively in all subfolders.')
@click.option('--ttim', default='./ttim.yaml', help='Path to a type and traceability information model (TTIM) in json format.')
@click.option('--verbose/--no-verbose', type=bool, default=False ,help='Print verbose output instead of only the most important messages.', show_default=True)
@click.argument('filename', nargs=-1)#, help='Give a file or directory to list from.')
def check(recursive, filename, ttim, verbose):
   setVerbosity(verbose)
   ce = check_elements()
   click.echo(ce.check_elements(filename,recursive, ttim))

#TODO GL: Imho too many options here. Confusing. Address in the future by having a single strategy attribute with different string options?
@click.command(help='Process a treqs-controlled file, i.e. generate content in protected areas.')
@click.option('--recursive',type=bool,default=True,help='Process all subfolder recursively.',show_default=True)
@click.option('--web/--no-web', default=False, help='Uses an external webservice to generate PlantUML images (only with Treqs extensions).', show_default=True)
@click.option('--links/--no-links', default=False, help='Generates diagram code to URL links from a file (only with Treqs extensions).', show_default=True)
@click.option('--html',type=str, metavar='', default=False, is_flag=True, help='Generate HTML with traceable diagrams (only with Treqs extensions).', show_default=False)
@click.option('--svg',type=str, metavar='', default=False, is_flag=True, help='Generate SVG diagram images instead of PNGs (only with Treqs extensions).', show_default=False)
@click.option('--verbose/--no-verbose', type=bool, default=False ,help='Print verbose output instead of only the most important messages.', show_default=True)
@click.argument('filename')
def process(filename, recursive, web, html, svg, links, verbose):
   setVerbosity(verbose)
   pe = process_elements()
   pe.process_elements(filename, recursive, web, html, svg, links) 

@click.command(help='Generate a new id used for treqs element.')
@click.option('--amount',help='Specify amount of generated ids',type=int, default=1,show_default=True)
def generateid(amount):
   click.echo(create_elements.generate_id(amount))

treqs.add_command(list)
treqs.add_command(create)
treqs.add_command(createlink)
treqs.add_command(check)
treqs.add_command(process)
treqs.add_command(generateid)

def setVerbosity(verbose):
   if verbose:
      logging.getLogger('treqs-on-git.treqs-ng').setLevel(10)
   else:
      logging.getLogger('treqs-on-git.treqs-ng').setLevel(20)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, format='%(message)s')
    treqs()
