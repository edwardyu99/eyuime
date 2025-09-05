#!/bin/bash
uv pip freeze | sed 's/==.*$//' | grep -v '@' > requirements.txt
# sed -i 's/^ta-lib$/shap==0.47.2/' requirements.txt
# sed -i 's/^numpy/numpy==2.2.6/' requirements.txt
sed -i 's/^ta-lib$/ta-lib==0.4.28/' requirements.txt
sed -i 's/^pystan$/pystan==3.10.0/' requirements.txt
uv pip install --upgrade -r requirements.txt
# uv pip install --upgrade -r <(uv pip freeze)
