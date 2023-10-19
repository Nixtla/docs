import yaml


with open('nbs/_quarto.yml', 'rt') as f:
    cfg = yaml.safe_load(f)

cfg['project']['type'] = 'mintlify'
cfg['format'] = {'mintlify-md': True}

with open('nbs/_quarto.yml', 'wt') as f:
    yaml.dump(cfg, f, allow_unicode=True)
