{% extends "layouts/post.html" %}
{% set title="PATHMAN -- A Simple Path Manager for MATLAB" %}
{% set date="June 28, 2016" %}
{#
---
title: PATHMAN -- A Simple Path Manager for MATLAB
date: 2016-06-28
author: Jacob Peoples
summary:
    Managing the MATLAB path variable can be a pain, and PATHMAN is
    an attempt to help.
---
#}

{% set body_html %}
{% filter markdown %}

MATLAB finds functions/classes/packages by searching the current working
directory, followed by the list of directories in its path variable.
Directories can be added or removed from the path via the [`addpath`][1]
and [`rmpath`][2] functions.

Often, when using MATLAB for data analysis, I want to run algorithms or
visualisation code that I have written myself, or retrieved from, for
example, the [MathWorks File Exchange (FEX)][3].  In order to do this, I
either need to add all the code-containing directories to my path, or
write the analysis scripts in the code directory itself.

Doing the analysis in the same directory as the code is a poor option if
its an algorithm you intend to reuse, but getting all the directories
right to add the necessary path directories can be cumbersome as well.
Finally, just adding all your code permanently to your path can result
in name collisions.  This can be avoided by using smart naming schemes,
and packages, but in the case of third-party code, you may not have that
control.

[PATHMAN][4] is a tool, implemented in MATLAB, to help with this
situation.  In particular it allows you to give short names to packs of
code, and add/remove them from the path using the commands

    pathman use shortname
    % and
    pathman unuse shortname

It also allows you to list installed packs via

    pathman list [glob]

where `glob` can be used to narrow pack names, and update installed
packs after editing their source directories via

    pathman update packname

Such usage becomes particularly useful if you have many different code
packs in different locations, or complex logic to add code directories
to the path (see below).

[1]: http://www.mathworks.com/help/matlab/ref/addpath.html
[2]: http://www.mathworks.com/help/matlab/ref/rmpath.html
[3]: https://www.mathworks.com/matlabcentral/fileexchange/
[4]: https://github.com/jpeoples/PATHMAN


USAGE
-----

Here I will discuss a sample use-case. (All subsequent commands are
intended to be run on the MATLAB command line).

Suppose I've got some algorithms developed during a recent research
project located in `~/research/somealgs` which I now want to add to
PATHMAN with the name "somealgs".  Suppose the source directory looks
like

    somealgs/
        somesubalgs/
            % functions
        moresubalgs/
            % functions
        examples/
            % example scripts
        % more functions

If I run

    pathman install ~/research/somealgs as somealgs

then this directory will be copied to a configurable PATHMAN root
directory, and that copy directory, and all subdirectories can be added
to path via

    pathman use somealgs

and removed via

    pathman unuse somealgs

Suppose I then realize the examples/ subdirectory should not be added to
the path.

In my source directory, I can add the functions `addtopath` and
`rmfrompath` to implement this addpath, rmpath logic.

```matlab
% addtopath.m
function addtopath(root)
    % root will be passed by pathman, specifying the root of source
    % tree
    addpath(root);
    addpath(fullfile(root, 'somesubalgs'));
    addpath(fullfile(root, 'moresubalgs'));
end

% rmfrompath.m
function rmfrompath(root)
    rmpath(root);
    rmpath(fullfile(root, 'somesubalgs'));
    rmpath(fullfile(root, 'moresubalgs'));
end
```

Finally, to tell PATHMAN about my updated source tree I call

    pathman update somealgs

Now PATHMAN will use that logic when I call `use` and `unuse`.

Alternatively, I can tell PATHMAN to exclude that directory when copying
and then just use the default use/unuse logic.  To do so, add the file
`.pathmanignore` to the source directory containing the single line

```
example
```

This will cause PATHMAN to delete the copied example subdirectory after
copying the source tree. (Note that the lines of `.pathmanignore` should
be relative paths to subdirectories, or files only.  globs, etc, do not
work).


### Installation and More Information

For install information and further usage guidelines see the [PATHMAN
repository][4] and the PATHMAN MATLAB help

    pathman help
    % or
    help(pathman)

which lists and documents all the command-line options for pathman.

Feel free to ask any questions here or there as well.
{% endfilter %}
{% endset %}
