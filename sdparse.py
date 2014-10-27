class Poke():
	name = ""
	hasNick = False
	nick = ""
	moves = []
	item = ""
	ability = ""

	def __init__(self, name):
		self.name = name

pokes = []
name = raw_input( "Who do you want to track: " )
pov = bool( raw_input( 
	"Does that player have POV? Leave blank for false: " ) )
team = raw_input( "What team is the player on: " )
filename = raw_input( "Enter file to read: " )
currentPoke = 0 # Index for current pokemon
sendMessage = []
attMessage = []

if pov:
	sendMessage.append("Go!")
	sendSplit = 1
	attMessage.append("")
else:
	sendMessage.append(name)
	sendMessage.append( "sent" )
	sendMessage.append( "out" )
	# Takes into account names with spaces
	sendSplit = len(name.split(' ')) + len(sendMessage) - 1

print "sendMessage =", sendMessage
print "sendSplit =", sendSplit
print "len(name).split =", len(name.split(' '))

with open(filename, "r") as infile:
	for line in infile:
		# Looks for list of name's pokemon and stores them.
		# Have to make the line you check is at least as long as
		# the player's name. Then if the player has a name with
		# multiple words, just check the last one for the 's.
		# Should catch the first instance as the team immediately.
		# If anyone types their name with a 's and it catches again
		# we'll only pay attention to the first 6 instances so
		# it won't matter.
		match = False
		if len(line.split(' ')) > len(name.split(' '))-1:
			if name.split(' ')[len(name.split(' '))-1] + "'s" == \
			line.split(' ')[len(name.split(' '))-1]:
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +1]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +3]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +5]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +7]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' ')) +9]) )
				pokes.append( 
					Poke(line.split(' ')[len(name.split(' '))+11]) )
				#Removes \r\n from last pokemon
				pokes[5].name = pokes[5].name[:len(pokes[5].name)-2]
				match = False
		
		# Find the current poke. If the pattern maches,
		# it's a switch line. First check looks for the
		# matching opening line. Second check looks for
		# the name of the pokemon.
		if sendMessage == line.split(' ')[0:sendSplit]:
			# Used to index current pokemon
			curr = 0
			# Used to index name of pokemon in case of nicknames
			indexOfName = 0 
			# Go through each word looking for the name of a pokemon
			for word in line.split(' '):
				for e in pokes:
					# Checks for names without nicknames
					if e.name + "!\r\n" == word:
						print "Switched to", e.name
						currentPoke = curr
						break
					# Names found like this mean there is a
					# nickname somewhere
					elif "(" + e.name +")!\r\n" == word:
						if not e.hasNick:
							for i in range(sendSplit, indexOfName):
								e.nick += line.split(' ')[i] + " "
							# Removes trailing whitespace
							e.nick = e.nick[0:len(e.nick)-1]
							e.hasNick = True
						currentPoke = curr
						break
					else:
						curr += 1
				curr = 0
				indexOfName += 1

		# Looks to see if the current pokemon uses a new move 