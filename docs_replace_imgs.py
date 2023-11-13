import re
from functools import partial
from pathlib import Path

def main():
    pattern = r'!\[(.*)\]\(((?!https:\/\/).+?)\)'
    for file in Path('_docs').rglob('*.mdx'):
        content = file.read_text()
        parent = str(file.parent.relative_to('_docs'))
        content = re.sub(pattern, partial(url_replace, parent=parent), content)
        file.write_text(content)

def url_replace(match, parent):
    new_url = f'{parent}/{match[2]}'
    if not new_url.startswith('/'):
      new_url = '/' + new_url
    return f'![{match[1]}]({new_url})'


if __name__ == '__main__':
  main()
