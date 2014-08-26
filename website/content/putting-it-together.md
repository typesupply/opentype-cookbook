Title: Putting it Together
Summary: Short version for index and feeds
Sortorder: 6

You now have the building blocks for writing everything from simple to complex features and you understand how it is actually going to work. Right? Great! Now, let's start looking at the bigger picture.

All of your features will be in a text file somewhere, either stored in your font source file or in an external file. I like to structure the code in my files like this:

1. languagesystem declarations
2. global classes
3. all substitution features
4. all positioning features

The language system declarations must come first. After that, the order is up to you, but I like to add any classes that I will use frequently, then all of the substitution features and then all of the positioning features.

## Building a Feature

Here is a basic example combined into the proper form:

    :::fea
    languagesystem DFLT dflt;
    langaugesystem latn dflt;

    @lowercase = [a    b    c];
    @uppercase = [A    B    C];
    @smallcaps = [A.sc B.sc C.sc];

    @figures         = [zero    one    two];
    @figuresSmallcap = [zero.sc one.sc two.sc];

    @punctuation         = [exclam];
    @punctuationSmallcap = [exclam.sc];

    feature smcp {
        sub @lowercase by @smallcaps;
    } smcp;

    feature c2sc {
        sub @uppercase by @smallcaps;
        sub @lowercase by @smallcaps; _Is this line necessary?_
        sub @figures by @figuresSmallcap;
        sub @punctuation by @punctuationSmallcap;
    } c2sc;

Note that there are no lookups declared. Why? The first lookup is implied to be anything before you define a lookup. Consider this example:

    :::fea
    feature c2sc {
        sub @uppercase by @smallcaps;

        lookup Lowercase {
            sub @lowercase by @smallcaps;
        } Lowercase;
    } c2sc;

The first rule, sub @uppercase by @smallcaps;, is implicitly in a lookup. The result is the same as this:

    :::fea
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

The order in which you list your features is very important. This is the order in which they will be processed. If you do something like put your ligatures before any alternates, your alternate code will have to take into account potential ligatures. It may even possibly have to break the ligatures down. That's possible, but it results in overly complex code that is hard to read, edit and debug. I generally order my features like this:

1. script language specific forms (locl)
2. fractions (frac, numr, dnom)
3. superscript and subscript (sups, subs)
4. figures (lnum, onum, pnum, tnum)
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

    :::fea
    include(features/family.fea);

The text inside of the parenthesis must be the path to your external features file relative to the font source file. In the example above, the file family.fea is located in a folder called features right next to my font source file.

You can even include multiple files in a single font source file. For example:

    :::fea
    include(features/family.fea);
    include(features/bold-kern.fea);

Even in other folders, below the current one:

    :::fea
    include(../tables.fea);
