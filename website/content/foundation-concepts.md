Title: Foundation Concepts
Summary: Short version for index and feeds
Sortorder: 3

Before we start writing any code, let's first look at what the code will actually do. If you are reading this document just to find out how to do something simple like write a small caps feature, you may skip this section and jump ahead to the code snippets. But, if you want to develop complex, nuanced and amazing features, you really should read this section. Understanding the underlying mechanics of how features work will allow you to carry your vision all the way from how the glyphs the glyphs look to how the *behave*.

Ready? Alright, let's get into some heavy stuff.

## Structures

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in features. Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

The actual behavior within the features are defined with rules. Following the small caps example above, you can define a rule that states that the `a` glyph should be replaced with `A.sc`.

Within a feature, it is often necessary to group a set of rules together. This group of rules is called a lookup.

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

## Processing

When text is processed, the features that the user wants applied are gathered into two groups: substitution features and positioning features. The substitution features are processed first and then the positioning features are processed. The order in which you have defined the features, lookups and rules is the order in which they will be applied to the text. This order is very important.

Features process sequences of glyphs. These glyph runs may represent a complete line of text or a sub-section of a line of text.

For example, let's assume that you have the following features, lookups and rules:

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

Let's also assume that the user wants to apply small caps and ligatures to a glyph run that displays "Hello".

A glyph run is processed one feature at a time. So, here is what "Hello" will look like as it enters and exists each feature:

    (this will be an illustration)
    Hello > [feature: small caps] > Hello (with ello in .sc)
    Hello (with ello in .sc) > [feature: ligatures] > Hello (with ello in .sc)

Within each feature, the glyph run is processed one lookup at a time. Here is what our example looks like as it moves through the small caps feature:

    (this will be an illustration)
    Hello > [lookup: letters] > Hello (with ello in .sc)
    Hello (with ello in .sc) > [lookup: numbers] > Hello (with ello in .sc)

Within each lookup, things are a little different. The glyph run is passed one glyph at a time from beginning to end over each rule within the lookup. If a rule transforms the current glyph, the following rules are skipped for the current glyph. The next glyph is then current through the lookup. That's complex, so let's look at it with our example:

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

    (ideally I will be able to include an animation of a complete processing run)

The process is the same for positioning features, except that instead of rule evaluation stopping when a glyph is transformed, the evaluation is stopped when a glyph's position is changed.

That's how processing works and it is the most complex part of OpenType features that you will need to understand. Got it? Great!
