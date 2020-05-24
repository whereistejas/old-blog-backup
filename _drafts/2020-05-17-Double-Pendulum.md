---
layout: post
author: Tejas Sanap
title: "Double Pendulums (Part 1)"
---

This series is basically going to be about how to animate stuff using python's `matplotlib` library. `matplotlib` has an excellent [documentation](https://matplotlib.org/3.2.1/contents.html) where you can find a detailed documentation on each of the methods I have used in this blog post. Also, I will be publishing each part of this series in the form of a jupyter notebook, which can be found [here]().

I would like to say a few words about the methodology of these series:
1. Each part, will have a list of references at the end of the post, mostly leading to appropriate pages of the documentation and helpful blogs written by other people. **THIS IS THE MOST IMPORTANT PART**. The sooner you get used to reading the documentation, the better.
2. The code written here, is meant to show you how you can piece everything together. I will try my best to describe the nuances of my implementations and the tiny lessons I learned.

## Generating the data points.

To get acquainted with the basics of plotting with `matplotlib`, let's try plotting how much distance an object under free-fall travels with respect to time and also, it's velocity at each time step.

If, you have ever studied physics, you can tell that is a classic case of Newton's equations of motion, where...

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

The above code gives us two `numpy` arrays populated with the distance and velocity data points. You will notice that when looping over the arrays, I have used the `enumerate` method. We can often see people using the `list.index()` method or using the `len()` to generate the index. Both of these approaches, are wasteful. Using the `enumerate` method offers two advantages:

1. The `enumerate` method is internally implemented as a python generator. This means that the index and values are generated on the fly and just in time. This can prove immensely helpful when you are iterating over an array with a 100,000 floating data points. This makes our code faster and prevents unnecessary memory consumption.
2. It makes the code more *pythonic*.

## Functional vs. Object-Oriented interface

`matplotlib` on the surface is made to imitate the MATLAB's state-machine like interface called `pyplot`. This interface allows us to quickly and easily generate plots. Because of the state-based nature of this interface, it keeps track of the pyplot object and changes we make to it, this helps us to add elements and/or modify the plot as we need. But, this approach doesn't really scale when we are required to make multiple plots or when we have to make intricate plots that require a lot of customisation.

However, internally `matplotlib` has an Object-Oriented interface that can be accessed just as easily.

The module used most often to make plots is called `matplotlib.pyplot`. Thankfully, you will find that most syntax in `matplotlib` is such that it makes sense to a layman (like you and me).

When using `matplotlib` it is important to know, that there are two different approaches to making plots in `matplotlib`. The two approaches are:
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
When dealing with the object-oriented approach, it is important to understand how `matplotlib` makes plots. Every plot is made up of two objects, a `Figure` object and an `Axes` object. EAch `Axes` object refers to one plot. One can have as many of them as one wants. All of these various objects are brought together in the `Figure` object.

This will prove immensely helpful in solving our problem. We can have two different `Axes` objects for distance and velocity and show it in a single `Figure`.

```python
fig, ax1 = plt.subplots()

ax1.set_ylabel("distance (m)")
ax1.set_xlabel("time")
ax1.plot(time, distance, "blue")

ax2 = ax1.twinx() # create another y-axis sharing a common x-axis

ax2.set_ylabel("velocity (m/s)")
ax2.set_xlabel("time")
ax2.plot(time, velocity, "green")

fig.set_size_inches(7,5)
fig.set_dpi(100)

plt.show()
```

![png](/assets/images/double-pendulum/section-1-basics-of-plotting/distance-and-velocity-different-axes-unfinished.png)

Let's break down the code that we have written. The `plt.subplots()` method returns to us a `Figure` and `Axes` object. Each `Axes` object is in itself an entire plot, with it's own labels, ticks, legends and everything else. This gives us a very fine level of control. It is worth noting that all methods used to set the various properties start with `set_`. So, when in doubt one can just look through the methods list starting with `set_`.

However, we can still add some finishing touches to the plot we have created. This is where we start seeing the power that can be derived from the flexibility of the Object Oriented Approach.

```python
fig, ax1 = plt.subplots()

ax1.set_ylabel("distance (m)", color="blue")
ax1.set_xlabel("time")
ax1.plot(time, distance, "blue")
ax1.set_yticks(np.linspace(*ax1.get_ybound(), 10))
ax1.tick_params(axis="y", labelcolor="blue")
ax1.xaxis.grid()
ax1.yaxis.grid()

ax2 = ax1.twinx() # create another y-axis sharing a common x-axis

ax2.set_ylabel("velocity (m/s)", color="green")
ax2.set_xlabel("time")

ax2.tick_params(axis="y", labelcolor="green")
ax2.plot(time, velocity, "green")
ax2.set_yticks(np.linspace(*ax2.get_ybound(), 10))

fig.set_size_inches(7,5)
fig.set_dpi(100)
fig.legend(["Distance", "Velocity"])
plt.show()
```

![png](/assets/images/double-pendulum/section-1-basics-of-plotting/distance-and-velocity-different-axes-finished.png)

## Conclusion

In this part, we covered some basics of `matplotlib` plotting, covering the basic two approaches of how to make plots. In the next part, we will cover how to make simple animations.

## References

1. [Matplotlib: An Introduction to its Object-Oriented Interface](https://medium.com/@kapil.mathur1987/matplotlib-an-introduction-to-its-object-oriented-interface-a318b1530aed)
2. [Lifecycle of a Plot](https://matplotlib.org/3.2.1/tutorials/introductory/lifecycle.html)
3. [Basic Concepts](https://matplotlib.org/faq/usage_faq.html)
