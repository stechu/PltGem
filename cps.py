#!/usr/bin/python3
"""
example code and text are from:
https://www.ps.uni-saarland.de/~duchier/python/continuations.html
http://matt.might.net/articles/by-example-continuation-passing-style/

Continuation-passing style gives continuations meaning in terms of code.

Even better, a programmer can discover continuation-passing style by themselves 
if subjected to one constraint:

    No procedure is allowed to return to its caller--ever.

One hint makes programming in this style possible:

    Procedures can take a callback to invoke upon their return value.

When a procedure is ready to "return" to its caller, 
it invokes the "current continuation" callback (provided by its caller) on the return value.

A continuation is a first-class return point.
"""

# 3 warm up examples
# example 1: 2*x + y in CPS

def add(x, y, c):
	return c(x+y)

def mul(x, y, c):
	return c(x*y)

def baz(x, y, c):
	return mul(2, x, lambda v, y=y, c=c: add(v, y, c))


# example 2: factorial

def fact(n):
	if n == 0:
		return 1
	else:
		return n * fact(n-1)


def cps_fact(n, c):
	if n == 0:
		return c(1)
	else:
		return cps_fact(n-1, lambda x: c(n * x))


# example 3: tail-recursive factorial

def tail_fact(n):
	return t_fact(n, 1)

def t_fact(n, a):
	if n == 0:
		return a
	else:
		return t_fact(n-1, n * a)

def cps_tail_fact(n, c):
	return cps_t_fact(n, 1, c)

def cps_t_fact(n, a, c):
	if n == 0:
		return c(a)
	else:
		return cps_t_fact(n - 1, n * a, c)


# up the game: CPS for distributed computation
# now suppose you want to implement choose function that will call a potentially remote
# factorial function:
# choose(n, k) = fact(n) / (fact(k) * fact(n-k))
# using CPS could let you asynchronously compute factorial on the server:

def cps_choose(n, k, c):
	return cps_fact(n, lambda fact_n:
				cps_fact(n-k, lambda fact_nk:
					  cps_fact(k, lambda fact_k: c(fact_n/(fact_nk * fact_k)))))

# More read:
# [Matt Might: How to compile with continuations](http://matt.might.net/articles/cps-conversion/)


