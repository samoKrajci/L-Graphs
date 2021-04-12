# Grounded-L graphs

## bruteforce

For each vertex ordering we consider every combination of the heights of L-shapes. 
Then for given ordering and heights for each L we try to find the appropriate length for it to intersect with required Ls. That we can do in $O(n)$.

## bruteforce-smarter

For each vertex ordering we try to construct an L-graph representation with the same method as described in the paper.

That is, for each vertex we find the minimal height required for it's vertical line to intersect with every smaller vertex (in current ordering) and minimal lenght of it's horizontal line such as it reaches every greater vertex.
If during this process two lines that should not intersect do intersect, there is no representation which induces given ordering.