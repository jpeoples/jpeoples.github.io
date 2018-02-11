{% extends "layouts/post.html" %}
{% set title = "Lying cat: Bizarre Filesystem Behaviour" %}
{% set date = "May 5, 2017" %}
{#
---
title: "Lying cat: Bizarre Filesystem Behaviour"
date: 2017-05-05
summary:
    Just a short post on something odd that happened to me last night.
---
#}

{% set body_html %}
{% filter markdown %}
Just a short post on something odd that happened to me last night.

I was working on the Jinja template to generate the posts on this
website. I had a local server launched in the build directory of the
website so I could preview the results as I went. It was working fine; I
could make changes, rebuild, refresh, and immediately see those changes.
The usual.

However, I noticed that the dates I wanted to appear underneath the
title of blog posts were not showing up. I double checked the template,
which seemed to be correct. It is a snippet like so:

```html
{% raw %}
{% if formatted_date is defined %}
<p id="date">{{formatted_date}}</p>
{% endif %}
{% endraw %}
```

The odd thing was that in the rendered templates I was viewing in the
browser, the actual result was:

```html
<p id="date"></p>
```

So somehow the `formated_date` variable was being defined, but was
empty...

Except it wasn't.

I printed out the variable in the context dictionary just before
rendering and saw the correct dates displayed for each post.

The Weird Part
==============

So far this is just a typical annoying bug story. Here's the weird part:

I opened the file directly by double clicking it in the build directory
and the page showed up in the browser, *with the date*, even though it
wouldn't show up when browsing from the local server, which should have
been the same file. Even this I would have been happy to attribute to
some weird browser behaviour, or some weird behaviour of the python http
server. I don't know that much about web stuff in general so I can
believe anything.

But here's the thing. I closed the server and reopened it. Still the
date didn't show up. Weird. So then I literally typed:

    cat path/to/post | less

and scrolled down to where the date should be. It still wasn't there.
Meanwhile, I have the very same file open in the browser and it *is*.

Then I go:

    pushd path/to/
    cat post | less

and sure enough, *the date shows up!*. Then:

    popd
    cat path/to/post | less

and it still shows up!

So what on earth was going on the first time I typed `cat`?!

{% endfilter %}
{% endset %}
