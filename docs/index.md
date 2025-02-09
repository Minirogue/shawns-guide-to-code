# Shawn's Colorful Guide to Code

This is where I will document my opinionated approach to coding best practices, specifically in Android/Kotlin/KMP.
It's a work-in-progress.

Topics left to cover:
- The standard way to collect `Flow` in an `Activity` or `Fragment` in a lifecycle safe manner.
- Discuss state management for MVVM/MVI/UDF. 
  - I will cover 3 main approaches to representing the state (monolith `data class`, mutually exclusive`sealed inteface` subclasses, microstates).
  - [Article with reference tweet](https://gpeal.medium.com/modeling-android-screens-as-state-97aa5511657d).
- Discuss keeping Data Transfer Objects (DTOs) and Domain Models separate. 
  - I will also mention how gradle modularization can help encapsulate the DTO details.
- Discuss separated interface pattern, modularization strategy, benefits, drawbacks, the whole shebang.
- Standard general coroutines practices
  - injectable dispatchers
- Expand on Kotlin idioms and anti-idioms
- Trailing commas: they're good