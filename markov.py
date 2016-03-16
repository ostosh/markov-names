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
      # prefix with one char postfix occurrence to
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

  # normalize: convert prefix/postfix index to
  # occurrence weighted probability lookup index
  def normalize(self):

      # create probability lookup array for each
      # prefix in index
      for prefix in self.table:
          if prefix not in self.lookup:
              self.lookup[prefix] = []
          for postfix in self.table[prefix]:

              # create postfix array equal to the
              # size of postfix occurrences for a
              # given prefix and add to prefix index
              weighted_postfix = self.table[prefix][postfix] * [postfix]
              self.lookup[prefix] += weighted_postfix

  # get_name: get name of length n given from
  # markov model.
  #
  # invariant: markov model must me normalized.
  def get_name(self, min_len, max_len):

    # start name with n order delemiter
    name = self.delim

    # continue adding characters to name
    # until ending delimiter is found or
    # name exceeds length
    while len(name.replace('*', '')) < max_len:

        # use last n-order bits to lookup
        # probability array to find next
        # character
        if len(name) <= self.order:
            lookup = name
        else:
            lookup = name[-self.order:]

        # append next random character from
        # weighted prefix lookup array to name
        next = random.choice(self.lookup[lookup])
        name += next

        # test for ending delimiter
        if name[-self.order:] == self.delim:
            if len(name.replace('*', '')) >= min_len:
                break # name meets min threshold, return
            else:
                name = self.delim # restart
    return name


# generate_names: create markov model from
# input name file and generate random
# n names of max size s using order to
# define markox probabilty
def generate_names(gender, order, min_len, max_len, n):
    model = Markov(order)
    training_set = set()
    file_name = ''
    if gender is 0:
        file_name = './data/namesBoys.txt'
    else:
        file_name = './data/namesGirls.txt'
    names = open(file_name)
    for name in names:
        name = name.replace('\n', '')
        model.add(name)
        training_set.add(name)
    names.close()
    model.normalize()
    i = 0
    created_names = []
    while i < n:
        name = model.get_name(min_len, max_len).replace('*','')
        if name in training_set: #only add new names
            continue
        else:
            training_set.add(name)
            created_names.append(name)
            i += 1
    return created_names


# input: parse user input as int
def get_input(name):
    n = ''
    while True:
        n = input('Enter {0}:'.format(name))
        try: 
            return int(n)
        except ValueError:
            print('opps! invalid input')


# run: start stdin text interface 
def run():
    while True:
        print('Markov random name generator')
        print('-' * 20)
	
	# get user inputs
        gender = get_input('gender [boy=0,girl=1]')
        order = get_input('markov order > 1')
        if order < 1:
            print('opps! markov model order must be > 0. try again')
            print('-' * 20)
            continue
        min_len = get_input('min name length')
        max_len = get_input('max name length')
        count = get_input('name count')
        print('-' * 20)
        print('names:')
        print('-' * 20)
	
	# generate and print names
        names = generate_names(gender, order, min_len, max_len, count)
        for name in names:
            print(name)
        print('-' * 20)
        next = get_input('try again [no=0,yes=1]')
        if next == 0:
            break

run()


