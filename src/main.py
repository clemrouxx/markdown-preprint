from mistletoe import Document
from preprint_renderer import PreprintRenderer
import os
import sys

# Useful functions to call from external script

def renderToLaTeX(file_in:str, file_out=None, encoding='utf-8',debug=False):
    with open(file_in, 'r', encoding=encoding) as f:
        with PreprintRenderer() as renderer:
            doc = Document(f)
            rendered = renderer.render(doc)
    if file_out is not None:
        with open(file_out,'w',encoding=encoding) as f:
            f.write(rendered)
    if debug:
        return doc,rendered
    return rendered

# Directly from md to pdf
def renderPDF(file_in:str,encoding='utf-8',quickrender=False,clean=False,runbiber=False,debug=False):
    tex_file = file_in.replace(".md",".tex")
    raw_file = file_in.replace(".md","")

    ret = renderToLaTeX(file_in,encoding=encoding,file_out=tex_file,debug=debug) # md -> LaTeX
    if debug:
        doc_tree,rendered = ret

    os.system(f'pdflatex "{tex_file}" -quiet') # LaTeX -> PDF (first pass)
    if runbiber:
        os.system(f'biber "{raw_file}" -quiet')
    if not quickrender:
        os.system(f'pdflatex "{tex_file}" -quiet') # Second pass

    if clean:
        os.system(f'del "{raw_file}.aux"')
        os.system(f'del "{raw_file}.bbl"')
        os.system(f'del "{raw_file}.bcf"')
        os.system(f'del "{raw_file}.blg"')
        os.system(f'del "{raw_file}.out"')
        os.system(f'del "{raw_file}.run.xml"')
        os.system(f'del "{raw_file}.toc"')
        os.system(f'del "{raw_file}.loc"')
        if not debug:
            os.system(f'del "{raw_file}.log"')
            os.system(f'del "{tex_file}"')
    
    if debug:
        return doc_tree

# So that this file can be run directly by Obsidian through the python scripter plugin.
if __name__ == "__main__":
    file_path = sys.argv[1]
    file_name = sys.argv[2]
    steps = file_name.split("/")
    file_path += "/" + "/".join(steps[:-1])
    file_name = steps[-1]
    os.chdir(file_path)
    renderPDF(file_name,quickrender=True)
    print("Rendering finished !")
    