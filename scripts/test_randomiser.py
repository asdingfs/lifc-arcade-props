from numpy import clip, random
from collections import defaultdict
import math

def group_and_count_log_bins(arrays):
  """
  Takes a list of arrays or a single array, flattens them, and groups numbers by floor(log10(n)).
  Returns a dictionary mapping each log group to its count.
  """
  log_groups = defaultdict(int)

  # Flatten all arrays into a single list
  flat_list = [item for sublist in arrays for item in sublist]

  for num in flat_list:
    if num <= 0:
      continue  # log10 not defined for zero or negative numbers
    log_group = math.floor(math.log10(num))
    log_groups[log_group] += 1

  return dict(log_groups)


def rand_lognormal(min_value: int, max_value: int):
  return int(clip(random.lognormal(mean=10, sigma=1.5), min_value, max_value))


# Generate 10,000 scores
scores = [rand_lognormal(0, 9999999) for _ in range(10000)]
print(group_and_count_log_bins([scores]))
