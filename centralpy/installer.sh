#!/bin/bash
sudo apt-get update
sudo apt-get dist-upgrade -y
sudo apt-get install -y git openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev sqlite3
sudo apt autoremove -y
sudo rm -rf $HOME/thermo-stat-pi
systemctl stop centralpy
systemctl disable centralpy
sudo rm -f /etc/systemd/system/centralpy.service
systemctl daemon-reload
systemctl reset-failed
if ! pyenv global; then
  sudo rm -rf $HOME/.pyenv
  curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init --path)"
  eval "$(pyenv virtualenv-init -)"
  echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> .bashrc
  echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
  echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
else
  pyenv update
fi
if ! $(pyenv versions | grep 3.9.7); then
    pyenv install 3.9.7
fi
pyenv global 3.9.7

checkout() {
  [ -d "$2" ] || git clone --depth 1 "$1" "$2" || failed_checkout "$1"
}
set -e
checkout "https://github.com/studioj/thermo-stat-pi.git" "$HOME/thermo-stat-pi"
cd $HOME/thermo-stat-pi/centralpy
python -m pip install -r requirements.txt
set -x
sed -i "s|USERHOMEDIR|$HOME|" $HOME/thermo-stat-pi/centralpy/centralpy.service
sed -i "s|PYENVPATHONBINPATH|$(pyenv which python)|" $HOME/thermo-stat-pi/centralpy/centralpy.service

sudo cp $HOME/thermo-stat-pi/centralpy/centralpy.service /etc/systemd/system/centralpy.service
sudo systemctl daemon-reload
sudo systemctl start centralpy
sudo systemctl enable centralpy
sudo systemctl restart centralpy
