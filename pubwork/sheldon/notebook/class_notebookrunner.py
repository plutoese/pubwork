import io
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell


def run_notebook(path,start=0,last=None):
    shell = InteractiveShell.instance()
    with io.open(path, 'r', encoding='utf-8') as f:
                nb = read(f, 4)

    result = []
    if last is None:
        last = len(nb.cells)

    for cell_num in range(start,last):
        if nb.cells[cell_num].cell_type == 'code':
            # transform the input to executable Python
            code = shell.input_transformer_manager.transform_cell(nb.cells[cell_num].source)
            # run the code in themodule
        else:
            code = nb.cells[cell_num].source
        result.append(shell.run_cell(code))

    return result

