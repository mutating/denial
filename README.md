<details>
  <summary>ⓘ</summary>

[![Downloads](https://static.pepy.tech/badge/denial/month)](https://pepy.tech/project/denial)
[![Downloads](https://static.pepy.tech/badge/denial)](https://pepy.tech/project/denial)
[![Coverage Status](https://coveralls.io/repos/github/mutating/denial/badge.svg?branch=main)](https://coveralls.io/github/mutating/denial?branch=main)
[![Lines of code](https://sloc.xyz/github/mutating/denial/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/mutating/denial?branch=main&label=Hits-of-Code&exclude=docs/)](https://hitsofcode.com/github/mutating/denial/view?branch=main)
[![Test-Package](https://github.com/mutating/denial/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/mutating/denial/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/denial.svg)](https://pypi.python.org/pypi/denial)
[![PyPI version](https://badge.fury.io/py/denial.svg)](https://badge.fury.io/py/denial)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/mutating/denial)

</details>


![logo](https://raw.githubusercontent.com/mutating/denial/develop/docs/assets/logo_1.svg)

Python's built-in [`None`](https://docs.python.org/3/library/constants.html#None) constant may not be sufficient to [distinguish situations](https://en.wikipedia.org/wiki/Semipredicate_problem) where a value is *undefined* from situations where it is *defined as undefined*. If that sounds abstract, see the detailed [description of the problem](#the-problem) and its [solutions](#analogs) below.


## Table of contents

- [**The problem**](#the-problem)
- [**Installation**](#installation)
- [**The second `None`**](#the-second-none)
- [**Your own `None` objects**](#your-own-none-objects)
- [**Type hinting**](#type-hinting)
- [**Analogs**](#analogs)
- [**FAQ**](#faq)


## The problem

Programmers encounter uncertainty everywhere. We [don't know](https://en.wikipedia.org/wiki/Semipredicate_problem) in advance whether a user will enter a valid value into a form, or whether a given operation on two numbers is possible. To highlight uncertainty as a separate entity, programmers have come up with so-called [sentinel objects](https://en.wikipedia.org/wiki/Sentinel_value). These can take many forms: [`NULL`](https://en.wikipedia.org/wiki/Null_pointer), [`None`](https://docs.python.org/3/library/constants.html#None), [`nil`](https://ru.wikipedia.org/wiki/Nil), [`undefined`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/undefined), [`NaN`](https://en.wikipedia.org/wiki/NaN), and an infinite number of others.

Different programming languages and environments offer [different models](#analogs) for representing uncertainty as objects. This is usually related to how a particular language has evolved and what forms of uncertainty its users most often encounter. Broadly, I see [three](https://numberwarrior.wordpress.com/2010/07/30/is-one-two-many-a-myth/) main models:

- **One simple sentinel object**. This approach works great in most cases. In most real code, we don't need to distinguish between more than one type of uncertainty. This is the default model offered by Python (although there is much room for debate here: for example, [exceptions](https://docs.python.org/3/tutorial/errors.html#exceptions) can, in a sense, also be considered sentinel objects). However, it breaks down when we need to [distinguish between](https://en.wikipedia.org/wiki/I_know_that_I_know_nothing) situations where *we know we don't know* something and situations where *we don't know that we don't know* something.

- **Two sentinel objects**. This is more common in languages where, for example, a lot of user input is processed and where it is necessary to distinguish between different types of empty values. If our task is to program Socrates, that will be quite sufficient.

- **An infinite recursive hierarchy of sentinel objects**. From a philosophical point of view, uncertainty cannot be considered a finite object, because that would already be a definite judgment about uncertainty. Therefore, we should consider uncertainty as consisting of an infinite number of layers. In practice, such structures can arise, for example, when we extract data from a large number of diverse sources but want to clearly distinguish at which stage of the pipeline the data was not found.

![One, Two, Many](https://imgs.xkcd.com/comics/one_two.png)

> *Yes, this library was also created by [primitive cultures](https://en.wiktionary.org/wiki/Pythonist#English)*

The first option is almost always sufficient. The `denial` library offers special primitives for the second and third options to address the remaining uncertainty cases in Python:

- The first option is built into Python and does not require any third-party libraries: [`None`](https://docs.python.org/3/library/constants.html#None).
- The second option is represented by the [`InnerNone`](#the-second-none) constant from `denial`. It is practically the same as `None`, just a second `None`.
- For the most complex cases, you can create your own sentinel objects using the [`InnerNoneType`](#your-own-none-objects) class from `denial`.

As you can see, `denial` provides primitives only for rare cases of complex forms of uncertainty, which are practically never encountered in everyday programming. However, this is much more common among programmers who create their own libraries.


## Installation

Install [`denial`](https://pypi.org/project/denial/) with `pip`:

```bash
pip install denial
```

You can also use [`instld`](https://github.com/pomponchik/instld) to quickly try out this package and others without installing them.


## The second `None`

This library defines an object that is used much like the built-in `None`. This is how it is imported:

```python
from denial import InnerNone
```

Like `None`, this object compares equal only to itself:

```python
print(InnerNone == InnerNone)
#> True
print(InnerNone == False)
#> False
```

This object is also an instance of the [`InnerNoneType`](#your-own-none-objects) class (an analog of [`NoneType`](https://docs.python.org/3/library/types.html#types.NoneType), though it does not inherit from it), which means you can check it with [`isinstance`](https://docs.python.org/3/library/functions.html#isinstance):

```python
from denial import InnerNoneType

print(isinstance(InnerNone, InnerNoneType))
#> True
```

Like `None`, `InnerNone` (as well as all other `InnerNoneType` objects) is always falsy:

```python
print(bool(InnerNone))
#> False
```

> ⓘ It is recommended to use the `InnerNone` object inside libraries where a value close to `None` is required, but to indicate that a value is unset rather than explicitly set to `None`. This object should be kept entirely out of user-facing code. None of the public methods of your library should return this object.


## Your own `None` objects

If `None` and [`InnerNone`](#the-second-none) are not enough for you, you can create your own similar objects by instantiating `InnerNoneType`:

```python
sentinel = InnerNoneType()
```

This object will also be equal only to itself:

```python
print(sentinel == sentinel)
#> True

print(sentinel == InnerNoneType())  # Comparison with another object of the same type
#> False
print(sentinel == InnerNone)  # Also comparison with another object of the same type
#> False
print(sentinel == None)  # Comparison with None
#> False
print(sentinel == 123)  # Comparison with an arbitrary object
#> False
```

You can also pass an integer or a string to the class constructor. An `InnerNoneType` object is equal to another such object with the same argument:

```python
print(InnerNoneType(123) == InnerNoneType(123))
#> True
print(InnerNoneType('key') == InnerNoneType('key'))
#> True

print(InnerNoneType(123) == InnerNoneType(1234))
#> False
print(InnerNoneType('key') == InnerNoneType('another key'))
#> False
print(InnerNoneType(123) == InnerNoneType())
#> False
print(InnerNoneType(123) == 123)
#> False
```

> 💡 Any `InnerNoneType` objects can be used as keys in dictionaries.

> ⚠️ For most situations, I do not recommend passing arguments to the class constructor. This can lead to situations where two identifiers from different parts of your code accidentally end up being the same, which can result in errors that are difficult to catch. If you do not pass arguments, the uniqueness of each `InnerNoneType` object created is guaranteed.

All `InnerNoneType` objects have concise string representations:

```python
print(InnerNone)
#> InnerNone
print(InnerNoneType())
#> InnerNoneType(1)
print(InnerNoneType())
#> InnerNoneType(2)
print(InnerNoneType(123))
#> InnerNoneType(123, auto=False)
```

You can also add a documentation string to the object. It will also appear in the string representation:

```python
print(InnerNoneType(doc='My doc string!'))
#> InnerNoneType(1, doc='My doc string!')
print(InnerNoneType(123, doc='My doc string!'))
#> InnerNoneType(123, doc='My doc string!', auto=False)
```

Documentation strings are not taken into account when comparing `InnerNoneType` objects.


## Type hinting

> When used in a type hint, the expression `None` is considered equivalent to `type(None)`.

> *[Official typing documentation](https://typing.python.org/en/latest/spec/special-types.html#none)*

`None` is a special value for which Python type checkers make an exception, allowing it to be used as an annotation of its own type. Unfortunately, this behavior cannot be reproduced without changing the internal implementation of existing type checkers, which I would not expect to happen unless the [PEP](https://peps.python.org/pep-0661/) is adopted. However, there is one type checker that can work with objects from `denial`: [`simtypes`](https://github.com/mutating/simtypes). But this tool is minimal and intended only for runtime use.

Therefore, it is recommended to use the `InnerNoneType` class as a type annotation:

```python
def function(default: int | InnerNoneType):
    ...
```

If you need a universal annotation for `None` and [`InnerNoneType`](#your-own-none-objects) instances, use the `SentinelType` annotation:

```python
from denial import SentinelType

variable: SentinelType = InnerNone
variable: SentinelType = InnerNoneType()
variable: SentinelType = None  # All 3 annotations are correct.
```

On the other hand, some programmers care deeply about type safety and prefer to delegate more type checking to static type checkers such as [`mypy`](https://mypy-lang.org/). In such cases, it may be useful to create your own types based on `InnerNoneType`:

```python
class MySentinelType(InnerNoneType):
    ...

def some_function(sentinel: MySentinelType):
    ...
```

At runtime, a derived class behaves exactly like `InnerNoneType` and lets you narrow the intended usage of a specific sentinel type.

If you need to prevent more than one instance of your class from being created, use the `singleton` flag:

```python
class MySentinelType(InnerNoneType, singleton=True):
    ...

sentinel = MySentinelType()
second_sentinel = MySentinelType()
#> ...
#> denial.errors.DoubleSingletonsInstantiationError: Class "MySentinelType" is marked with a flag prohibiting the creation of more than one instance.
```

To avoid misunderstandings, if you mark a class with the `singleton` flag, all its descendants must also have this flag.


## Analogs

Programmers often face [the problem of distinguishing types of uncertainty](#the-problem) and they solve it in a variety of ways. This problem concerns all programming languages, because it ultimately describes our *knowledge*, and the [questions about knowledge](https://colinmcginn.net/truth-value-gaps-and-meaning/) are universal. And everyone (including me!) has [*their own opinions*](https://en.wikipedia.org/wiki/Not_invented_here) on how to solve this problem.

![standards](https://imgs.xkcd.com/comics/standards.png)
> *Current state of affairs*

Some languages provide more explicit built-in support for this distinction than Python. For example, [JavaScript](https://en.wikipedia.org/wiki/JavaScript) explicitly distinguishes between `undefined` and `null`. Likely because [form](https://en.wikipedia.org/wiki/HTML_form) validation is often written in JS, and it often requires such a distinction. However, this approach is not completely universal, since in the general case the number of layers of uncertainty is infinite, and here there are only two of them. In contrast, `denial` provides both features: the basic [`InnerNone`](#the-second-none) constant for simple cases and the ability to create an unlimited number of [`InnerNoneType`](#your-own-none-objects) instances for complex ones. Other languages, such as [AppleScript](https://en.wikipedia.org/wiki/AppleScript) and [SQL](https://en.wikipedia.org/wiki/SQL), also distinguish several different types of undefined values. A separate category includes languages like [Rust](https://en.wikipedia.org/wiki/Rust_(programming_language)), [Haskell](https://en.wikipedia.org/wiki/Haskell), [OCaml](https://en.wikipedia.org/wiki/OCaml), and [Swift](https://en.wikipedia.org/wiki/Swift_(programming_language)), which use algebraic data types.

The Python standard library uses at least [15 sentinel objects](https://mail.python.org/archives/list/python-dev@python.org/message/JBYXQH3NV3YBF7P2HLHB5CD6V3GVTY55/):

- **_collections_abc: __marker__**
- **cgitb.__UNDEF__**
- **configparser: _UNSET**
- **dataclasses: _HAS_DEFAULT_FACTORY, MISSING, KW_ONLY**
- **datetime.timezone._Omitted**
- **fnmatch.translate() STAR**
- **functools.lru_cache.sentinel** (each @lru_cache creates its own sentinel object)
- **functools._NOT_FOUND**
- **heapq**: temporary sentinel in nsmallest() and nlargest()
- **inspect._sentinel**
- **inspect._signature_fromstr()** invalid
- **plistlib._undefined**
- **runpy._ModifiedArgv0._sentinel**
- **sched: _sentinel**
- **traceback: _sentinel**

Because Python does not standardize sentinels, projects often implement them independently. Before creating this library, I used one of them, but later realized that importing a module that I don't need for anything other than its sentinel object is a bad idea.

I wasn't the only one to come to this conclusion; the community also tried to standardize it. A standard for sentinels was proposed in [PEP-661](https://peps.python.org/pep-0661/), but at the time of writing it has still not been adopted, as there is no consensus on a number of important issues. This topic was also indirectly raised in [PEP-484](https://peps.python.org/pep-0484/), as well as in [PEP-695](https://peps.python.org/pep-0695/) and in [PEP-696](https://peps.python.org/pep-0696/). Without an official solution, projects continue to reinvent the wheel. Some projects, such as [Pydantic](https://github.com/pydantic/pydantic/issues/12090), already behave as though `PEP-661` were adopted. Personally, I don't like the solution proposed in `PEP-661`, mainly because of the implementation examples that suggest using a global registry of all created sentinels, which can lead to memory leaks and concurrency limitations.

In addition to `denial`, there are many packages with sentinels on [`PyPI`](https://pypi.org/). For example, there is the [sentinel](https://pypi.org/project/sentinel/) library, but its API seemed overcomplicated to me for such a simple task. The [sentinels](https://pypi.org/project/sentinels/) package is quite simple, but in its internal implementation it also relies on the [global registry](https://github.com/vmalloc/sentinels/blob/37e67ed20d99aa7492e52316e9af7f930b9ac578/sentinels/__init__.py#L11) and has some other implementation issues. The [sentinel-value](https://github.com/vdmit11/sentinel-value) package is very similar to `denial`, but I did not see the possibility of auto-generating sentinel IDs there. Of course, there are other packages that I haven't reviewed here.

And of course, there are still different ways to implement primitive sentinels in just a few lines without using third-party packages.


## FAQ

<a name="q1">Q1</a>: Is this library the best option for sentinels?

A: Sentinels seem conceptually simple: we just need more `None`-like values. In practice, creating a good sentinel design is one of the most difficult issues. There are too many ways to do this and too many trade-offs in which you need to choose a side. So I'm not claiming to be the best solution to this issue, but I've tried to eliminate all the obvious disadvantages that don't involve trade-offs. I'm not sure if it's even possible to find *the best solution* in this area, so all I can do is make *[an arbitrary decision](https://en.wikipedia.org/wiki/Analysis_paralysis)* and stick to it. If you want, join me.

<a name="q2">Q2</a>: Why is the uniqueness of the values not ensured? The `None` object is a singleton. In Python, it is impossible to access the `None` name and get a different value. But in `denial`, it is possible for a user to create two different objects by passing two identical IDs there. In rare cases, this can lead to unintended errors, for example, if the same identifier is accidentally used in two different places in the program. Why is that?

A: To ensure that a certain value is used in the program only once, there are two possible ways:

1. create a registry of all such values and check each new value for uniqueness at runtime.
2. check the source code statically, for example using a special [linter](https://en.wikipedia.org/wiki/Lint_(software)).

I found the second option too difficult for now, so the first one remains. The main problem is the possibility of [memory leaks](https://en.wikipedia.org/wiki/Memory_leak). There is a good general rule for programming: rely as little as possible on global state, because it can create unexpected side effects. For example, if you create unique identifiers in a loop, the registry may overflow. You might argue that nobody would create them in a loop, but I’d rather not rely on that. It also creates problems with concurrency. The fact is that checking the value in the registry and entering it into the registry are two independent operations that take some time between them, which means that errors are possible due to a [race condition](https://en.wikipedia.org/wiki/Race_condition). If you protect this operation with a [mutex](https://en.wikipedia.org/wiki/Lock_(computer_science)), it will increase the sequential portion of execution time, which means it will slow down the entire program due to [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law). This matters if sentinel creation is frequent in a given workload, which could create performance problems (it's time to make fun of Python's performance because of the [GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock), but I hope for a better future). The current compromise is this: always use [`InnerNoneType`](#your-own-none-objects) without arguments, unless you have a serious reason to do otherwise. In this case, the uniqueness of each object is guaranteed, since "under the hood", each time a new object is created, an internal counter is incremented (thread-safe!), and that value becomes the object's unique identifier.

<a name="q3">Q3</a>: Why would you use `InnerNoneType` with arguments? It always seems like a bad idea. How about removing this feature altogether?

A: This is *almost always* a bad idea. But in some extremely *rare cases*, it can be useful. It may be that two sections of code that do not know about each other may need to exchange a compatible sentinel. It is even possible that it will be transmitted over the network and "recreated" on the other side. It is for such cases that the option to use your own identifiers has been left. But it's better to call `InnerNoneType()` without arguments.

<a name="q4">Q4</a>: Why not use a separate singleton class for each sentinel use case? Then it will be possible to make checks through [`isinstance`](https://docs.python.org/3/library/functions.html#isinstance), and it will also be possible to write more accurate type hints.

A: The ability to use classes as type hints is a compelling argument. It would be possible to create several classes in different parts of the program, assigning different semantics to each of them, and then checking compatibility using a type checker such as [`mypy`](https://mypy-lang.org/). However, I did not make this a basic mechanism for `denial`, as I believe that in most cases the semantics will not actually differ. At the same time, creating a new class each time is more verbose than creating objects. However, I left the option to inherit from `InnerNoneType` if you still consider it necessary in your code. Instances of derived classes (if you do not override the behavior of the class in any way) will behave the same as `InnerNoneType` objects. But they will not be singletons, which allows you to group several different objects with the same semantics within a single class.

<a name="q5">Q5</a>: You're using only one `InnerNoneType` class, but the internal ID that makes objects unique can be either generated automatically or passed by the user. Doesn't this mean that it would be worthwhile to split this into two separate classes?

A: I did this to reduce cognitive load. I haven't seen any cases where a clear division into two classes provides a practical (rather than aesthetic) benefit, while you don't have to think about which class to import and how its use differs.

<a name="q6">Q6</a>: Why is `InnerNoneType` not inherited from `NoneType`?

A: These classes serve very similar purposes. However, I felt that inheriting from `NoneType` could break existing code, which might expect that only one `NoneType` instance exists, and therefore uses the `isinstance` check as an analog of the `is None` check. However, I cannot give figures on how often such constructions occur in existing code. It would be interesting to measure this using the GitHub API.

<a name="q7">Q7</a>: How is the uniqueness of `InnerNoneType` objects ensured?

A: If you create `InnerNoneType` objects without passing any arguments to the constructor, each object receives a process-unique ID at creation time. It is by this ID that the object will check whether it is equal to another `InnerNoneType` object. It will be equal to another object only if it has the same ID inside it, which is usually impossible, and therefore the object remains equal only to itself. If you passed your own ID when creating the object, the automatic ID is not created, yours is used. In this case, it is your job to track possible collisions. The library can also distinguish between objects where the ID is created automatically and where it is passed from outside, using a special flag inside each value. This guarantees that there are no intersections between automatically generated and non-automatically generated IDs.

<a name="q8">Q8</a>: Why all these complications and an additional library for sentinels? I just write `sentinel = object()` in my code and then do checks like `x is sentinel`. It works, but you've overcomplicated things.

A: Indeed, we already have one source of unique IDs for objects: their addresses in memory. Checks like `x is sentinel` can be semantically equivalent to those used in this library. However, this option has two significant drawbacks. First, you lose the compactness of string representation that `denial` provides. Second, this method does not allow you to create two identical sentinel objects if you want to, which prevents you from, for example, transferring sentinel objects over the network or between processes. Unfortunately, this is impossible with memory addresses. Since this library is positioned as universal, I had to abandon this option.

<a name="q9">Q9</a>: Why don't we use [Enums](https://docs.python.org/3/library/enum.html) as sentinels? It's already in the standard library, no need to invent anything. And it can do all the things we expect from sentinels.

A: [Various](https://t.me/ru_python/2680685) [people](https://www.reddit.com/r/Python/comments/1qraodv/comment/o2n0d94/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button) have suggested this method to me, and it was also mentioned in [PEP-661](https://peps.python.org/pep-0661/). The PEP argues that Enum's `__repr__` is too long. In `denial`, I made a short and informative `__repr__`, which should be sufficient in principle. However, here are some other reasons not to use Enum: 1. Denial can be used in recursive algorithms where the number of nesting levels is unknown in advance. This is possible because the number of distinct sentinel values is not limited here. In the case of Enum, you must know the number of nesting levels in advance. 2. Using a single Enum class with all sentinels in the program contradicts the idea of modularity. In essence, this is equivalent to using global variables, which is usually a code smell. If you create an Enum class for each sentinel, it will look too verbose. 3. Under the hood, Enum uses the global registry approach that I discussed in the FAQ section of the README. 4. Enum usually has slightly different semantics. For example, I can hardly imagine a situation where I would want to iterate through all sentinels. 5. Enum is generally [too complex](https://t.me/opensource_findings/883) a tool for such a simple purpose. In my opinion, the entire Enum module should have been deprecated long ago. The sheer size of the module's documentation and the existence of several official manuals for it suggest that something is wrong here. 6. Another argument may seem ridiculous given the slowness of CPython, but I'll mention it anyway. Enum forces the user to use values via a dot, such as `EnumClass.SENTINEL`. This leads to an unnecessary lookup operation and a slight slowdown of the program. However, I haven't done any measurements, so perhaps this has been optimized in some way by the CPython developers.

<a name="q10">Q10</a>: Why does the `singleton` flag prohibit the creation of a second instance if you can simply return the same object?

A: There are different possible implementations of the [Singleton pattern](https://en.wikipedia.org/wiki/Singleton_pattern). In Python code, you often see implementations that “hide” the uniqueness check behind instance creation and simply return the first instance when you try to create a second one. But in my opinion, this implementation of the pattern is flawed because it hides the true nature of objects from the reader, which violates [the Zen of Python](https://en.wikipedia.org/wiki/Zen_of_Python) ("explicit is better than implicit"). The code implicitly propagates attempts to create multiple objects of the same class, when in fact only one object is needed. In my opinion, if we want an object to have only one instance, we should explicitly prohibit the creation of more than one instance. In this case, there will be no more than one instance of the class in the codebase, which makes the code base more consistent and transparent.
