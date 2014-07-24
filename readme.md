This document is going to be a designer friendly introduction to the OpenType processing model and the techniques for implementing features. Specifically, the [Adobe Feature File Syntax](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html) will be shown as the way to implement features.

I believe that a high-level introduction to OpenType features would be beneficial to the general type design community. The Adobe Feature File Syntax is great and the syntax reference is quite useful. But, it has a steep learning curve and the reference makes broad assumptions about what the reader already knows. (As it should. It's a technical document.) That said, I am primarily writing this for my students who want to learn how to write their own OpenType features.

I'm not sure what the final form of this document will be. I want it to be very portable. There will be illustrations, some may even be animated. Sphinx + Read-the-Docs may be the way to go.

I am still considering the license for this document and illustrations, but I am leaning towards [Creative Commons Attribution-NonCommercial-ShareAlike](http://creativecommons.org/licenses/by-nc-sa/3.0/). Basically, I don't want someone (other than me, maybe) to encapsulate this document and its illustrations into a sellable form and then profit from it. Developing this is going to be a non-trivial amount of work.


## Assumptions
- general understanding of the parts of a font (glyphs, characters)
- basic understanding of what substitutions and positioning are trying to do


## Intro
- briefly explain opentype and its capabilities


## General Concepts

### Structures

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in "features." Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

The actual behavior within the features are defined with "rules." Following the small caps example above, you can define a rule that states that the a glyph should be replaced with A.sc.

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

    (this will be an illustration)
    Hello > [feature: small caps] > Hello (with ello in .sc)
    Hello (with ello in .sc) > [feature: ligatures] > Hello (with ello in .sc)

Within each feature, the glyph run is processed one lookup at a time. Here is what our example looks like as it moves through the small caps feature:

    (this will be an illustration)
    Hello > [lookup: letters] > Hello (with ello in .sc)
    Hello (with ello in .sc) > [lookup: numbers] > Hello (with ello in .sc)

Within each lookup, things are a little different. The glyph run is passed one glyph at a time from beginning to end over each rule within the lookup. If a rule transforms the passed glyph, the following rules are skipped for the passed glyph. The next glyph is then passed through the lookup. That's complex, so let's look at it with our example:

    (this will be an illustration)
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

    ideally I will be able to include an animation of a complete processing run

That's how processing works and it is the most complex part of OpenType features that you will need to understand. Now we can move on to the fun stuff.

(For you experts reading this: Yeah, I know this isn't technically 100% accurate. But, I don't really want to confuse everyone by going through the processing model with the GSUB and GPOS data structures. Those are different from the .fea syntax just enough to make things **very confusing** unless you know both sides of the process very well. So, I'm going to explain the processing model following the .fea structures.)


## Syntax Intro

You will be writing your features in the [Adobe OpenType Feature File Syntax](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html) (commonly referred to as ".fea"). .fea is a simple, text format that is easily editable in text and font editors. There are other syntaxes and tools for developing features, but .fea is the most widely supported and the most easily accessible. We'll be going through the important parts of .fea in detail, but for now we need to establish some basics.

### Comments

It's useful to be able to write comments about your code. To do this, add a # and everything from the # to the end of the line of text will be marked as a comment.

    # This is a comment.

Comments are ignored when your font is compiled, so you can write anything you want in your comments.

### White Space

In some syntaxes the amount of white space is important. This is not the case in .fea. You can use spaces, tabs and line breaks as much as you like.

### Special Characters

Some characters have special meanings in .fea.

#### ;

A semicolon indicates the end of something--a feature, lookup, rule, etc. These are important.

#### {}

Braces enclose the contents of a feature or lookup.

#### []

Brackets enclose the contents of a class. More information on classes will be coming shortly.

### Features

Features are identified with a four character long feature tag. These are either [registered tags](https://www.microsoft.com/typography/otspec/featurelist.htm) or private tags. Unless you have a very good reason to create a private tag, you should always use the registered tags. Applications that support OpenType features uses these tags to identify which features are supported in your font. For example, if you have a feature with the smcp tag, applications will know that your font supports small caps.

Features are defined with the feature keyword, the appropriate tag, a pair of braces and a semicolon.

    feature smcp {
        # lookups and rules go here
    } smcp;

(Should it be noted that these are called blocks? Or is that too much jargon?)

### Lookups

Lookups are defined in a similar way to features. They have a name, but the name is not restricted to four characters or to a tag database. You can make up your own name, as long as it follows the general naming rules.

    lookup Letters {
        # rules go here
    } Letters;

### Classes

You'll often run into situations where you want use a group of glyphs in a rule. These groups are called classes and they are defined with a list of glyphs names or class names inside of brackets.

    [A E I O U Y]

Classes can have a name assigned to them so that they can be used more than once. Class names follow the general naming rules and they are always preceded with an @. To create a named class you set the name, then an =, then the class definition and end it with a semicolon.

    @vowels = [A E I O U Y];

After a class has been defined, it can be referenced by name.

    @vowels

(Is this the place to talk about inline classes or should that be in the sub and pos sections?)

### General Naming Rules

A name for a glyph, class or lookup must adhere to the following constraints:

- No more than 31 characters in length.
- Only use characters in A-Z a-z 0-9 . _
- Must not start with a number or a period.

You should avoid naming anything with the same name as a [reserved keyword](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html#2.c). If you do need to name a glyph with one of these names, precede an reference to the glyph with a \. But, really, try to avoid needing to do this.


## Substitutions
- target and replacement
-- classes
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


## Common Features (and sample code)
- intro about supporting only what is needed, how to order these, etc.
- small caps (smcp, c2sc)
- all caps (case, cpsp)
- figures (pnum, tnum, lnum, onum)
- fractions (frac: adobe, contextual; afrc?)
- numerators
- denominators
- swashes (swsh, cswh, demonstrate collision detection)
- titling alternates
- ligatures (liga, dlig)
- localized forms
- ordinals
- superscript, subscript
- aalt
- fun stuff
-- randomization (trigger, cycle, quantum)
-- swashes with collision detection
-- init, medi, fina without init, medi, fina
-- roman numerals


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
- should there be a section that documents my preferred syntax style?
