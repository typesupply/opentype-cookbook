# Read Me First

**This is an in-progress rough draft. Your feedback is welcome!**

This document will eventually be hosted on a small, static website. This site will either be generated with Sphinx or built directly as HTML files. If HTML is built directly, this [syntax highlighter](http://alexgorbatchev.com/SyntaxHighlighter/manual/brushes/custom.html) could be used with a customization to support .fea.

The planned title is <drumroll> The (Unofficial) OpenType Cookbook. I know that the document doesn't cover "OpenType" in totality, but, details details.


# Troubleshooting

Should this section even be in here? What form should it take?

(Yes, but perhaps Trouble and Tips?)

- did you forget a special character? you probably forgot a } ; or something like that.
- did you name a lookup or class with the same name twice?
- all of the rule types in a lookup must be the same type
- table overflow (subtable, useExtension)
- features can't know if other features are active or not
- complex contextual rules leading to slowness of overflow errors (limit the contexts to what is *likely* to happen, not *everything*)


# Things That Should Not Be In This Document (and why)

Should this be in the final document? It's here now to keep me on track.

- ranges in glyph classes (why: not that useful, hard to debug)
- CID (why: complex)
- contour point (why: complex)
- GDEF (why: complex)
- named value records (why: haven't ever used it)
- subtable breaking (why: because I said so)
- enumerating pairs (why: complex)
- contextual kerning (why: support is consistent)
- the aalt construction technique of including complete features (why: I don't like it)
- the optical size feature (why: not widely supported) _(I think we use it for InDesign)_
- tables (OS/2, hhea, name, etc.) (why: your font editor is going to do this for you)
- anonymous data blocks (why: obviously)
- reversed chaining lookup types (why: too complex for this)
- feature implementations (adobe CS, CSS, etc.) (why: not something I want to keep up to date)
_Link to the Typotheque Table – still a good overview._
- known bugs of implementations (why: not something I want to keep up to date)
- cursive positioning (why: too complex for this; not easy to test)
- mark to base positioning (why: too complex for this; not easy to test)
- mark to ligature positioning (why: too complex for this; not easy to test)
- mark to mark positioning (why: too complex for this; not easy to test)
- lookupflag (why: relates to the positioning rules that aren't covered)

_I think that the cursive and the mark-related features are interesting, and actually not that difficult to write and to understand. But I agree that it does not need to be in version 1 of this document because they'll be only relevant to a small set of people._

# Thanks




# Appendix: My .fea Style Guide


