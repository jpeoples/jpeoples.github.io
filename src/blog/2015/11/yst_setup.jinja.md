{% extends "layouts/post.html" %}
{% set title = "Running yst on Windows" %}
{% set date = "November 22, 2015" %}
{#
---
title: Running yst on Windows
date: 2015-11-22
author: Jacob Peoples
summary:
    I was considering switching the site over to `yst` (and ultimately
    decided against it) but there were some hiccups during installation
    and running on my Windows 10 laptop.  Here is how they got solved.
---
#}

{% set body_html %}
{% filter markdown %}
[yst] is a static site generator by John McFarlane, the originator of
the most utilitarian [Pandoc].  It is, as far as I can tell, very
simple, and that simplicity is what drew me to consider switching the
site over.  Even though I ultimately decided not to go with it, I did
manage to get it set up and building the test site on my machine.  In
that process I hit a few road-blocks, so I thought I'd put the details
here in one place in case anyone else is having similar problems.

## Installing ##

The [readme] on github makes it sound so easy:

    cabal update
    cabal install yst

I did not get the error detailed in the readme regarding
template-haskell dependencies.

Instead, I had an error installing a dependency: hdbc-sqlite3.  It's a
simple enough error -- you simply need to install sqlite3 on your system
-- but for me at least, nothing is obvious when it comes to Windows.

After poking around on Google I found [this][sqlite3-build] post that
explained the correct sqlite3 files to download to get hdbc-sqlite3 to
build.  No worries.  Problem solved, right? Wrong.

yst complains really fast if the sqlite3 dll is not on your path, so add
it now.

[readme]: https://github.com/jgm/yst
[yst]: https://github.com/jgm/yst
[sqlite3-build]: http://xyz.mmizzi.com/stuff/2014/11/3/install-hdbc-sqlite3-on-windows
[Pandoc]: http://pandoc.org/

## First Run ##

After getting yst installed the next step in the read me is to generate
the test site:

    yst create mysite

generates the test site source, then

    cd mysite
    yst

and voilà! Under the `site` subdirectory you have your static site.

Right?  Wrong.

Here's the output when I run yst:

    Updating site\js\nav.js
    Updating site\css\screen.css
    Updating site\css\print.css
    Updating site\css\hk-pyg.css
    Updating site\april_events.tex
    yst: site\april_events.tex: commitBuffer: invalid argument (invalid
    character)

Invalid character?

The yst test site likes to show off it's unicode support, and this is
the source of our issue.

As detailed by the [hakyll FAQ][hakyll]

> If you get any of the errors:
>
>    commitBuffer: invalid argument (invalid character) 
>
>or:
>
>    hGetContents: invalid argument (Invalid or incomplete multibyte or wide
>    character)
>    
>It means that your Hakyll executable couldn’t write to (in
>the former case) or read (in the latter) from an UTF-8 encoded file.

So for some reason yst can't write unicode to the output file.

I'm not sure why, but the same FAQ page provides a solution for Windows
just a short ways down the page.  Running

    chcp 65001

before running `yst` solved the problem for me, and left me with a
beautiful test site.

[hakyll]: http://jaspervdj.be/hakyll/tutorials/faq.html
{% endfilter %}
{% endset %}
