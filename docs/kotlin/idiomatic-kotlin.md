# Idiomatic Kotlin

Kotlin provides many helpful functions that can be used to write "idiomatic" kotlin code.
For example, null-safe usages of scoping functions can be used to simplify null checks, e.g. 

[//]: # (TODO add more background on why this would be done)
```kotlin
val someNullableVal = someMutableVar
val result = if (someNullableVal != null) {
    someOperation(someNullableVal) // local val is cast as non-null here
} else {
    null
}
```

becomes
```kotlin
val result = someMutableVar?.let { someOperatoin(it) }
```

## Too Idiomatic Kotlin
Sometimes enthusiasm for Kotlin paradigms can lead to what I like to call "too idiomatic Kotlin".
Here are some examples:
```kotlin
(someValue as? SomeClass)?.let {
    performSomeOperation(it)
} ?: alternativeOperation()
```

This is no easier to read than
```kotlin
if (someValue is SomeClass) {
    performeSomeOperation(someValue)
} else {
    alternativeOperation()
}
```