#!/usr/bin/env python3
import json
from pathlib import Path

fname = 'docs.json'

def prepend_prefix(item, prefix):
    """Recursively prepend prefix to pages."""
    if isinstance(item, str):
        return f"{prefix}/{item}"
    if 'pages' in item:
        return {**item, 'pages': [prepend_prefix(p, prefix) for p in item['pages']]}
    return item


def merge_navigation(main_nav, sub_nav, prefix):
    """Merge sub navigation into main with prefix."""
    # Find the anchor that matches this repo
    anchor_name_map = {
        'nixtla': 'TimeGPT',
        'statsforecast': 'StatsForecast',
        'mlforecast': 'MLForecast',
        'neuralforecast': 'NeuralForecast',
        'hierarchicalforecast': 'HierarchicalForecast',
        'utilsforecast': 'UtilsForecast',
        'datasetsforecast': 'DatasetsForecast',
        'coreforecast': 'CoreForecast'
    }
    
    anchor_name = anchor_name_map.get(prefix)
    if not anchor_name:
        return main_nav
    
    # Find the matching anchor in main navigation
    anchors = main_nav.get('anchors', [])
    target_anchor = None
    for anchor in anchors:
        if anchor.get('anchor') == anchor_name:
            target_anchor = anchor
            break
    
    if target_anchor:
        # Replace groups and pages from sub navigation into the target anchor
        for key in ['groups', 'pages']:
            if key in sub_nav:
                target_anchor[key] = [prepend_prefix(i, prefix) for i in sub_nav[key]]
    
    # Also update root-level groups if they exist
    # Remove old groups for this prefix and add new ones
    if 'groups' in main_nav and 'groups' in sub_nav:
        # Filter out existing groups for this repo
        main_nav['groups'] = [g for g in main_nav['groups'] 
                              if not any(isinstance(p, str) and p.startswith(f"{prefix}/") 
                                       for p in g.get('pages', []))]
        # Add new groups
        main_nav['groups'].extend([prepend_prefix(i, prefix) for i in sub_nav['groups']])
    
    return main_nav


repos = ['nixtla', 'statsforecast', 'mlforecast', 'neuralforecast',
         'hierarchicalforecast', 'utilsforecast', 'datasetsforecast', 'coreforecast']

main_config = json.loads(Path(fname).read_text())

for repo in repos:
    config_path = Path(repo) / fname
    if config_path.exists():
        sub_config = json.loads(config_path.read_text())
        if 'navigation' in sub_config:
            main_config.setdefault('navigation', {})
            merge_navigation(main_config['navigation'], sub_config['navigation'], repo)


Path(fname).write_text(json.dumps(main_config, indent=2))