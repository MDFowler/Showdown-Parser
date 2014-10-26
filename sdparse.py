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
currentPoke = 0 # Index for current pokemon
sendMessage = []

if pov:
	sendMessage.append("Go!")
	sendSplit = 1
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
				pokes.append( Poke(line.split(' ')[2]) )
				pokes.append( Poke(line.split(' ')[4]) )
				pokes.append( Poke(line.split(' ')[6]) )
				pokes.append( Poke(line.split(' ')[8]) )
				pokes.append( Poke(line.split(' ')[10]) )
				pokes.append( Poke(line.split(' ')[12]) )
				#Removes \r\n from last pokemon
				pokes[5].name = pokes[5].name[:len(pokes[5].name)-2]
				match = False
				print "Got the team!"

		#print line.split(' ')[0:sendSplit]
		
		# Find the current poke. If the pattern maches,
		# it's a switch line.
		#print sendMessage, "==", line.split(' ')[0:sendSplit]
		if sendMessage == line.split(' ')[0:sendSplit]:
			curr = 0
			# Go through each word looking for the name of a pokemon
			for word in line.split(' '):
				for e in pokes:
					# Both checks are needed in case of nicknames
					if e.name + "!\r\n" == word or \
					"(" + e.name +")!\r\n" == word:
						currentPoke = curr
						print "Found! at", currentPoke
						break
					else:
						curr += 1
				curr = 0