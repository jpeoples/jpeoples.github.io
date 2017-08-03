{% extends "layouts/post.html" %}
{% set title= "Extending Arun's Method for Least Square Point Set Fitting with Isotropic Scaling" %}
{% set date = "June 30, 2016" %}
{% set has_math = True %}
{#
---
title: Extending Arun's Method for Least Squares Point Set Fitting with Isotropic Scaling
date: 2016-06-30
author: Jacob Peoples
hasmath: true
summary:
    I'd be remiss not to do a little math on this blog, so here we are.
    Here's a method to extend Arun's method with isotropic scaling.
    Let's warm up our matrix muscles...
---
#}

{% set body_html %}
{% filter markdown %}
I recently wanted to extend my implementation of the ICP algorithm to
include isotropic scaling.  Internally, ICP alternates between finding
the closest points in the target shape to those in the source shape --
thus giving two corresponding point sets -- and finding the optimal
rigid transformation to align those point sets.  As the alignment of the
shapes improve, so do the estimates of the closest points, and so on,
hence, the Iterative Closest Point algorithm.

In the original paper Besl and McKay[^1]
use a quaternion based method for finding the optimal rigid
transformation, but the algorithm can be implemented just as well
using a rotation-matrix method such as Arun's method.[^2]

[^1]: Besl, Paul J., and Neil D. McKay. "Method for registration of 3-D shapes." In Robotics-DL tentative, pp. 586-606. International Society for Optics and Photonics, 1992.

[^2]: Arun, K. S.; Huang, T. S. & Blostein, S. D. Least-squares fitting of two 3-D point sets IEEE Transactions on pattern analysis and machine intelligence, IEEE, 1987, 698-700

Without Scaling
---------------

The method of Arun et al. is as follows:

Given $\{X_i\}$, and $\{Y_i\}$ as two sets of $N$
$d$-dimensional points,  we want to find rotation matrix $R$ and
translation vector $t$ such that
$$
\sum_{i=1}^n || R X_i + t - Y_i||^2
$$
is minimised.

The solution for translation is simple: the optimal translation will be
that which matches the centroid of the rotated source shape to that of
the target.  That is
$$
t = \mu_Y - R\mu_X
$$
where $\mu_Z$ refers to the centroid of $Z$, and $R$ is the optimal
rotation.  See the next section for a proof of this.

The rotation is more complex, but they show that given the singular
value decomposition
$$
\sum_i (X_i-\mu_X)(Y_i-\mu_Y)^T = U \Lambda V^T
$$
then
$$
R = VSU^T
$$
where
$$
S = \left\lbrace
\begin{aligned}
    & I & \mathrm{if} & \det(U)\det(V) = 1 \\
    &\mathrm{diag}(1,1,\dots,1,-1) & \mathrm{if} & \det(U)\det(V) = -1
\end{aligned}
\right.
$$

Adding Scaling
--------------

A solution including isotropic scaling was published by Umeyama in
1991.[^3] However, I also gave a shot at my own derivation, and I will
show that our results are the same.

[^3]: Umeyama, S. Least-squares estimation of transformation parameters between two point patterns IEEE Transactions on pattern analysis and machine intelligence, IEEE, 1991, 13, 376-380

Adding in a scale factor, the objective function becomes
$$
f(X, Y; s, R, t) = \sum_i ||sRX_i +t - Y_i||^2
$$

The solution for $t$ can be found by setting the partial derivative to
zero
$$
\frac{\partial f}{\partial t} = 2\sum_i sRX_i + t - Y_i = 0
$$
hence
$$
t = \frac{\sum_i Y_i - sRX_i}{N} = \mu_Y - sR\mu_X.
$$

This is exactly the result mentioned above for $t$, with the addition of
the scale factor $s$.

We can solve for $s$ by taking a partial derivative, this time with
respect to $s$
$$
\frac{\partial f}{\partial s} = \sum_i 2(sRX_i + t - Y_i)^T RX_i = 0
$$

It is a straightforward expnsion of the above to arrive at
$$
0 = \sum_i sX_i^T X_i + t^T R X_i - Y_i^T R X_i
$$

and expanding $t$ with the previous solution and rearranging yields
$$
\sum_i s(X_i - \mu_X)^T X_i = \sum_i Y_i^T RX_i - \mu_Y^T R X_i
$$

Now note that $\sum_i (X_i - \mu_X) = 0$ and expand $X_i$ on the left
hand side to $X_i - \mu_X + \mu_X$:
$$
\begin{multline*}
\sum_i s(X_i - \mu_X)^T X_i = \sum_i s(X_i - \mu_X)^T (X_i - \mu_X +
\mu_X) = \\ \sum_i s(X_i - \mu_X)^T (X_i - \mu_X) + (X_i - \mu_X)^T\mu_X
\end{multline*}
$$

That last term is 0 and so
$$
\sum_i s(X_i - \mu_X)^T (X_i - \mu_X) = \sum_i Y_i^TRX_i - \mu_Y^T R X_i
$$

That is
$$
s = \frac{ \sum_i (Y_i^T R X_i) - N \mu_Y^T R \mu_X }{ \sum_j || X_j - \mu_X ||^2 }
= \frac{\sum_i (Y_i- \mu_Y)^T R (X_i - \mu_X)}{\sum_j || X_j - \mu_X
||^2}
$$
both of which are pretty nice.

*Note: In my implementation I found that though the second form is more
satisfying to me mathematically, the 1st form seemed to work better for
computations. I don't have an explanation for this.*


Comparing with Umeyama's Solution
---------------------------------

Using the notation I have been using in this post, Umeyama showed that
$$
s = \frac{\operatorname{Tr}(\Lambda S)}{\sum_j ||X_j - \mu_X||^2}
$$

Already, we see our denominators match, so we want to show
$$
\operatorname{Tr}(\Lambda S) = \sum_i (Y_i- \mu_Y)^T R (X_i - \mu_X)
$$

Somehow we have to get the trace in there, so we'll need two facts about
trace:

1.  The trace of the product of two matrices is related by
    $\operatorname{Tr}(A^T B) =
    \operatorname{Tr}(A B^T) =
    \operatorname{Tr}(B A^T) =
    \operatorname{Tr}(B^T A)$.
2.  For vectors $u$and $v$, the inner product and outer product are
    related by $u^Tv = \operatorname{Tr}(vu^T)$

Based on the 2nd fact, and recalling that
$$
\sum_i (X_i - \mu_X)(Y_i - \mu_Y)^T = U\Lambda V^T
$$
we can write the numerator of our $s$ equation as
$$
\sum_i (Y_i - \mu_Y)^T R (X_i - \mu_X) = \operatorname{Tr}(R \sum_i (X_i-\mu_X)(Y_i -
\mu_Y)^T)
$$

We can now immediately substitute in $R = VSU^T$ and
$\sum_i (X_i - \mu_X)(Y_i - \mu_Y)^T = U\Lambda V^T$
giving
$$
\sum_i (Y_i - \mu_Y)^T R (X_i - \mu_X) = \operatorname{Tr}(VSU^T U \Lambda V^T)
$$

immediately the $U$, and $U^T$ cancel leaving $VS \Lambda V^T$.
Transposing $VS$ and $\Lambda V^T$ (from the 1st fact) gives
$$
\sum_i (Y_i - \mu_Y)^T R (X_i - \mu_X) = \operatorname{Tr}(SV^T V
\Lambda) = \operatorname{Tr}(S \Lambda) = \operatorname{Tr}(\Lambda S)
$$
as required.
{% endfilter %}
{% endset %}
