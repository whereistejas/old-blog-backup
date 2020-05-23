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

The module used most often to make plots is called `matplotlib.pyplot`. Thankfully, you will find that most syntax in `matplotlib` is such that it makes sense to a layman (like you and me).

To get acquainted with the basics, let's try plotting how much distance an object under free-fall travels with respect to time and also, it's velocity at each time step.

If, you have ever studied physics, you can tell that is a classic case of Newton's equations of motion.

$$ v = a \times t $$

$$ S = 0.5 \times a \times t^{2} $$

```python
import numpy as np

time = np.arange(0., 10., 0.2)
velocity = np.zeros_like(time, dtype=float)
distance = np.zeros_like(time, dtype=float)
```

We know that under free-fall, all objects move with the constant acceleration of 9.8 m/s<sup>2</sup>.

```python
g = 9.8 	# m/s^2

for index, vel in enumerate(velocity):
    # velocity = acceleration (g) * time
    velocity[index] = g * time[index] 

for index, dis in enumerate(distance):
    # distance = 0.5 * acceleration (g) * time^2
    distance[index] = 0.5 * g * time[index]**2 
    
```

When using `matplotlib` it is important to know, that there are two different approaches to making plots in `matplotlib` [lifecycle-of-a-plot](). The two approaches are:
1. Functional approach
2. Object oriented approach

### 1.1 Functional Approach

The functional approach uses MATLAB-like syntax. It makes making small plots very easy and quick.

The plot below shows us how much distance was covered by the free-falling object with each passing second.

```python
plt.figure(figsize=(9,7), dpi=100)
plt.plot(distance,'bo-')
plt.ylabel("Distance")
plt.xlabel("Time")
plt.legend(["Distance"])
plt.grid(True)
```

![png](/assets/images/double-pendulum/section-1-basics-of-plotting/just-distance.png)

We can see that the amount of distance travlled in each second is increasing, which is a direct result of increasing velocity due to the gravitational acceleration.

The plot below shows us how the velocity is increasing.
```python
plt.figure(figsize=(9,7), dpi=100)
plt.plot(velocity,'go-')
plt.ylabel("Velocity")
plt.xlabel("Time")
plt.legend(["Velocity"])
plt.grid(True)
```

![png](/assets/images/double-pendulum/section-1-basics-of-plotting/just-velocity.png)

It is very to surmise that the velocity is increasing in fixed steps, due to a "constant" acceleration.

Let's try to see, what kind of plot we get when we plot both distance and velocity in the same plot.

```python
plt.figure(figsize=(9,7), dpi=100)
plt.plot(velocity,'g-')
plt.plot(distance,'b-')
plt.ylabel("Distance and Velocity")
plt.xlabel("Time")
plt.legend(["Distance", "Velocity"])
plt.grid(True)
```

![png](/assets/images/double-pendulum/section-1-basics-of-plotting/distance-and-velocity-same-axes.png)

Here, we run into some obvious and serious issues. We can see that since both the quantities share the same scale, but have very different magnitudes, the graph looks disproportionate. What we need to do is seperate the two quantities on two different axes. This is where the second approach to making plot comes into play.

### 1.2 Object Oriented Approach

## references

* **Section 0**
	1. [matplotlib an introduction to its object-oriented interface](https://medium.com/@kapil.mathur1987/matplotlib-an-introduction-to-its-object-oriented-interface-a318b1530aed)
* **Section 1**
	1. [lifecycle-of-a-plot](https://matplotlib.org/3.2.1/tutorials/introductory/lifecycle.html)
