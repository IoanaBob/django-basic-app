#takes parameters from element in django template???


#vote id, election id, region id, candidate id, voter id,
a = [(1, 1, 1, 1, 1), (2, 1, 3, 5, 2), (3, 1, 2, 8, 3)]
a = [list(tup) for tup in a]

#registered to vote
#voter id
b = [(1,1), (2,1), (3,1)]
#b = [list(tup) for tup in b]

votersVoted = 0
def voteCount(votersVoted):
	for i in range(len(a)):
		votersVoted += 1
	return(votersVoted)
votersVoted = voteCount(votersVoted)
print(votersVoted)

registeredVoters = 0
def noVote(registeredVoters):
	for i in range(len(b)):
		registeredVoters += 1
	return registeredVoters
registeredVoters = noVote(registeredVoters)
print(registeredVoters)

remainingVotes = registeredVoters - votersVoted
print(remainingVotes)

votersVotedRegion = 0
def voteCountRegion(votersVotedRegion):
	for i in range(len(a)):
		if a[i][2] == 1:
			votersVotedRegion += 1
	return(votersVotedRegion)
votersVotedRegion = voteCountRegion(votersVotedRegion)
print(votersVotedRegion)

registeredVotersRegion = 0
def noVoteRegion(registeredVotersRegion):
	for i in range(len(b)):
		if b[i][1] == 1:
			registeredVotersRegion += 1
	return registeredVotersRegion
registeredVotersRegion = noVoteRegion(registeredVotersRegion)
print(registeredVotersRegion)

remainingVotesRegion = registeredVotersRegion - votersVotedRegion
print(remainingVotesRegion)

candidateVote = 0
def partyVotes(candidateVote):
	for i in range(len(a)):
		if a[i][3] == 1:
			candidateVote += 1
	return candidateVote
candidateVote = partyVotes(candidateVote)
print(candidateVote)

candidateVoteRegion = 0
def candidateVotesRegion(candidateVoteRegion):
	for i in range(len(a)):
		if a[i][3] == 1:
			if a[i][2] == 1:
				candidateVoteRegion += 1
	return candidateVoteRegion
candidateVoteRegion = candidateVotesRegion(candidateVoteRegion)
print(candidateVoteRegion)