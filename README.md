# markdown-preprint

Markdown-preprint is a Markdown-to-LaTeX compiler based on the [mistletoe project](https://github.com/miyuchina/mistletoe.git), but specifically focused on writing scientific reports or preprints. Compared to other converters, this one interpretes the markdown syntax slightly differently (for example, all inserted images must have a label and caption, and are compiled into LaTeX figures). More syntax is also added to add features to Markdown such as references, citations, author lists, etc.

# Getting started
Requirements : 
- Python 3.10+
- Python packages from requirements.txt
- For LaTeX compilation : pdfLaTeX (it normally comes when installing a LaTeX distribution, such as MiKTeX).

After downloading the code, you can run the function `renderToLaTeX(input_file_name,output_file_name)` to generate the LaTeX code.
The function `renderPDF(file_name)` also compiles the LaTeX to produce a PDF file.

The "main.py" file can also be called in the command line. It takes a file path and a file name as arguments, and by default does a "quick render" of your markdown to PDF.

You will find an example of markdown file, including most added features in the "example" folder. You can try to compile it yourself to see if everything works.

# How to write markdown for markdown-preprint

Docs coming soon... in the meantime, looking at the example markdown file should give you a good idea.

## YAML Header

Some information can be included in a YAML header (see the example file) at the start of the Markdown file. Recognized YAML fields are : 
- title
- author (name, with affiliation in parentheses)
- authors (list of authors)
- packages (list of LaTeX packages to use)
- include-in-header (string of LaTeX code that will be included as given after packages imports)
- conversion-options (list of opt-ins for the markdown-LaTeX conversion). List of recognized conversion options : 
    - render-displaymath-as-equations

# Using markdown-preprint in Obsidian

I use Obsidian to take notes and edit markdown files. So I made this script to work especially well with this editor, although you can use any markdown-editor you prefer. 
The code in the "main.py" file can be called using the Obsidian plugin "Python Scripter" for a very fast and convenient workflow.
