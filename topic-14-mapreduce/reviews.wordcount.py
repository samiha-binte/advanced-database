import json
from mapreduce import MapReduce

# ----------------------------------------
def cleanup(word):
    word = word.lower()
    word = "".join([c for c in word if c.isalpha()])
    return word


class ReviewsWordCount(MapReduce):

    def mapper(self, _, line):
        data = json.loads(line)
        for word in data["text"].split():
            yield (cleanup(word),1)

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)

# ----------------------------------------

input = [
    "this is an example of this line",
    "this is an example of some example text",
    "this is another example example example",
    "and this is some more text and text and text"
]

input = open("reviews.json").readlines()

output = ReviewsWordCount.run(input)
for item in output:
    print (item)

for item in output:
    word, n = item
    if n > 15:
        print(item)
