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
- complex contextual rules leading to slowness of overflow errors (limit the contexts to what is *likely* to happen, not *everything*)

## .fea vs. Compiled Tables
- this is technical, but should probably be explained lightly

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

### Structures

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in "features." Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

The actual behavior within the features are defined with "rules." Following the small caps example above, you can define a rule that states that the *a* glyph should be replaced with *A.sc*.

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

### Processing

When text is processed, the features that the user wants applied are gathered into two groups: substitution features and positioning features. The substitution features are processed first and then the positioning features are processed. (Add note or footnote here explaining why this is logical.) The order in which you have defined the features is the order in which they will be applied to the text. So, the order of your features, lookups and rules is very important.

Features process sequences of glyphs known as "glyph runs." These glyph runs may represent a complete line of text or a sub-section of a line of text.

For the following, let's assume that you have the following features, lookups and rules:

    feature: small caps
        lookup: letters
            replace a with A.sc
            replace b with B.sc
            ...
            replace z with Z.sc
        lookup: numbers
            replace zero with zero.sc
            ...
            replace nine with nine.sc
    feature: ligatures
        lookup: basic
            replace f f i with f_f_i
            replace f f l with f_f_l
            replace f f with f_f
            replace f i with f_i
            replace f l with f_l

(Note: this is an odd example. there is no reason for the lookups, but I can't think of a way to show lookups at this point that doesn't make things overly complex.)

Let's also assume that the user wants to apply small caps and ligatures to a glyph run that displays "Hello".

A glyph run is processed one feature at a time. So, here is what "Hello" will look like as it enters and exists each feature:

    Hello > [feature: small caps] > Hello (with ello in .sc)
    Hello (with ello in .sc) > [feature: ligatures] > Hello (with ello in .sc)

Within each feature, the glyph run is processed one lookup at a time. Here is what our example looks like as it moves through the small caps feature:

    Hello > [lookup: letters] > Hello (with ello in .sc)
    Hello (with ello in .sc) > [lookup: numbers] > Hello (with ello in .sc)

Within each lookup, things are a little different. The glyph run is passed one glyph at a time from beginning to end over each rule within the lookup. If a rule transforms the passed glyph, the following rules are skipped for the passed glyph. The next glyph is then passed through the lookup. That's complex, so let's look at it with our example:

    H ello > [replace a with A.sc] > H ello
    H ello > [replace b with B.sc] > H ello
    ...
    H ello > [replace z with Z.sc] > H ello

    e llo > [replace a with A.sc] > H e llo
    e llo > [replace b with B.sc] > H e llo
    ...
    e llo > [replace e with E.sc] > H (E.sc) llo
    (the rest are skipped)

    l lo > [replace a with A.sc] > H(E.sc) l lo
    l lo > [replace b with B.sc] > H(E.sc) l lo
    ...
    l lo > [replace l with L.sc] > H(E.sc) (L.sc) lo
    (the rest are skipped)

    l o > [replace a with A.sc] > H(E.sc)(L.sc) l o
    l o > [replace b with B.sc] > H(E.sc)(L.sc) l o
    ...
    l o > [replace l with L.sc] > H(E.sc)(L.sc) (L.sc) o
    (the rest are skipped)

    o > [replace a with A.sc] > H(E.sc)(L.sc)(L.sc) o
    o > [replace b with B.sc] > H(E.sc)(L.sc)(L.sc) o
    ...
    o > [replace o with O.sc] > H(E.sc)(L.sc)(L.sc) (O.sc)
    (the rest are skipped)

Here is our example, animated:

    ideally I can include an animation of a complete processing run

That's how processing works and it is the most complex part of OpenType features that you will need to understand. Now we can move on to the fun stuff.

(For you experts reading this: Yeah, I know this isn't technically 100% accurate. But, I don't really want to confuse everyone by going through the processing model with the GSUB and GPOS data structures. Those are different from the .fea syntax just enough to make things **very confusing** unless you know both sides of the process very well. So, I'm going to explain the processing model following the .fea structures.)
