import re
from functools import partial
from pathlib import Path

def main():
    pattern = r'!\[([^\]]*)\]\(((?!https:\/\/).+?)\)'
    equation_pattern = r'(\$\$[^\$]+\$\$)'
    for file in Path('_docs').rglob('*.mdx'):
        content = file.read_text()
        parent = str(file.parent.relative_to('_docs'))
        content = re.sub(pattern, partial(url_replace, parent=parent), content)
        content = re.sub(equation_pattern, multiline_equations, content)
        file.write_text(content)

def url_replace(match, parent):
    if parent == '.':
        new_url = match[2]
    else:
        new_url = f'{parent}/{match[2]}'
    if not new_url.startswith('/'):
      new_url = '/' + new_url
    return f'![{match[1]}]({new_url})'


def multiline_equations(matches):
    match = matches[1]
    if '\n' not in match:
        return match
    symbols = match.replace('$', '')
    return f'$$\n{symbols}\n$$'


if __name__ == '__main__':
  main()
