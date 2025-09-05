#!/bin/bash

# Backup the shap directory before making changes
cp -r shap shap_backup

# Comment out numba imports and decorators in Python files
sed -i 's/^import numba/#import numba/' shap/explainers/pytree.py
sed -i 's/^from numba import/#from numba import/' shap/explainers/_exact.py
sed -i 's/^from numba import/#from numba import/' shap/explainers/_partition.py
sed -i 's/^import numba/#import numba/' shap/links.py
sed -i 's/^@numba\.njit/#@numba.njit/' shap/links.py
sed -i 's/^import numba\.typed/#import numba.typed/' shap/maskers/_image.py
sed -i 's/^from numba import/#from numba import/' shap/maskers/_image.py
sed -i 's/^from numba import/#from numba import/' shap/maskers/_tabular.py
sed -i 's/^from numba import/#from numba import/' shap/utils/_clustering.py
sed -i 's/^from numba import/#from numba import/' shap/utils/_masked_model.py
sed -i 's/^@numba\.jit/#@numba.jit/' shap/explainers/pytree.py

# Comment out specific numba.typed.List line in shap/maskers/_image.py
sed -i 's/^\s*q = numba\.typed\.List/#q = numba.typed.List/' shap/maskers/_image.py

# Comment out numba in requirements.txt if present
if grep -q "numba" requirements.txt; then
    sed -i 's/^numba/#numba/' requirements.txt
fi

# Comment out numba in setup.py if present
if grep -q "numba" setup.py; then
    sed -i "s/'numba'/# 'numba'/" setup.py
fi

echo "Numba references have been commented out in the specified files."
echo "Backup of shap directory created at shap_backup."
echo "You can now reinstall SHAP with: pip install -e ."
