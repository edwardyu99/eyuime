rem #!/bin/bash
rem uv pip freeze | sed 's/==.*$//' | grep -v '@' > requirements.txt
rem sed -i 's/^ta-lib$/ta-lib==0.4.28/' requirements.txt
rem sed -i 's/^pystan$/pystan==3.10.0/' requirements.txt
uv pip install --upgrade -r requirementswin.txt
rem # uv pip install --upgrade -r <(uv pip freeze)
