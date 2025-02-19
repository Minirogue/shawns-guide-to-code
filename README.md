# Shawn's Guide to Code

This is the repository where I document my opinionated approach to coding best practices.
There is a focus on Android and Kotlin, but many things can be applied more generally.

## The Site
This documentation is published as a GitHub Pages site that can be found here: https://minirogue.github.io/shawns-guide-to-code.

## Upcoming Topics to Cover

- State management for MVVM/MVI/UDF.
    - I will cover 3 main approaches to representing the state (monolith `data class`, mutually exclusive`sealed inteface` subclasses, microstates).
    - [Article with reference tweet](https://gpeal.medium.com/modeling-android-screens-as-state-97aa5511657d).
- Discuss keeping Data Transfer Objects (DTOs) and Domain Models separate.
    - I will also mention how gradle modularization can help encapsulate the DTO details.
- Discuss separated interface pattern, modularization strategy, benefits, drawbacks, the whole shebang.
- Standard general coroutines practices
    - injectable dispatchers
    - Responsibility of thread switching at source
    - Collecting `Flow` in an `Activity` or `Fragment` in a lifecycle safe manner.
    - Using MutableStateFlow for VM state
    - Using channels + `receiveAsFlow()` for one-shot events.
- Expand on Kotlin idioms and anti-idioms
- Trailing commas: they're good
