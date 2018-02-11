{% extends "layouts/post.html" %}
{% set title = "A brainfuck interpreter in C" %}
{% set date = "November 1, 2017" %}

{% set body_html %}
{% filter markdown %}

```
$ bf "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
Hello World!
```

[brainfuck][bf] is a minimalistic esoteric programming language. The
basic model is to imagine an infinite array of byte cells all
initialized to 0. The data pointer begins at the beginning of the array.
A program is a sequence made up of eight different commands:
[bf]: https://en.wikipedia.org/wiki/Brainfuck

1. `>` increments the data pointer.
2. `<` decrements the data pointer.
3. `+` increments the byte in the cell pointed to by the data pointer.
4. `-` decrements the byte in the cell pointed to by the data pointer.
5. `.` outputs the byte at the data pointer.
6. `,` reads one byte of input into the byte at the data pointer.
7. `[` and `]` allow looping. At `[`, if the current byte is 0, jump to
   the command after the matching `]`.  At `]`, if the byte is nonzero
   jump to the command after the matching `[`.

This is pretty straightforward to implement, but many of the
interpreters I've seen around online use a fixed data array. Below I'll
discuss a nice simple means for implementing a dynamically
growing data array.

## The block structure

```C
struct block_data
{
    size_t block_size;
    size_t blocks_allocated;
    size_t block_array_cap;
    unsigned char **blocks;
};
/* Initialize block_data, and free internal memory */
void create_block_data(struct block_data *blks, size_t block_size);
void destroy_block_data(struct block_data *blks);

/* Handles growing the blocks array, and allocating blocks */
int block_data_grow_array(struct block_data *blks, size_t min_cap);
int block_data_allocate_blocks(struct block_data *blks, size_t up_to);

/* Clear block_data. This just initialized all allocated blocks to 0 */
void block_data_clear(struct block_data *blks);

/* Lookup a cell */
unsigned char *block_data_get_cell(struct block_data *blks, size_t i);
```

Here `blocks` is an array of `block_array_cap` pointers to blocks.
`blocks_allocated` tracks how many of those blocks are already
allocated. `block_size` is the number of bytes in each block.

The key function here is `block_data_get_cell`, which makes looking up a
cell trivial. Simply provide the data pointer index `i`, and it will do any
necessary allocations, and do the math to find the correct block and
index inside that block, returning a pointer to the requested data.


## The interpreter loop

Given this structure, implementing the interpreter is pretty easy. The
whole shebang lives in one function:

```C
void interpret(char *begin, char *end, FILE *in, FILE *out,
               struct block_data *blocks);
```

`begin` and `end` point to the instructions to interpret, `in` and
`out` are streams for the I/O commands `.` and `,`, and `blocks` is an
initialized `block_data` structure to represent the data array.

With all this in place the actual loop logic is not much different from
that in the various
[fixed-size](https://github.com/saulpw/brainfuck/blob/master/main.c)
[interpreters](https://gist.github.com/maxcountryman/1699708)
floating around on the internet:

```C
void interpret(char *begin, char *end, FILE *in, FILE *out,
               struct block_data *blocks)
{
    int           r = 0;
    char          *ip = begin;
    size_t        data_ptr_ix = 0;

    unsigned char *data_ptr = block_data_get_cell(blocks, data_ptr_ix);

    while (ip < end) {
        switch (*ip) {
        case '>':
            data_ptr_ix++;
            data_ptr = block_data_get_cell(blocks, data_ptr_ix);
            break;
        case '<':
            data_ptr_ix--;
            data_ptr = block_data_get_cell(blocks, data_ptr_ix);
            break;
        case '+':
            *data_ptr += 1;
            break;
        case '-':
            *data_ptr -= 1;
            break;
        case '.':
            fputc(*data_ptr, out);
            break;
        case ',':
            *data_ptr = fgetc(in);
            break;
        case '[':
            if (*data_ptr) break;
            ip = match_pairs(ip, begin, end, '[', ']', 1);
            break;
        case ']':
            if (!*data_ptr) break;
            ip = match_pairs(ip, begin, end, ']', '[', -1);
            break;
        default: /* All other characters are simply ignored */
            break;
        }
        ip++;
    }
    return SUCCESS;
}
```

Here `match_pairs` is a function to search for matching brackets in a
given range.

The entire source code for this interpreter, which includes a bit more
error handling than shown here is available
[here](https://gist.github.com/jpeoples/e71d432d1765c1d67f9ebb91b9b906e2).
It includes a bit of additional code for reading files for instructions.
You can call the interpreter with

    bf your,instructions.here
    # OR
    bf -f path/to/file/with/bf/code

## Making it better
There are some things we could do to make the interpreter better. For
one thing, we could eliminate all the ignored characters from the code
before calling interpret. Also
searching for matching brackets every loop iteration could be
sped up by creating a jump table before hand.
Finally, the same loop structure could be used to implement a compiler
converting a given brainfuck program into C code.
I might look at some of these things in a future post.

{% endfilter %}
{% endset %}
