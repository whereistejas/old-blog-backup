---
layout: post
title: "Double Pendulums (Part 2)"
author: Tejas Sanap
---

In the previous, post we learned about how to make some basic plots in `matplotlib`. In this blog post, we will talk about double pendulums. The topics that we will be covering are:

1. The mathematics behind simulating a double pendulum
2. How can we solve those equations
3. Requirements of the animation functions

## draw the double pendulum
We will first draw a double pendulum (obviously, using `matplotlib`) to get a sense of what we are trying to simulate. The full source code of the figure you can see below, can be found [here]().

I will just cover the some nuances about the python code I wrote to make this plot.

![png](/assets/images/double-pendulum-part2/double-pendulum-drawing.png)
<div class="image-caption">
<b>Fig. 1.1</b> The structure of a double pendulum.
</div>


The first part we had to get done, was make sure that the origin of our plot was in the centre of the figure. The `plt.axis('scaled')` method does exactly, that. This method has two ways of equalizing scales, the first is by resizing the plot dimensions (`scaled`) and the second is by changing the axis limits (`equal`). Since we want to control the limits of our axes, we went with the `scaled` option.

```python
plt.axis('scaled')
plt.xlim(-total_length,total_length)
plt.ylim(-total_length,total_length)
plt.grid(True)
```

The part where I would like to focus is the manner in which I have sliced the numpy arrays, to get the co-ordinates I want. The `x` and `y` have 3 elements and therefore, an index ranging from `0` to `2`.

```python
plt.plot(x[0:2],y[0:2],'g-') #what a lot of beginners fail to understand is how to slice mumpy arrays 
plt.plot(x[1:],y[1:],'b-')
```

To get the first two elements, I will slice it like `x[0:2]` which will return all the elements with an index smaller than 2.

## generate the data
Let's talk about some of the math behind the double pendulum.

## references

1. [discussion on scaling the algorithim](https://in.mathworks.com/matlabcentral/answers/346738-how-to-run-the-animation-of-double-pendulum-chaotic-nature#answer_272478)
2. [github repo with code](https://github.com/dassencio/double-pendulum)
