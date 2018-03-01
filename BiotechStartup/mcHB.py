#!/anaconda/bin/python

import scipy, math, re
from scipy import stats
from scipy.stats import norm, lognorm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

############################# 
# Program: mcsimulation v.0.1
# Created: H.A. Boer, August 15, 2010 
#
# Function: 
# Reads the input file 'filename' to be given in the input section
# and performs a Monte Carlo simulation on the data provided the distributions
# to be used are the normal distribution, the log-normal distribution, the
# triangular distribution, and the uniform distribution.
# Note: the lognormal distribution is not working yet and has to be fixed in the next version!
#############################

#draw = int(raw_input("How many draws do you want to perform?\n"))
draw = 1000
filename = '/Users/harryboer/Desktop/InTray/Python_Programs/MonteCarlo/mcarlo_Biovec.txt'

class Mcnode:
    def __init__(self, distribution, mean, stdv, c, years):
        self.distribution = int(distribution)
        self.mean = float(mean)
        self.stdv = float(stdv)
        self.c = float(c)
        self.years = int(years)

node=[] # initialize the node list
f = open(filename) # open the file
for line in f:
    if not line.strip(): # skip empty lines
        continue
    elif re.match('[a-zA-Z]', line):
        continue
    else:
        node_no, distribution, mean, stdv, c, years = line.split()
        #print node_no, distribution, mean, stdv, c, years # Here the nodes are printed out
        x = Mcnode( distribution, mean, stdv, c, years )
        node.append(x)

tot_profit, total_profit, result_node_0, result_node_1, result_node_2, result_node_3, result_node_4 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 
gross_profit, revenue, costs, nprofit, profit, totnpv, totsalvage, b = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

# must be adapted for each new situation
DISCOUNT_RATE, GROWTH_RATE, RDCOST, MARKETING, YRS = 0.05, 0.04, 7, 7, 8

# Payoff definitions
def payoffnode_0(x):
    return float(x)

def payoffnode_1(x,y): # Market share = E^2/(E^2 + A^2)
    y = float(x)**2/(float(x)**2 + float(y)**2) -0.4# minus 40% to make it around 10%
    if y > 0: return y
    else: return 0

def payoffnode_2(x):
    if x > 84:
        return 1
    else:
        return 0

def payoffnode_3(x):
    if x > 0.50:
        return int(1)
    else:
        return int(0)

def payoffnode_4(x):
    return float(x)

# etc. for more payoffnode_5(x), 6(x),...,n(x) definitions

def salvage(x,y):
    return float(x)/(float(x) + float(y)) * 10

# The pay-off of each node will be different for each new valuation and
# should be adapted if so required.
market_size, market_share, efficacy, inverse, npv, result = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

npvlist = []
totnpvlist = []
marketsharelist = []
marketsharelist2 = []
marketsizelist = []
efficacylist = []
efficacylist2 = []
alternativelist = []

i = 1
for i in range(draw):
    j = 0
    while j <= len(node)-1: # the length of the node is 3, however, we count j=0, 1, 2, 3
        
        # check which distribution belongs to what node and calculate the inverse
        # in each j++ round, the inverse gets a new value assigned to it, so we don't need to reset it
        for node_no in node: 
            if node[j].distribution == 3:  # Triangular Distribution
                phi = np.random.random()
                if phi <= (node[j].c - node[j].mean)/(node[j].stdv - node[j].mean):
                    inverse = node[j].mean + math.sqrt(phi * (node[j].c - node[j].mean) * (node[j].stdv - node[j].mean))
                else:
                    inverse = node[j].stdv - math.sqrt( (1-phi) * (node[j].stdv - node[j].c) * (node[j].stdv - node[j].mean))
                    
            elif node[j].distribution == 4:  # Uniform Distribution
                inverse = np.random.random()

            elif node[j].distribution == 1:  # Normal Distribution
                phi = np.random.random()
                inverse = norm.ppf(phi, loc=node[j].mean, scale=node[j].stdv)

            elif node[j].distribution == 2:  # Lognormal Distribution
                phi = np.random.random()
                inverse = math.exp(norm.ppf(lognorm.cdf(phi, loc=node[j].mean, scale=node[j].stdv)))
                
			# now put the inverse into the right result
            if j == 0:
                result_node_0 = inverse # = Market Size
                marketsizelist.append(result_node_0)
            elif j == 1:
                result_node_1 = inverse # = Alternative efficacy
                alternativelist.append(result_node_1)
            elif j == 2:                        
                result_node_2 = inverse # = Efficacy
                efficacylist2.append(result_node_2)
            elif j == 3:
                result_node_3 = inverse 
                
            j += 1
            # END READING THE NODES and the inverse of them
            # next we must calculate the payoffs of this draw
            
    if payoffnode_2(result_node_2) == 0: #No FDA approval START MAIN IF STATEMENT. The R&D costs are spend and there is no salvage value
        npv = -RDCOST
        npvlist.append(npv)
        totnpvlist.append(totnpv)
        marketsharelist.append(payoffnode_1(result_node_2, result_node_1)) # this is line 144; comment out when wanting to show market share
        marketsharelist2.append(payoffnode_1(result_node_2, result_node_1))
        efficacylist.append(payoffnode_2(result_node_2))
        totnpv = totnpv + npv
        #print "No FDA approval during draw %d and totnpv is %.2f" % (i, totnpv)
        # and then everything stops here => GoTo next draw
   
    else:
        gross_profit = (payoffnode_0(result_node_0) * payoffnode_1(result_node_2, result_node_1) * payoffnode_2(result_node_2))
        salvage_value = salvage(result_node_2, result_node_1)/((1 + DISCOUNT_RATE)**node[2].years)
        
        # Spread Sheet calculation: calculate profit for the next YRS years
        k = 0
        while k <= (YRS-1):
            revenue = (gross_profit * (1 + GROWTH_RATE)**k)
            costs = 0.25 * revenue # only valid for Biovec, as they are not involved in marketing
            #costs = (MARKETING * (1 + GROWTH_RATE)**k) # in year k=0, costs=marketing
            profit = (revenue - costs)/((1 + DISCOUNT_RATE)**k) # each profit stream gets discounted immediately from year "node[len(node)].years" onward
            npv = npv + profit # the sum of the discounted profits
            revenue = 0
            costs = 0
            k += 1
            
        # now the value for the npv is corrected for the half year effect and discount back from year years to 0
        #npv = npv * (1 + DISCOUNT_RATE)**0.5/((1 + DISCOUNT_RATE)**node[2].years) - RDCOST
        npv = npv * (1 + DISCOUNT_RATE)**0.5/((1 + DISCOUNT_RATE)**5) - RDCOST
        npvlist.append(npv)
        marketsharelist.append((payoffnode_1(result_node_2, result_node_1))*100) # multiply by 100 to make it %
        efficacylist.append(result_node_2)

        if npv < salvage_value - RDCOST:
            totnpv = totnpv + salvage_value - RDCOST
            totnpvlist.append(totnpv)
        else:
            totnpv = totnpv + npv
            totnpvlist.append(totnpv)

    # reset all values to prepare for the next draw
    inverse, result_node_0, result_node_1, result_node_2, result_node_3, result_node_4 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    npv = 0
    #print "Draw %d" % i
    #END MONTE CARLO SIMULATION (while i <= draw block); it ends here or => "next draw"
    
