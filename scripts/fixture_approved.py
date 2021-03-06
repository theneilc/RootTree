from django.db import models
from core_roottree.models import Command, CommandInstance, Session, Task, Developer,\
    ClientUser

for i in Command.objects.all():
	i.delete()

commands = {
	'install_grunt': ["""osascript -e 'display notification "We will let you know when this is done" with title "Installing Grunt!"'; npm install -g grunt-cli; osascript -e 'display notification "Huzzah" with title "Done installing Grunt!"'""",'b'],
	'install_pip': ["""curl https://bootstrap.pypa.io/get-pip.py > get-pip.py; python get-pip.py; rm get-pip.py;osascript -e 'display notification "Pip is installed." with title "Successful!"'""", 'b'],
	'install_brew': ['ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"', 'b'],
	'install_npm': ['curl -O -L https://npmjs.org/install.sh; sudo sh install.sh', 'b'],
	'install_node': ['ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; brew install node', 'b'],
	'install_clumsybird': ["""osascript -e 'display notification "A browser will open up when done" with title "Cloning and setting up!"';git clone https://github.com/ellisonleao/clumsy-bird; cd clumsy-bird; npm install; (grunt connect&); sleep 2; open http://localhost:8001/;""", 'b'],
	'install_ino': ['pip install ino', 'b'],
	'upload_arduino': ['mkdir tutorial_1;cd tutorial_1; ino init; echo "%s"> src/sketch.ino; ino build; ino upload; osascript -e "Sketch uploaded!" with title "Complete!"','b'],
	'notify_desktop': ['osascript -e \'display notification \"%s\" with title \"%s\"\'', 'b'],
	'setup_django_project':['virtual project_root; cd project_root; git clone %s; cd','b']
}

for key,val in commands.iteritems():
	Command.objects.create(name=key, code=val[0], language=val[1])

ci1 = CommandInstance()
ci1.command = Command.objects.all()[3]
ci1.save()

t1 = Task()
t1.commandinstance = ci1
t1.save()

s1 = Session()
s1.uuid = '4'
s1.developer = Developer.objects.all()[0]
s1.client = ClientUser.objects.all()[0]
s1.status = 'P'
s1.commandinstance = ci1
s1.save()

