This document is going to be a designer friendly introduction to the OpenType processing model and the techniques for implementing features. Specifically, the [Adobe Feature File Syntax](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html) will be shown as the way to implement features.

I believe that a high-level introduction to OpenType features would be beneficial to the general type design community. The Adobe Feature File Syntax is great and the syntax reference is quite useful. But, it has a steep learning curve and the reference makes broad assumptions about what the reader already knows. (As it should. It's a technical document.) That said, I am primarily writing this for my students who want to learn how to write their own OpenType features.

I'm not sure what the final form of this document will be. I want it to be very portable. There will be illustrations, some may even be animated. Sphinx + Read-the-Docs may be the way to go.

I am still considering the license for this document and illustrations, but I am leaning towards [Creative Commons Attribution-NonCommercial-ShareAlike](http://creativecommons.org/licenses/by-nc-sa/3.0/). Basically, I don't want someone (other than me, maybe) to encapsulate this document and its illustrations into a sellable form and then profit from it. Developing this is going to be a non-trivial amount of work.

# Outline

## Assumptions
- general understanding of the parts of a font (glyphs, characters)
- basic understanding of what substitutions and positioning are trying to do

## Intro
- briefly explain opentype and its capabilities

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
- cumulative
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
- init, medi, fina without init, medi, fina

## Common Problems
- all of the rule types in a lookup must be the same type
- table overflow
- bad feature and rule ordering can lead to needless complexity
- features can't know if other features are active or not

## Things That Should Not Be In This Document (and why)
- ranges in glyph classes (why: not that useful, hard to debug)
- CID (why: complex)
- contour point (why: complex)
- GDEF (why: complex)
- named value records (why: haven't ever used it)
- subtable breaking (why: because I said so)
- enumerating pairs (why: complex)
- contextual kerning (why: support is consistent)
- the aalt construction technique of including complete features (why: I don't like it)
- the optical size feature (why: not supported)
- tables (OS/2, hhea, name, etc.) (why: your font editor is going to do this for you)
- anonymous data blocks (why: obviously)
- reversed chaining lookup types (why: too complex for this)
- feature implementations (adobe CS, CSS, etc.) (why: not something I want to keep up to date)
- known bugs of implementations (why: not something I want to keep up to date)

## Copyrights, Credits, etc.
- The Adobe Feature File Syntax is copyright Adobe Systems Incorporated.
- OpenType is either a registered trademark or trademark of Microsoft Corporation in the United States and/or other countries.


# Random Ideas
- in the general concepts section, use plain language to describe the desired behaviors. illustrate how the processing model works by showing an iterative animation that pairs an input glyph run with sequential rules and the line by line result of applying the rules to the glyph run.

# Style Notes
- don't refer to a type designer in abstract. always use "you" instead.
- the person using a font should be referred to as "user."

# Content

## General Concepts

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in "features." Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

The actual behavior within the features are defined with "rules." Following the small caps example above, you can define a rule that states that the *a* glyph should be replaced with *a.sc*.

Within a feature, it is often necessary to group a set of rules together. This group of rules is called a "lookup."

Visually, you can think of features, lookups and rules like this:

    feature
      lookup
        rule
        rule
        ...
      lookup
      ...
    feature
    ...

When text is processed, the features that the user wants applied are gathered into two groups: substitution features and positioning features. The substitution features are processed first and then the positioning features are processed. (Add note or footnote here explaining why this is logical.) The order that you have defined the features is the order in which they will be applied to the text. So, the order of your features, lookups and rules is very important.

Features process sequences of glyphs known as "glyph runs." These glyph runs may represent a complete line of text or a sub-section of a line of text.
