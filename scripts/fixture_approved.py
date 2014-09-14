from django.db import models
from core_roottree.models import Command

commands = {
	'Install pip': ['curl https://bootstrap.pypa.io/get-pip.py > get-pip.py; sudo python get-pip.py', 'b'],
	'Install brew': ['ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"', 'b'],
	'Install npm': ['curl -O -L https://npmjs.org/install.sh; sudo sh install.sh', 'b'],
	'Install node': ['ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; brew install node', 'b'],
	'Install clumsy-bird': ['git clone https://github.com/ellisonleao/clumsy-bird.git; npm install; grunt connect; open http://localhost:8001/', 'b'],
	'Upload sketch': ['pip install ino; ', 'b'],
	'Notify desktop': ['osascript -e \'display notification \"%s\" with title \"%s\"\'', 'b']
}

for key,val in commands.iteritems():
	Command.objects.create(name=key, code=val[0], language=val[1])

