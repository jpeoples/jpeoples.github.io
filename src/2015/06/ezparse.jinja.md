{% extends "layouts/post.html" %}
{% set title = "A dead simple argument parser for MATLAB" %}
{% set date = "June 25, 2015" %}
{#
---
title: A dead simple argument parser for MATLAB
date: 2015-06-25
author: Jacob Peoples
summary:
    Implementing a very simple argument parser for MATLAB functions.
---
#}

{% set body_html %}
{% filter markdown %}
*Dear Readers*,

First off, my name is Jacob, and I am a master's computer science
student.  Nice to meet you.

A lot of my day-to-day work for my master's is done -- originally to my
chagrin -- in MATLAB (I'll admit sometimes I kind of like it).  Since a
lot of the code I write is for numerical computations, there are often a
variety of parameters and what not that need to be set.  Often, for
whatever I am doing there are reasonable default values to use.
However, MATLAB does not support default values for parameters the way
languages like Python do.  To get around this I have seen a couple of
approaches.

One approach is to use an options struct.  For this  you would write
your function as

```matlab
function [outputargs] = funcname(what, ever, args, options)
%
% Let's imagine we want 3 optional parameters, foo, bar, baz, each
% taking default values of 0.
% set defaults
foo = 0;
bar = 0;
baz = 0;

% parse options parameter, iff it has been passed.
if nargin > 3
if isfield(options, 'foo')
    foo = options.foo;
end
if isfield(options, 'bar')
    bar = options.bar;
end
if isfield(options 'baz')
    baz = options.baz;
end
end

% get on with the code
% ...
```

Then for a user to use this function they can simply do something like

```matlab
opt.foo = 24;
funcname(what, ever, args, opt);
```

and the function will run with `foo = 24`, `bar = 0` and `baz = 0`.  If
they want *all* default parameters, they can either pass in an empty
struct, or simply leave out the argument altogether.

Another very common approach, which I personally prefer, is to accept
name-value pairs of arguments.  This uses a builtin MATLAB feature,
`varargin`, which allows you to collect all parameters beyond a certain
number into a single cell array.

```matlab
function [out] = funcname(what, ever, varargin)
% ...
```

In this code, if I call

```matlab
funcname(1, 2, 3, 4, 5, ...
    'everybody in the car so come on lets ride')
```

then the function will have `what = 1`, `ever = 2` and
`varargin = {3, 4, 5, 'everybody in the car so come on lets ride'}`.

Using this, we can implement optional arguments that follow the
so-called name-value pair convention.  The user specifies a series of
pairs, where the first item is a string -- the name -- referring to an
optional parameter, and the second is the value to assign to the
optional parameter.  Therefore, going back to the `foo`, `bar`, `baz`
example above, if I wanted to simply set `foo` to 24 I would call the
function as

```matlab
funcname(what, ever, args, 'foo', 24);
```

It is the function's job to parse this input, but MATLAB provides a tool
for doing this, called the [input parser][matlabinputparser].  Though
this tool provides a good deal of flexibility, it offers more options
than I really need, and requires more work to use than I would really
prefer.  For a while I found myself instead writing something along the
following lines whenever I needed such optional arguments:

```matlab
function [out] = funcname(what, ever, varargin)
% set defaults
foo = 0;
bar = 0;
baz = 0;

na = length(varargin);

% ensure there are optional arguments supplied, and there should be
% an even number if they are name-value pairs
if na > 0 && mod(na, 2) == 0
    for i=1:2:na
        name = varargin{i};
        switch name
            case 'foo'
                foo = varargin{i+1};
            case 'bar'
                var = varargin{i+1};
            case 'baz'
                var = varargin{i+1};
            otherwise
                error('Argument %s not recognised.', name);
        end
    end
elseif na>0
    % there are not an even number of arguments
    error('Every argument after ''ever'' must be a name-value pair.');
end

% ...
```

This wasn't so bad, I could copy and paste the code between files
whenever I needed name-value pair parsing, and simply modify the
names.  However, copy-and-pasting code is always a good hint that you
should just write a function, so I finally broke down and did exactly
that.

## ezparse.m
I had a couple of desired behaviours for this function in addition to
parsing name-value pairs.

1. Optional arguments should be case insensitive so calling
   `function('foo', 10)` is equivalent to `function('FOO', 10)`.

2. I wanted to also support flags -- names with no corresponding
   value -- that simply toggle a certain behaviour on (e.g. `function('verbose')`
   to toggle verbose behaviour).

3. Setting up optional parameters and default values should take as
   little coding as possible.

The function addresses point 3. by accepting a struct argument, whose
field names define the names in the name-value pairs, and whose values
define the values in the name-value pairs.  Moreover, a specific default
value is used to indicate that the field should create a flag, instead
of a name-value pair.

To clarify, recreating our foo, bar, baz example above, and adding a
'verbose' flag would look like this:

```matlab
function [out] = funcname(what, ever, args, varargin)
    opt.foo = 0;
    opt.bar = 0;
    opt.baz = 0;
    opt.verbose = '%FLAG%';

    [opt, unparsed] = ezparse(opt, varargin);

    % rest of code here
    % ...
```

Now `opt` contains all user supplied values, and defaults where no user
supplied value exists.  The verbose flag, if passed in by the user will
be set to 1, otherwise it will be set to 0.

The second output of `ezparse`, `unparsed`, simply contains any
remaining arguments that could not be parsed.  These would be any
arguments not matched by a field in the `opt` struct, trailing
arguments not following the name-value pattern, repeated options, etc.
Whether or not the existence of unparsed arguments should throw an
error, or simply be ignored is up to the function author.

To give an example, if I passed in

```matlab
funcname(what, ever, args, 'baz', 10, 'foo', 24, 'baz', 2, ...
         'verbose', 1, 2, 3, 'bar', 3);
```

then the resulting `opt` struct would have

```matlab
opt.foo = 24;
opt.bar = 3;
opt.baz = 10;
opt.verbose = 1;
```

and

```matlab
    unparsed = {'baz', 2, 1, 2, 3};
```



The resulting function is available [here][ezparserepo], but for
completeness here is the code listing.

```matlab
function [ argstruct, unparsed ] = ezparse( argstruct, argin )
%EZPARSE Fast and easy arg parser for 'key',val pair type optional args.
%   Pass in 2 parameters:
%       ARGSTRUCT: a struct populated with default values for all optional
%                  arguments.  Fields should be named corresponding to the
%                  desired 'key' in the key,value pairs.
%
%       ARGIN:     The varargin cell array from your function
%
%   This also supports 'flag' type arguments, where there is a string 'key'
%   with no value to be input, (for example
%       func(blabh, blah, 'optarg1', 2, 'verbose')
%   where 'verbose' is just a flag that gets toggled on.  These are
%   achieved by setting argstruct.flagname = '%FLAG%' in the default values
%   to signify a flag.
%
%   Note that all fields are case INsensitive
%
%   The returned 'unparsed' is a cellarray of all args in argin that
%   couldn't be parsed based on your input struct.  Most likely these are
%   simply arguments for which no corresponding field exists.  Handling
%   this is up to the user, for example it could simply be ignored, warned
%   about, or throw an error, depending on the application.
%

argnames = fieldnames(argstruct);

na = length(argin);
nf = length(argnames);

for j=1:nf
    fld = argnames{j};
    for i=1:na
        arg = argin{i};
        if strcmpi(arg, fld)
            % then we have matched a field
            % check for flag
            if strcmp(argstruct.(fld), '%FLAG%')
                % arg is a flag
                argstruct.(fld) = true;
                argin(i) = []; % delete field from argin
                na = na-1;
                break; % no need to search for this fld anymore
            end
            argstruct.(fld) = argin{i+1};
            argin(i:i+1) = []; %delete field from argin
            na = na-2;
            break;
        end
    end
    % set a field arg to false if not found in argin
    if strcmp(argstruct.(fld), '%FLAG%')
        argstruct.(fld) = false;
    end
end

% all remaining args could not be parsed!
unparsed = argin;


end
```

So that's it.  It is only a few lines longer than the manual
implementation of the name-value pair parsing I showed previously, and
it's usage requires only one more line of code after simply setting all
the defaults.

[matlabinputparser]: http://www.mathworks.com/help/matlab/ref/inputparser-class.html
[ezparserepo]: https://github.com/jpeoples/matlab-ezparse


{% endfilter %}
{% endset %}

