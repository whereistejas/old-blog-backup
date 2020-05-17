---
layout: post
author:
- Tejas Sanap
title: Let's talk about double pendulums.
---

This post is basically going to be about how to animate stuff using python's `matplotlib` library.
Some disclaimers, before we get started:
1. I'm not an expert at any of this.
2. I don't use python on a daily basis.
3. My code is meant to be easy to understand not efficient to run.

You can find each section in the form of a jupyter notebook at the following [link]().

## 1. let's start with some basic plotting.

The module used most often to make plots is called `matplotlib.pyplot`. Thankfully, you will find that most syntax in matplotlib is such that it makes sense to a layman (like you and me). To get acquainted with the basics, let's try plotting how much distance an object under free-fall travels with respect to time and also, it's velocity at each time step.

If, you have ever studied physics, you can tell that is a classic case of Newton's equations of motion.

$$ v = a \times t $$

$$ S = 0.5 \times a \times t^{2} $$

``` python
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
```

## references

* **Section 1**
	1. [matplotlib an introduction to its object-oriented interface](https://medium.com/@kapil.mathur1987/matplotlib-an-introduction-to-its-object-oriented-interface-a318b1530aed)
