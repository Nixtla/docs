import sys
from pathlib import Path

new_domain = f'https://nixtla.mintlify.app/{sys.argv[1]}'

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirecting...</title>
    <script type="text/javascript">
        window.location.replace('{new_url}');
    </script>
</head>
<body>
    <p>If you are not redirected, <a href="{new_url}">click here</a>.</p>
</body>
</html>"""

pages_dir = Path('gh-pages')
for page in Path('nbs').rglob('*.ipynb'):
    rel_page = page.with_suffix('.html').relative_to('nbs')
    new_path = pages_dir / rel_page
    new_path = new_path.parent / new_path.name.lower()
    new_path.parent.mkdir(exist_ok=True, parents=True)
    content = template.format(new_url=f'{new_domain}/{rel_page}')
    new_path.write_text(content)
