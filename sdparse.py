

class Poke():
	name = ""
	moves = []
	item = ""
	ability = ""

	def __init__(self, name):
		self.name = name

pokes = []
name = raw_input( "Please enter the name of the player: " )
pov = bool( raw_input( "Does Snagem have POV? True or False: " ) )
filename = raw_input( "Enter file to read: " )


with open(filename, "r") as infile:
	for line in infile:
		#Looks for list of name's pokemon and stores them
		if name + "'s" == line.split(' ')[0]:
			pokes.append( Poke(line.split(' ')[2]) )
			pokes.append( Poke(line.split(' ')[4]) )
			pokes.append( Poke(line.split(' ')[6]) )
			pokes.append( Poke(line.split(' ')[8]) )
			pokes.append( Poke(line.split(' ')[10]) )
			pokes.append( Poke(line.split(' ')[12]) )
			#Removes \r\n from last poke
			pokes[5].name = pokes[5].name[:len(pokes[5].name)-2]