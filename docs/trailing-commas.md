---
tags:
  - Kotlin
  - Code Style
---
# Trailing Commas in Kotlin

## Opinionated TLDR

- Trailing commas provide tangible benefits that outweigh any drawbacks (once fully adopted)
- Configure your static analysis (presumably [ktlint](https://github.com/pinterest/ktlint) or [detekt-formatting](https://github.com/detekt/detekt?tab=readme-ov-file#adding-more-rule-sets)) to mandate trailing commas.
- Enable some kind of tooling to help automate trailing comma addition (e.g. pre-commit hooks, dependent gradle tasks, etc.).

## What is a Trailing Comma?

A trailing comma is an optional comma that you put at the end of a list of line-broken arguments.
Take the following data class definition for example:

```kotlin
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
)
```
The comma after `val middleName: String?` is the trailing comma.
The comma isn't strictly necessary because there is no argument after `middleName`, but it is still considered syntactically correct. 
Trailing commas were introduced in [Kotlin 1.4](https://kotlinlang.org/docs/whatsnew14.html#trailing-comma).

Trailing can sometimes seem as contentious and potentially trivial as the [Oxford comma](https://en.wikipedia.org/wiki/Serial_comma), which makes them a great candidate for [bike-shedding](https://en.wikipedia.org/wiki/Law_of_triviality).
Indeed, once I started adding more trailing commas in a codebase that didn't have an enforced decision about whether to use them, I would often get "was this intentional?" comments in my code reviews.
At the other end, how useful is "a trailing comma might have prevented this" as a comment on a one-line commit fixing a merge issue?
At the end of the day, the choice to use or not use trailing commas isn't going to make or break your codebase, but leaving it up to each developer to make the choice for themselves is likely to burn more developer time than it's worth.

So, at minimum, I'd recommend putting forth some kind of official guidance for your codebase/organization encouraging or discouraging the use of trailing commas.
That way you can just follow whatever the official guidance is and resolve any code review comments with a link to the codebase/organization's official guidance.
I'd go even further by recommending a stronger stance of either mandating or forbidding trailing commas as part of your static code analysis tooling, which should prevent any unnecessary comments in the first place (see [Tooling](#tooling) section).

For the rest of this post, I will be arguing for why you should **mandate** trailing commas as opposed to forbidding them. 

## The Benefits of Trailing Commas

If you've never seen them before, trailing commas can seem like a weird choice.
However, there are several tangible benefits that make them worthwhile.

### Cleaner Diffs

Suppose we want to add an `age` property to `Person`.
If we do not initially have a trailing comma on the `middleName` property, then the diff will look like this:

```diff
data class Person(
    val givenName: String,
    val surname: String,
-   val middleName: String?
+   val middleName: String?,
+   val age: Int
)
```
But if we had the trailing comma on `middleName`, then the diff will have one less removal and one less addition:

```diff
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
+   val age: Int,
)
```
There is a slightly higher cognitive load to reading the first diff.
At first glance, you might ask "Why are we removing the middle name?" but after a moment it is clear that the line changed, and we're just adding a comma.
In the second diff, it's immediately clear that all we're doing is adding one new property.
It may not be a world-changing improvement, but it's still an improvement.

Adding arguments to class constructors, list creations, etc. is very common in almost any codebase.
So, while the immediate benefit is small, it adds up over the lifetime of the codebase.

### Reordering Arguments

A smaller (but perhaps more apparent) benefit of trailing commas is the ease of reordering arguments.
For example, if we wanted to move `middleName` so our `Person` class reads more in order, we would turn

```kotlin
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
)
```

into

```kotlin
data class Person(
    val givenName: String,
    val middleName: String?,
    val surname: String,
)
```

With the trailing comma present, we can easily select the whole line for the `middleName` property, cut, and paste it in the line above.
The result will have all of its commas and will compile cleanly (although you may have an issue with any call-sites that aren't using named arguments).

On the other hand, if we want to turn 
```kotlin
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?
)
```

into

```kotlin
data class Person(
    val givenName: String,
    val middleName: String?,
    val surname: String
)
```

Then cutting and pasting requires us to also move the cursor around to add a comma and remove another comma.
It's small, but it's annoying when you know there's an alternative world where you didn't have to do that.

Of course, there are also IDE shortcuts for moving lines up/down in JetBrains IDEs (and Android Studio): <kbd>⌘Сmd</kbd>+<kbd>Shift</kbd>+<kbd>↑</kbd>/<kbd>↓</kbd> on Mac or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>↑</kbd>/<kbd>↓</kbd> on Windows/Linux.
Using these commands automatically handles the commas for you and is usually easier than copy/paste as long as you can remember the commands.
If you use these commands, then trailing commas aren't better or worse in this case... until we compare the diffs again:

```diff
data class Person(
    val givenName: String,
-   val surname: String,
    val middleName: String?,
+   val surname: String,
)
```

vs.

```diff
data class Person(
    val givenName: String,
-   val surname: String,
-   val middleName: String?
+   val middleName: String?,
+   val surname: String
)
```

Again, we see a simpler diff in the trailing comma case, where it is clear that just one line moved.
Without trailing commas, we get two lines changing simultaneously, and it takes just a second more to comprehend it.
Again, it's not a huge difference, but it's still a difference.

### Easier Merge Conflict Resolution

Now suppose I want to add an age property, but someone else is adding a height property in another branch.
So, without trailing commas, I have 
```diff
data class Person(
    val givenName: String,
    val surname: String,
-   val middleName: String?
+   val middleName: String?,
+   val age: Int
)
```

and I will have a merge conflict with this change:
```diff
data class Person(
    val givenName: String,
    val surname: String,
-   val middleName: String?
+   val middleName: String?,
+   val height: Int
)
```
And the result of merging the other branch's code into mine will be

```kotlin
data class Person(
    val givenName: String,
    val surname: String,
<<<<<<< HEAD
    val middleName: String?,
    val age: Int
=======
    val middleName: String?,
    val height: Int
>>>>>>> other-branch
)
```

Whether I'm using a merge conflict tool or resolving this by hand, I'm going to have to delete an extraneous `middleName` property.
Also, if I'm not careful with my conflict resolution, I can easily end up with this

```kotlin
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
    val age: Int
    val height: Int
)
```

If I commit this code without verifying it, I could waste time waiting for the CI to reject it as not compilable (no comma after the `age` property).
It's an easy fix, just add the missing comma, but we wouldn't even be missing the comma if we were using trailing commas.

Suppose that we instead start with 
```diff
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
+   val age: Int,
)
```
and 
```diff
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
+   val height: Int,
)
```
then we'll still get a merge conflict, but it will be trivial to resolve:
```kotlin
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
<<<<<<< HEAD
    val age: Int,
=======
    val height: Int,
>>>>>>> other-branch
)
```
We just accept both changes and get
```kotlin
data class Person(
    val givenName: String,
    val surname: String,
    val middleName: String?,
    val age: Int,
    val height: Int,
)
```

If your codebase has any functions or lists that are regularly updated with new arguments such as test suites, feature flag definitions, etc., then this kind of conflict can come up regularly.
Unlike the previous arguments of "cognitive load" or saving a couple of seconds/keystrokes, an improperly handled merge conflict can cost you some real tangible time and CI resources.
Of course, you may be more careful with your merge conflicts, but that only matters if you're the only one working on this codebase.
It may not be a huge time/resource loss on an individual basis, but the benefits we gain here multiply as the number of developers and rate of PRs in your codebase grows.

## Drawbacks of Trailing Commas
There are a few drawbacks to trailing commas, but I argue that all of them are either negligible, temporary, or easily overcome with proper tooling.

### Aesthetics
A comma with no subsequent item?
It just kind of looks and feels wrong, doesn't it?
It certainly wouldn't look or be grammatically correct if we were to try to end sentence with a comma,

The fact that static analysis is often used to enforce rules around spacing of parentheses, empty lines, and locations of line breaks would indicate that the aesthetics argument should be enough of a reason to forbid trailing commas.
However, as I have already argued, they provide other tangible benefits, which isn't something we gain from not following other formatting rules.
I'll argue that any amount of tangible benefits should immediately render any aesthetic arguments null and void.

### Initial Adoption
The journey of getting from 0 to 100% trailing commas can be overwhelming.
No matter how you approach the PR(s) to get trailing commas into your existing codebase, you should definitely use some kind of automated tool (e.g. `ktlintFormat`, detekt auto-correct, IDE formatting with trailing commas enabled, etc.) to perform the actual additions.

The first approach you can take is to do an add-as-you-go approach.
That would mean adding commas to files as those files are changed.
Unfortunately, this can add a good deal of noise to diffs of existing files, which negates the expected benefits of cleaner diffs that I described above.

A more clear-cut rip-the-bandaid-off approach would be to add trailing commas to your entire codebase in one go.
Depending on the size of your codebase, this can result in an absolutely massive PR that no one wants to review.
This can also result in merge conflicts with any active working branches and open PRs, which negates the benefits of simpler merges described above.

A middle-ground choice would be to do more targeted PRs that update entire sections of your codebase at a time.
This should be straightforward to do if you have a well-modularized codebase.
This is extra work for the individual/team introducing the commas, but eases the burden for reviewers.

Whichever approach you take, this is a temporary hurdle.
As long as you've mandated trailing commas in your static analysis, then they're there to stay and you get all their benefits in perpetuity as soon as they're fully added to the existing code.

### Dev Adoption

You or your fellow devs may have issues remembering to adopt trailing commas into your daily code.
This can result in wasted time dealing with CI failures.
With the benefits of trailing commas being admittedly small, this can make them appear to be a net negative.

This can be mitigated with proper tooling so the trailing commas get added without anyone even needing to think about them.

## Tooling

Whether you choose to mandate or forbid trailing commas, it will only likely add overhead for your fellow devs without the proper tooling.

### Enforcing Your Trailing Comma Policy
You can enforce mandatory or forbidden trailing commas via [ktlint](https://github.com/pinterest/ktlint).
If you are using detekt, but you are not yet using ktlint in any fashion, then you can add [detekt-formatting](https://github.com/detekt/detekt?tab=readme-ov-file#adding-more-rule-sets) to your detekt configuration.
Detekt-formatting is just a wrapper around ktlint that plugs directly into your existing detekt checks.
Trailing commas were added to the standard ktlint ruleset in [ktlint 0.46.0](https://github.com/pinterest/ktlint/releases/tag/0.46.0) and to the detekt-formatting ruleset in [detekt 1.22.0](https://detekt.dev/changelog#1220---2022-11-20).
Ktlint will mandate trailing commas by default, but you will have to enable the rule in your detekt config if you use detekt-formatting[^1].

### Automatically Adding Commas

As detailed above, it can be difficult for devs to get into the habit of adding trailing commas.
There are a couple ways to make trailing commas a little more automatic:

- You can have the devs on your team install pre-commit hooks.
    - Ktlint [has instructions](https://pinterest.github.io/ktlint/latest/install/cli/#git-hooks) for setting up a pre-commit hook.
    - Detekt also [has instructions](https://detekt.dev/docs/gettingstarted/git-pre-commit-hook) for setting up pre-commit hooks.
- Ktlint and detekt also have IDE plugins that you can encourage your devs to use
- In Android Studio, you can turn on trailing commas
    - From the menu bar: `Android Studio` -> `Settings...` -> `Editor` -> `Code Style` -> `Kotlin` -> `Other` and check the "Use Trailing Commas" box.
    - Then, if you check in the `.idea/codeStyles` directory to your version control, everyone will share these settings.
    - This will automatically add trailing commas to code whenever a dev auto-formats a file (<kbd>⌘Сmd</kbd>+<kbd>⌥Option</kbd>+<kbd>L</kbd> on Mac or <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>L</kbd> on Windows/Linux).
- You can set up gradle task dependencies so that compiling a module depends on a detekt task with auto-correct on, or a ktlintFormat task
- You can have a CI task that runs a formatting task (like `detekt` with auto-correct or `ktlintFormat`) and automatically commit the results to the branch.

## Related Links
- [ktlint](https://github.com/pinterest/ktlint)
- [detekt](https://github.com/detekt/detekt)

[^1]: This statement is true as of the latest versions of ktlint and detekt, which are 1.5.0 and 1.23.8 respectively.