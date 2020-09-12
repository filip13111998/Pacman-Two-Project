# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'TamnoPlavi', second = 'TirkizniAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)



ukupnoHrane = 0

class MyAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    global ukupnoHrane
    ukupnoHrane = len(self.getFoodYouAreDefending(gameState).asList())


    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]


    foodLeft = len(self.getFood(gameState).asList())


    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start, pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != util.nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights


  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

#TAMNO PLAVI
maxPojedeneHraneTamnoPlavi = 2
kolkoSamPojeoTamnoPlavi = 0
pozicijaNajblizeHraneTamnoPlavi = ()

ukupnoHraneOstalo = 0

class TamnoPlavi(MyAgent):

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    self.features = util.Counter()
    self.successor = self.getSuccessor(gameState, action)
    self.narednoStanje = self.successor.getAgentState(self.index)
    self.listaHrane = self.getFood(self.successor).asList()
    self.listaKapsula = self.getCapsules(gameState)
    self.narednaPozicija = self.narednoStanje.getPosition()
    self.protivnici = [self.successor.getAgentState(i) for i in self.getOpponents(self.successor)]
    self.tim = [self.successor.getAgentState(i) for i in self.getTeam(self.successor)]
    self.plaviDuh = [t for t in self.tim if t.isPacman == False and t.getPosition() != None]
    self.plaviPakman = [t for t in self.tim if t.isPacman and t.getPosition() != None]
    self.pakmaniCrveni = [prot for prot in self.protivnici if prot.isPacman and prot.getPosition() != None]
    self.duhoviCrveni = [prot for prot in self.protivnici if prot.isPacman == False and prot.getPosition() != None]
    self.akcija = action
    self.trenutnoStanje = gameState
    global ukupnoHraneOstalo

    ukupnoHraneOstalo = len(self.getFoodYouAreDefending(self.successor).asList())


    self.features['brojHranaCrveni'] = 0
    self.features['udaljenostNajblizeCrveneHrane'] = 0
    self.features['brojKapsulaCrveni'] = 0
    self.features['udaljenostKapsulaCrveni'] = 0
    self.features['udaljenostCrvenogDuha'] = 0
    self.features['AkcijaStop'] = 0
    self.features['AkcijaReverse'] = 0
    self.features['udaljenostOdTirkiznog'] = 0
    self.features['napad'] = 0
    self.features['odbrana'] = 0
    self.features['udaljenostOdStarta'] = 0
    self.features['udaljenostCrvenogPacmana'] = 0
    self.features['bonus'] = 0
    self.napadOdbrana()
    self.stop()
    self.reverse()
    self.udaljenostTirkizni()

    return self.features

  def napadOdbrana(self):
    global maxPojedeneHraneTamnoPlavi
    global kolkoSamPojeoTamnoPlavi
    # Ako sam pakman
    if self.narednoStanje.isPacman:
      # Ako je ostalo malo hrane na mojoj polovini
      if (ukupnoHraneOstalo < (ukupnoHrane * 50 / 100)):
        self.features['napad'] = -1
        duhBlizu = self.brDuhovaBlizu()

        if (duhBlizu == 0):
          # Ako ima crvenih pakmana na mojoj polovini koji prave problem onda se vrati i pojedi ih.
          if len(self.pakmaniCrveni) > 0:
            self.minPakmanDistance()
          else:
            # Skoro pa nemoguce da se desi.Ovde ispada da se vracam na svoju polovinu a da nema crvenog..a to dalje
            # znaci da je ipak sva hrana na mojoj polovini pa ne moram da se vratim ali sam zadrzao i ovaj slucaj.
            self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*5
        else:
          # Ovde gledam minimalnu udaljenost od starta,medjutim ako ta udaljenost ide preko crvenog duha to nije dobro.
          # jer ce me pojesti pa stoga bezim od njega pre svega ali i trazim put do mog dela terena.
          # self.minDuhoviDistance() #ovo je sada uradjeno u metodi self.brDuhovaBlizu()
          self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*5
      # Ako je ostalo puno hrane na mojoj polovini
      else:
        duhBlizu = self.brDuhovaBlizu()
        if duhBlizu == 0:
          if kolkoSamPojeoTamnoPlavi >= maxPojedeneHraneTamnoPlavi:
            if self.narednoStanje.isPacman == False:
              kolkoSamPojeoTamnoPlavi = 0
            self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*10
            self.features['napad'] = -3
          else:

            self.napadaj()

        else:

          #Ako me juri crveni duh,vrati se na svoju polovinu
          self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*5
          self.features['napad'] = -1

    # Ako nisam pakman
    else:
      if (ukupnoHraneOstalo < (ukupnoHrane * 50 / 100)):
        self.features['odbrana'] = 1
        self.minPakmanDistance()

      else:
        self.features['odbrana'] = -1
        self.napadaj()

  ##################################################################################################################
  def stop(self):
    if self.narednoStanje.isPacman:
      if self.akcija == Directions.STOP:
        self.features['AkcijaStop'] = -4

    else:
      if self.akcija == Directions.STOP:
        self.features['AkcijaStop'] = -3

  def reverse(self):
    rev = Directions.REVERSE[self.trenutnoStanje.getAgentState(self.index).configuration.direction]
    if self.narednoStanje.isPacman:

      if self.akcija == rev:
        self.features['AkcijaReverse'] = -4

    else:
      if self.akcija == rev:
        self.features['AkcijaReverse'] = -3

  def udaljenostTirkizni(self):
    if self.narednoStanje.isPacman:
      dis = min([self.getMazeDistance(self.narednaPozicija, pak.getPosition()) for pak in self.plaviPakman])
      self.features['udaljenostOdTirkiznog'] = -dis

  #################################################################################################################
  def brDuhovaBlizu(self):

    pozicijaDuhova = [e.getPosition() for e in self.duhoviCrveni]
    duhBlizu = 0
    for pozDuh in pozicijaDuhova:

      if ((self.getMazeDistance(self.narednaPozicija, pozDuh)) <7):
        duhBlizu += 1
    if duhBlizu > 0:
      self.minDuhoviDistance()

    return duhBlizu

  def minPakmanDistance(self):
    pozicijaPakmana = [p.getPosition() for p in self.pakmaniCrveni]
    minDis = 100000
    for poz in pozicijaPakmana:
      udaljenost = self.getMazeDistance(poz, self.narednaPozicija)
      if (udaljenost < minDis):
        minDis = udaljenost
    if (minDis == 0):
      self.features['bonus'] = 1
    self.features['udaljenostCrvenogPacmana'] = -minDis*3

  def minDuhoviDistance(self):
    pozicijaDuhova = [p.getPosition() for p in self.duhoviCrveni]
    minDis = 100000
    for poz in pozicijaDuhova:
      udaljenost = self.getMazeDistance(poz, self.narednaPozicija)
      if (udaljenost < minDis):
        minDis = udaljenost
    # if (minDis<7):
    # if (minDis == 0):
    #   self.features['bonus'] = 1
    self.features['udaljenostCrvenogDuha'] = - minDis


  def napadaj(self):
    global kolkoSamPojeoTamnoPlavi
    global pozicijaNajblizeHraneTamnoPlavi
    global pozicijaNajblizeHraneSvetloPlavi

    # global maxPojedeneHraneTamnoPlavi
    # if(kolkoSamPojeoTamnoPlavi ==maxPojedeneHraneTamnoPlavi):
    #   if self.narednoStanje.isPacman == False:
    #     kolkoSamPojeoTamnoPlavi = 0

    minDistanceFood = 10000
    f = ()

    if len(self.listaHrane) > 0:  # This should always be True,  but better safe than sorry

      for food in self.listaHrane:
        if (minDistanceFood < self.getMazeDistance(self.narednaPozicija,
                                                   food) and food != pozicijaNajblizeHraneSvetloPlavi):
          minDistanceFood = self.getMazeDistance(self.narednaPozicija, food)
          f = food
      # minDistanceFood = min([self.getMazeDistance(self.narednaPozicija, food) for food in self.listaHrane])
    pozicijaNajblizeHraneTamnoPlavi = f
    minDistanceCap = 10000
    if len(self.listaKapsula) > 0:  # This should always be True,  but better safe than sorry
      minDistanceCap = min([self.getMazeDistance(self.narednaPozicija, cap) for cap in self.listaKapsula])

    if (minDistanceCap < minDistanceFood * 1.3):
      self.features['udaljenostKapsulaCrveni'] = -minDistanceCap
      self.features['brojKapsulaCrveni'] = -len(self.listaKapsula)


    else:
      self.features['udaljenostNajblizeCrveneHrane'] = -minDistanceFood
      self.features['brojHranaCrveni'] = -len(self.listaHrane)
      if (minDistanceFood == 0):
        kolkoSamPojeoTamnoPlavi += 1


  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'brojHranaCrveni': 90,
            'udaljenostNajblizeCrveneHrane': 1,
            'brojKapsulaCrveni': 40,
            'udaljenostKapsulaCrveni': 1.5,
            'udaljenostCrvenogDuha': 100,
            'AkcijaStop': 100,
            'AkcijaReverse': 60,
            'udaljenostOdTirkiznog': 1,
            'idiUNapad': 100,
            'idiUOdbranu': 100,
            'udaljenostOdStarta': 400,
            'udaljenostCrvenogPacmana': 50,
            'bonus' : 200
            }


