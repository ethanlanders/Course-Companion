Title: Types of Tests
Author: Thomas J. Kennedy
TOC: yes

There are quite a few types of tests... They are better described as testing
*techniques* or *methodologies.* We are interested in:

  - **General Testing Techniques**
    - White-Box Testing
    - Black-Box Testing
    - Head-to-Head Testing

  - **Formal Testing Frameworks**
    - Unit Testing
    - Integration Testing
    - System Testing


# General Testing Techniques

Let us focus on general testing techniques first.


## Head-to-Head Testing

Head-to-head-testing is essentially comparing to sets
of output:

  - "correct" (reference) output generated by hand (e.g., based on a
    requirements document) or from a known "correct" program.

  - actual output generated by the program being evaluated.


## Black-Box Testing

\bSidebar

Note that Unit Testing is a topic that will be discussed in a future lecture.
For the moment... just remember that a unit test focuses on a single piece of
code (e.g., a single function).

\eSidebar

Black-Box testing involves writing tests for a "black box."

> What is a "black box?"
>
> This type of testing focuses creating test data for a function, class, or
> program with a known interface, but whose implementation details are unknown.

In fact... this technique is used in Test Driven Development (TDD) to write
unit tests before actually implementing any code.

Let us go through a quick example. Suppose you are provided the following
function declaration and told to design a few tests.

\bExample{Simple Addition Function}

```python

def add_two_integers(num1: int, num2: int) -> int:
    """
    Add two integers (any combination of positive, negative, or zero) together.

    Args:
        num1: first number
        num2: second number

    Returns:
        sum of num1 and num2  (i.e., num1 + num2)

    Raises:

        ValueError if `num1` and `num1` are not in the range -10000 to 10000
        (inclusive).
    """
```

\eExample 

As a point of reference both C++ Doxygen and Java Javadoc versions are listed
below.

^^^[C++ Documentation]

```cpp
/**
 * Add two integers (any combination of positive, negative, or zero) together.
 *
 * @param num1 - first number
 * @param num2 - second number
 *
 * @returns sum of num1 and num2  (i.e., num1 + num2)
 *
 * @pre (num1 >= -10000 && num1 <= 10000) 
 *   && (num2 >= -10000 && num2 <= 10000) 
 */
int addTwoIntegers(const int num1, const int num2);
```

^^^

^^^[Java Documentation]

```java
    /**
     * Add two integers (any combination of positive, negative, or zero) together.
     *
     * @param num1 - first number
     * @param num2 - second number
     *
     * @returns sum of num1 and num2  (i.e., num1 + num2)
     *
     * @throws ArithmeticException if `num1` and `num1` are not in the range -10000
     * to 10000 (inclusive).
     */
    public int addTwoIntegers(const int num1, const int num2)
    {
        //...
    }
```

^^^

The function has full documentation. The constraints (e.g., preconditions) of
the function are explicitly stated. All numbers must fall in the range
$-10,000$ to $10,000$. We would want to test a few things:

  - boundary conditions
    - combinations of 10,000 and -10,000
    - combinations close 10,000 and -10,000 but still in the defined range
  - combinations of positive numbers
  - combinations of negative numbers
  - two zeroes
  - combinations of negative numbers, zeroes, and positive numbers

Since we know how to add (usually...), the correct sums can be computed by
hand. When we obtain the definition of `add_two_integers` the results generated
by the function can be compared to the known correct results.


## White-Box Testing

White-Box testing complements Black-Box testing. While Black-Box testing
ignores the code itself (instead focusing on interfaces and requirements),
White-Box testing focuses on the code and all but ignores the requirements.

White-Box testing often examines which lines of code are executed and which
branches are taken. The process generally makes use of a tool such as

  - `gcov` (C++)
  - `jacoco` (Java)
  - `coverage.py` (Python)
  - Tarpaulin (Rust)


These are code coverage tools... used to track which lines of code are
"touched" during a program's normal execution (i.e., using the `main`
driver function) or when some type of tests (e.g., Black-Box or Unit) are run.


# Formal Testing Frameworks

In previous lectures (within this course and in previous coursework) most tests
were run manually. Formal testing frameworks (e.g., JUnit) allow the process to
be automated.

Suppose that we have a function that:

  1. accepts an integer
  2. adds one to the integer
  3. doubles that result
  4. returns the final result

The function might have a signature in the form...

```python
def add_one_then_double(val: int) -> int:
    pass
```

*I have forgone pydoc documentation in this example.* Note the use of

```python
pass
```

This keyword is the Python equivalent of an empty block in C++...

```cpp
int add_one_then_double(const int val)
{
    return -1;
}
```

or Java...

```java
public int add_one_then_double(final int val)
{
    return -1;
}
```

or Rust...

```Rust
fn add_one_then_double(val: u32) -> u32
{
    return 0 as u32;
}
```

However, our focus is on Python. While writing good tests is a discussion in
its own right...


## Defining a Test

It is still possible to write a simple test. The key is knowing *a priori*
(i.e., ahead of time) what output will be generated for a given input. Assuming
`add_one_then_double` were fully documented... we could compute the following...

| val | plus 1 | double |
| -:  | -:     | -:     |
| 0   | 1      | 2      |
| 1   | 2      | 4      |
| 2   | 3      | 6      |
| 3   | 4      | 8      |
| 4   | 5      | 10     |

A Python unit test written using <a href="https://docs.pytest.org/en/7.4.x/" target="_blank">pytest</a>
and <a href="https://github.com/hamcrest/PyHamcrest/" target="_blank">PyHamcrest</a> would start off
similar to...

```python
def test_quick_demo():
    assert_that(add_one_then_double(0), is_(equal_to(2)))
    assert_that(add_one_then_double(1), is_(equal_to(4)))
    assert_that(add_one_then_double(2), is_(equal_to(6)))
    assert_that(add_one_then_double(3), is_(equal_to(8)))
    assert_that(add_one_then_double(4), is_(equal_to(10)))
```

The syntax (and missing `import` statements) will be discussed in a separate
(maybe even the next) lecture. For now... we just need to note that any
properly implemented version of `add_one_then_double` will pass the
`test_quick_demo` unit test.


## What are Unit, Integration and System Tests?


The three types of tests can be defined as follows...

  - **Unit Test** - a type of test that focuses on a single piece of code
    (e.g., function, module, or class).

  - **Integration Test** - a type of test that focuses on multiple pieces of
    code working together (two or three steps), e.g.,

      - a function that calls a sequence of functions 

      - a class that interacts with another class

  - **System Test** - a type of test that focuses on a program from start to
    finish. These tests evaluate the results of an entire sequence of
    function calls and class interactions (i.e., multiple steps).
