class Poke():
	name = ""
	moves = []
	item = ""
	ability = ""

	def __init__(self, name):
		self.name = name

pokes = []
name = raw_input( "Who do you want to track: " )
pov = bool( raw_input( "Does that player have POV? Leave blank for false: " ) )
team = raw_input( "What team is the player on: " )
filename = raw_input( "Enter file to read: " )
currentPoke = 0 #Index for current pokemon
sendMessage = []

if pov:
	sendMessage = "Go!"
	sendSplit = 2
else:
	sendMessage.append(name)
	sendMessage.append( "sent" )
	sendMessage.append( "out" )
	sendSplit = 3

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
			#Removes \r\n from last pokemon
			pokes[5].name = pokes[5].name[:len(pokes[5].name)-2]
		
		#Find the current poke. If the pattern maches,
		#it's a switch line.
		elif sendMessage == line.split(' ')[0:sendSplit]:
			curr = 0
			#Go through each word looking for the name of a pokemon
			for word in line.split(' '):
				for e in pokes:
					#Both checks are needed in case of nicknames
					if e.name + "!\r\n" == word or \
					"(" + e.name +")!\r\n" == word:
						currentPoke = curr
						print "Found! at", currentPoke
						break
					else:
						curr += 1
				curr = 0