# #SVETLO PLAVI
maxPojedeneHraneSvetloPlavi = 1
kolkoSamPojeoSvetloPlavi = 0
pozicijaNajblizeHraneSvetloPlavi = ()




class TirkizniAgent(MyAgent):

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    self.features = util.Counter()
    self.successor = self.getSuccessor(gameState, action)
    self.narednoStanje = self.successor.getAgentState(self.index)
    self.listaHrane = self.getFood(self.successor).asList()
    #self.listaKapsula = self.getCapsules(gameState)
    self.narednaPozicija = self.narednoStanje.getPosition()
    self.protivnici = [self.successor.getAgentState(i) for i in self.getOpponents(self.successor)]
    self.tim = [self.successor.getAgentState(i) for i in self.getTeam(self.successor)]
    self.plaviDuh = [t for t in self.tim if t.isPacman == False and t.getPosition() != None]
    self.plaviPakman = [t for t in self.tim if t.isPacman and t.getPosition() != None]
    self.pakmaniCrveni = [prot for prot in self.protivnici if prot.isPacman and prot.getPosition() != None]
    self.duhoviCrveni = [prot for prot in self.protivnici if prot.isPacman == False and prot.getPosition() != None]
    self.akcija = action
    self.trenutnoStanje = gameState
    global ukupnoHraneOstalo

    ukupnoHraneOstalo = len(self.getFoodYouAreDefending(self.successor).asList())


    self.features['brojHranaCrveni'] = 0
    self.features['udaljenostNajblizeCrveneHrane'] = 0
    #self.features['brojKapsulaCrveni'] = 0
    #self.features['udaljenostKapsulaCrveni'] = 0
    self.features['udaljenostCrvenogDuha'] = 0
    self.features['AkcijaStop'] = 0
    self.features['AkcijaReverse'] = 0
    #self.features['udaljenostOdTirkiznog'] = 0
    self.features['napad'] = 0
    self.features['odbrana'] = 0
    self.features['udaljenostOdStarta'] = 0
    self.features['udaljenostCrvenogPacmana'] = 0
    self.features['bonus'] =0
    self.napadOdbrana()
    self.stop()
    self.reverse()
    #self.udaljenostTirkizni()

    return self.features

  def napadOdbrana(self):
    global maxPojedeneHraneSvetloPlavi
    global kolkoSamPojeoSvetloPlavi
    # Ako sam pakman
    if self.narednoStanje.isPacman:
      # Ako je ostalo malo hrane na mojoj polovini
      if (ukupnoHraneOstalo < (ukupnoHrane * 80 / 100)):
        self.features['napad'] = -2
        duhBlizu = self.brDuhovaBlizu()

        if (duhBlizu == 0):
          # Ako ima crvenih pakmana na mojoj polovini koji prave problem onda se vrati i pojedi ih.
          if len(self.pakmaniCrveni) > 0:
            self.minPakmanDistance()
          else:
            # Skoro pa nemoguce da se desi.Ovde ispada da se vracam na svoju polovinu a da nema crvenog..a to dalje
            # znaci da je ipak sva hrana na mojoj polovini pa ne moram da se vratim ali sam zadrzao i ovaj slucaj.
            self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*2
        else:
          # Ovde gledam minimalnu udaljenost od starta,medjutim ako ta udaljenost ide preko crvenog duha to nije dobro.
          # jer ce me pojesti pa stoga bezim od njega pre svega ali i trazim put do mog dela terena.
          # self.minDuhoviDistance() #ovo je sada uradjeno u metodi self.brDuhovaBlizu()
          self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*2
      # Ako je ostalo puno hrane na mojoj polovini
      else:
        duhBlizu = self.brDuhovaBlizu()
        if duhBlizu == 0:
          if kolkoSamPojeoSvetloPlavi >= maxPojedeneHraneSvetloPlavi:
            if self.narednoStanje.isPacman == False:
              kolkoSamPojeoSvetloPlavi = 0
            self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*2
            self.features['napad'] = -2
          else:

            self.napadaj()

        else:

          #Ako me juri crveni duh,vrati se na svoju polovinu
          self.features['udaljenostOdStarta'] = -self.getMazeDistance(self.start, self.narednaPozicija)*2
          self.features['napad'] = -2

    # Ako nisam pakman
    else:
      if (self.duhoviCrveni != []):
        self.features['odbrana'] = 1
        self.minPakmanDistance()

      else:
        self.features['odbrana'] = -1
        self.napadaj()

  ##################################################################################################################
  def stop(self):
    if self.narednoStanje.isPacman:
      if self.akcija == Directions.STOP:
        self.features['AkcijaStop'] = -15

    else:
      if self.akcija == Directions.STOP:
        self.features['AkcijaStop'] = -10

  def reverse(self):
    rev = Directions.REVERSE[self.trenutnoStanje.getAgentState(self.index).configuration.direction]
    if self.narednoStanje.isPacman:

      if self.akcija == rev:
        self.features['AkcijaReverse'] = -10

    else:
      if self.akcija == rev:
        self.features['AkcijaReverse'] = -8

  # def udaljenostTirkizni(self):
  #   if self.narednoStanje.isPacman:
  #     dis = min([self.getMazeDistance(self.narednaPozicija, pak.getPosition()) for pak in self.plaviPakman])
  #     self.features['udaljenostOdTirkiznog'] = -dis

  #################################################################################################################
  def brDuhovaBlizu(self):

    pozicijaDuhova = [e.getPosition() for e in self.duhoviCrveni]
    duhBlizu = 0
    for pozDuh in pozicijaDuhova:

      if ((self.getMazeDistance(self.narednaPozicija, pozDuh)) < 7):
        duhBlizu += 1
    if duhBlizu > 0:
      self.minDuhoviDistance()

    return duhBlizu

  def minPakmanDistance(self):
    pozicijaPakmana = [p.getPosition() for p in self.pakmaniCrveni]
    minDis = 100000
    for poz in pozicijaPakmana:
      udaljenost = self.getMazeDistance(poz, self.narednaPozicija)
      if (udaljenost < minDis):
        minDis = udaljenost

    if (minDis == 0):
      self.features['bonus'] = 2
    self.features['udaljenostCrvenogPacmana'] = -minDis*4

  def minDuhoviDistance(self):
    pozicijaDuhova = [p.getPosition() for p in self.duhoviCrveni]
    minDis = 100000
    for poz in pozicijaDuhova:
      udaljenost = self.getMazeDistance(poz, self.narednaPozicija)
      if (udaljenost < minDis):
        minDis = udaljenost
    # if (minDis<7):

    self.features['udaljenostCrvenogDuha'] = - minDis

  def napadaj(self):
    global kolkoSamPojeoSvetloPlavi
    global pozicijaNajblizeHraneTamnoPlavi
    global pozicijaNajblizeHraneSvetloPlavi

    # global maxPojedeneHraneTamnoPlavi
    # if(kolkoSamPojeoTamnoPlavi ==maxPojedeneHraneTamnoPlavi):
    #   if self.narednoStanje.isPacman == False:
    #     kolkoSamPojeoTamnoPlavi = 0

    minDistanceFood = 10000
    f = ()

    if len(self.listaHrane) > 0:  # This should always be True,  but better safe than sorry

      for food in self.listaHrane:
        if (minDistanceFood < self.getMazeDistance(self.narednaPozicija,
                                                   food) and food != pozicijaNajblizeHraneTamnoPlavi):
          minDistanceFood = self.getMazeDistance(self.narednaPozicija, food)
          f = food
      # minDistanceFood = min([self.getMazeDistance(self.narednaPozicija, food) for food in self.listaHrane])
    pozicijaNajblizeHraneSvetloPlavi = f
    # minDistanceCap = 10000
    # if len(self.listaKapsula) > 0:  # This should always be True,  but better safe than sorry
    #   minDistanceCap = min([self.getMazeDistance(self.narednaPozicija, cap) for cap in self.listaKapsula])

    # if (minDistanceCap < minDistanceFood * 3):
    #   self.features['udaljenostKapsulaCrveni'] = minDistanceCap
    #   self.features['brojKapsulaCrveni'] = -len(self.listaKapsula)
    #
    #
    # else:
    self.features['udaljenostNajblizeCrveneHrane'] = -minDistanceFood
    self.features['brojHranaCrveni'] = -len(self.listaHrane)
    if (minDistanceFood == 0):
      kolkoSamPojeoSvetloPlavi += 1


  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'brojHranaCrveni': 50,
            'udaljenostNajblizeCrveneHrane': 2,
            #'brojKapsulaCrveni': 100,
            #'udaljenostKapsulaCrveni': 3,
            'udaljenostCrvenogDuha': 70,
            'AkcijaStop': 100,
            'AkcijaReverse': 60,
            #'udaljenostOdTirkiznog': 1,
            'idiUNapad': 100,
            'idiUOdbranu': 100,
            'udaljenostOdStarta': 1000,
            'udaljenostCrvenogPacmana': 400,
            'bonus' : 1000
            }