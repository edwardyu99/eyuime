#!/bin/bash
uv pip freeze | sed 's/==.*$//' | grep -v '@' > requirements.txt
# sed -i 's/^ta-lib$/shap==0.47.2/' requirements.txt
# sed -i 's/^numpy/numpy==1.26.4/' requirements.txt
# sed -i 's/^prophet$/prophet==1.1.7/' requirements.txt
# sed -i 's/^cmdstanpy$/cmdstanpy==1.2.5/' requirements.txt
# sed -i 's/^cmdstanpy$/cmdstanpy==0.9.5/' requirements.txt
# sed -i 's/^ta-lib$/ta-lib==0.4.28/' requirements.txt
# sed -i 's/^pystan$/pystan==3.10.0/' requirements.txt
# sed -i 's/^onnx$/onnx==1.17.0/' requirements.txt
# sed -i 's/^onnxruntime$/onnxruntime==1.23.2/' requirements.txt
# sed -i 's/^protobuf$/protobuf==5.29.5/' requirements.txt
uv pip install --upgrade -r requirements.txt
# uv pip install --upgrade -r <(uv pip freeze)
