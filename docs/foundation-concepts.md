---
layout: default
navigation: true
title: Foundation Concepts
order: 2
---

Before we start writing any code, let’s first look at what the code will actually do. If you are reading this cookbook just to find out how to do something simple like write a small caps feature, you may skip this section and jump ahead to the [code snippets](common-techniques.html). But, if you want to develop complex, nuanced, amazing features, you really should read this section. Understanding the underlying mechanics of how features work will allow you to carry your vision all the way from how the glyphs *look* to how they *behave*.

Ready? Alright, let’s get into some heavy stuff.

## Structures

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in *features*. Features can do two things: they can *substitute glyphs* and they can *adjust the positions of glyphs*.

The actual behavior within the features are defined with *rules*. Following the small caps example above, you can define a rule that states that the `a` glyph should be replaced with `A.sc`.

Within a feature, it is often necessary to group a set of rules together. This group of rules is called a *lookup*.

Visually, you can think of features, lookups and rules like this:

<object type="image/svg+xml" data="/media/illustrations/foundation-internal-structure.svg"></object>

*(Note: In these illustrations if you see a jagged line cutting something off, it means “There is a bunch of the same kind of stuff so we’ll cut it off to avoid too much repetition.”)*

## Processing

When text is processed, the features that the user wants applied are gathered into two groups: substitution features and positioning features. The substitution features are processed first and then the positioning features are processed. The order in which you have defined the features, lookups and rules is the order in which they will be applied to the text. This order is *very* important.

Features process sequences of glyphs. These glyph runs may represent a complete line of text or a sub-section of a line of text.

For example, let’s assume that you have the following features, lookups and rules:

<object type="image/svg+xml" data="/media/illustrations/foundation-example-features.svg"></object>

Let’s also assume that the user wants to apply small caps and ligatures to a glyph run that displays `Hello`.

A glyph run is processed one feature at a time. So, here is what `Hello` will look like as it enters and exists each feature:

<object type="image/svg+xml" data="/media/illustrations/foundation-processing-feature.svg"></object>

Within each feature, the glyph run is processed one lookup at a time. Here is what our example looks like as it moves through the small caps feature:

<object type="image/svg+xml" data="/media/illustrations/foundation-processing-lookup.svg"></object>

Within each lookup, things are a little different. The glyph run is passed one glyph at a time from beginning to end over each rule within the lookup. If a rule replaces the current glyph, the following rules are skipped for the current glyph. The next glyph is then current through the lookup. That’s complex, so let’s look at it with our example:

<object type="image/svg+xml" data="/media/illustrations/foundation-processing-rule.svg"></object>

The process is the same for positioning features, except that instead of rule evaluation stopping when a glyph is replaced, the evaluation is stopped when a glyph’s position is changed.

That’s how processing works and it is the most complex part of OpenType features that you will need to understand. Got it? Great!
