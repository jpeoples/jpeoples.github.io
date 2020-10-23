{% extends "layouts/base.html" %}
{% set title = "Now" %}
{% set social_image = "now.png" | ensure_fullhref %}
{% set description = "What I'm doing now" %}

{% import "layouts/macros.html" as macros %}

{% block content_header %}
{{macros.header("What I'm Doing Now", "Last updated: 2020-10-23")}}
{% endblock %}

{% block content %}
{% filter markdown %}


I am currently working as a post-doc with the [Medical Computing
Laboratory](https://simpsonlab.org), working on radiomic analysis of
medical images. We are at the moment particularly interested in the
repeatability/stability of radiomic features as potential biomarkers.


Outside my academic work -- though not unrelated to it -- I am also
interested in the meta-process of synthesizing streams of incoming
information into coherent structures and narratives. This is something
I've been writing about here in my [Boredom World](/blog/boredom-world)
blog-chain.

Finally, having recently finished my PhD, I am using this transitory
time to reevaluate my career goals and aspirations. To know more about
my past work, see my [about](/about) page. I'd love to hear from you
about interesting opportunities coming up in 2021.


*[Previous version of this page](/now_20200603)*

{% endfilter %}
{% endblock %}
