

class Poke():
	name = ""
	moves = []
	item = ""
	ability = ""

	def __init__(self, name):
		self.name = name

class Team():
	poke = []

class Player():
	name = ""
	team = []

def loadPlayers():
	''' Make this function to load up previous data '''
	pass

pokes = []
name = raw_input( "Please enter the name of the player: " )
pov = bool( raw_input( "Does Snagem have POV? True or False: " ) )
filename = raw_input( "Enter file to read: " )


with open(filename, "r") as infile:
	for line in infile:
		#Looks for list of name's pokemon and stores them
		if name + "'s" == line.split(' ')[0]:
			pokes.append( line.split(' ')[2] )
			pokes.append( line.split(' ')[4] )
			pokes.append( line.split(' ')[6] )
			pokes.append( line.split(' ')[8] )
			pokes.append( line.split(' ')[10] )
			pokes.append( line.split(' ')[12] )
			#Removes \r\n from last poke
			pokes[5] = pokes[5][:len(pokes[5])-2]