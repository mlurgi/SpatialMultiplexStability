ROWS = 50   #200

COLUMNS = 50    #200

ITERATIONS = 3000

#percentage of occupied cells by living organisms in the environment
OCCUPIED_CELLS = 0.4

REFRESH_RATE = 1

SPECIES = 60   #60

CONNECTANCE = 0.08

PROB_NICHE_MODEL = False

#number of iterations (interval) for the recalculation of network metrics
NETWORK_RECORD = 200

#fraction of iterations that will be considered for the species output
ITERATIONS_TO_RECORD = 0.1

#fraction of iterations before the end of the simulation when the network
#state will be reset in order to obtain a snapshot of the current network
NETWORK_RESET = 0.1

#whether to calculate the metrics for quantifying spatial variation among species
SPATIAL_VARIATION = False

RECORD_SPATIAL_VAR = 500

#the fraction of points to remove that are farthest from the centroid of the population
#before calculating the population radius
DISPERSAL_KERNEL = 0.03

##whether to calculate the interaction strengths matrices
INT_STRENGTHS = False

#fraction of primary producer species in the network
PRIMARY_PRODS = 0.25

#percentage of herbivore species in the network
HERBIVORY = 0.25

#fraction of top predator species in the original network
TOP_PREDATORS = 0.05

#whether to double the number of herbivore individuals
DOUBLE_HERBIVORY = False

#minimum nestedness of the mutualistic sub-network
MIN_NESTEDNESS = 0.0

MAX_NESTEDNESS = 0.0

#fraction of herbivores that are mutualists
MUTUALISM = 0.5

#minimum number of mutualists (in case number of herbivores is less than
#1/MUTUALISM number of mutualists desired)
MIN_MUTUALISTS = 0

#maximum amount of resource an individual may possess
MAX_RESOURCE = 20

#minimum amount of resource an individual must possess in order to survive 
MIN_RESOURCE = 3

#fraction of resource an individual expends in living
LIVING_EXPEND = 0.04   #0.04

#fraction of living expenditure applied exclusively to mutualistic animals
MUTUALISTIC_LOSS = 1.0

MUT_PRODUCER_LOSS = 1.0

#fraction of maximum resource that must be available for mating when meeting a 
#suitable partner
MATING_RESOURCE = 0.5    #0.3

#fraction of resource to be given to the offspring when born
MATING_ENERGY = 0.2

#number of neighbour cells that a species can have to find a mate
MATING_SPATIAL_RATIO = 4   #5

#probability per cell in the grid that a new individual from a species
#randomly selected from the initial pool may enter the world
INMIGRATION = 0    #0.001

#fraction of its own resource an individual is able to synthesise (for primary producers)
SYNTHESIS_ABILITY = 0.5

#fraction of the biomass of a primary producer lost to a herbivore consumer
HERBIVORY_FRACTION = 1.0

#fraction of resource that omnivores can assimilate when feeding on primary producers
OMNIVORY_TRADEOFF = 0.4

#fraction of the biomass of a primary producer that a mutualistic partner gets
MUTUALISTIC_FRACTION = 0.25 #0.25

#number of cells, in each direction, an individual can move in a given iteration
MOVE_RADIUS = 1

#number of cells, in each direction, a mutualistic individual can move in a given iteration
MOVE_RADIUS_MUTUALISTS = 1

#number of cells, in each direction, a top predator individual can move in a given iteration
MOVE_RADIUS_TOP = 5

#probability of capture of predators over their prey
CAPTURE_PROB = 0.4 #0.4

#efficiency of energy/resource transfer in animals (predators)
EFFICIENCY_TRANSFER = 2.0   #2.0

#efficiency of energy/resource transfer in herbivores (from plants to herbivore)
HERBIVORY_EFFICIENCY = 0.1   #0.1

#####
#The next parameters are for the reproduction of plants (either via mutualism or by wind dispersal)

#efficiency of the animal mutualists when dispersing a plant
MUTUALISTIC_EFFICIENCY = 0.8

#cooling factor for the efficiency of mutualists for plant dispersal
MUTUALISTIC_COOLING = 0.9

#minimum mutualistic dispersal efficiency after which no more dispersal of the plant
#partner is allowed
MIN_MUTUALISTIC_EFF = 0.1

#probability with which a primary producer with no mutualistic partners will reproduce
REPRODUCTION_RATE = 1.0 #*CONNECTANCE*MUTUALISM

#probability with which the reproduction of species above the basal level is sexual (0 = always asexual - 1 = always sexual)
SEXUAL_REPRODUCTION = 0.0

#probability of asexual reproduction actually occurring... when reproduction is sexual this probability is given
#by the probability of finding a partner in the neighbourhood, and hence, this additional parameter is not needed
ASEXUAL_REPRODUCTION_RATE = 1.0

ASEXUAL_REPRODUCTION_RATE_HIGH = 0.05

#number of habitats present in the ecosystem
HABITATS = 1

#max number of habitats a given species is allowed to inhabit
#if the case of type 2 habitats this only applies to primary producers, since the 
#other species will get their distributions from the habitats inhabited by their prey
MAX_HABITATS = 1

#whether to apply a habitat loss event
HABITAT_LOSS = True

#it must be less than the number of iterations. It specifies the time step at which the 
#habitat loss is going to take place 
HABITAT_LOSS_ITER = 100

# this number specifies the heuristic to be followed to destroy the habitat when HABITAT_LOSS = True
# 1 = contiguous (hole-like patch), 2 = random cells lost, 3 = TBA
HABITAT_LOSS_TYPE = 1

#fraction of habitat that will become lost, which will produce habitat loss and fragmentation
LOST_HABITAT = 0.3

#this parameter controls whether the habitat should be recovered after habitat loss has
#happened. When set to True the iteration at which habitat will be recovered will be taken
#from the next parameter (HABITAT_RECOVERY_ITER) 
HABITAT_RECOVERY = True

#number of the interation in the simulation at which habitat will be recovered if 
#HABITAT_RECOVERY is set to True
HABITAT_RECOVERY_ITER = 300

#whether to apply an invasion event
INVASION = False

#iteration at which the invader is set to enter the network
INVASION_ITER = 200

#number of possible invader species
POSSIBLE_INVADERS = 0

#number of individuals of the invader species to introduce into the world
INVADER_NUMBER = 200


##########
#These parameters are used for the calculation of stability measures

#number of iteration at which the extinction event is going to happen
EXTINCTION_EVENT = 400

#number of iterations to be considered for the calculation of stability measures
TIME_WINDOW = 150

#level at which species will be removed; values: 'top', 'cons', 'herb', 'prod'
REMOVAL_LEVEL = 'top'

#fraction of species to be removed
REMOVAL_FRACTION = 1.0


##########
READ_FILE_NETWORK = False

SRC_NET_FILE = 'initial_network.graphml'

