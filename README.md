# markdown-preprint

Markdown-preprint is a Markdown-to-LaTeX compiler based on the [mistletoe project](https://github.com/miyuchina/mistletoe.git), but specifically focused on writing scientific reports or preprints. Compared to other converters, this one interpretes the markdown syntax slightly differently (for example, all inserted images must have a label and caption, and are compiled into LaTeX figures). More syntax is also added to add features to Markdown such as references, citations, author lists, etc.

# Getting started

To use this script, you will need Python 3 with the packages detailed in the requirements.txt file. If you want to compile the LaTeX, you also need pdfLaTeX (it normally comes when installing a LaTeX distribution, such as MiKTeX).

After downloading the code, you can run the function `renderToLaTeX` with your file name as argument to generate the LaTeX code.
Alternatively, the function `renderPDF` also compiles the LaTeX to produce a PDF file.

The "main.py" file can also be called in the command line. It takes a file path and a file name as arguments, and by default does a "quick render" of your markdown to PDF.

You will find an example of markdown file, including most added features in the "example" folder. You can try to compile it yourself to see if everything works.

# How to write markdown for markdown-preprint

Docs coming soon... in the meantime, looking at the example markdown file should give you a good idea.

# Using markdown-preprint in Obsidian

I use Obsidian to take notes and edit markdown files. So I made this script to work especially well with this editor, although you can use any markdown-editor you prefer. 
The code in the "main.py" file can be called using the Obsidian plugin "Python Scripter" for a very fast and convenient workflow.