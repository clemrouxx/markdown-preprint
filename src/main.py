from mistletoe import Document
from preprint_renderer import PreprintRenderer
import os
import sys

# Useful functions to call from external script
def renderToLaTeX(file_in:str, file_out=None, encoding='utf-8',):
    with open(file_in, 'r', encoding=encoding) as f:
        with PreprintRenderer() as renderer:
            doc = Document(f)
            rendered = renderer.render(doc)
    if file_out is not None:
        with open(file_out,'w',encoding=encoding) as f:
            f.write(rendered)
    return rendered

def renderPDF(file_in:str,encoding='utf-8',quickrender=False,clean=False):
    tex_file = file_in.replace(".md",".tex")
    raw_file = file_in.replace(".md","")
    renderToLaTeX(file_in,encoding=encoding,file_out=tex_file)
    os.system(f"pdflatex {tex_file} -quiet")
    if not quickrender:
        os.system(f"biber {raw_file} -quiet") # Maybe check if this is necessary ?
        os.system(f"pdflatex {tex_file} -quiet")

    if clean:
        os.system(f"del {raw_file}.aux")
        os.system(f"del {raw_file}.bbl")
        os.system(f"del {raw_file}.bcf")
        os.system(f"del {raw_file}.blg")
        os.system(f"del {raw_file}.out")
        os.system(f"del {raw_file}.run.xml")
        os.system(f"del {raw_file}.toc")
        os.system(f"del {raw_file}.log")

# So that this file can be run directly by Obsidian through the python scripter plugin.
if __name__ == "__main__":
    file_path = sys.argv[1]
    file_name = sys.argv[2]
    steps = file_name.split("/")
    file_path += "/" + "/".join(steps[:-1])
    file_name = steps[-1]
    os.chdir(file_path)
    print("Rendering",file_path,file_name)
    renderPDF(file_name,quickrender=True)
    