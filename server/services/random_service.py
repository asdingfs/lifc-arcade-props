from numpy import random, clip

MAX_SCORE = 9_999_999  # non-inclusive, i.e. MAX_SCORE is actually 9_999_999


def random_score():
  """Generate a random score between 0 and max (inclusive)."""
  return rand_lognormal(0, MAX_SCORE)


def rand_int(min_value: int, max_value: int) -> int:
  return random.randint(min_value, max_value + 1)

def rand_lognormal(min_value: int, max_value: int):
  return int(clip(random.lognormal(mean=10, sigma=1.5), min_value, max_value))
