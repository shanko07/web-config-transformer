import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser(usage="%(prog)s [OPTION]", description="Modify a supplied web.config file to disable .NET event validation")
parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version 1.0.0")
parser.add_argument("-i", "--infile", default="web.config", help="input file to be transformed (default: web.config)")
parser.add_argument("-o", "--outfile", default="web.config", help="output file to write the transformation to (default: web.config)")
args = parser.parse_args()


# parse the input file as xml
tree = ET.parse(args.infile)
root = tree.getroot()

# attempt to find the system.web tag under the root level
system_web = root.find('system.web')
if system_web is None:
	print('system.web tag not found, are you sure this is a valid web.config file?')
	exit()

# find all pages tags under system.web and modify them to turn off event validation
all_pages = system_web.findall('pages')
for pages_tag in all_pages:
	pages_tag.set('enableEventValidation', 'false')

# if there were no pages tags, add one and turn off event validation with it
if len(all_pages) == 0:
	system_web.append(ET.Element('pages', {'enableEventValidation': 'false'}))

# write the result to the output file
tree.write(args.outfile)
