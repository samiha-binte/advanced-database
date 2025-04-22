import json
import statistics
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
            yield (cleanup(word),data["stars"])

    # def combiner(self, key, values):
    #     yield key, sum(values)

    def reducer(self, key, values):
        if len(values) > 30:
            yield key, statistics.mean(values)

# ----------------------------------------

input = [
    "this is an example of this line",
    "this is an example of some example text",
    "this is another example example example",
    "and this is some more text and text and text"
]

input = open("reviews.json").readlines()

output = ReviewsWordCount.run(input)
approval = {}
for item in output:
    print (item)
    name, stars = item
    approval[name] = stars

# print(approval)


# output = [(stars, name) for name, stars in output]
#
# for item in sorted(output)[0:50]:
#    print(item)

text = json.loads(input[620])["text"]
words = [cleanup(word) for word in text.split()]
print(words)
scores = [approval[word] for word in words if word in approval]
print(scores)
print(statistics.mean(scores))
print(input[620])

## What businesses had a score of 5 or more? 
## Whae business was the best rated? 