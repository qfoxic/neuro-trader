import os
import shutil
import compileall

shutil.rmtree('built', ignore_errors=True)
os.makedirs('built', exist_ok=True)
shutil.copy('main.pyw', 'built')
shutil.copy('config.ini', 'built')
compileall.compile_dir('built', force=True)
shutil.copytree(os.path.join('lib', '__pycache__'), os.path.join('built', 'lib', '__pycache__'), dirs_exist_ok=True)
