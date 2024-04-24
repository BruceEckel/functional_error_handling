My thesis is that most of what we've been working towards in programming—whether we are aware of it or not—is about composability. And the first question this produces is: “What do you mean by that?” I’d argue that discovering the very definition of composability is part of this path, as we’ve seen different definitions depending on the programming language paradigm under scrutiny.

Here’s the definition I put forward:

> Composability: the ability to assemble bigger pieces from smaller pieces.

This is less-precise than some definitions; for example, composition in object-oriented programming means “putting objects inside other objects.” However, that fits with my overall definition; it achieves the same goal but in a specific way. When dealing with functions, composability means “calling functions within other functions.”

To enable the easy construction of programs, we need to be able to effortlessly assemble components in the same way that a child assembles Legos—by simply sticking them together, without requiring extra activities to do so. On top of that, such assemblages become their own components that can be stuck together just as easily. This composability scales up regardless of the size of the components.

Over the years we have encountered numerous roadblocks to this goal. Let’s look at a few of these.
## Goto Considered Harmful

[Djikstra’s 1968 note](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) had quite an impact on the programming community, which at the time consisted largely of assembly-language programmers. For these, the goto statement was foundational, and denigrating it was a shock. Although he never explicitly mentioned functions in his note, the effect was to push programmers towards functions. [The creator of Structured Concurrency](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/) provides a clear description of this.

Rather than jumping about within a limited program, functions restrict you to a single entry and single exit point, and this dramatically improves composability because you can no longer leave a section of code at any point using a goto (note that within a function scope you cannot know what’s outside that scope, thus you can’t jump somewhere because you don’t know a destination to jump to). 

My programming training was primarily as a computer engineer and I spent the first few years of my career programming in assembly. Assembly supports subroutine calls and returns, but not the loading of arguments on the stack and passing results back out—the programmer must write this error-prone code by hand.

Higher-level languages handle function arguments and returns for you, which made them a very desirable improvement as the size and complexity of programs grew beyond what the assembly programmer was able to hold in their head.
## Modules

Tim Peters’ observation of the value of namespaces (see [The Zen of Python](https://peps.python.org/pep-0020/)) is the core of the idea of modules, which more modern languages incorporate (unfortunately C++ had to inherit C’s messy system, for backwards compatibility). In Python, files are automatically modules which is certainly one of the easiest solutions.

But it wasn’t always this way. Breaking assembly-language programs into pieces was not easy, and early higher-level languages did not consider modularity. When the idea began to surface it was incorporated as a main feature of the Modula-2 language (a descendent of Pascal). The name tells you what a significant shift it was considered at the time.

Modula-2 and similar languages required an explicit declaration of a module:
```modula-2
MODULE Hello;
FROM STextIO IMPORT WriteString;
BEGIN
  WriteString("Hello World!")
END Hello.
```
This allowed complete granularity independent of file organization; perhaps this was because programmers were used to thinking in terms of a big file-per-program. Python’s merging of modules with files makes more sense in hindsight and has the benefit of eliminating the [(significant) extra verbiage](https://en.wikipedia.org/wiki/Modula-2), only a portion of which is shown here.

The main benefit of modules is name control—each module creates a scope for names (a namespace) which allows programmers the freedom to choose any name at will within a module. This prevents name collisions across a project and reduces the cognitive load on the programmer. Prior to this, programs reached scaling limits as they grew larger. Program size in assembly language programs was limited by many different factors, so the need for modules was not seen until systems were able to grow larger because higher-level languages solved enough of these other factors.

In modern languages, modularity is part of the background of a language and we don’t think much about it. At one time, however, the lack of modularity was a significant roadblock to code composability.
## Inheritance

Object-oriented programming has a bit of a tortured history. Although the first OO language was Simula-67 (a compiled language), OO found its first real success with Smalltalk. But Smalltalk might be the most dynamic language you’ll ever encounter—literally everything is evaluated at runtime. While this worked well for the kinds of problems Smalltalk was good at solving, it turned out that taking the ideas of Smalltalk and imprinting them into a statically-typed language lost a LOT in translation

## Error Handling

The focus of this paper is a significant impediment to composability.
### History

The original programs were small (by present-day standards), written in assembly language (after machine code rapidly became too unwieldy), and tightly coupled to the underlying hardware.
### The Problem with Exceptions
maybe you can't prove it, things work in the small but don't scale). We only figure it out when scaling composability.
### Two Kinds of Errors
Recoverable vs panic