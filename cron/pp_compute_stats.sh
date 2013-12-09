#!/bin/bash
cd /home/eddie/parksplazas  && ./bin/myapp
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#cd $DIR
#pwd
#cd ..
pwd
date
which python
nohup python $HOME/parksplazas/stats.py >> $HOME/parksplazas/log/stats.log &
