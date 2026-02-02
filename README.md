<details>
  <summary>ⓘ</summary>

[![Downloads](https://static.pepy.tech/badge/denial/month)](https://pepy.tech/project/denial)
[![Downloads](https://static.pepy.tech/badge/denial)](https://pepy.tech/project/denial)
[![Coverage Status](https://coveralls.io/repos/github/pomponchik/denial/badge.svg?branch=main)](https://coveralls.io/github/pomponchik/denial?branch=main)
[![Lines of code](https://sloc.xyz/github/pomponchik/denial/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/denial?branch=main&label=Hits-of-Code&exclude=docs/)](https://hitsofcode.com/github/pomponchik/denial/view?branch=main)
[![Test-Package](https://github.com/pomponchik/denial/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/denial/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/denial.svg)](https://pypi.python.org/pypi/denial)
[![PyPI version](https://badge.fury.io/py/denial.svg)](https://badge.fury.io/py/denial)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/pomponchik/denial)

</details>


![logo](https://raw.githubusercontent.com/pomponchik/denial/develop/docs/assets/logo_1.svg)

Python's built-in [`None`](https://docs.python.org/3/library/constants.html#None) constant may not be sufficient to [distinguish situations](https://en.wikipedia.org/wiki/Semipredicate_problem) where a value is *undefined* from situations where it is *defined as undefined*. Does that sound too abstract? Then read below the more detailed [description of the problem](#the-problem) and what [solutions](#analogues) exist for it.


## Table of contents

- [**The problem**](#the-problem)
- [**Installation**](#installation)
- [**The second None**](#the-second-none)
- [**Your own None objects**](#your-own-none-objects)
- [**Type hinting**](#type-hinting)
- [**Analogues**](#analogues)
- [**FAQ**](#faq)


## The problem

Programmers encounter uncertainty everywhere. We [don't know](https://en.wikipedia.org/wiki/Semipredicate_problem) in advance whether a user will enter a valid value into a form, or whether a given operation on two numbers is possible. To highlight uncertainty as a separate entity, programmers have come up with so-called [sentinel objects](https://en.wikipedia.org/wiki/Sentinel_value). These can be very different: [NULL](https://en.wikipedia.org/wiki/Null_pointer), [`None`](https://docs.python.org/3/library/constants.html#None), [nil](https://ru.wikipedia.org/wiki/Nil), [undefined](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/undefined), [NaN](https://en.wikipedia.org/wiki/NaN), and an infinite number of others.

Different programming languages and environments offer [different models](#analogues) for representing uncertainty as objects. This is usually related to how a particular language has evolved and what forms of uncertainty its users most often encounter. Globally, I distinguish [three](https://numberwarrior.wordpress.com/2010/07/30/is-one-two-many-a-myth/) main models:

- **One simple sentinel object**. This approach works great in most cases. In most real code, we don't need to distinguish between more than one type of uncertainty. This is the default model offered by Python (although there is much room for debate here: for example, [exceptions](https://docs.python.org/3/tutorial/errors.html#exceptions) can, in a sense, also be considered sentinel objects). However, it breaks down when we need to [distinguish between](https://en.wikipedia.org/wiki/I_know_that_I_know_nothing) situations where *we know we don't know* something and situations where *we don't know that we don't know* something.

- **Two sentinel objects**. This is more common in languages where, for example, a lot of user input is processed and where it is necessary to distinguish between different types of empty values. If our task is to program Socrates, that will be quite sufficient.

- **An infinite recursive hierarchy of sentinel objects**. From a philosophical point of view, uncertainty cannot be considered as a finite object, because that would already be a definite judgment about uncertainty. Therefore, we should consider uncertainty as consisting of an infinite number of layers. In practice, such structures can arise, for example, when we extract data from a large number of diverse sources but want to clearly distinguish at which stage of the pipeline the data was not found.

![One, Two, Many](https://imgs.xkcd.com/comics/one_two.png)

> *Yes, this library was also created by [primitive cultures](https://en.wiktionary.org/wiki/Pythonist#English)*

The first option is almost always sufficient. The `denial` library offers special primitives that cover the second and third options, providing complete coverage of uncertainty options for Python:

- The first option is built into Python and does not require any third-party libraries: [`None`](https://docs.python.org/3/library/constants.html#None).
- The second option is represented by the [`InnerNone`](#the-second-none) constant from `denial`. It is practically the same as `None`, just a second `None`.
- For the most complex cases, you can create your own sentinel objects using the [`InnerNoneType`](#your-own-none-objects) class from `denial`.

As you can see, `denial` provides primitives only for rare cases of complex forms of uncertainty, which are practically never encountered in everyday programming. However, this is much more common among programmers who create their own libraries.


## Installation

Install it:

```bash
pip install denial
```

You can also quickly try out this and other packages without having to install using [instld](https://github.com/pomponchik/instld).


## The second `None`

This library defines an object that is proposed to be used in almost the same way as a regular `None`. This is how it is imported:

```python
from denial import InnerNone
```

This object is equal only to itself:

```python
print(InnerNone == InnerNone)
#> True
print(InnerNone == False)
#> False
```

This object is also an instance of [`InnerNoneType`](#your-own-none-objects) class (an analog of [`NoneType`](https://docs.python.org/3/library/types.html#types.NoneType), however, is not inherited from this), which makes it possible to check through [`isinstance`](https://docs.python.org/3/library/functions.html#isinstance):

```python
from denial import InnerNoneType

print(isinstance(InnerNone, InnerNoneType))
#> True
```

Like `None`, `InnerNone` (as well as all other `InnerNoneType` objects) always returns `False` when cast to `bool`:

```python
print(bool(InnerNone))
#> False
```

> ⓘ It is recommended to use the `InnerNone` object inside libraries where a value close to `None` is required, but meaning a situation where the value is not really set, rather than set as `None`. This object should be completely isolated from the user code space. None of the public methods of your library should return this object.


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

All `InnerNoneType` objects have beautiful string mappings:

```python
print(InnerNoneType())
#> InnerNoneType(1)
print(InnerNoneType(123))
#> InnerNoneType(123, auto=False)
```

You can also add a documentation string to the object, it will also be displayed:

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

`None` is a special value for which Python type checkers make an exception, allowing it to be used as an annotation of its own type. Unfortunately, this behavior cannot be reproduced without changing the internal implementation of existing type checkers, which I would not expect until the [PEP](https://peps.python.org/pep-0661/) is adopted. However, there is one type checker that can work with objects from `denial`: [`simtypes`](https://github.com/pomponchik/simtypes). But this thing is very primitive and is only intended for runtime.

Therefore, it is suggested to use class `InnerNoneType` as a type annotation:

```python
def function(default: int | InnerNoneType):
    ...
```

In case you need a universal annotation for `None` and [`InnerNoneType`](#your-own-none-objects) objects, use the `SentinelType` annotation:

```python
from denial import SentinelType

variable: SentinelType = InnerNone
variable: SentinelType = InnerNoneType()
variable: SentinelType = None  # All 3 annotations are correct.
```


## Analogues

[The problem of distinguishing types of uncertainty](#the-problem) is often faced by programmers and they solve it in a variety of ways. This problem concerns all programming languages, because it ultimately describes our *knowledge*, and the [questions of cognition](https://colinmcginn.net/truth-value-gaps-and-meaning/) are universal for everyone. And everyone (including me!) has [*their own opinions*](https://en.wikipedia.org/wiki/Not_invented_here) on how to solve this problem.

![standards](https://imgs.xkcd.com/comics/standards.png)
> *Current state of affairs*

Some programming languages are a little better thought out in this matter than Python. For example, [JavaScript](https://en.wikipedia.org/wiki/JavaScript) explicitly distinguishes between `undefined` and `null`. I think this is due to the fact that [form](https://en.wikipedia.org/wiki/HTML_form) validation is often written in JS, and it often requires such a distinction. However, this approach is not completely universal, since in the general case the number of layers of uncertainty is infinite, and here there are only 2 of them. In contrast, `denial` provides both features: the basic [`InnerNone`](#the-second-none) constant for simple cases and the ability to create an unlimited number of [`InnerNoneType`](#your-own-none-objects) instances for complex ones. Other languages, such as [AppleScript](https://en.wikipedia.org/wiki/AppleScript) and [SQL](https://en.wikipedia.org/wiki/SQL), also distinguish several different types of undefined values. A separate category includes the languages like [Rust](https://en.wikipedia.org/wiki/Rust_(programming_language)), [Haskell](https://en.wikipedia.org/wiki/Haskell), [OCaml](https://en.wikipedia.org/wiki/OCaml), and [Swift](https://en.wikipedia.org/wiki/Swift_(programming_language)), which use algebraic data types.

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

Since the language itself does not regulate this in any way, there is chaos and code duplication. Before creating this library, I used one of them, but later realized that importing a module that I don't need for anything other than sentinel is a bad idea.

Not only did I come to this conclusion, the community also tried to standardize it. A standard for sentinels was proposed in [PEP-661](https://peps.python.org/pep-0661/), but at the time of writing it has still not been adopted, as there is no consensus on a number of important issues. This topic was also indirectly raised in [PEP-484](https://peps.python.org/pep-0484/), as well as in [PEP-695](https://peps.python.org/pep-0695/) and in [PEP-696](https://peps.python.org/pep-0696/). Unfortunately, while there is no "official" solution, everyone is still forced to reinvent the wheel on their own. Some, such as [Pydantic](https://github.com/pydantic/pydantic/issues/12090), are proactive, as if `PEP-661` has already been adopted. Personally, I don't like the solution proposed in `PEP-661`, mainly because of the implementation examples that suggest using a global registry of all created sentinels, which can lead to memory leaks and concurrency limitations.

In addition to `denial`, there are many packages with sentinels in [`Pypi`](https://pypi.org/). For example, there is the [sentinel](https://pypi.org/project/sentinel/) library, but its API seemed to me overcomplicated for such a simple task. The [sentinels](https://pypi.org/project/sentinels/) package is quite simple, but in its internal implementation it also relies on the [global registry](https://github.com/vmalloc/sentinels/blob/37e67ed20d99aa7492e52316e9af7f930b9ac578/sentinels/__init__.py#L11) and contains some other code defects. The [sentinel-value](https://github.com/vdmit11/sentinel-value) package is very similar to `denial`, but I did not see the possibility of autogenerating sentinel ids there. Of course, there are other packages that I haven't reviewed here.

And of course, there are still different ways to implement primitive sentinels in your code in a few lines of code without using third-party packages.


## FAQ

Q: Is this library the best option for sentinels?

A: Sentinel seems like a very simple task conceptually, we just need more `None`'s. But suddenly, creating a good sentinel option is one of the most difficult issues. There are too many ways to do this and too many trade-offs in which you need to choose a side. The design of sentinel objects is similar to the creation of axioms: it delves deep into parts of our psyche that are not usually subject to critical analysis, and therefore it is very difficult to talk about the problems that arise. So I'm not claiming to be the best solution to this issue, but I've tried to eliminate all the obvious disadvantages that don't involve trading. I'm not sure if it's even possible to find *the best solution* in this area, so all I can do is make *[an arbitrary decision](https://en.wikipedia.org/wiki/Analysis_paralysis)* and stick to it. If you want, join me.

Q: Why is the uniqueness of the values not ensured? The `None` object is a singleton. In Python, it is impossible to access the `None` name and get a different value. But in `denial`, it is possible for a user to create two different objects by passing two identical IDs there. In rare cases, this can lead to unintended errors, for example, if the same identifier is accidentally used in two different places in the program. Why is that?

A: To ensure that a certain value is used in the program only once, there are 2 possible ways: 1. create a registry of all such values and check each new value for uniqueness in runtime; 2. check the source code statically, for example using a special [linter](https://en.wikipedia.org/wiki/Lint_(software)). I found the second option too difficult for now, so the first one remains. The main problem is the possibility of [memory leaks](https://en.wikipedia.org/wiki/Memory_leak). There is a good general rule for programming: rely as little as possible on global state, because it can create unexpected side effects. For example, if you create unique identifiers in a loop, the registry may overflow. Would you say that no one will create them in a loop? Well, I'm not ready to take any chances. It also creates problems with concurrency. The fact is that checking the value in the registry and entering it into the registry are two independent operations that take some time between them, which means that errors are possible due to the [race condition](https://en.wikipedia.org/wiki/Race_condition). If you protect this operation with a [mutex](https://en.wikipedia.org/wiki/Lock_(computer_science)), it will increase the percentage of sequential execution time in the program, which means it will slow down the entire program due to [Amdahl's law](https://en.wikipedia.org/wiki/Amdahl%27s_law). Because I can imagine situations where creating sentinels would be a fairly frequent operation and it would create performance problems (it's time to make fun of Python's performance because of the [GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock), but I hope for a better future). Current compromise: always use [`InnerNoneType`](#your-own-none-objects) without arguments, unless you have a serious reason to do otherwise. In this case, the uniqueness of each object is guaranteed, since "under the hood", each time a new object is created, an internal counter is incremented (thread-safe!), which then checks the uniqueness of the object.

Q: What could be the reasons to use `InnerNoneType` with arguments? It always seems like a bad idea. How about removing this feature altogether?

A: This is *almost always* a bad idea. But in some extremely *rare cases*, it can be useful. It may be that two sections of code that do not know about each other will want to transfer a compatible sentinel to each other. It is even possible that it will be transmitted over the network and "recreated" on the other side. It is for such cases that the option to use your own identifiers has been left. But it's better to use empty brackets.

Q: Why not use a separate class with singleton objects for each situation when we need a sentinel? Then it will be possible to make checks through [`isinstance`](https://docs.python.org/3/library/functions.html#isinstance), and it will also be possible to write more accurate type hints.

A: The ability to use classes as type hints is a compelling argument. It would be possible to create several classes in different parts of the program, assigning different semantics to each of them, and then checking compliance using a type checker such as [`mypy`](https://mypy-lang.org/). However, I did not make this a basic mechanism for `denial`, as I believe that in most cases the semantics will not actually differ. At the same time, creating a new class each time is more verbose than creating objects. However, I left the option to inherit from `InnerNoneType` if you still consider it necessary in your code. Objects of inheriting classes (if you do not override the behavior of the class in any way) will behave the same as `InnerNoneType` objects. But they will not be singletons, which allows you to group several different objects with the same semantics within a single class.

Q: You're using only one `InnerNoneType` class, but the internal id that makes objects unique can be either generated automatically or passed by the user. Doesn't this mean that it would be worthwhile to allocate 2 independent classes?

A: I did this to reduce cognitive load. I haven't seen any cases where a clear division into two classes provides a practical (rather than aesthetic) benefit, while you don't have to think about which class to import and how its use differs.

Q: Why is `InnerNoneType` not inherited from `NoneType`?

A: The purpose of these classes is really quite similar. However, I felt that inheriting from `NoneType` could lead to breakdowns in the old code, which might expect that only one instance of `NoneType` is possible, and therefore uses the `isinstance` check as an analogue of the `is None` check. However, I cannot give figures on how often such constructions occur in existing code. Perhaps you should collect such statistics using the GitHub API.

Q: How is the uniqueness of `InnerNoneType` objects ensured?

A: If you create `InnerNoneType` objects without passing any arguments to the constructor, an id that is unique within the process is created inside each object when it is created. It is by this id that the object will check whether it is equal to another `InnerNoneType` object. It will be equal to another object only if it has the same id inside it, which is usually impossible, and therefore the object remains equal only to itself. If you passed your own id when creating the object, the automatic id is not created, yours is used. In this case, it is your job to track possible unwanted intersections. The library can also distinguish between objects where the id is created automatically and where it is passed from outside, using a special flag inside each value. This guarantees that there are no intersections between automatically generated and non-automatically generated ids.

Q: Why all these complications and an additional library for sentinels? I just write `sentinel = object()` in my code and then do checks like `x is sentinel`. It works, but you've overcomplicated things.

A: Indeed, we already have one source of unique IDs for objects: their addresses in memory. Checks of the type x is sentinel can be identical in meaning to those used in this library. However, this option has two significant drawbacks. First, you lose the compactness of string representation that `denial` provides. Second, this method does not allow you to create two identical sentinel objects if you want to, which prevents you from, for example, transferring sentinel objects over the network or between processes. Unfortunately, this is impossible with memory addresses. Since this library is positioned as universal, I had to abandon this option.
