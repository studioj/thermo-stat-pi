#!/bin/bash
apt-get update
apt-get upgrade -y
apt-get install -y git openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> .bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
pyenv update
pyenv install 3.9.7
pyenv global 3.9.7
git checkout "https://github.com/studioj/thermo-stat-pi.git" "~/thermo-stat-pi"
cd ~/thermo-stat-pi/central
python -m pip install -r requirements.txt
