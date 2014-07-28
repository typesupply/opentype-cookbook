**(Please note, this is a work in progress. Feedback is welcome!)**

# Introduction

OpenType features allow fonts to behave smartly. This behavior can do simple things like change text to small caps or they can do complex things like insert swashes, alternates and ligatures to make text in a script font feel handmade. This document aims to be a designer friendly introduction to understanding and developing these features. The goal is not to teach you how to write a small caps feature or a complex script feature. Rather, the goal is to teach you the logic and techniques for developing features. Once you understand those, you'll be able to create features of your own design.

This document is written with the assumption that you have a basic working knowledge of the structure of a font. You need to know the differences between characters and glyphs, understand the coordinate system in glyphs and so on.


(make a note about writing direction. that the examples show LTR, but the features are language agnostic.)

# Foundation Concepts

Before we get into writing any code, let's first establish what we are actually building and how it actually works. This is probably the toughest thing to understand about OpenType features, but understanding the underlying mechanics will free you to build new and innovative features of your own.

## Structures

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

## Processing

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

**note that this is the same for positioning**

(For you experts reading this: Yeah, I know this isn't technically 100% accurate. But, I don't really want to confuse everyone by going through the processing model with the GSUB and GPOS data structures. Those are different from the .fea syntax just enough to make things **very confusing** unless you know both sides of the process very well. So, I'm going to explain the processing model following the .fea structures.)


# Syntax Intro

You will be writing your features in the [Adobe OpenType Feature File Syntax](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html) (commonly referred to as ".fea"). .fea is a simple, text format that is easily editable in text and font editors. There are other syntaxes and tools for developing features, but .fea is the most widely supported and the most easily accessible. We'll be going through the important parts of .fea in detail, but for now we need to establish some basics.

## Comments

It's useful to be able to write comments about your code. To do this, add a # and everything from the # to the end of the line of text will be marked as a comment.

    # This is a comment.

Comments are ignored when your font is compiled, so you can write anything you want in your comments.

## White Space

In some syntaxes the amount of white space is important. This is not the case in .fea. You can use spaces, tabs and line breaks as much as you like.

## Special Characters

Some characters have special meanings in .fea.

### ;

A semicolon indicates the end of something--a feature, lookup, rule, etc. These are important.

### {}

Braces enclose the contents of a feature or lookup.

### []

Brackets enclose the contents of a class. More information on classes will be coming shortly.

## Features

Features are identified with a four character long feature tag. These are either [registered tags](https://www.microsoft.com/typography/otspec/featurelist.htm) or private tags. Unless you have a very good reason to create a private tag, you should always use the registered tags. Applications that support OpenType features uses these tags to identify which features are supported in your font. For example, if you have a feature with the smcp tag, applications will know that your font supports small caps.

Features are defined with the feature keyword, the appropriate tag, a pair of braces and a semicolon.

    feature smcp {
        # lookups and rules go here
    } smcp;

(Should it be noted that these are called blocks? Or is that too much jargon?)

## Lookups

Lookups are defined in a similar way to features. They have a name, but the name is not restricted to four characters or to a tag database. You can make up your own name, as long as it follows the general naming rules.

    lookup Letters {
        # rules go here
    } Letters;

## Classes

You'll often run into situations where you want use a group of glyphs in a rule. These groups are called classes and they are defined with a list of glyphs names or class names inside of brackets.

    [A E I O U Y]

Classes can have a name assigned to them so that they can be used more than once. Class names follow the general naming rules and they are always preceded with an @. To create a named class you set the name, then an =, then the class definition and end it with a semicolon.

    @vowels = [A E I O U Y];

After a class has been defined, it can be referenced by name.

    @vowels

(Is this the place to talk about inline classes or should that be in the sub and pos sections?)

## General Naming Rules

A name for a glyph, class or lookup must adhere to the following constraints:

- No more than 31 characters in length.
- Only use characters in A-Z a-z 0-9 . _
- Must not start with a number or a period.

You should avoid naming anything with the same name as a [reserved keyword](http://www.adobe.com/devnet/opentype/afdko/topic_feature_file_syntax.html#2.c). If you do need to name a glyph with one of these names, precede an reference to the glyph with a \. But, really, try to avoid needing to do this.


# Rules

Now that we have introduced some terminology, covered the way text is processed and established the general syntax rules, we can get into the fun part: actually doing stuff.

## Substitutions

Substitutions are the most visually transformative thing that features can do to text. And, they are easy to understand. There are two main parts to a substitution:

1. Target -- This is what will be replaced.
2. Replacement -- This is what will be inserted in place of the target.

The syntax for a substitution is:

    substitute target by replacement;

We can abbreviate substitute with sub to cut down on how much stuff we have to type, so let's do that:

    sub target by replacement;

Targets and replacements can often be classes. These classes can be referenced by name or they can be defined as an unnamed class inside of a rule.

### Replace One With One

To replace one thing with another, you do this:

    sub target by replacement;

(In the .fea documentation, this is known as GSUB Lookup Type 1: Single Substitution.)

For example, to transform a to A.sc, you would do this:

    sub a by A.sc;

If you have more than one thing that can be replaced with a single thing, you can use a class as the target and a glyph as the replacement:

    sub [A A.alt1 A.alt2] by A.alt4;

If you want to replace several things with corresponding things, you can use classes as both the target and the replacement.

    sub [a b c] by [A.sc B.sc C.sc];

It's usually more readable if define the classes earlier in your code and then reference them by name.

    sub @lowercase by @smallcaps;

The order of the glyphs in your classes in this situation is critical. In the example above, the classes will correspond with each other like this:

    a -> A.sc
    b -> B.sc
    c -> C.sc

If you order the target and replacement classes incorrectly, things will go wrong. For example, if you have this as your rule:

    sub [a b c] by [B.sc C.sc A.sc];

The classes will correspond like this:

    a -> B.sc
    b -> C.sc
    c -> A.sc

This is obviously undesired behavior, so keep your classes ordered properly.

### Replace Many With One

To replace a sequence of things with one thing, you do this:

    sub target sequence with replacement;

(In the .fea documentation, this is known as GSUB Lookup Type 4: Ligature Substitution.)

For example, for a fi ligature, you would do this:

    sub f i by f_i;

You can also use classes as part of the target sequence:

    sub [f f.alt] i by f_i;
    sub f [i i.alt] by f_i;
    sub [f f.alt] [i i.alt] by f_i;
    sub @f @i by f_i;
    sub @f i by f_i;
    sub f @i by f_i;
    sub @f [i i.alt] by f_i;
    sub [f f.alt] @i by f_i;

(Obviously you wouldn't use all of these rules in real code since they do the same thing.)

### Replace One With Many

To replace a sequence of things with a single thing, you do this:

    sub target by replacement sequence;

(In the .fea documentation, this is known as GSUB Lookup Type 2: Multiple Substitution.)

For example, to convert an fi ligature back into f and i, you would do this:

    sub f_i by f i;

Classes can't be used as the target or the replacement in this rule type.

### Replace One From Many

To give the user a choice of alternates, you do this:

    sub target from replacement;

(In the .fea documentation, this is known as GSUB Lookup Type 3: Alternate Substitution.)

The replacement must be a glyph class.

For example, to give the user several options to replace a with, you would do this:

    sub a from [a.alt1 a.alt2 a.alt3];

If you want to name the class and reference it in the rule, you can do this:

    sub a from @aAlternates;

Note that the keyword in the middle of the rule changes from by to from.

## Positioning

Positioning glyphs may not be as visually interesting as what can be achieved with substitution, but the positioning support in OpenType is incredibly powerful. The positioning rules can be broken into two separate categories to make them easier to understand:

1. Simple Rules -- These adjust either the space around one glyph or the space between two glyphs.
2. Mind-Blowingly Complex and Astonishingly Powerful Rules -- These do things like properly shift combining marks to align precisely with the base forms in Arabic and Devanagari so that things look incredibly spontaneous and beautiful.

We're going to cover the simple rules in this document. The complex rules are amazing, but too advanced for now.

### Position and Advance

Before we go much further we need to talk about coordinate systems and value records. As you know, the coordinate system in fonts is based on X and Y axes. The X axes moves from left to right with numbers increasing as you move to the right. The Y axis moves from bottom to top with numbers increasing as you move up. The origin for these axis is the intersection of the 0 X coordinate, otherwise known as the baseline, and the 0 Y coordinate.

    (illustration showing a g with the origin and axes highlighted)

In the positioning rules, we can adjust the placement and advance of glyphs. The placement is the spot at which the origin of the glyph will be aligned. The advance is the width and the height of the glyph from the origin. In horizontal typesetting, the height will be zero and the width will be the width of the glyph. The placement and advance can each be broken down into X and Y values. Thus, there is an x placement, a y placement, an x advance and a y advance.

    (illustration showing a g with the placements and advance highlighted)

The units that these values represent are the same units in which you have drawn your glyph. Together, these four values form a value record. In the .fea syntax, we express these value records like this:

    <xPlacement yPlacement xAdvance yAdvance>

For example:

    <1 2 3 4>

In this case, the value record is adjusting the x placement to the right by one unit, the y placement up by two units, the x advance by 3 unites and the y advance by four units.

When the positioning features are started, each glyph in the glyph run has a value record of <0 0 0 0>. As the processing happens and rules are matched, these value records are modified cumulative. So, if one feature adjust a glyph's x placement by 10 units and then another feature adjust the glyph's x placement by 30 units, the glyph's x placement would be 40 units.

### Adjustment Of One Glyph

To adjust the space around a single thing, you do this:

    pos target valueRecord;

(In the .fea documentation, this is known as GPOS Lookup Type 1: Single Adjustment Positioning.)

For example, to put some space to the left and right of the A, you would do this:

    pos A <10 0 20 0>;

You can also use a class as the target:

    pos [A B C] <10 0 20 0>;
    pos @upperclass <10 0 20 0>;

### Adjustment Of The Space Between Two Glyphs

To adjust the space between two glyphs, you do this:

    pos target1 target2 valueRecord;

(In the .fea documentation, this is known as GPOS Lookup Type 2: Pair Adjustment Positioning.)

In this case, you can shorten the value record to be only the x advance adjustment. Or, you can use the full value record if you prefer that.

This rule is used almost exclusively for kerning. In fact, this is so common that you shouldn't have to write any of these rules yourself. Your font and/or kerning editor should do this for you.

If you do want to see all the ways that you can use glyphs and classes in this rule, here you go:

    pos A T -50;
    pos [A Aacute] T -50;
    pos A [T Tbar] -50;
    pos [A Aacute] [T Tbar] -50;
    pos @A @T -50;
    pos @A T -50;
    pos A @T -50;
    pos @A [T Tbar] -50;
    pos [A Aacute] @T -50;

But, seriously, let your editor do this for you.


## Substitutions and Positioning Based on Context

The substitution and positioning rules that we have discussed so far are quite useful, but the real power is in triggering these rules only when certain conditions are met. These are known as contextual rules.

Contextual rules allow you to specify a sequence before and/or a sequence after the target in a substitution or positioning rule. For example: replace r with r.alt if the r is preceded by wo and followed by ds. There are two new parts of this rule type in addition to the parts we defined in the substitution and positioning sections.

1. Backtrack -- This is the sequence of things that occur before the target in the rule. This sequence can be composed of glyphs, classes or a mix of both.
2. Lookahead -- This is the sequence of glyphs that occur after the target in the rule. Like the backtrack, this sequence can be composed of glyphs, classes or a mix of both.

The backtrack and lookahead are both optional. Either can appear (or neither, but we'll cover that later). If a sequence is present, it can contain one or more things.

In addition to the backtrack and lookahead, a new character is needed in these rules: '. This character is used to mark the target of the rule.

Here is the words example from above in the correct syntax:

    sub w o r' d s by r.alt;

All of the substitution and positioning rule types can be defined with a context.

- replace one with one: sub a b' c by b.alt;
- replace many with one: sub a b' c' d by b_c;
- replace one with many: sub a b_c' d by b c;
- replace one from many: sub a b' c from [b.alt1 b.alt2];
- adjust position of one glyph: pos A B' C <10 0 20 0>;
- adjust positioning of the space between two glyphs: pos A B' C' D -50;

Please note that just because you can apply this to all rule types doesn't mean that you should.

### Exceptions

What if you have a short context that you want to match, but a longer context that contains the short context? For example, say we want to change the r in words but not in words!. To do that we can specify an exception to the contextual rule. For example:

    ignore sub w o r' d s exclam;
    sub w o r' d s by r.alt;

The ignore keyword followed by a backtrack (optional), target and lookahead (optional) creates the exception.

These can also be used to reduce the number and complexity of subsequent rules. (need an example of this)


## Advanced Techniques

By now you have the rules needed to make most features that you'll need to make--small caps, ligatures, tabular figures, etc. But, when you want to do some more complex things, you'll need a few more things.

Everything covered so far is enough for most features. You can make small caps, ligatures, tabular figures and more.

### Language Systems

One of OpenType's best attributes is the way that it handles languages and scripts. You can define rules that only apply when the user has indicated that they are writing a particular language or using a particular script. To do this, you state the script and the language that the rules apply to. After these have been made, all subsequent rules in the feature belong to this language and script unless you declare another language and script.

Let's look at an example. Let's say that we have a special IJ that should only be used when Dutch is the declared language. We need to say: when the script is latin and the language is Dutch, replace IJ with IJ.alt. Here is how we do that:

    script latn;
    language NLD;
    sub IJ by IJ.alt;

When you do this, you need to register that the features include a particular language and script combination, known as a language system. We'll go over where to do this later, but for now, this is the syntax:

    languagesystem script language;

The script tags are defined [here](https://www.microsoft.com/typography/otspec/scripttags.htm) and language tags are defined [here](http://www.microsoft.com/typography/developers/opentype/languagetags.aspx). For example, this is what we would use for our example:

    languagesystem latn NLD;

Before you define any language system, you should always declare this:

    languagesystem DFLT dflt;

This will register all rules for a fallback system in case an OpenType layout gets confused about which language or script your features apply to. Additionally, before you register a script with a specific language, you should register it with the default language for the same reason. So, the complete set of language system statements would look like this:

    languagesystem DFLT dflt;
    languagesystem latn dflt;
    languagesystem latn NLD;

### Lookups

We studied lookups when we went through the feature processing model, but they deserve some extra emphasis. Multiple lookups are allowed in a single feature and the fact that they process an entire glyph run before moving on to the next lookup makes them incredibly useful. You can use this technique to produce some very complex behavior. (Need to come up with an example for this.)

You can also reuse lookups if they are declared outside of a feature. To do this, define your lookup like this:

    lookup Example {
        # rules go here
    } Example;

Then, inside of your features you can have this lookup called by referencing its name:

    lookup Example;


# Putting It All Together

You know how the building blocks for writing everything from simple to complex features and you understand how it is actually going to work. Right? Great! Now, let's start looking at the bigger picture.

All of your features will be in a text file somewhere, either stored in your font source file or in an external file. I like to structure the code in my files like this:

1. languagesystem declarations
2. global classes
3. all substitution features
4. all positioning features

The language system declarations must come first. After that, the order is up to you, but I like to add any classes that I will use frequently, then all of the substitution features and then all of the positioning features.

## Building a Feature

Here is a basic example of a lot of this stuff combined into the proper form:

    languagesystem DFLT dflt;
    langaugesystem latn dflt;

    @lowercase = [a    b    c];
    @uppercase = [A    B    C];
    @smallCaps = [A.sc B.sc C.sc];

    @figures         = [zero    one    two];
    @figuresSmallCap = [zero.sc one.sc two.sc];

    @punctuation         = [exclam];
    @punctuationSmallcap = [exclam.sc];

    feature smcp {
        sub @lowercase by @smallcaps;
    } smcp;

    feature c2sc {
        sub @uppercase by @smallcaps;
        sub @lowercase by @smallcaps;
        sub @figures by @figuresSmallcap;
        sub @punctuation by @punctuationSmallcap;
    } c2sc;

Note that there are no lookups declared. Why? The first lookup is implied to be anything before you define a lookup. Consider this example:

    feature c2sc {
        sub @uppercase by @smallcaps;

        lookup Lowercase {
            sub @lowercase by @smallcaps;
        } Lowercase;
    } c2sc;

The first rule, sub @uppercase by @smallcaps;, is implicitly in a lookup. The result is the same as this:

    feature c2sc {
        lookup Uppercase {
            sub @uppercase by @smallcaps;
        } Uppercase;

        lookup Lowercase {
            sub @lowercase by @smallcaps;
        } Lowercase;
    } c2sc;

That's pretty much how you combine things. There will be more examples that demonstrate advanced techniques that you can study later.

## Feature Order

The order in which you list your features is very important. This is the order in which they will be processed. If you do something like put your ligatures before any alternates, your alternate code will have to take into account ligatures. It may even possibly have to break the ligatures down. That's possible, but results in overly complex code that is hard to read, edit and debug. I generally order my features like this:

1. script language specific forms (locl)
2. fractions (frac, numr, dnom)
3. superscript and subscript (sups, subs)
4. figures (lnum, tnum, pnum, tnum)
5. ordinals (ordn)
6. small caps (smcp, c2sc)
7. all caps (case)
8. various alternates (cswh, titl, salt, ss01, ss02, ss...)
9. ligatures (liga, dlig)
10. manual alternate access (aalt)
11. capital spacing (cpsp)

There are, of course, exceptions. The point is that you should think through this ordering so that you don't make things harder on yourself than you have to.

## Including an External File

If you are working on a family that shares features across multiple styles, it's cumbersome to store the features in each font source file. To get around this, you can store the features in an external file and reference them from the features in your font source file. To do this you use the include keyword:

    include(features/family.fea);

The text inside of the parenthesis must be the path to your external features file relative to the font source file. In the example above, the file family.fea is located in a folder called features right next to my font source file.

You can even include multiple files in a single font source file.


# Common Features And Techniques

Up until now, almost everything that has been discussed has been indisputable. The next section is far more subjective as there are numerous ways to write the code to create certain behaviors. What follows includes my own personal opinion.

I have prepared a demo font that includes all of the features and techniques defined below. You can open it up in your favorite font editor and play around with the features if you want to see how they work. The feature tags in the code below doesn't always match the tags in the font. I had to do it this way since there can't be more than one version of each feature.

The features in the demo font are by no means to complete or an indication of what is necessary to include in a particular feature. You should develop your own interpretation of what should be included in each feature based on the design of your font.

## Glyph Run and Word Boundary Detection

Often we want to make substitutions based on the bounds of words and glyph runs. For example, to inset a swash only at the beginning or at the end. There are three features in the specification for dealing with these situations:

- init -- Performs substitutions only at the beginning of a word.
- fina -- Performs substitutions only at the end of a word.
- medi - Performs substitutions only on the glyphs between the first and last in a word.

Unfortunately the specification is a bit vague about how these are supposed to be implemented. What exactly constitutes a word boundary? The Unicode specification details a word boundary detection algorithm and conceivably that's what would be used by the layout engines that are processing your font. That specification is quite thorough, but it thinks about word boundaries in a different way than type designers do (or at least this type designer does). For example, where are the word boundaries in this text?

    Hello “World!”

They are at the o, the W and the d. (I'm 99.999999% sure about this, but I should test it again.) If we use this for swashes our W and d are likely to clash with the marks “ and ! around them. We think of word boundaries as an empty space around words. If we want to use init and fina, we'll need to build in exceptions. You can certainly do that, but I generally do it all myself with some special classes:

- all -- This class contains all glyphs.
- filled -- This class contains all glyphs that contain positive space.
- empty -- This glyph contains all glyphs that contain only negative space.

With these, we can build lookups that handle boundary detection reasonable well enough for things like swashes.

    lookup GlyphRunInitial {
        ignore sub @all @initialsOff';
        sub @initialsOff by @initialsOn;
    } GlyphRunInitial;

    lookup GlyphRunFinal {
        ignore sub @finalsOff' @all;
        sub @finalsOff by @finalsOn;
    } GlyphRunFinal;

    lookup WordInitial {
        ignore sub @filled @initialsOff';
        sub @initialsOff by @initialsOn;
    } WordInitial;

    lookup WordMedial {
        sub @filled @medialOff' @filled by @medialOn;
    } WordMedial;

    lookup WordFinal {
        ignore sub @finalsOff' @filled;
        sub @finalsOff by @finalsOn;
    } WordFinal;

To be clear, you should not use this for shaping a Arabic or anything like that. This is strictly for things like swashes.

## Script And Language Specific Forms

The locl feature is specifically designed to implement global script and language specific changes that need to happen before any other features are processed. You can certainly put stylistic specific changes in other features, but the big important ones should be in locl.

    feature locl {

        script latn;

            language NLD exclude_dflt;
                lookup DutchIJ {
                    sub IJ by IJ.dutch;
                } DutchIJ;

    } locl;

## Fractions

I have used two different algorithms for implementing on-the-fly fractions. The first is fairly straightforward. The second is more complex but I think it is easier for users.

### Method 1: Individual

This method has been along for as long as I have been working on OpenType features. Adobe probably developed it in the very early days of the .fea language. It is probably still the most common implementation.

    (need to dig up an example)

### Method 2: Contextual

Around 2006 Kent Lew asked me if I had any ideas for a better fraction implementation. Specifically, he was referring to the fact that with the existing implementation, users had to manually select only the text that should be converted to fractions and apply the feature. If the feature was applied to more than just that text, all numbers not in a fraction would be converted to numerators. This was a big problem in things like cookbooks where there could be thousands of little bits of text that had to be converted to fractions.

I developed a new method that is built on the common form of writing fractions as an integer, a space, a numerator, a slash and a denominator. For example: 2 1/2. The code considers 1-10 numbers followed by a slash followed by 1 or more numbers to be a fraction. The slash is converted to a fraction bar, the numbers before the slash are converted to numerators and the numbers after the slash are converted to denominators. If the new fraction is preceded by a number followed by a space, the space is converted to a thin space to pull the fraction closer to the integer.

After I published the first version of this code, Karsten Luecke pointed out some some problems with dates, German tax numbers and things like that. I published a new version that handles these properly and this version is below.

With this implementation, users can globally activate fractions. The only drawback that I have found with this is that it doesn't allow numerators to be longer than 10 numbers long. In the unlikely event that a user runs into this problem, they can select the unconverted numerators and activate the numerator feature.

    feature frac {

        lookup FractionBar {
        ignore sub slash @figures @figures @figures @figures @figures @figures @figures @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures @figures @figures @figures @figures @figures @figures @figures slash;
        ignore sub slash @figures @figures @figures @figures @figures @figures @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures @figures @figures @figures @figures @figures @figures slash;
        ignore sub slash @figures @figures @figures @figures @figures @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures @figures @figures @figures @figures @figures slash;
        ignore sub slash @figures @figures @figures @figures @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures @figures @figures @figures @figures slash;
        ignore sub slash @figures @figures @figures @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures @figures @figures @figures slash;
        ignore sub slash @figures @figures @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures @figures @figures slash;
        ignore sub slash @figures @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures @figures slash;
        ignore sub slash @figures @figures @figures slash';
        ignore sub slash' @figures @figures @figures slash;
        ignore sub slash @figures @figures slash';
        ignore sub slash' @figures @figures slash;
        ignore sub slash @figures slash';
        ignore sub slash' @figures slash;
        ignore sub slash slash';
        ignore sub slash' slash;
        sub @figures slash' @figures by fraction;
        } FractionBar;

        lookup Numerator1 {
        sub @figures' fraction by @figuresNumerator;
        } Numerator1;

        lookup Numerator2 {
        sub @figures' @figuresNumerator fraction by @figuresNumerator;
        } Numerator2;

        lookup Numerator3 {
        sub @figures' @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator3;

        lookup Numerator4 {
        sub @figures' @figuresNumerator @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator4;

        lookup Numerator5 {
        sub @figures' @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator5;

        lookup Numerator6 {
        sub @figures' @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator6;

        lookup Numerator7 {
        sub @figures' @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator7;

        lookup Numerator8 {
        sub @figures' @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator8;

        lookup Numerator9 {
        sub @figures' @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator9;

        lookup Numerator10 {
        sub @figures' @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator @figuresNumerator fraction by @figuresNumerator;
        } Numerator10;

        lookup Denominator {
        sub [fraction @figuresDenominator] @figures' by @figuresDenominator;
        } Denominator;

        sub @figures space' @figuresNumerator by uni2009;
    } frac;

### Numerators

The numr feature is designed to convert all numbers to numerators.

    feature numr {
        sub @figures' by @figuresNumerator;
    } numr;

### Denominators

The dnom feature is designed to convert all numbers to denominators.

    feature dnom {
        sub @figures' by @figuresDenominator;
    } dnom;

## Superscript

The sups feature is for superscript forms.

    feature sups {
        sub @figures' by @figuresSuperscript;
    } sups;

## Subscript

The subs feature is for subscript forms.

    feature subs {
        sub @figures' by @figuresSubscript;
    } subs;

## Figures

If your font only includes one figure style, you don't need to do anything. If you do have more than one, you have to do some awkward things due to some odd behaviors in various applications. First off, it's best to define a feature for your default figures even though it will never be used. For example, in the demo font the default figures are lining and there are old style figures as alternates. First up we need to define the lining figures feature (lnum) even though it will never actually be used. Then we define the old style feature (onum).

    feature lnum {
        sub @figuresOldStyle by @figures;
    } lnum;

    feature onum {
        sub @figures by @figuresOldStyle;
    } onum;

Likewise, if your default figures are proportional and you have tabular alternates, you need to define the proportional figures feature (pnum) and then define the tabular figures feature (tnum).

    feature pnum {
        sub @figuresTabular by @figures;
        sub @figuresOldStyleTabular by @figuresOldStyle;
    } pnum;

    feature tnum {
        sub @figures by @figuresTabular;
        sub @figuresOldStyle by @figuresOldStyleTabular;
    } tnum;

## Ordinals

The sups feature is for ordinal forms.

    feature ordn {
        sub [A a] by ordfeminine;
        sub [O o] by ordmasculine;
    } ordn;

## Small Caps

There are two features that invoke small caps: small caps (smcp) and all small caps (c2sc). The all small caps version is for situations in which the user wants everything possible, not just letters, to be converted to small cap forms.

    feature smcp {
        sub @lowercase by @smallCaps;
    } smcp;

    feature c2sc {
        sub @uppercase by @smallCaps;
        sub @lowercase by @smallCaps;
        sub @figures by @figuresSmallCap;
    } c2sc;

## All Caps

There are two features that should be invoked when the user indicates that they want all text converted to uppercase. The first feature (case) transforms any glyphs that should be changed to an uppercase alternate. You should not define the transformation from lowercase to uppercase for alphabetic forms. The layout engine will do that for you.

    feature case {
        sub @punctuationUppercaseOff by @punctuationUppercaseOn;
    } case;

The second feature (cpsp) allows you to define all caps specific spacing.

    feature cpsp {
        pos @uppercase <100 0 200 0>;
        pos @punctuationUppercaseOn <100 0 200 0>;
    } cpsp;

Note that these features will be invoked whenever the user types in all capitals. The features must be activated manually.

## Swashes

    feature swsh {
        sub @uppercase by @swashCaps;
    } swsh;

Need cswh example.

## Titling Alternates

    feature titl {
        sub @uppercase by @titlingCaps;
    } titl;

## Stylistic Sets

- 1-20
- mention naming syntax but refer to the .fea spec

    feature ss01 {
        sub J by J.alt;
        sub J.sc by J.scalt;
    } ss01;

## Ligatures

    feature liga {
        sub f i by f_i;
        sub f l by f_l;
    } liga;


    feature dlig {
        sub O O by O_O;
    } dlig;

## Manual Alternate Access
aalt

## Fun Stuff

### Randomization

Everyone wants their font to look like the glyphs were randomly drawn. But, let's establish something first: No one will ever do randomization better than LettError did in their famous Beowolf. No one. Still want try some randomization? Okay.

Randomization is a bit of a Holy Grail in the OpenType world. The problem is that it's not actually possible for a couple of reasons. For one thing, we can only select from alternates, not actually modify glyph outlines. For another, for true pseudo-randomization there needs to be an external source that influences the random selection process and we can't build a random seed generator with the OpenType tables. So, we have to fake it. There are a number of methods that can be used to do this. I have three that I like.

(PS: That rand "random alternates" feature in the OpenType Layout Tag Registry? It's not supported widely, if at all. Sorry.)

#### Method 1: Endless Cycle

This method is useful when you don't have a preferred version of a glyph. For example, say you draw three glyphs for every character and you want those spread out across the text. This method will cycle between the glyphs.

For example:

    (illustration of AAAAAAAAAAAA in the demo font)

Given enough alternates, this creates an effective illusion in a large block of text.

The code is very simple:

    feature calt {
        @randomCycle1 = [@uppercase];
        @randomCycle2 = [A.random1 B.random1 C.random1 D.random1 E.random1 F.random1 G.random1 H.random1 I.random1 J.random1 K.random1 L.random1 M.random1 N.random1 O.random1 P.random1 Q.random1 R.random1 S.random1 T.random1 U.random1 V.random1 W.random1 X.random1 Y.random1 Z.random1];
        @randomCycle3 = [A.random2 B.random2 C.random2 D.random2 E.random2 F.random2 G.random2 H.random2 I.random2 J.random2 K.random2 L.random2 M.random2 N.random2 O.random2 P.random2 Q.random2 R.random2 S.random2 T.random2 U.random2 V.random2 W.random2 X.random2 Y.random2 Z.random2];

        sub @randomCycle1 @randomCycle1' by @randomCycle2;
        sub @randomCycle2 @randomCycle1' by @randomCycle3;
    } calt;

#### Method 2: Duplicate Eliminator

This method is useful if you want to tightly control the deployment of alternates. Specifically, if you only want an alternate to appear if the glyph that it is an alternate to has appeared recently.

For example:

    (illustration of BOOKKEEPING in the demo font)

The code is lengthy, but fairly straightforward:

    feature calt {

        @randomDuplicateSkip = [@uppercase];

        lookup RandomDuplicate1 {
            sub A A' by A.random1;
            sub B B' by B.random1;
            sub C C' by C.random1;
            sub D D' by D.random1;
            sub E E' by E.random1;
            sub F F' by F.random1;
            sub G G' by G.random1;
            sub H H' by H.random1;
            sub I I' by I.random1;
            sub J J' by J.random1;
            sub K K' by K.random1;
            sub L L' by L.random1;
            sub M M' by M.random1;
            sub N N' by N.random1;
            sub O O' by O.random1;
            sub P P' by P.random1;
            sub Q Q' by Q.random1;
            sub R R' by R.random1;
            sub S S' by S.random1;
            sub T T' by T.random1;
            sub U U' by U.random1;
            sub V V' by V.random1;
            sub W W' by W.random1;
            sub X X' by X.random1;
            sub Y Y' by Y.random1;
            sub Z Z' by Z.random1;
        } RandomDuplicate1;

        lookup RandomDuplicate2 {
            sub A @randomDuplicateSkip A' by A.random1;
            sub B @randomDuplicateSkip B' by B.random1;
            sub C @randomDuplicateSkip C' by C.random1;
            sub D @randomDuplicateSkip D' by D.random1;
            sub E @randomDuplicateSkip E' by E.random1;
            sub F @randomDuplicateSkip F' by F.random1;
            sub G @randomDuplicateSkip G' by G.random1;
            sub H @randomDuplicateSkip H' by H.random1;
            sub I @randomDuplicateSkip I' by I.random1;
            sub J @randomDuplicateSkip J' by J.random1;
            sub K @randomDuplicateSkip K' by K.random1;
            sub L @randomDuplicateSkip L' by L.random1;
            sub M @randomDuplicateSkip M' by M.random1;
            sub N @randomDuplicateSkip N' by N.random1;
            sub O @randomDuplicateSkip O' by O.random1;
            sub P @randomDuplicateSkip P' by P.random1;
            sub Q @randomDuplicateSkip Q' by Q.random1;
            sub R @randomDuplicateSkip R' by R.random1;
            sub S @randomDuplicateSkip S' by S.random1;
            sub T @randomDuplicateSkip T' by T.random1;
            sub U @randomDuplicateSkip U' by U.random1;
            sub V @randomDuplicateSkip V' by V.random1;
            sub W @randomDuplicateSkip W' by W.random1;
            sub X @randomDuplicateSkip X' by X.random1;
            sub Y @randomDuplicateSkip Y' by Y.random1;
            sub Z @randomDuplicateSkip Z' by Z.random1;
        } RandomDuplicate2;

        lookup RandomDuplicate3 {
            sub A @randomDuplicateSkip @randomDuplicateSkip A' by A.random1;
            sub B @randomDuplicateSkip @randomDuplicateSkip B' by B.random1;
            sub C @randomDuplicateSkip @randomDuplicateSkip C' by C.random1;
            sub D @randomDuplicateSkip @randomDuplicateSkip D' by D.random1;
            sub E @randomDuplicateSkip @randomDuplicateSkip E' by E.random1;
            sub F @randomDuplicateSkip @randomDuplicateSkip F' by F.random1;
            sub G @randomDuplicateSkip @randomDuplicateSkip G' by G.random1;
            sub H @randomDuplicateSkip @randomDuplicateSkip H' by H.random1;
            sub I @randomDuplicateSkip @randomDuplicateSkip I' by I.random1;
            sub J @randomDuplicateSkip @randomDuplicateSkip J' by J.random1;
            sub K @randomDuplicateSkip @randomDuplicateSkip K' by K.random1;
            sub L @randomDuplicateSkip @randomDuplicateSkip L' by L.random1;
            sub M @randomDuplicateSkip @randomDuplicateSkip M' by M.random1;
            sub N @randomDuplicateSkip @randomDuplicateSkip N' by N.random1;
            sub O @randomDuplicateSkip @randomDuplicateSkip O' by O.random1;
            sub P @randomDuplicateSkip @randomDuplicateSkip P' by P.random1;
            sub Q @randomDuplicateSkip @randomDuplicateSkip Q' by Q.random1;
            sub R @randomDuplicateSkip @randomDuplicateSkip R' by R.random1;
            sub S @randomDuplicateSkip @randomDuplicateSkip S' by S.random1;
            sub T @randomDuplicateSkip @randomDuplicateSkip T' by T.random1;
            sub U @randomDuplicateSkip @randomDuplicateSkip U' by U.random1;
            sub V @randomDuplicateSkip @randomDuplicateSkip V' by V.random1;
            sub W @randomDuplicateSkip @randomDuplicateSkip W' by W.random1;
            sub X @randomDuplicateSkip @randomDuplicateSkip X' by X.random1;
            sub Y @randomDuplicateSkip @randomDuplicateSkip Y' by Y.random1;
            sub Z @randomDuplicateSkip @randomDuplicateSkip Z' by Z.random1;
        } RandomDuplicate3;

    } calt;

#### Method 3: Quantum

This method is for dedicated randomization aficionados. A little history about how this came about: in 2005 I wanted to see if I could come up with a randomization technique that produced less predictable results than the methods above. I realized that I could use the text that the feature is transforming as a poor man's random seed. I was reading a tiny bit about quantum mechanics around the same time and my very limited understanding of some of the experiments in that field gave me an idea. That's a story that I won't get into here. Anyway, the code is long and convoluted, but the idea is pretty simple. I'll give you an overview.

Before we get to rules, we establish several important classes. First we create two trigger classes. The first will contain half of the glyphs in the font and the next will contain the other half of the glyphs. These need to be randomly chosen. In other words, don't put A-z in the same class. That won't produce the desired result. Next, we establish alternate states for glyphs. These states are defined in a series of classes. Each of these classes contain a glyph and its alternate. The next class contains the opposite of the previous class. For example:

    @class1 = [A A.alt];
    @class2 = [A.alt A];

Finally, we establish a skip class that contains everything in the font.

The glyph processing happens in a series of lookups that each pass over the entire glyph run. As a glyph, let's call it P, is being processed the lookup backtracks a specific number of glyphs. The glyph at the beginning of that backtrack, let's call it B, is then tested against a class, let's call it @T. Importantly, @T only contains half of the glyphs in the font. If B is in @T, P is switched to an alternate state. Thus, each glyph state is dependent on the state of all the glyphs that precede it. Given that the text is most likely going to have unpredictable letter combinations, we get a fairly effective randomization. For example:

    (illustration of the same string repeated in the demo font)

Is it real randomization? No. Is it perfect? No. Is it incredibly complex and hard to write? Yes (unless you use a script to write it). Can it be slow if a font contains a large number of glyphs and the glyph run being processed is very long? Yes. Is it awesome anyway? I think so.


    feature calt {
        @randomQuantumTrigger1 = [A.random1 A.random2 B B.random2 C C.random1 C.random2 D D.random1 E.random1 G G.random2 H H.random2 I J K.random1 L.random2 N.random1 O O.random1 P.random1 P.random2 Q.random1 S S.random1 S.random2 T T.random1 U.random2 V W.random1 W.random2 X X.random1 Y Y.random1 Y.random2 Z.random2];
        @randomQuantumTrigger2 = [A B.random1 D.random2 E E.random2 F F.random1 F.random2 G.random1 H.random1 I.random1 I.random2 J.random1 J.random2 K K.random2 L L.random1 M M.random1 M.random2 N N.random2 O.random2 P Q Q.random2 R R.random1 R.random2 T.random2 U U.random1 V.random1 V.random2 W X.random2 Z Z.random1 space];

    @randomQuantumGlyphs1 = [A         B         C         D         E         F         G         H         I         J         K         L         M         N         O         P         Q         R         S         T         U         V         W         X         Y         Z];
    @randomQuantumGlyphs2 = [A.random1 B.random1 C.random1 D.random1 E.random1 F.random1 G.random1 H.random1 I.random1 J.random1 K.random1 L.random1 M.random1 N.random1 O.random1 P.random1 Q.random1 R.random1 S.random1 T.random1 U.random1 V.random1 W.random1 X.random1 Y.random1 Z.random1];
    @randomQuantumGlyphs3 = [A.random2 B.random2 C.random2 D.random2 E.random2 F.random2 G.random2 H.random2 I.random2 J.random2 K.random2 L.random2 M.random2 N.random2 O.random2 P.random2 Q.random2 R.random2 S.random2 T.random2 U.random2 V.random2 W.random2 X.random2 Y.random2 Z.random2];

    @randomQuantumState1 = [@randomQuantumGlyphs1 @randomQuantumGlyphs3 @randomQuantumGlyphs2];
    @randomQuantumState2 = [@randomQuantumGlyphs2 @randomQuantumGlyphs1 @randomQuantumGlyphs3];
    @randomQuantumState3 = [@randomQuantumGlyphs3 @randomQuantumGlyphs2 @randomQuantumGlyphs1];

        @randomQuantumSkip = [@uppercase space];

        lookup RandomQuantum10 {
            sub @randomQuantumTrigger1 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState1' by @randomQuantumState2;
        } RandomQuantum10;

        lookup RandomQuantum9 {
            sub @randomQuantumTrigger2 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState2' by @randomQuantumState3;
        } RandomQuantum9;

        lookup RandomQuantum8 {
            sub @randomQuantumTrigger1 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState3' by @randomQuantumState1;
        } RandomQuantum8;

        lookup RandomQuantum7 {
            sub @randomQuantumTrigger2 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState1' by @randomQuantumState2;
        } RandomQuantum7;

        lookup RandomQuantum6 {
            sub @randomQuantumTrigger1 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState2' by @randomQuantumState3;
        } RandomQuantum6;

        lookup RandomQuantum5 {
            sub @randomQuantumTrigger2 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState3' by @randomQuantumState1;
        } RandomQuantum5;

        lookup RandomQuantum4 {
            sub @randomQuantumTrigger1 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState1' by @randomQuantumState2;
        } RandomQuantum4;

        lookup RandomQuantum3 {
            sub @randomQuantumTrigger2 @randomQuantumSkip @randomQuantumSkip @randomQuantumSkip @randomQuantumState2' by @randomQuantumState3;
        } RandomQuantum3;

        lookup RandomQuantum2 {
            sub @randomQuantumTrigger1 @randomQuantumSkip @randomQuantumSkip @randomQuantumState3' by @randomQuantumState1;
        } RandomQuantum2;

        lookup RandomQuantum1 {
            sub @randomQuantumTrigger2 @randomQuantumState1' by @randomQuantumState2;
        } RandomQuantum1;

        lookup RandomQuantum0 {
            sub @randomQuantumTrigger1 @randomQuantumState2' by @randomQuantumState3;
        } RandomQuantum0;

    } calt;

#### Bonus: Quantum Positioning

It's possible to extend the quantum randomization method above and use it to randomly shift glyphs around. Possible, but probably not advisable. The support for this is almost certainly going to be uneven.

The code is similar to the substitution method. In this case, instead of states, the cumulative effect that lookups have on glyph records is used.

    feature ss01 {
        @randomPositionQuantumTrigger1 = [A.random2 B B.random1 C.random2 D D.random1 E.random2 F F.random1 F.random2 G G.random2 H H.random2 I.random1 I.random2 J.random1 J.random2 K.random2 L.random1 M.random1 N O Q Q.random1 R S S.random1 T.random1 T.random2 U U.random1 U.random2 W.random1 X.random1 X.random2 Z Z.random2 space];
        @randomPositionQuantumTrigger2 = [A A.random1 B.random2 C C.random1 D.random2 E E.random1 G.random1 H.random1 I J K K.random1 L L.random2 M M.random2 N.random1 N.random2 O.random1 O.random2 P P.random1 P.random2 Q.random2 R.random1 R.random2 S.random2 T V V.random1 V.random2 W W.random2 X Y Y.random1 Y.random2 Z.random1];

        @randomPositionQuantumTarget = [@randomPositionQuantumTrigger1 @randomPositionQuantumTrigger2];

        @randomPositioningQuantumSkip = [@randomPositionQuantumTrigger1 @randomPositionQuantumTrigger2];

        lookup RandomPositioningQuantum9 {
            pos @randomQuantumTrigger2 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 50 0 0>;
        } RandomPositioningQuantum9;

        lookup RandomPositioningQuantum8 {
            pos @randomQuantumTrigger1 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 40 0 0>;
        } RandomPositioningQuantum8;

        lookup RandomPositioningQuantum7 {
            pos @randomQuantumTrigger2 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 30 0 0>;
        } RandomPositioningQuantum7;

        lookup RandomPositioningQuantum6 {
            pos @randomQuantumTrigger1 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 20 0 0>;
        } RandomPositioningQuantum6;

        lookup RandomPositioningQuantum5 {
            pos @randomQuantumTrigger2 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 10 0 0>;
        } RandomPositioningQuantum5;

        lookup RandomPositioningQuantum4 {
            pos @randomQuantumTrigger1 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 -10 0 0>;
        } RandomPositioningQuantum4;

        lookup RandomPositioningQuantum3 {
            pos @randomQuantumTrigger2 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 -20 0 0>;
        } RandomPositioningQuantum3;

        lookup RandomPositioningQuantum2 {
            pos @randomQuantumTrigger1 @randomPositioningQuantumSkip @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 -30 0 0>;
        } RandomPositioningQuantum2;

        lookup RandomPositioningQuantum1 {
            pos @randomQuantumTrigger2 @randomPositioningQuantumSkip @randomPositionQuantumTarget' <0 -40 0 0>;
        } RandomPositioningQuantum1;

        lookup RandomPositioningQuantum0 {
            pos @randomQuantumTrigger1 @randomPositionQuantumTarget' <0 -50 0 0>;
        } RandomPositioningQuantum0;

    } ss01;

### Roman Numerals


# Troubleshooting
- did you forget a special character? you probably forgot a } ; or something like that.
- did you name a lookup or class with the same name twice?
- all of the rule types in a lookup must be the same type
- table overflow (subtable, useExtension)
- features can't know if other features are active or not
- complex contextual rules leading to slowness of overflow errors (limit the contexts to what is *likely* to happen, not *everything*)


# .fea vs. Compiled Tables
- this is technical, but should probably be explained lightly


# Things That Should Not Be In This Document (and why)
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
- cursive positioning (why: too complex for this; not easy to test)
- mark to base positioning (why: too complex for this; not easy to test)
- mark to ligature positioning (why: too complex for this; not easy to test)
- mark to mark positioning (why: too complex for this; not easy to test)
- lookupflag (why: relates to the positioning rules that aren't covered)

# Thanks

Thanks to the Adobe Type Department for developing the .fea syntax. It gets criticized from time to time, but it is actually a great abstraction of the GSUB, GPOS and GDEF binary data structures. I've tried, and failed, to invent a better syntax several times. .fea is hard to beat. Thanks Adobe!


# Licenses, Copyrights and Credits

(Please note that the following license statement is a draft. I'm still thinking this through. For now, consider this document Copyright Type Supply LLC.)

The text of this document, except the code samples, is licensed as [Creative Commons Attribution-NonCommercial-ShareAlike](http://creativecommons.org/licenses/by-nc-sa/3.0/).

The code samples are released into the public domain. You may modify them, use them in commercial fonts and distribute them without attribution. You may not claim authorship of the original code or patent or copyright the original code.

The demo font included with this document is copyright Type Supply LLC. It may be used for reference only. You may not modify, extend, convert or sell it. I have used one of the fonts developed by my foundry so that there would be a high-quality example for you to study. Please be courteous.

The Adobe Feature File Syntax is copyright Adobe Systems Incorporated.

OpenType is either a registered trademark or trademark of Microsoft Corporation in the United States and/or other countries.


# Appendix: My .fea Style Guide

This will be a brief explanation the style guidelines I follow when writing .fea, because, obviously, I'm right. It'll be something like [PEP 8](http://legacy.python.org/dev/peps/pep-0008/), but not as long.
