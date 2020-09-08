# pypathtree
A python path tree module and cli tool

## Important notice
Just an important point, if you use this to prune, delete, restructure or in anyway modify file or directories, please be VERY careful as you should be with any tool that can modify an entire tree.  It's best to use the "--test-only" option if you will be doing anything with a muliple level directory structure, or jut anything at all before doing a real run.  Even so, no matter what you do or do not do it is your responsibility for whatever or however you use this tool, even if the tool or modules does or does not do what is expected or detail in any documentation or other material.  You have been warned.  Please be cautious with any tool like this one and especially this one.  It can potentially wipe important files and worse if you are running as root or a permissive user or have bad permissions setup, you can easily destroy your system.  Capiche?

## Installation
Clone it.

## Module usage
```
from pathtree import PathTree
pt = PathTree("some/path", parent="~")
```

## Command usage (cli)
```
pathtree -- a path tree manager.
Usage:
    pathtree batch [ file | - ]  -- Run multiple comamnds from file or stdin.
    pathtree help [ topic ]  -- Prints command (or this) help doc.
    pathtree [ command ] { option } { path }  -- (see Commands)
Commands:
    check           Check that directory structure exists (default command).
    create          Create non-existent directories.
    list            Prints path tree report.
    prune           Remove path and any sub directories or files.
    quit            Exits (useful in batch mode).
    sanity          Run pathtree module sanity check.
    walk            Walk through path tree and query action for each item.
Options:
    --help, -?, -h  Prints this document and terminates.
    --test-only     All paths are fictious and none will be created,
                    removed or altered (default).
    --no            Respond "No" to any queries.
    --parent=path   Relative paths will to relative to parent path.
    -q              Report nothing but exit with value (-1).
    --strict        Exit if path does not already exist.
    -v              Report errors (default).
    -vv             Report errors and warnings.
    -vvv            Report all.
    -vvvv           Report all, plus debugging.
    --yes           Respond "Yes" to any queries.
    --warning       Issue warning if directory does not already exist.
    --              Terminate argument parsing.
```
