"""Parse the netlist files."""
from typing import Dict, List, Optional
import argparse
import json
from os.path import join
from functools import reduce
from PySpice.Spice import Parser # type: ignore

TOP_MODULE = 'core_top'

class CircParser:
    """A Spice circuit parser."""

    _HW_FOLDER = 'hardware'
    _MAP_FILE = join('lib', 'model_name_map.json')

    def __init__(self, module_name: str, hw_folder: Optional[str]=None,
                 model_map: Optional[str]=None,
                 verbose: bool=False):
        self._module_name = module_name
        if hw_folder is None:
            self._hw_folder = self._HW_FOLDER
        else:
            self._hw_folder = hw_folder
        self._model_map: Dict[str, Dict[str, str]] = {}
        model_map_file = model_map
        if model_map_file is None:
            model_map_file = self._MAP_FILE
        with open (model_map_file, 'r', encoding='utf-8') as map_file:
            self._model_map = json.load(map_file)
        self._sub_circuits: Optional[List[Parser.SubCircuit]] = None
        self._verbose = verbose

    def parse(self) -> None:
        """Parse the circuit."""
        c_parser = Parser.SpiceParser(self._rcir_file)
        c_parser.build_circuit()
        self._sub_circuits = c_parser.subcircuits

    def write(self) -> None:
        """Write the parsed circuit to the target circuit file."""
        if not self._sub_circuits:
            self._print('First parse the circuit.')
            return
        with open(self._cir_file, 'w', encoding='utf-8') as cir_file:
            cir_file.write(f'* Top cell name: {self._module_name}\n')
            cir_file.write('\n')
            line_to_write = ''
            for sub_circ in self._sub_circuits:
                cir_file.write(line_to_write)
                circ_name = sub_circ.name.lower()
                if circ_name in self._model_map['modules']:
                    circ_name = self._model_map['modules'][circ_name]
                cir_file.write(f'.SUBCKT {circ_name} '
                               f'{reduce(lambda x, y: str(x).lower() + " " + str(y).lower(),
                                         sub_circ.nodes)}\n')
                for sub_sub_circ in sub_circ:
                    if not isinstance(sub_sub_circ, Parser.Element):
                        continue
                    if sub_sub_circ._parameters: # pylint: disable=protected-access
                        name = sub_sub_circ._parameters[0].lower() # pylint: disable=protected-access
                        if name in self._model_map['modules']:
                            name = self._model_map['modules'][name]
                    else:
                        model_name = sub_sub_circ._dict_parameters['model'] # pylint: disable=protected-access
                        if model_name not in self._model_map['models']:
                            self._print(f'No map name for: {model_name}')
                            continue
                        name = self._model_map['models'][model_name]
                    cir_file.write(f'    {sub_sub_circ._prefix}{sub_sub_circ.name.lower()} ') # pylint: disable=protected-access
                    nodes = [n for n in sub_sub_circ._nodes if n != '/'] # pylint: disable=protected-access
                    cir_file.write(reduce(lambda x, y: str(x).lower() + ' ' + str(y).lower(),
                                          nodes))
                    cir_file.write(f' {name}')
                    for k, v in sub_sub_circ._dict_parameters.items(): # pylint: disable=protected-access
                        if k == 'model':
                            continue
                        cir_file.write(f' {k}={v}')
                    cir_file.write('\n')
                cir_file.write('.ENDS\n')
                line_to_write = '\n'

    @property
    def _module_folder(self) -> str:
        """The module source folder."""
        return join(self._hw_folder, self._module_name)

    @property
    def _cir_file(self) -> str:
        """The target CIR file."""
        return join(self._module_folder, f'{self._module_name}.cir')

    @property
    def _rcir_file(self) -> str:
        """The source CIR file."""
        return join(self._module_folder, f'{self._module_name}.rcir')

    def _print(self, txt: str) -> None:
        """Print the given text."""
        if self._verbose:
            print(txt)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', help='Enable verbose output', action='store_true')
    # parser.add_argument('-l', help='Enable time log output', action='store_true')
    # parser.add_argument('-i', help='Enable intermediate SVG output', action='store_true')
    parser.add_argument('-m', help='Hardware module name')
    # parser.add_argument('-k', help='Keep temp SVG files', action='store_true')
    args = parser.parse_args()

    if not args.m:
        m_name = TOP_MODULE # pylint: disable=invalid-name
        print(f'No module chosen, selected top module: {TOP_MODULE}')
    else:
        m_name = args.m

    circ_parser = CircParser(m_name)
    circ_parser.parse()
    circ_parser.write()
