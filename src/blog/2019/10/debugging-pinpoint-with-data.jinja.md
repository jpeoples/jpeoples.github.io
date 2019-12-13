{% extends 'layouts/post.html' %}
{% set title= "Pinpoint Bugs Based on Data, Not Intuition" %}
{% set date = "2019-10-23, 22:43:01" %}
{% set social_image = "debugging.png" %}

{% set description | markdown %}
Often when debugging a problem, our brains have a strong intuition as to
exactly where the bug "must" be. We may even have seemingly valid
rational arguments as to why the bugs "must" be located in this
particular part of the code. *Whenever possible, I think it is best to
ignore these impulses and pinpoint bugs based on hard data*.
{% endset %}

{% set body_html | markdown %}

{{ description }}

While knowledge of the code structure can help you narrow down the
source of the problem to a particular area within a larger program,
beyond that it may be most effective to ask what assumptions the program
makes, and to find where exactly those assumptions break. This is a
matter than can be addressed by hard facts, rather than an intuition.


As a concrete example, yesterday I was debugging an algorithm I have
been developing as part of my research. The faulty behaviour was
occurring only when running it on a particular data set. And since this
algorithm is a bit complicated in implementation, and this particular
data set leading to the algorithm executing a less-commonly-used code
path, I reasoned, the bug must be a mistake in the logic of that
less-commonly-used code path. Knowing that the correct logic was a bit
complicated even in theory, I was confident that this would prove to be
the problem.

So I reread the code, which was written more than a year ago now, and
gradually reloaded all the necessary context into my brain to understand
how it works. Stepping through, both mentally and literally in the
debugger, I simply could not see any problem.

I even racked my brain to come up with two alternative inputs, which
theoretically, in a correct implementation, should have produced
identical results. In actuality, one hit the bug, and the other didn't.
Bingo!

At each stage of the algorithm, I plotted the output to try and pinpoint
exactly *when* along the way the error occured. It told me nothing I
didn't already suspect: the bug was in that aforementioned
less-commonly-used code path just like I knew it had to be.

The only problem was, staring at the code, I could still find no error.

Finally, I realized there was theoretically an invariant that should be
maintained across several of the steps taken in the relevant code path.
*Computing this invariant quantity after each line affecting the
relevant variables provided a hard data-based test.* If ever the
invariant was broken, the bug -- or at least *a* bug -- was found.

This was exactly what solved it: it turned out that the error was in
a particular method, being called only in that less-commonly-used code
path, that was so simple in intent that my intuition would
never have taken me there. I quickly fixed it, and proceeded to find a
couple other bugs, similar in nature, that simply hadn't bitten me yet.

What I observed from this is that while my intuition and reasoning got
me to the right area of the code right away, it proceeded to lead me
astray. I was sure the bug was an error in the complicated logic of the
algorithm, when in fact it was a simple oversight in a simple method
being called in the process of executing that complicated logic. Only by
using data in the form of a broken invariant to prove the bug *had to
occur within that method* did it occur to me to even look there.

I think this gets back at the fact that as programmers we often can't
reason that accurately about the complexity of our programs.  Conceptual
complexity and complexity of implementation are not the same.  But worse
is that even the simplest implementations are subject to the complexity
of evolution over time.  The problematic method in my case was
conceptually trivial. It's implementation was clear and concise.  But in
the course of the evolution of the code a few new options had been added
to the class somewhere along the way which were not properly being taken
into account in this particular method. And because this method was only
called in what was a largely neglected code path, the bug remained
hidden in plain sight for a long time. In contrast, the big, complicated
block of logic implementing the algorithm -- a seemingly ideal habitat
for all kinds of nasty bugs -- where my intuition immediately led me,
having me step through code with my eyes glazed over for over an hour,
was, at the end of it all, just fine.

And so, I conclude, when investigating a bug, try to ground your
investigation in hard data as quickly as possible. Avoid just blindly
stepping around the code except as a last resort. And ignore that
intuition that tells you the problem just has to be in this nasty bit of
logic here, because sometimes it's the rosy patches that are the thorn
in your side.

{% endset %}
