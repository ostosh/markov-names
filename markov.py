import random


# Markov model class
class Markov():

  # markov model cosntructor
  def __init__(self, order):
      self.order = order
      self.table = {}
      self.lookup = {}
      self.delim = "*" * self.order

  # add: add token to markov model
  def add(self, token):

      # add delimiter to token
      token = self.delim + token + self.delim

      # split token by order and add each n order
      # prefix with one char postfix occurence to
      # model
      for i in range(0, len(token) - self.order):
          prefix = token[i: i + self.order]
          postfix = token[i + self.order]
          if prefix in self.table:
              if postfix in self.table[prefix]:
                  self.table[prefix][postfix] += 1
              else:
                  self.table[prefix][postfix] = 1
          else:
               self.table[prefix] = {postfix : 1}

  # normalize: convert prefix/posfix index to
  # occurence weighted probability lookup index
  def normalize(self):

      # create probability lookup array for each
      # prefix in index
      for prefix in self.table:
          if prefix not in self.lookup:
              self.lookup[prefix] = []
          for postfix in self.table[prefix]:

              # create postfix array equal to the
              # size of postfix occurences for a
              # given prefix and add to prefix index
              weighted_postfix = self.table[prefix][postfix] * [postfix]
              self.lookup[prefix] += weighted_postfix

  # get_name: get name of length n given from
  # markov model.
  #
  # invariant: markov model must me normalized.
  def get_name(self, length):

    # start name with n order delmiter
    name = self.delim

    # continue adding characters to name
    # until ending delimiter is found or
    # name exceeds length
    while len(name.replace('*', '')) < length:

        # use last n-order bits to lookup
        # probability array to find next
        # character
        if len(name) <= self.order:
            lookup = name
        else:
            lookup = name[-self.order:]

        # append next random character from
        # weighte prefix lookup array to name
        next = random.choice(self.lookup[lookup])
        name += next
        if name[-self.order:] == self.delim:
            break
    return name


# generate_names: create markov model from
# input name file and generate random
# n names of max size s using order to
# define markox probabilty
def generate_names(gender, order, s, n):
    model = Markov(order)
    file_name = ''
    if gender is 'boy':
        file_name = './data/namesBoys.txt'
    else:
        file_name = './data/namesGirls.txt'
    names = open(file_name)
    [model.add(name.replace('\n', '')) for name in names]
    names.close()
    model.normalize()
    [print(model.get_name(s).replace('*','')) for i in range(n)]




generate_names('girl', 5, 7, 10)
print()
generate_names('boy', 3, 10, 10)
print()

