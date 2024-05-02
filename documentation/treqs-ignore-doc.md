
# TReqs ignore

TReqs ignore allows you to exclude any type or files or pattern using the unix style pathname expansion.
The only thing you need is to create the '.treqs-ignore' file in the root of your project.


## Syntax

The special characters used in shell-style wildcards are:

| PATTERN  | MEANING                    |
| :--------| :------------------------- |
| **[seq]**| Matches any character in seq. Cannot be empty. Any special character loses its special meaning in a set. |
| **[!seq]**| Matches any character not in seq. Cannot be empty. Any special character loses its special meaning in a set. |
| **?**| Matches any single character. |
| **\***| Matches everything but the directory separator. |
| **\*\***| Matches everything.|

## Examples

### `[seq]`

Matches any character in seq. Cannot be empty. Any special character loses its special meaning in a set.

> **_NOTE:_** Opening and closing brackets can be part of a set, although closing brackets have to be placed at the first position.

```
>>> match("aaa", "a[abc]a")
True
>>> match("aaa", "a[bcd]a")
False
>>> match("aaa", "a[a]]a")
False
>>> match("aa]a", "a[a]]a")
True
```

### `[!seq]`
Matches any character not in seq. Cannot be empty. Any special character loses its special meaning in a set.

```
>>> match("bbb", "b[!b]b")
False
>>> match("bbb", "b[!a]b")
True
>>> match("bbb", "b[a!a]b")
False
```

### `?`

Matches any single character.

```
>>> match("xzy", "x?y")
True
>>> match("xzzy", "x?y")
False
>>> match("x/y", "x?y")
True
```

### `*`
Matches everything but the directory separator.

> **_NOTE:_** The directory separator is platform specific. `/` is never matched by `\*`. `\\` is matched on Linux, but not on Windows.

```
>>> match("xzzy", "x*y")
True
>>> match("x/y", "x*y")
False
>>> match("xy", "x*y")
True
```

### `**`
Matches everything.

```
>>> match("xzzy", "x**y")
True
>>> match("x/y", "x**y")
True
```
