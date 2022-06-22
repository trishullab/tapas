def digitsum(d) :
    return sum(k*v for k, v in d.iteritems())

def digitcount(d) :
    return sum(v for v in d.itervalues())