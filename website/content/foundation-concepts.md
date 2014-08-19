Title: Foundation Concepts
Summary: Short version for index and feeds
Sortorder: 3

Before we start writing any code, let's first look at what the code will actually do. If you are reading this document just to find out how to do something simple like write a small caps feature, you may skip this section and jump ahead to the code snippets. But, if you want to develop complex, nuanced and amazing features, you really should read this section. Understanding the underlying mechanics of how features work will allow you to carry your vision all the way from how the glyphs the glyphs look to how the behave.

Ready? Alright, let's get into some heavy stuff.

## Structures

In OpenType we can define behaviors that we want to happen upon request from users. For example, the user may decide that text should be displayed with small caps. You, the type designer, can define which glyphs should be changed when this request is made by the user. These behaviors are defined in features. Features can do two things: they can substitute glyphs and they can adjust the positions of glyphs.

The actual behavior within the features are defined with rules. Following the small caps example above, you can define a rule that states that the a glyph should be replaced with A.sc.
Within a feature, it is often necessary to group a set of rules together. This group of rules is called a lookup.
Visually, you can think of features, lookups and rules like this:
