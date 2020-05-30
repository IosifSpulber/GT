import ipdb
from pprint import pprint

import sys
import re

winCount = 0
winRate = 0
winBounties = [0, 0, 0, 0]
winBountiesRates = [0, 0, 0, 0]
loseCount = 0
loseBounties = [0, 0, 0, 0]
loseBountiesRates = [0, 0, 0, 0]
sprintsWon = 0

def parse(fileName):
    global winCount
    global winRate
    global winBounties
    global winBountiesRates
    global loseCount
    global loseBounties
    global loseBountiesRates
    global sprintsWon

    with open(fileName, 'r') as file:
        # Reset stats
        winCount = 0
        winRate = 0
        winBounties = [0, 0, 0, 0]
        winBountiesRates = [0, 0, 0, 0]
        loseCount = 0
        loseBounties = [0, 0, 0, 0]
        loseBountiesRates = [0, 0, 0, 0]
        sprintsWon = 0

        content = file.read()

        # Strip potential email file line endings.
        content = content.replace("=\n", "")

        regex = re.compile(r"PokerStars Grand Tour Tournament.*\n4 players\n(..*\n)*\nYou finished in (1st|2nd|3rd|4th) place.(You won the race and a \$([^ ]*) award has been credited to your Stars Account|You started with a value of \$([^ ]*) and finished with (.*))\.\n(\nYou collected ([0-9]*) bounties for a total of USD (.*)\.\n)?")
        it = regex.finditer(content)

        for match in it:
            bounties = 0 if match.groups()[7] is None else int(match.groups()[7])
        
            if match.groups()[1] == '1st':
                if 'won the race' in match.groups()[2]:
                    sprintsWon += 1

                winBounties[bounties] += 1

                winCount += 1
            else:
                loseBounties[bounties] += 1

                loseCount += 1
        
        total = winCount + loseCount
        winRate = winCount * 1.0 / total
        totalBounties = 0
        for i in range(0, 4):
            totalBounties += winBounties[i] * i
            totalBounties += loseBounties[i] * i
        for i in range(0, 4):
            winBountiesRates[i] = winBounties[i] * 1.0 / winCount
            loseBountiesRates[i] = loseBounties[i] * 1.0 / loseCount
        bountyRate = totalBounties * 1.0 / total
    
        print('====== Parsed stats ======')
        print('Total games: {}'.format(total))
        print('Won tables: {:.2f}%'.format(100 * winRate))
        print('Bounties per game: {:.2f}'.format(bountyRate))
        print('# of bounties when winning:\n\t0: {:.2f}%\n\t1: {:.2f}%\n\t2: {:.2f}%\n\t3: {:.2f}%'.format(winBountiesRates[0] * 100.0, winBountiesRates[1] * 100.0, winBountiesRates[2] * 100.0, winBountiesRates[3] * 100.0))
        print('# of bounties when busting:\n\t0: {:.2f}%\n\t1: {:.2f}%\n\t2: {:.2f}%\n\t3: {:.2f}%'.format(loseBountiesRates[0] * 100.0, loseBountiesRates[1] * 100.0, loseBountiesRates[2] * 100.0, loseBountiesRates[3] * 100.0))

rake = 0.10
tiers = [1, 2, 5, 12, 25, 60]

def calculateEV(startTier):
    global winCount
    global winRate
    global winBounties
    global winBountiesRates
    global loseCount
    global loseBounties
    global loseBountiesRates
    global sprintsWon
    global tiers

    tiers = tiers[tiers.index(startTier):]

    won = {}
    ownBounty = tiers[0] * (1 - rake) # NB: This isn't weighted down by the winrate throughout the calculation.

    print('\n====== EV calculation ======')

    for tier in tiers:
        #ipdb.set_trace()
        initialBounty = tier * (1 - rake)

        avgTableBounty = (ownBounty + 3 * initialBounty) / 4
        if avgTableBounty > 10.80:
            bountyCashFactor = 0.4
        else:
            bountyCashFactor = 0.5

        # NB: We assume all players at the table (except us) have initial bounties
        # NB: We assume the multiplier is the average one (2x)

        ###############################
        # Winnings when busting table #
        ###############################

        # NB: own bounty is irrelevant

        wonWhenBust = 0

        # 1 bounty
        wonWhenBust += loseBountiesRates[1] * (bountyCashFactor * initialBounty)

        # 2 bounties (initial bounties)
        wonWhenBust += loseBountiesRates[2] * (2 * bountyCashFactor * initialBounty)

        ###############################
        # Winnings when winning table #
        ###############################

        wonWhenWon = 0

        # 1 bounty from someone who knocked two other players out
        wonWhenWon += winBountiesRates[1] * (bountyCashFactor * (initialBounty + 2 * (1 - bountyCashFactor) * initialBounty))
        ownBounty += winBountiesRates[1] * ((1 - bountyCashFactor) * (initialBounty + 2 * (1 - bountyCashFactor) * initialBounty))

        # 2 bounties : 1 initial bounty + 1 from someone who knocked a player out
        wonWhenWon += winBountiesRates[2] * (bountyCashFactor * initialBounty + bountyCashFactor * (initialBounty + (1 - bountyCashFactor) * initialBounty))
        ownBounty += winBountiesRates[2] * ((1 - bountyCashFactor) * initialBounty + (1 - bountyCashFactor) * (initialBounty + (1 - bountyCashFactor) * initialBounty))

        # 3 bounties
        wonWhenWon += winBountiesRates[3] * (3 * bountyCashFactor * initialBounty)
        ownBounty += winBountiesRates[3] * (3 * (1 - bountyCashFactor) * initialBounty)

        won[tier] = winRate * wonWhenWon + (1 - winRate) * wonWhenBust

        print('Buy-in ${}:'.format(tier))
        print('\tExpected winnings: ${:.2f}'.format(won[tier]))
        print('\t\tfrom busting: ${:.2f}'.format((1 - winRate) * wonWhenBust))
        print('\t\tfrom winning: ${:.2f}'.format(winRate * wonWhenWon))
        print('\tExpected own bounty when winning: ${:.2f}'.format(ownBounty))

    totalStr = "\nTotal EV: "
    total = 0
    for i in range(len(tiers)):
        weighted = won[tiers[i]] * (winRate ** i)
        total += weighted
        totalStr += '{:.2f}'.format(weighted) + " + "
    weightedBounty = ownBounty * (winRate ** len(tiers))
    total += weightedBounty
    totalStr += '{:.2f}'.format(weightedBounty)
    totalStr += " = " + '{:.2f}'.format(total)
    print(totalStr)

    roi = (total - tiers[0]) / tiers[0]
    print("ROI: {:.2f}%".format(100 * roi))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Expecting args: <filename> <starting tier>")
        sys.exit(-1)
    
    startTier = int(sys.argv[2])
    if startTier not in tiers:
        print("Invalid tier supplied: {}, choose one from {}".format(startTier, tiers))
        sys.exit(-1)

    parse(sys.argv[1])
    calculateEV(startTier)
