{% extends "layouts/post.html" %}
{% set title= "Abuse of the Equals Sign" %}
{% set date = "February 9, 2018" %}
{% set has_math = True %}

{% set body_html %}
{% filter markdown %}

The symbol "=" means "equals". It is to be written only when the things
on either side are known to be equal, or if we are saying some meta
statement like, "we want to show that X = Y".

Suppose we have proved or assumed that $\sum_{i=2}^n 2i = (n-1)(n+2)$,
and we want to show that $\sum_{i=2}^{n+1} 2i = n(n+3)$.

Here's one way:


> $$\begin{aligned}
> \sum_{i=2}^{n+1} 2i &= \sum_{i=1}^n 2i + 2(n+1) \\
>      &= \sum_{i=2}^n 2i + 2(n+1) \\
>      &= (n-1)(n+2) + 2(n+1) \text{ (by the induction hypothesis) } \\
>      &= n^2 + n - 2 + 2n + 2 \\
>      &= n^2 + 3n \\
>      &= n(n+3)
> \end{aligned}$$

Here every line and equals sign is justified by either basic algebra or
previously established facts. Every "=" really means "equals".

However, sometimes we may not know ahead of time how to go from left to
right directly. In such cases, here is an alternative way:

> We want to show $\sum_{i=2}^{n+1} 2i = n(n+3)$. Observe that
> $$\sum_{i=2}^{n+1} 2i = \sum_{i=2}^n 2i + 2(n+1)
>      = (n-1)(n+2) + 2(n+1) 
>      = n^2 + n - 2 + 2n + 2
>      = n^2 + 3n $$
>
> On the other hand,
> $$n(n+3) = n^2 + 3n$$
>
> Indeed they are equal and so we have shown $\sum_{i=2}^{n+1} 2i = n(n+3)$.

*Either of these approaches is perfectly acceptable in a test situation,
and which is clearest may depend on the problem at hand, or the
preferences of the reader.*

"Equals" vs "Equals?"
=====================

What a lot of students end up writing is something like the following:

$$\begin{aligned}
 \sum_{i=2}^{n+1} 2i &= n(n+3) \\
 (n-1)(n+2) + 2(n+1) &= n(n+3) \\
  n^2 + n - 2 + 2n + 2 &= n^2 + 3n \\
  n^2 + 3n &= n^2 + 3n
\end{aligned}$$

Up until the very last line, none of these "=" mean "equals". They mean
something like "equals?". On the other hand, adjacent lines in the left
column or the right column really are known to be equal, yet no "=" is
written between them! *This is abuse of the equals sign*! The true known
equalities flow down the left column and back up the right column (or
down the right and up the left).

I know it makes sense while you write it, but as readers (or graders)
we now need to not only try and follow your calculations, but also
decide whether you really mean "equals" or "equals?" anywhere you've
written "=".

If you're unsure how to go from left to right and want to manipulate
each side separately that is OK. *But do not abuse the equal sign*. Go
for the second style shown above instead. Or if you have extra time you
could figure out how to do the calculations in order on the back of the
page, and then write a clearer presentation for your final answer.

In any case, by consistently using "=" to mean "equals" and never
"equals?", graders don't need to try and figure out what you mean at
every "=".  They just need to follow your calculations and decide if
they are correct.

{% endfilter %}
{% endset %}
