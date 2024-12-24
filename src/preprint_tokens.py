from mistletoe import span_token, block_token
import re
import yaml

class Reference(span_token.SpanToken):
    pattern = re.compile(r"\*\*(\S*):(\S+)\*\*")

    def __init__(self, match_obj):
        if match_obj.group(1) == "": # References of the form ':abc' get converted to 'abc'
            self.target = match_obj.group(2)
        else:
            self.target = match_obj.group(1) + ":" + match_obj.group(2)

class Citation(span_token.SpanToken):
    pattern = re.compile(r"@([\w+-]+)")
    def __init__(self, match_obj):
        self.key = match_obj.group(1)

class Label(span_token.SpanToken):
    pattern = re.compile(r"\^(\S+)")
    def __init__(self, match_obj):
        self.name = match_obj.group(1)

class Figure(span_token.SpanToken):
    pattern = re.compile(r'^!\[.*\]\((.*)\)\n?\^(\S*)\s+(.+)$')
    parse_inner = True
    parse_group = 3

    def __init__(self, match):
        super().__init__(match)
        self.src = match.group(1)
        self.label = match.group(2)

class Callout(block_token.Quote):
    pattern = re.compile(r" {0,3}> ?\[!(\S+)\]")

    def __init__(self, lines):
        super().__init__(lines)

    @classmethod
    def start(cls, line):
        match_obj = cls.pattern.match(line)
        if match_obj is None:
            return False
        cls.type = match_obj.group(1).lower()
        return True

    @classmethod
    def read(cls, lines): # Parsing is identical to Quote, except that we remove the first line that defines the Callout type
        next(lines) # first line (already done)
        return super().read(lines)

class LabeledEquation(span_token.SpanToken):
    pattern =  re.compile(r"\$\$([^$]+)\$\$\n?\^(.*)")
    parse_inner = False

    def __init__(self,match):
        super().__init__(match)
        self.inner = match.group(1)
        self.label = match.group(2)

class MainContent(block_token.BlockToken):
    def __init__(self, lines):
        super().__init__(lines,block_token.tokenize)

    @classmethod
    def start(cls, line):
        if line.startswith("#"):
            block_token.remove_token(MainContent) # Janky way to have maximum one MainContent. (and importantly, no MainContent in MainContent)
            return True
        return False

    @classmethod
    def read(cls, lines):
        line_buffer = [next(lines)]
        next_line = lines.peek()
        while next_line is not None: # Here we go until the end of the file
            line_buffer.append(next(lines))
            next_line = lines.peek()
        return line_buffer

class YamlHeader(block_token.BlockToken):
    def __init__(self,lines):
        super().__init__("",span_token.tokenize_inner)
        self.data = yaml.safe_load(''.join(lines).replace("\t","    "))

    @classmethod
    def start(cls,line):
        return line.strip() == "---"

    @classmethod
    def read(cls,lines):
        next(lines)
        line_buffer = []
        next_line = lines.peek()
        while next_line is not None and next_line.strip() != "---":
            line_buffer.append(next(lines))
            next_line = lines.peek()
        if next_line.strip() == "---":
            next(lines) # Remove end '---'
        return line_buffer