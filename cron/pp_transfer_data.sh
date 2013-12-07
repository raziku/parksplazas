DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
cd ..
date
nohup python transfer_data.py >> ./log/transfer.log &