#!/usr/bin/env bash
echo "Copying extension"
mkdir -p nbs/_extensions
cp -r docs-scripts/mintlify nbs/_extensions

echo "Updating quarto"
python docs-scripts/update-quarto.py

echo "Running nbdev_docs..."
nbdev_docs
echo "nbdev_docs is done"

echo "Running docs-final-formatting.bash..."
./docs-scripts/docs-final-formatting.bash
echo "docs-final-formatting.bash is done"

echo "Moving necessary assets..."
cp nbs/mint.json _docs/mint.json
cp docs-scripts/imgs/* _docs/
echo "Done moving necessary assets"

cd ./_docs
mintlify dev
