import os
import sys
print("os.path.dirname(sys.executable): ", os.path.dirname(sys.executable))
print("sys.version: ", sys.version)
print('os.system("where python"):')
os.system("where python")
'''
import win32com.shell.shell as shell
ASADMIN = 'asadmin'

if sys.argv[-1] != ASADMIN:
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
    sys.exit(0)
'''
