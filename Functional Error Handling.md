My thesis is that most of what we've been working towards in programming—whether we are aware of it or not—is about composability. And the first question this produces is: “What do you mean by that?” I’d argue that discovering the very definition of composability is part of this path, as we’ve seen different definitions depending on the programming language paradigm under scrutiny.

Here’s the definition I put forward:

> Composability: the ability to assemble bigger pieces from smaller pieces.

This is less-precise than some definitions; for example, composition in object-oriented programming means “putting objects inside other objects.” However, that fits with my overall definition; it achieves the same goal but in a specific way. When dealing with functions, composability means “calling functions from within other functions.”

To enable the easy construction of programs, we need to be able to effortlessly assemble components in the same way that a child assembles Legos—by simply sticking them together, without requiring extra activities to do so. On top of that, such assemblages become their own components that can be stuck together just as easily. This composability scales up regardless of the size of the components.

Over the years we have encountered numerous roadblocks to this goal. Let’s look at a few of these.

## Goto Considered Harmful