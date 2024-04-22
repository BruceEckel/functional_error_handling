My thesis is that most of what we've been working towards in programming—whether we are aware of it or not—is about composability. And the first question this produces is: “What do you mean by that?” I’d argue that discovering the very definition of composability is part of this path, as we’ve seen different definitions depending on the programming language paradigm under scrutiny.

Here’s the definition I put forward:

> Composability: the ability to assemble bigger pieces from smaller pieces.

This is less-precise than some definitions; for example, composition in object-oriented programming means “putting objects inside other objects.” However, that fits with my overall definition; it achieves the same goal but in a specific way. When dealing with functions, composability means “calling functions from within other functions.”

To enable the easy construction of programs, we need to be able to effortlessly assemble components in the same way that a child assembles Legos—by simply sticking them together, without requiring extra activities to do so. On top of that, such assemblages become their own components that can be stuck together just as easily. This composability scales up regardless of the size of the components.

Over the years we have encountered numerous roadblocks to this goal. Let’s look at a few of these.
## Goto Considered Harmful

[Djikstra’s 1968 note](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) had quite an impact on the programming community, which at the time largely consisted of assembly-language programmers. For these, the goto statement was foundational and denigrating it was a shock. Although he never explicitly mentioned functions in his note, the effect was to push programmers towards functions. [The creator of Structured Concurrency](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/) makes a strong case for this.

Rather than jumping about within a limited program, functions restrict you to a single entry and single exit point, and this dramatically improves composability because you can no longer leave a section of code at any point using a goto (note that within a function scope you cannot know what’s outside that scope, thus you can’t jump somewhere because you don’t know a destination to jump to). 

My programming training was primarily as a computer engineer and I spent the first few years of my career programming in assembly. Assembly supports subroutine calls and returns, but not the loading of arguments on the stack and passing results back out—the programmer must write this error-prone code by hand.

Higher-level languages handle function arguments and returns for you, which made them a very desirably improvement as the size and complexity of programs grew beyond what the assembly programmer was able to hold in their head.
## Modules

## Inheritance

## The History of Error Handling

### The Problem with Exceptions
maybe you can't prove it, things work in the small but don't scale). We only figure it out when scaling composability.
### Two Kinds of Errors
Recoverable vs panic