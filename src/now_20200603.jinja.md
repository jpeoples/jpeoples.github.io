{% extends "layouts/base.html" %}
{% set title = "Now" %}
{% set social_image = "now.png" | ensure_fullhref %}
{% set description = "What I'm doing now" %}

{% import "layouts/macros.html" as macros %}

{% block content_header %}
{{macros.header("What I'm Doing Now", "Last updated: 2020-06-03")}}
{% endblock %}

{% block content %}
{% filter markdown %}

I successfully defended my PhD thesis on April 21, 2020, on the
*Composition of Transformations in Feature-Based Registration*.

**I am actively looking for work opportunities, ideally to start in
September 2020.** I am located in Ontario, Canada, but am
**open to relocation, especially within North America** (post-lockdown
of course).

If you are interested, please contact me on [LinkedIn][my_linkedin],
[Twitter][my_twitter], or email me at `jacobjpeoples` at gmail.

Here's a quick overview of my skills and experience.

I have, over the years, developed practical **technical skills** with a
variety of programming languages and tools including

* Python, MATLAB, C, and C++
* scientific computing libraries including
    * `numpy`, `scipy`, and `matplotlib` in Python
    * Eigen and `libigl` in C++
* TensorFlow
* LaTeX


In addition to technical skills, my PhD has required me to develop
**transferable skills** in

* Project management;
* Time management;
* Writing and communication;
* Public speaking;
* Moving from idea to implementation to application; and
* Execution in the face of considerable uncertainty.

I have **presented my research at an international conference** ([IPCAI
2019](http://www.ipcai2019.org/)).

 As  graduate student I have completed **course work** in

* Algorithms
* Pattern Recognition
* Research Methods
* Systems Biology
* Computational Geometry
* Fuzzy Logics
* Formal Methods in Software Engineering
* Differentiable Manifolds

I also have a **strong mathematical background**, having studied
mathematical physics as an undergraduate.



My PhD work has focused on point set registration, which has
applications in **computer vision and medical imaging**.  More details
about my academic research and teaching experience can be found in my
**academic CV** ([html]({{base_url}}about/) | [pdf]({{base_url}}web_cv.pdf)).

[my_linkedin]: https://www.linkedin.com/in/jacob-peoples-20239b17b/
[my_twitter]: https://twitter.com/__jpeoples

{% endfilter %}
{% endblock %}
