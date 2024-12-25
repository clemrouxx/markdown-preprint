from mistletoe import span_token, block_token
import re
import yaml

# Span tokens

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
    parse_group = 3 # Caption is parsed
    def __init__(self, match_obj):
        super().__init__(match_obj)
        self.src = match_obj.group(1)
        self.label = match_obj.group(2)
    
class LabeledEquation(span_token.SpanToken):
    pattern =  re.compile(r"\$\$([^$]+)\$\$\n?\^(.*)")
    parse_inner = False
    def __init__(self,match_obj):
        super().__init__(match_obj)
        self.inner = match_obj.group(1)
        self.label = match_obj.group(2)

# Block tokens

class Callout(block_token.Quote):
    pattern = re.compile(r" {0,3}> ?\[!(\S+)\]")
    firstline_pattern = re.compile(r" *\[!(\S+)\](.*)$")

    def __init__(self, lines):
        firstline = lines[0][1].pop(0) # Ugly, but it works
        match_obj = self.firstline_pattern.match(firstline)
        self.type = match_obj.group(1).lower()
        self.name = match_obj.group(2).strip()
        super().__init__(lines)
        
    @classmethod
    def start(cls, line):
        match_obj = cls.pattern.match(line)
        if match_obj is None:
            return False
        return True

    @classmethod
    def read(cls, lines): # Parsing is identical to Quote, except that we remove the first line that defines the Callout type
        return super().read(lines)

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
        self.data = yaml.safe_load(''.join(lines))

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
            next(lines) # Remove ending three dashes '---'
        return line_buffer