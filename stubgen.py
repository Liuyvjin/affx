import os, sys
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="pybind11 stubgen")
parser.add_argument("-p", "--path", help="path to .pyd file", required=True)
parser.add_argument("-n", "--name", help="name of module", required=True)

args = parser.parse_args()
output_path = args.path
module_name = args.name

sys.path.append(output_path)
exec("import %s" % module_name)

from pybind11_stubgen import ModuleStubsGenerator

module = ModuleStubsGenerator(module_name)
module.parse()
module.write_setup_py = False

with open(f"{output_path}/{module_name}.pyi", "w") as fp:
    fp.write("#\n# Automatically generated file, do not edit!\n#\n\n")
    fp.write("\n".join(module.to_lines()))