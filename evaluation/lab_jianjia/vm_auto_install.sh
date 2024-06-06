sudo apt install vim
sudo apt-get install xfce4 xfce4-goodies -y
sudo apt-get install tightvncserver -y
sudo apt install python
sudo apt install python-pip
pip install tqdm
sudo apt install python3
sudo apt install python3-pip
echo 'alias sangoto="cd /media/data1/zfk/Documents/sanchecker/src"
alias goto="cd /media/data1/zfk/"

export PATH="$PATH:/media/data1/zfk/Documents/depot_tools"
export CAPNP_INSTALL="/media/data1/zfk/Documents/capnproto-install"
export PATH="$PATH:$CAPNP_INSTALL/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CAPNP_INSTALL/lib"

export LC_ALL=C # for pip install to work' >> ~/.bashrc
echo "alias temp_runexe='out/Bytecode/chrome 247sports.com/?__proto__[testk]=testv --js-flags=\"--taint_log_file=/media/data1/zfk/Documents/sanchecker/testdir/247sports --no-crankshaft --no-turbo --no-ignition\" --new-window --no-sandbox --disable-hang-monitor --disable-gpu &> /media/data1/zfk/Documents/sanchecker/src/247sports_log_file'" >> ~/.bashrc

cd /media/data1/zfk/Documents/sanchecker
sudo ./src/build/install-build-deps.sh

sudo dpkg -i /media/data1/zfk/libgcrypt11_1.5.3-2ubuntu4_amd64.deb
