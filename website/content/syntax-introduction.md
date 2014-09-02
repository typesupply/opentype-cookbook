Title: Syntax Introduction
Sortorder: 3

We will be writing our features in the [Adobe OpenType Feature File Syntax](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html) (commonly referred to as “.fea”). This is a simple, text format that is easily editable in text and font editors. There are other syntaxes and tools for developing features, but .fea is the most widely supported and the most easily accessible. We’ll be going through the important parts of .fea in detail, but for now we need to establish some basics.

## Comments

It’s useful to be able to write comments about your code. To do this, add a `#` and everything from the `#` to the end of the line of text will be marked as a comment.

    :::fea
    # This is a comment.

Comments are ignored when your font is compiled, so you can write anything you want in your comments.

## White Space

In some syntaxes the amount of white space is important. This is not the case in .fea. You can use spaces, tabs and line breaks as much and in any combination as you like.

## Special Characters

Some characters have special meanings in .fea.

### ;

A semicolon indicates the closing of something—a feature, lookup, rule, etc. These are important.

### {}

Braces enclose the contents of a feature or lookup.

### []

Brackets enclose the contents of a class.

## Features

Features are identified with a four character tag. These are either [registered tags](https://www.microsoft.com/typography/otspec/featurelist.htm) or private tags. Unless you have a very good reason to create a private tag, you should always use the registered tags. Applications that support OpenType features use these tags to identify which features are supported in your font. For example, if you have a feature with the `smcp` tag, applications will know that your font supports small caps.

Features are defined with the feature keyword, the appropriate tag, a pair of braces, the tag again, and a semicolon.

    :::fea
    feature smcp {
        # lookups and rules go here
    } smcp;

## Lookups

Lookups are defined in a similar way to features. They have a name, but the name is not restricted to four characters or to a tag database. You can make up your own name, as long as it follows the general naming rules.

    :::fea
    lookup Letters {
        # rules go here
    } Letters;

## Classes

You’ll often run into situations where you want use a group of glyphs in a rule. These groups are called classes and they are defined with a list of glyph names or class names inside of brackets.

    :::fea
    [A E I O U Y]

Classes can have a name assigned to them so that they can be used more than once. Class names follow the general naming rules and they are always preceded with an `@`. To create a named class you set the name, then an `=`, then the class definition and end it with a semicolon.

    :::fea
    @vowels = [A E I O U Y];

After a class has been defined, it can be referenced by name.

    :::fea
    @vowels

## General Naming Rules

A name for a glyph, class or lookup must adhere to the following constraints:

- No more than 31 characters in length.
- Only use characters in A-Z a-z 0-9 . _
- Must not start with a number or a period.

You should avoid naming anything (including glyphs) with the same name as a [reserved keyword](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html#2.c). If you do need to name a glyph with one of these names, precede an reference to the glyph with a `\` But, really, try to avoid needing to do this.