# plotting starts here  

# FIGURE I.
fig = plt.figure(1, figsize=(12,10)) #*******************

# 1.1 ---------
ax = fig.add_subplot(221)
n, bins, patches = plt.hist(marketsizelist, 50, normed=1, facecolor='b', alpha=0.75)
plt.title('A. Market Size', fontsize=12)
plt.figtext(0.39, 0.95, 'Biovec: Input Variables', fontsize=20)
mu2, sigma2 = 1800, 100
y = mlab.normpdf(bins, mu2, sigma2)
ax.plot(bins, y, 'r', linewidth=1)
plt.xlabel('$mln', fontsize=12)

# 1.2 ------------
ax = fig.add_subplot(222)
n, bins, patches = plt.hist(efficacylist2, 50, normed=1, facecolor='y', alpha=0.75)
plt.title('B. Efficacy', fontsize=12)
mu3, sigma3 = 50, 15
y = mlab.normpdf(bins, mu3, sigma3)
ax.plot(bins, y, 'r', linewidth=1)
plt.xlabel('%', fontsize=12)

# 1.3 ------------
ax = fig.add_subplot(223)
n, bins, patches = plt.hist(alternativelist, 50, normed=1, facecolor='c', alpha=0.75)
plt.title('C. Alternative Efficacy', fontsize=12)
plt.xlabel('%', fontsize=12)

# 1.4 ------------
ax1 = fig.add_subplot(224)

n, bins, patches = plt.hist(marketsharelist2, 5, normed=0, facecolor='r', alpha=0.75)
plt.title('D. Market Share', fontsize=12)
plt.xlabel('%', fontsize=12)
ax2 = ax1.twinx()
#plt.ylim(0,1)
n, bins, patches = plt.hist(marketsharelist, 50, normed=0, facecolor='r', alpha=0.75)
plt.xlim(-5,40)
#plt.savefig('/Users/Harry/Documents/Data/LaTeXfiles/mcpics/figure1.png')

# FIGURE II.
fig = plt.figure(2, figsize=(12,10)) #**********************
plt.figtext(0.42, 0.95, 'Biovec: Results', fontsize=20)

# 2.1 -----------------
ax = fig.add_subplot(221)
ax.scatter(efficacylist2, marketsharelist, s=5, c='r') # this is line 234; comment out when wanting to show market share
plt.xlim(0, 105)
plt.xlabel('Efficacy %', fontsize=12)
plt.ylabel('Market share %', fontsize=12)
plt.title('A. Efficacy vs Marketshare')

# 2.2 -----------------
ax = fig.add_subplot(222)
ax.scatter(efficacylist2, npvlist, s=5) # scatter(x, y)
plt.xlim(0, 105)
plt.xlabel('Efficacy %', fontsize=12)
plt.ylabel('NPV $mln', fontsize=12)
plt.title('B. Efficacy vs Profitability')

# 2.3 -----------
ax = fig.add_subplot(223)
n, bins, patches = plt.hist(npvlist, 50, normed=0, facecolor='b', alpha=0.75)
plt.title('C. NPV view')
plt.ylim(0, 100)
plt.xlabel('$mln', fontsize=12)


# 2.4 ------------
ax = fig.add_subplot(224)
n, bins, patches = plt.hist(npvlist, 50, normed=1, facecolor='g', alpha=0.75)
plt.title('D. NPV view; normalized')
#mu, sigma = 40, 40
#y = mlab.normpdf( bins, mu, sigma )
#ax.plot(bins, y, 'r--', linewidth=1)
plt.xlabel('NPV', fontsize=12)
plt.ylabel('Frequency')
plt.ylim(0, 0.0005)

plt.savefig('/Users/Harry/Documents/Data/LaTeXfiles/mcpics/figure2.png')

plt.show() # to show or not show the plots on screen, that's the question

# to show market share better, first comment out savefig2, line 234 and marketsharelist in line 144

NPV = totnpv/draw #calculate mean of every npv
print("The NPV of the project is $%.2f" % NPV)

