from mistletoe.latex_renderer import LaTeXRenderer
from preprint_tokens import *
import re

class PreprintRenderer(LaTeXRenderer):
    def __init__(self,include_in_header=""):
        super().__init__(Reference,Citation,Label,Figure,Callout,MainContent,YamlHeader,LabeledEquation)
        self.packages["multicol"] = []
        self.has_bibliography = False
        self.title = ""
        self.header = include_in_header
        self.ending = ""
        self.authors = []
        self.yaml_data = {}
        self.number_all_equations = True

        # The following should rather be part of the style file
        self.packages["geometry"] = []
        self.header = "\\geometry{a4paper,left=20mm,top=20mm}\n"

    def render_reference(self, token):
        if token.target.startswith("eq:"): # Equation : we add parentheses automatically
            template = '(\\ref{{{}}})'
        else:
            template = '\\ref{{{}}}'
        return template.format(token.target)

    def render_citation(self, token):
        self.has_bibliography = True
        self.packages["biblatex"] = []
        template = '\\cite{{{}}}'
        return template.format(token.key)

    def render_label(self, token):
        template = '\\label{{{}}}'
        return template.format(token.name)

    def render_figure(self,token):
        self.packages["graphicx"] = []
        template = """
\\begin{{figure}}
    \\centering
    \\includegraphics[width=\\textwidth]{{{src}}}
    \\caption{{{caption}}}
    \\label{{fig:{label}}}
\\end{{figure}}
        """
        return template.format(src=token.src ,label=token.label,caption=self.render_inner(token))

    def render_callout(self, token):
        template = '\\begin{{{callout_type}}}\n{inner}\\end{{{callout_type}}}\n'
        if token.type == "theorem":
            pass # TODO : implement those (add the necessary packages)
        elif token.type == "proof":
            pass
        return template.format(inner=self.render_inner(token),callout_type=token.type)

    def render_quote(self, token):
        self.packages['csquotes'] = []
        template = '\\begin{{displayquote}}\n{}\\end{{displayquote}}\n'
        return template.format(self.render_inner(token))

    def render_labeled_equation(self,token):
        template = '\\begin{{equation}}\n\t{inner}\n\\label{{eq:{label}}}\\end{{equation}}\n'
        return template.format(inner = token.inner,label=token.label)
    
    def render_table(self, token): # Modified from the inherited version
        def render_align(column_align):
            if column_align != [None]:
                cols = [get_align(col) for col in token.column_align]
                return '{{{}}}'.format('|'.join(cols)) # Added vertical separators. Maybe add this as option ?
            else:
                return ''

        def get_align(col):
            if col is None:
                return 'l'
            elif col == 0:
                return 'c'
            elif col == 1:
                return 'r'
            raise RuntimeError('Unrecognized align option: ' + col)

        template = """
\\begin{{table}}
    \\centering
    \\begin{{tabular}}{align}\n{inner}\n\\end{{tabular}}\n
    \\caption{{{caption}}}
    \\label{{tab:{label}}}
\\end{{table}}
        """
        if hasattr(token, 'header'):
            head_template = '{inner}\\hline\n'
            head_inner = self.render_table_row(token.header)
            head_rendered = head_template.format(inner=head_inner)
        else:
            head_rendered = ''
        inner = self.render_inner(token)
        align = render_align(token.column_align)
        return template.format(inner=head_rendered + inner, align=align, caption="", label="")

    def render_main_content(self,token):
        template = '\\begin{{maincontent}}\n{}\n\\end{{maincontent}}\n'
        return template.format(self.render_inner(token))

    def render_yaml_header(self,token):
        data = token.data
        beginning_str = ""
        if "title" in data:
            self.title = data["title"]
            beginning_str += "\\maketitle\n"
        if "author" in data: # Single author, either just a name or key-value pairs
            self.packages["authblk"] = []
            self.add_author(data["author"])
        elif "authors" in data: # Multiple authors as a list
            self.packages["authblk"] = []
            for author in data["authors"]:
                self.add_author(author)
        if "packages" in data: # Easiest way to add other packages (with no parameters). Expects a list
            for package in data["packages"]:
                self.packages[package] = []
        if "include-in-header" in data: # More verbose way of adding LaTeX in the .tex header
            if type(data["include-in-header"]) == str:
                self.header += data["include-in-header"]+"\n"
            else: # Expect a list of strings in that case
                self.header += "\n".join(data["include-in-header"]) + "\n"
        self.yaml_data = data
        return beginning_str # Will be included where the YAML header is, so normally just after '\begin{document}'

    def add_author(self,author_info):
        if type(author_info) == str:
            author_pattern = re.compile(r'^([^\(]*)(\(.*\))?$') # For having multiple informations in just one string, eg : "Albert Einstein (ETH Zürich)"
            groups = author_pattern.match(author_info)
            author_info = {"name":groups.group(1)}
            if groups.group(2) is not None: # Affiliation
                author_info["affiliation"] = groups.group(2)[1:-1] # Removing the parentheses
        self.authors.append(author_info)

    def render_document(self, token):
        template = ('\\documentclass{{article}}\n'
                    '{packages}'
                    '{header}\n'
                    '\\begin{{document}}\n'
                    '{inner}'
                    '{ending}'
                    '\\end{{document}}\n')
        self.footnotes.update(token.footnotes)
        inner = self.render_inner(token)

        # Data from the YAML header
        if self.title != "":
            self.header += '\\title{{{title}}}\n'.format(title=self.title)
        for i,author in enumerate(self.authors):
            self.header += '\\author[{n}]{{{name}}}\n'.format(n=i+1,name=author["name"])
            if "affiliation" in author:
                self.header += '\\affil[{n}]{{{affil}}}\n'.format(n=i+1,affil=author["affiliation"])
        if "date" in self.yaml_data:
            self.header += '\\date{{{date}}}\n'.format(date=self.yaml_data["date"])
        if self.has_bibliography:
            self.header += "\\addbibresource{bibliography.bib}\n"
            self.ending += "\\printbibliography\n"
        return template.format(inner=inner,
                               packages=self.render_packages(),
                               ending=self.ending,header=self.header)

