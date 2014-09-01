Title: My Test Page
Status: hidden
Slug: test-page
Summary: A place to test markup
Sortorder: 3

Before we start writing any code, let's first look at what the code will actually do. If you are reading this document just to find out how to do something simple like write a small caps feature, you may skip this section and jump ahead to the [code snippets]({filename}introduction.md). But, if you want to develop complex, nuanced and amazing features, you really should read this section. Understanding the underlying mechanics of how features work will allow you to carry your vision all the way from how the glyphs the glyphs look to how the behave.

# A main header with "quotes" in it

    Codeblocks are created by indenting in the source.

    These:
        will be = treated
        as pre()

Ready? Alright, let's get into some heavy stuff.

## Head 2

This line contains some inline `code examples`.

* This is a bulletted list item
* This is a bulletted list item which should be long enough to wrap to a new line, probably
* This is a bulletted list item
* This is a `bulletted list` item with code

This is an ordered list:

1. This is an ordered list item
2. This is an ordered list item which should be long enough to wrap to a new line, probably
3. This is an ordered list item
4. This is an ordered list item
5. This is an ordered list item
5. This is an ordered list item
5. This is an ordered list item
5. This is an ordered list item
5. This is an ordered list item
5. This is an ordered list item
5. This is an ordered list item
5. This is an ordered list item

A second ordered list:

5. This is an ordered list item
5. This is an ordered list item that spans...

    ...multiple paragraphs.

5. This is an ordered list item
5. This is an ordered list item

### Head 3

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in features. Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

#### Head 4

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in features. Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

## Structures

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in features. Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

The actual behavior within the features are defined with rules. Following the small caps example above, you can define a rule that states that the a glyph should be replaced with A.sc.

Within a feature, it is often necessary to group a set of rules together. This group of rules is called a lookup.

Visually, you can think of features, lookups and rules like this:

## Processing

When text is processed, the features that the user wants applied are gathered into two groups: substitution features and positioning features. The substitution features are processed first and then the positioning features are processed. The order in which you have defined the features, lookups and rules is the order in which they will be applied to the text. This order is very important.

Features process sequences of glyphs. These glyph runs may represent a complete line of text or a sub-section of a line of text.

For example, let's assume that you have the following features, lookups and rules:
