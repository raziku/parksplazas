#!/bin/bash
cd /home/eddie/parksplazas
pwd
date
nohup python $HOME/parksplazas/transfer_data.py >> $HOME/parksplazas/log/transfer.log &
