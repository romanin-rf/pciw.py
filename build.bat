@echo off
python builder.py -pv cp39 -st win_amd64 -pdp "{localdir}{sep}pciw{sep}data{sep}t_cpu{sep}Windows-x86_64,{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Windows-x86_64"
python builder.py -pv cp310 -st win_amd64 -pdp "{localdir}{sep}pciw{sep}data{sep}t_cpu{sep}Windows-x86_64,{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Windows-x86_64"
python builder.py -pv py39 -st win_amd64 -pdp "{localdir}{sep}pciw{sep}data{sep}t_cpu{sep}Windows-x86_64,{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Windows-x86_64"
python builder.py -pv py310 -st win_amd64 -pdp "{localdir}{sep}pciw{sep}data{sep}t_cpu{sep}Windows-x86_64,{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Windows-x86_64"

python builder.py -pv cp39 -st manylinux1_x86_64 -pdp "{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Linux-x86_64"
python builder.py -pv cp310 -st manylinux1_x86_64 -pdp "{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Linux-x86_64"
python builder.py -pv py39 -st manylinux1_x86_64 -pdp "{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Linux-x86_64"
python builder.py -pv py310 -st manylinux1_x86_64 -pdp "{localdir}{sep}pciw{sep}data{sep}nsmi{sep}Linux-x86_64"

python setup.py sdist