import io
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell


def run_notebook(path):
    shell = InteractiveShell.instance()
    with io.open(path, 'r', encoding='utf-8') as f:
                nb = read(f, 4)

    result = []
    for cell in nb.cells:
        if cell.cell_type == 'code':
            # transform the input to executable Python
            code = shell.input_transformer_manager.transform_cell(cell.source)
            # run the code in themodule
        else:
            code = cell.source
        result.append(shell.run_cell(code))

    return result