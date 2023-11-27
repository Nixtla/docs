import re
from functools import partial
from pathlib import Path

def main():
    pattern = r'!\[([^\]]*)\]\(((?!https:\/\/).+?)\)'
    equation_pattern = r'(\$\$[^\$]+\$\$)'
    hyperlink_pat = r'(\[[^\]]*\])(\([^\)]+\))'
    for file in Path('_docs').rglob('*.mdx'):
        content = file.read_text()
        parent = str(file.parent.relative_to('_docs'))
        content = re.sub(pattern, partial(url_replace, parent=parent), content)
        content = re.sub(equation_pattern, multiline_equations, content)
        content = re.sub(hyperlink_pat, standardize_page_name, content)
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


def standardize_page_name(match):
    """Make name lowercase, remove numbers from the beginning and use html suffix."""
    parts = match[2].split('/')
    replaced = re.sub('\d+_', '', parts[-1]).lower().replace('ipynb', 'html')
    url = '/'.join(parts[:-1] + [replaced])
    return f'{match[1]}{url}'


if __name__ == '__main__':
  main()
