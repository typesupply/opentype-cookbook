Title: Style Guide
Summary: Short version for index and feeds
Sortorder: 8

I like to make my code look nice. I'm a designer, so I'll even go so far as to say that I try to make it look typographic. My goal is to make it comfortable to read because, as Guido van Rossum once put it, code is read much more often than it is written. Debugging problems is not fun. Debugging problems in poorly structured, hard to read code is a bag of hurt.

Honestly, I don't really care if you use my style recommendations or if you invent your own. There is plenty in this style guide to disagree with and even I don't always follow these rules. What I do hope you will do is find a consistent way to structure and style your code so that it is easy for you to work with. That said, I am 100% right and everyone else is 100% wrong.

My preferred style has grown out of my experience with Python and my general adherence to the legendary PEP 8. So, it shares some traits with Python code.

## Whitespace

I use whitespace, both horizontal and vertical, to indicate logical groupings. Indentation is used to visually connect features, lookups, scripts and languages. Blank lines are used to indicate feature changes, sections and so on.

I prefer that indentation be done with spaces (four per indentation level), but I'm not religious about it. If you prefer tabs, use tabs. However, do not under any circumstance mix tabs and spaces. Similarly, do not put pointless spaces at the end of a line.

There should be no lines that contain no characters other than spaces. That's just gross.

## Column Width

I don't have a set column width for class definitions or rules. I find that they are harder to read if they are broken over multiple lines than if they are in one long line. I do wrap my comments if they are longer than 50-60 characters in length. I try to follow standard typographic practice when writing and breaking lines in comments. Comments are among the most important things in the code, so I try to make them ultra readable.

## Comments

I precede all comments with a single # followed by a space.

    # This looks nice.
    #This does not.

Comments are always indented to the level of the code that they are meant to document. Sudden horizontal shifts are jarring.

## Features

I structure my features like this:

    # -----------------
    # Example Feature 1
    # -----------------

    feature xmp1 {
        # rules, lookups, etc.
    } xmp1;


    # -----------------
    # Example Feature 2
    # -----------------

    feature xmp2 {
        # rules, lookups, etc.
    } xmp2;

Each feature, or group of features in the case of interrelated features like figure styles, gets a human readable header with line of hyphens above and below. The number of hyphens matches the number of characters in the header. One blank line follows this.

The feature begins unindented with the keyword, a space, the tag, a space and the opening brace. It is closed with an unindented closing brace, a space, the tag and the closing semicolon. Between the opening and closing lines, the indentation level of any line containing text is increased one level.

Features always have two blank lines between them and whatever is next in the file.

## Lookups

Lookups are structured like this:

    lookup ExampleLookup1 {
        # rules
    } ExampleLookup1;

    lookup ExampleLookup2 {
        # rules
    } ExampleLookup2;

The lookup begins at the current indent level with the keyword, a space, the lookup name, a space and the opening brace. It is closed with an unindented closing brace, a space, the lookup name and the closing semicolon. Between the opening and closing lines, the indentation level of any line containing text is increased one level.

Lookup names should be descriptive of what the lookup does. For example, SwashInitials, QuadrupleLigatures, FractionBar. The names are composed of characters in A-z a-z and 0-9. The first letter should be capitalized and other letters may be capitalized as needed to improve readability.

There should be at least one blank line above a lookup and one blank line below.

## Classes

Classes are defined line this:

    @exampleClass1 = [A B C];
    @exampleClass2 = [a b c];

The definition begins at the current indent level with the @ special character, the class name, a space, an =, a space, the opening bracket, a space delimited list of glyph names in a meaningful order, a closing bracket and the closing semicolon.

Classes should be defined on a single line. The definition may be broken into multiple lines only in rare circumstances.

Class names should be descriptive of the class' contents and purpose. For example, @uppercase, @figuresNumerator, @randomCycle1. If there are two classes that are intended for substituting with each other, for example if you have swash targets and swash replacements, it's good to tag the classes with Off and On for clarity. For example, @swashInitialsOff and @swashInitialsOn. Class names are composed of characters in A-z a-z and 0-9. The first letter should be lowercase and other letters may be capitalized as needed to improve readability.

If there are two or more classes that are intended for substituting with each other, readability can be greatly increased by using spaces between glyph names as alignment padding. For example:

    @figures         = [zero     one     two];
    @figuresTabular  = [zero.tab one.tab two.tab];
    @figuresSmallCap = [zero.sc  one.sc  two.sc];

## Rules

Rules are defined with the short version of the keywords, sub and pos, instead of the long versions, substitution and position. The rules are always on a single line and they are always written at the current indentation level. Class names are preferred over inline classes, but that's not always practical or possible. There should be no double spaces and there should be no space before the closing semicolon.

## Script and Language

Script and language definitions each increase the indentation level by one level until the next script or language definition or until the end of the feature. For example:

    feature locl {

        script latn;

            language TRK exclude_dflt;

                lookup IDOT {
                    sub i' by idotaccent;
                } IDOT;

            language AZE exclude_dflt;
                lookup IDOT;

            language CRT exclude_dflt;
                lookup IDOT;

            language ROM exclude_dflt;

                lookup SCEDILLA {
                    sub scedilla by uni0219;
                    sub Scedilla by uni0218;
                } SCEDILLA;

    } locl;