This document is going to be a designer friendly introduction to the OpenType processing model and the techniques for implementing features. Specifically, the [Adobe Feature File Syntax](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html) will be shown as the way to implement features.

I believe that a high-level introduction to OpenType features would be beneficial to the general type design community. The Adobe Feature File Syntax is great and the syntax reference is quite useful. But, it has a steep learning curve and the reference makes broad assumptions about what the reader already knows. (As it should. It's a technical document.) That said, I am primarily writing this for my students who want to learn how to write their own OpenType features.

I'm not sure what the final form of this document will be. I want it to be very portable. There will be illustrations, some may even be animated, so, hm.

I am still considering the license for this document and illustrations, but I am leaning towards [Creative Commons Attribution-NonCommercial-ShareAlike](http://creativecommons.org/licenses/by-nc-sa/3.0/). Basically, I don't want someone (other than me, maybe) to encapsulate this document and its illustrations into a sellable form and then profit from it. Developing this is going to be a non-trivial amount of work.

# Outline

## Assumptions
- general understanding of the parts of a font (glyphs, characters)
- basic understanding of what substitutions and positioning are trying to do

## General Concepts
- processing model
-- substitutions and positioning
-- features
-- lookups
-- rules
-- glyph runs / lines
-- ordering
- classes

## Syntax Intro
- Adobe Feature File Syntax
- comments
- whitespace
- {} [] ;
- feature
- lookup
- class (define, use)
- naming rules (glyphs, classes, lookups, keywords)

## Substitutions
- sub by syntax
- replace one with one
- replace many with one
- replace one with many
- replace one from many

## Positioning
- position, advance
- value record
- single
- pair
- cursive (maybe)
- mark to base (maybe)
- mark to ligature (maybe)
- mark to mark (maybe)

## Contextual
- backtrack
- lookahead
- ignore
- substitutions
- positioning

## Features
- common feature tags and descriptions

### Special Features
- kern
-- assumptions that this is positioning only
-- contextual is possible, but not widely supported
- aalt
-- one from many
- stylistic sets
-- designer defined behavior (assumed to be substitutions?)
-- naming (unsupported)

## Advanced Techniques
- languages and scripts
- include
- recycling lookups
- lookupflag
- useExtension

## Useful Algorithms
- fractions (adobe, contextual)
- randomization (trigger, cycle, quantum)
- swashes with collision detection

## Common Problems
- all of the rule types in a lookup must be the same type
- table overflow
- bad feature and rule ordering can lead to needless complexity

## Things That (Probably) Should Not Be In This Document
- ranges in glyph classes
- CID
- contour point
- GDEF
- named value records
- subtable breaking
- enumerating pairs
- contextual kerning
- the aalt construction technique of including complete features
- the optical size feature
- tables (OS/2, hhea, name, etc.)
- anonymous data blocks
- reversed chaining lookup types
- feature implementations (adobe CS, CSS, etc.)
- known bugs of implementations

# Random Ideas
- in the general concepts section, use plain language to describe the desired behaviors. illustrate how the processing model works by showing an iterative animation that pairs an input glyph run with sequential rules and the line by line result of applying the rules to the glyph run.