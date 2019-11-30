{% extends 'layouts/post.html' %}
{% set title = 'What if this Web Service Dies? Connecting "Service Anxiety" and Information Overload' %}
{% set date = "2019-11-06, 17:26:56" %}
{% set description | markdown %}
Connecting the fear of the loss of access to web services we use with
the idea of information overload, and considering how strategies to
manage the latter map to the former.
{% endset %}
{% set social_image = "service-anxiety.jpg" %}


{% set body_html | markdown %}
I've spent a lot of time thinking about organization and note-taking as
a way to try and keep on top of all the various things I encounter that
seem particularly interesting or useful.
Along the way, I've experimented with a lot of different productivity
and note-taking apps and services. A great thing about these is that
they mostly make it easy to access our notes or task-lists, or whatever
else, at any time, and from any place we might find ourselves, any
device we may use.  And while many of them seem promising, there is
always this nagging fear in the back of my mind, a fear that seems to
return whenever I think too much about any of the many web services I
depend on: if I pour too much of myself into this thing — this black
box of features over which I have no real control — what will I do if
it's suddenly gone?

After all, [it's not as if web-based software services live forever][google-graveyard].
What if the company goes out of business?
Or if I decide to fork out the cash for a premium service, what if money
gets tight and I need to cut costs?


As a convenient shorthand, I'll refer to this fear as "service
anxiety" for the remainder of this post.


# Understanding Service Anxiety

As pointed out by Simon Pitt in
[Computer Files are Going Extinct][pitt-files], with these services
we no longer need to concern ourselves with maintaining information
stored as files on our hard drive.
Instead, through the magic of technology, all of our data can be accessed
anytime, on any device, through "bespoke, proprietary interfaces".
Indeed, the easy access afforded by these kinds of services can be seen as part
of a general trend — identified by Alex Danco as
[the rise of the access economy][danco-access] —
of technologies that allow cheap and easy access to the things we want
or need, all the while freeing us from the messy details and maintenance
work of ownership.
But this liberation from ownership is also a removal of agency. In
[*Everything is Amazing but Nothing is Ours*][danco-everything],
[Danco points out][danco-everything]:

> Worlds of scarcity are made out of things. Worlds of abundance are
> made out of dependencies. That’s the software playbook: find a system
> made of costly, redundant objects; and rearrange it into a fast,
> frictionless system made of logical dependencies. The delta in
> performance is irresistible, and dependencies are a compelling
> building block: they seem like just a piece of logic, with no cost and
> no friction. But they absolutely have a cost: the cost is complexity,
> outsourced agency, and brittleness. The cost of ownership is up front
> and visible; the cost of access is back-dated and hidden.

In dependence, we inherit the fragilities of that on which we
depend, a lesson learned in the Node.js/npm ecosystem when the removal
of the tiny, independently maintained "left-pad" package
["broke the internet"](https://arstechnica.com/information-technology/2016/03/rage-quit-coder-unpublished-17-lines-of-javascript-and-broke-the-internet/).
[Pitt has a story of his own on this note][pitt-files], comparing a
website he had built in the '90s to one from just a year and a half ago:

> The other day, I came across a website I’d written over two decades
> ago. I double-clicked the file, and it opened and ran perfectly. Then
> I tried to run a website I’d written 18 months ago and found I
> couldn’t run it without firing up a web server, and when I ran NPM
> install, one or two of those 65,000 files had issues that meant node
> failed to install them and the website didn’t run. When I did get it
> working, it needed a database. And then it relied on some third-party
> APIs and there was an issue with CORS because I hadn’t whitelisted
> localhost.
>
> My website made of files carried on, chugging along.


But this fragility goes beyond the potential brittleness of software
dependencies: the web services we use to power our lives — to manage our
data, to create, to access music, to read and to think — these are all
dependencies upon which we build our lives.
The price for all this ease and convenience is not only brittleness, but
more generally, our subjugation to the whims of the companies that are
building these services, defining the data structures that we can
create, where those data live, and how they can be interacted with and
used.



Services come and their stewards encourage us to integrate them into the
foundations of our lives. But these building blocks don't make much of a
foundation at all. They shift, and break, and disappear, and
change shape beneath the structures we've tried to build above, and we
must constantly adapt to maintain some semblance of stability lest it
all come crashing down.



# Information Overload

In some sense this all is just another facet of the general experience of
anxious ephemerality that I think characterizes much of our
interaction with the internet.
The news cycle churns faster than ever.
Scandals come and go in the blink of an eye.
All we ever hear or see is what's new.
[Pitt says:][pitt-files]

> I don’t like this shift from timeless content to what is newest. Now,
> when I visit websites, they promote to me the latest thing. Why should
> the content that is the newest be the most important? It seems so
> unlikely that something that was just created would happen to be
> better than everything created throughout all time. What are the odds
> that every time I arrive at the site, the pinnacle of human
> achievement has just been breached? But we don’t seem to have a way of
> sorting by quality. Only by recency.

The internet — that genie's lamp of access to information —
facilitates all of this. You can't have constant access through the
cloud, or automatically download thousands of dependencies you built
your software from, or provide an incessant stream of new information to
millions of users, without the [series of
tubes][series-of-tubes][^series-of-tubes] to move all that data about.
And for all the good the internet has done, all the convenience and
access to information it provides, it seems that more and more it's
gotten to be [too much of a good thing][wiki-info-overload].

[^series-of-tubes]: Hear Jonathan Blow humourously extend this term to
your CPU [here](https://youtu.be/YGTZr6bmNmk?t=1576).


A common response to this are calls to simply unplug from it all and do
some long, slow, deep work — something Venkatesh Rao has called
*Waldenponding*.
In [Against Waldenponding][against-waldenponding] Rao argues that such a
retreat is its own kind of hijacking of attention:

>  25/ LONG before the digital media companies tried to pwn your attention
>  by overloading it at difficult latency ranges, religious institutions
>  tried to pwn you by suckering you into checking out of "temporal"
>  matters by labeling them sinful/profane or whatever. This is utter
>  bs.
>
>  26/ That is in fact the original attention hack: powerful
>  religious leaders telling smart people to check out and unplug from
>  information flows. That way, they get the power.

Tim Wu's [*The Attention Merchants*][attention-merchants], a book examining
the history of the selling of attention, makes a similar point: "With
its combination of moral injunctions as well as daily and weekly
rituals, organized religion had long taken human attention as its
essential substrate," (p. 26). Wu further notes that "[m]any of the most
talented copywriters [...] came from families steeped in organized
religion," (p. 71).



Rather than disconnecting, Rao advocates that we embrace our
part in the "Global Social Computer in the Cloud (GSCITC)", arguing that
while retreating for short periods can surely be healthy, long-term
unplugging is driven primarily by the "Fear of Being Ordinary (FOBO)" —
fear of being just another node in the GSCITC.  To best do our part, he
says we should strive to consume and respond to information at all
latencies — from the micro-moments of Twitter, to the most timeless
works from history — maintaining that a balance too far to either end
of the latency spectrum is a disadvantage.


This contrary argument, that keeping plugged in is Good Actually, if
only you can manage it, is echoed by Tiago Forte. His [Building a Second
Brain][basb] course is based on, among other things, reaping the rewards
of plugging in to the relentless stream of information by processing it
and offloading the storage to a carefully curated collection of digital
information — a second brain.[^basb]

[^basb]: Reader beware, this is based on my understanding of the course,
having not taken it.

> 3/ So much of the success narrative today is still based on the old
> model: get smart, know a lot, do one thing at a time, as early as
> possible
>
> [...]
>
> 14/ This is the fundamental problem with what I call First Brainism
> (incl. spaced repetition, memory palaces, deep work, digital
> waldenponding, speed-reading, essentialism, paper notes
> fundamentalists, and trad’l education): it tells you to get really
> good at the old model
>
> 15/ Obviously we need both, but prioritizing the biological brian as
> the repository of knowledge is now the surest way to not only fall
> behind, but to be more and more overwhelmed and stressed out as you do
> so
>
> 16/ We are in the early stages of the Second Brain era, when your
> biological and cognitive deficiencies turn into superpowers, as along
> as you are willing to give up some control and learn the new way
>
> * [Thread](https://twitter.com/fortelabs/status/1148027264790958080)


Something else that both Forte and Rao seem to agree on is a certain key
role of serendipity within how we manage ourselves in relation to this
new era of information access.
In a [podcast on the Evernote blog](https://evernote.com/blog/podcast-tiago-forte-on-productivity/),
describing his progressive summarization method, Forte describes a
heuristic to triage the process of progressively improving notes
based on when they naturally come up in the process of doing
something else:

> I’ll take notes on a source, whether it’s a conversation, an article,
> a book, a podcast, audiobook, whatever. And then I just put it in my
> system. Just the raw notes. The next time I see that, the next time I
> serendipitously come across it — or it might be that I’m looking for a
> project or looking for a resource that I want to use this note for — I
> summarize it.

Rao argues that in a world of higher complexity — complexity often
beyond our grasp — things can look random and unpredictable. Such a
world makes personal growth in the traditional sense harder to pursue.
Instead, he favours a kind of progressive intensification, or [life
spirit distillation:][vkr-life-spirit-distillation]

> Reactionary retreat to deterministic personal growth actively defends
> a ghostly state. Stochastic personal growth is like trying to beat the
> "market" of life possibilities without factoring in your own capacity
> for unplanned change.
>
> What does lead to progressive intensification is recognizing the
> growing serendipity in the environment, and rapidly increasing
> potential for more imaginative solutions to life challenges, with more
> intense and unexpected rebirths, all around.


That both call to embrace serendipity in the way we interact with the
world is, I think, no accident. Indeed, a certain amount of faith that
the important things will come up again can help relieve the anxiety of
getting lost in a barrage of new information.  It is by learning to
methodically relinquish the need for control that we can come to reap
the rewards of the new world of information, while still maintaining
some base level of coherency.



# Alleviating Service Anxiety

In a time of increasing complexity, our interactions with the external
world themselves come to be characterized by ephemerality — fleeting
glimpses of reality that feel increasingly disjoint and stochastic.  And
it is atop this drifting reality we are tasked to build our lives.


This is the parallel between the previous discussions of service anxiety
and information overload: in both cases it is the rapid distribution of
information — facilitated by the internet — that begets the ephemeral
nature of the worlds we interact with, resulting in a loss of agency and
a spike of anxiety.


So to alleviate service anxiety, can we again methodically relinquish
the need for control and embrace serendipity? As far as note-taking
services go,
[Tiago Forte seems to have anticipated this question](https://twitter.com/fortelabs/status/1161515095463256066):

> If you wouldn’t be happy to see all your notes permanently erased,
> you’re doing it wrong. Destroying your notes through creative
> destruction is the goal, not meticulously hoarding them and treating
> them as sacred objects worthy of veneration. Your notes should be
> disposable


In light of the lack of control we have over the services we use,
perhaps the answer is to use them to our benefit while we can, without
becoming too attached, because always, they may go.[^backup] Why do you
take notes, if not to learn, and ultimately to do?[^davies] Why use any
of these services if not as tools to achieve some goal defined on your
own terms? Does the carpenter fret that his hammer may break and be
rendered unusable, or does he rest easy knowing that if it did there
would be other hammers?


To survive — perhaps even to thrive — in this ephemeral new world, is
to embrace its drifting nature and to develop processes with that drift
in mind.

> [There is no need for trust in information when there is faith in
> process.](https://twitter.com/context_ing/status/1160734161948168193)



[^backup]: Obviously not all contexts really allow one to embrace
ephemerality.  We really would prefer not to lose our tax records. But
these storage problems are not really new. The point is that with most
web-services we relinquish control of our data, and so we cannot back it
up in any meaningful sense.

[^davies]: There is in fact at least one other great reason to learn:
your own amusement.
> I knew I was going to like Prof. the Rev. Darcourt. He seemed to think
> that learning could be amusing, and that heavy people needed stirring
> up. Like Rabelais, of whom even educated people like Parlabane had
> such a stupid opinion. Rabelais was gloriously learned because
> learning amused him, and so far as I am concerned that is learning's
> best justification.
>
> * Maria Theotoky in Robertson Davies' [*The Rebel Angels*](https://www.amazon.ca/Rebel-Angels-Robertson-Davies/dp/0143196987)


[google-graveyard]: https://killedbygoogle.com/
[pitt-files]: https://onezero.medium.com/the-death-of-the-computer-file-doc-43cb028c0506
[danco-access]: https://alexdanco.com/2015/02/02/the-rise-of-the-access-economy/
[danco-everything]: https://alexdanco.com/2019/10/26/everything-is-amazing-but-nothing-is-ours/
[series-of-tubes]: https://en.wikipedia.org/wiki/Series_of_tubes
[wiki-info-overload]: https://en.wikipedia.org/wiki/Information_overload
[against-waldenponding]: https://mailchi.mp/ribbonfarm/against-waldenponding
[attention-merchants]: https://www.amazon.ca/Attention-Merchants-Scramble-Inside-Heads/dp/0804170045/
[basb]: https://www.buildingasecondbrain.com/
[vkr-life-spirit-distillation]: https://mailchi.mp/ribbonfarm/life-spirit-distillation
{% endset %}
