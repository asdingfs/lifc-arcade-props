from numpy import random

MAX_SCORE = 10_000_000  # non-inclusive, i.e. MAX_SCORE is actually 9_999_999


def random_score():
  """Generate a random score between 0 and max (inclusive)."""
  return random.randint(0, MAX_SCORE)
