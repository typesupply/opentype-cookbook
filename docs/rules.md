---
layout: default
navigation: true
title: Rules
order: 4
---

Now that we have introduced some terminology, covered the way text is processed and established the general syntax rules, we can get into the fun part: actually doing stuff.

## Substitutions

Substitutions are the most visually transformative thing that features can do to text. And, they are easy to understand. There are two main parts to a substitution:

1. Target — This is what will be replaced.
2. Replacement — This is what will be inserted in place of the target.

The syntax for a substitution is:

```opentype_feature_file
substitute target by replacement;
```

We can abbreviate `substitute` with `sub` to cut down on how much stuff we have to type, so let’s do that:

```opentype_feature_file
sub target by replacement;
```

Targets and replacements can often be classes. These classes can be referenced by name or they can be defined as an unnamed class inside of a rule.

### Replace One With One

To replace one thing with another, you do this:

```opentype_feature_file
sub target by replacement;
```

*(In the .fea documentation, this is known as GSUB Lookup Type 1: Single Substitution.)*

For example, to transform `a` to `A.sc`, you would do this:

```opentype_feature_file
sub a by A.sc;
```

If you want to replace several things with corresponding things, you can use classes as both the target and the replacement. However, in this case the number of things in the two classes needs to be the same, unlike above.

```opentype_feature_file
sub [a b c] by [A.sc B.sc C.sc];
```

It’s usually more readable to define the classes earlier in your code and then reference them by name.

```opentype_feature_file
sub @lowercase by @smallcaps;
````

The order of the glyphs in your classes in this situation is critical. In the example above, the classes will correspond with each other like this:

    a → A.sc
    b → B.sc
    c → C.sc

If you order the target and replacement classes incorrectly, things will go wrong. For example, if you have this as your rule:

```opentype_feature_file
sub [a b c] by [B.sc C.sc A.sc];
```

The classes will correspond like this:

    a → B.sc
    b → C.sc
    c → A.sc

This is obviously undesired behavior, so keep your classes ordered properly.

### Replace Many With One

To replace a sequence of things with one thing, you do this:

```opentype_feature_file
sub target sequence by replacement;
```

*(In the .fea documentation, this is known as GSUB Lookup Type 4: Ligature Substitution.)*

For example, for an `fi` ligature, you would do this:

```opentype_feature_file
sub f i by f_i;
```

You can also use classes as part of the target sequence:

```opentype_feature_file
sub @f @i by f_i;
```

Or:

```opentype_feature_file
sub @f i by f_i;
```

Or:

```opentype_feature_file
sub f @i by f_i;
```

### Replace One With Many

To replace a single thing with a sequence of things, you do this:

```opentype_feature_file
sub target by replacement sequence;
```

*(In the .fea documentation, this is known as GSUB Lookup Type 2: Multiple Substitution.)*

For example, to convert an `fi` ligature back into `f` and `i`, you would do this:

```opentype_feature_file
sub f_i by f i;
```

Classes can’t be used as the target or the replacement in this rule type.

### Replace One From Many

To give the user a choice of alternates, you do this:

```opentype_feature_file
sub target from replacement;
```

*(In the .fea documentation, this is known as GSUB Lookup Type 3: Alternate Substitution.)*

The replacement must be a glyph class, and (unlike above) does not happen automatically, but usually requires active user interaction (e.g. picking glyphs from a selection of alternates).

For example, to give the user several options to replace `a` with, you would do this:

```opentype_feature_file
sub a from [a.alt1 a.alt2 a.alt3];
```

Note that the keyword in the middle of the rule is `from` instead of `by`.

## Positioning

Positioning glyphs may not be as visually interesting as what can be achieved with substitution, but the positioning support in OpenType is incredibly powerful and important. The positioning rules can be broken into two separate categories:

1. Simple Rules — These adjust either the space around one glyph or the space between two glyphs.
2. Mind-Blowingly Complex and Astonishingly Powerful Rules — These do things like properly shift combining marks to align precisely with the base forms in Arabic and Devanagari so that things look incredibly spontaneous and beautiful.

We’re going to cover the simple rules in this cookbook. The complex rules are amazing, but too advanced for now.

### Position and Advance

Before we go much further we need to talk about coordinate systems and value records. As you know, the coordinate system in fonts is based on X and Y axes. The X axis moves from left to right with numbers increasing as you move to the right. The Y axis moves from bottom to top with numbers increasing as you move up. The origin for these axis is the intersection of the 0 X coordinate, otherwise known as the baseline, and the 0 Y coordinate.

<object type="image/svg+xml" data="/media/illustrations/rules-origin-axes.svg"></object>

In the positioning rules, we can adjust the *placement* and *advance* of glyphs. The placement is the spot at which the origin of the glyph will be aligned. The advance is the width and the height of the glyph from the origin. In horizontal typesetting, the height will be zero and the width will be the width of the glyph. The placement and advance can each be broken down into X and Y values. Thus, there is an x placement, a y placement, an x advance and a y advance.

<object type="image/svg+xml" data="/media/illustrations/rules-value-record.svg"></object>

The units that these values represent are the same units in which you have drawn your glyph. Together, these four values form a *value record*. In the .fea syntax, we express these value records like this:

```opentype_feature_file
<xPlacement yPlacement xAdvance yAdvance>
```

For example:

```opentype_feature_file
<10 20 30 40>
```

In this case, the value record is adjusting the x placement to the right by 10 units, the y placement up by 20 units, the x advance by 30 units and the y advance by 40 units.

<object type="image/svg+xml" data="/media/illustrations/rules-modified-value-record.svg"></object>

The syntax for a positioning rule is:

```opentype_feature_file
position target valueRecord;
```

We can abbreviate `position` with `pos` to cut down on how much stuff we have to type, so let’s do that:

```opentype_feature_file
pos target valueRecord;
```

Targets can be classes. These classes can be referenced by name or they can be defined as an unnamed class inside of a rule.

#### Cumulative Effect

When the positioning features are started, each glyph in the glyph run has a value record of `<0 0 0 0>`. As the processing happens and rules are matched, these value records are modified cumulatively. So, if one feature adjusts a glyph’s x placement by 10 units and then another feature adjusts the glyph’s x placement by 30 units, the glyph’s x placement would be 40 units.


### Adjust the Position of One Glyph

To adjust the space around a single target, you do this:

```opentype_feature_file
pos target valueRecord;
```

*(In the .fea documentation, this is known as GPOS Lookup Type 1: Single Adjustment Positioning.)*

For example, to put some space to the left and right of the `A`, you would do this:

```opentype_feature_file
pos A <10 0 20 0>;
```

### Adjust the Space Between Two Glyphs

To adjust the space between two targets, you do this:

```opentype_feature_file
pos target1 target2 valueRecord;
```

*(In the .fea documentation, this is known as GPOS Lookup Type 2: Pair Adjustment Positioning.)*

In this case, you can shorten the value record to be only the x advance adjustment. Or, you can use the full value record if you prefer that.

This rule is used almost exclusively for kerning. In fact, this is so common that you shouldn’t have to write any of these rules yourself. Your font and/or kerning editor should do this for you.

You can use a class as target 1, target 2 or both:

```opentype_feature_file
pos @A T -50;
```

Or:

```opentype_feature_file
pos A @T -50;
```

Or:

```opentype_feature_file
pos @A @T -50;
```

But, seriously, let your editor write these rules for you.


## Substitutions and Positioning Based on Context

The substitution and positioning rules that we have discussed so far are quite useful, but the real power is in triggering these rules only when certain conditions are met. These are known as contextual rules.

Contextual rules allow us to specify a sequence before the target, a sequence after the target or both in a substitution or positioning rule. For example: replace `r` with `r.alt` if the `r` is preceded by `wo` and followed by `ds`. There are two new parts of this rule type in addition to the parts we defined in the substitution and positioning sections.

1. Backtrack — This is the sequence of things that occur before the target in the rule. This sequence can be composed of glyphs, classes or a mix of both.
2. Lookahead — This is the sequence of glyphs that occur after the target in the rule. Like the backtrack, this sequence can be composed of glyphs, classes or a mix of both.

The backtrack and lookahead are both optional. Either, or neither, can appear. If a sequence is present, it can contain one or more things.

In addition to the backtrack and lookahead, a new character is needed in these rules: `'`. This character is used to mark the target of the rule.

Here is the words example from above in the correct syntax:

```opentype_feature_file
sub w o r' d s by r.alt;
```

Most of the substitution and positioning rule types can be defined with a context.

- replace one with one: `sub a b' c by b.alt;`
- replace many with one: `sub a b' c' d by b_c;`
- adjust position of one glyph: `pos A B' C <10 0 20 0>;`
- adjust positioning of the space between two glyphs: `pos A B' C' -50 D;`

Please note that just because you *can* apply this to a rule type doesn’t mean that it always makes sense; or that you should.

### Exceptions

What if we have a short context that you want to match, but a longer context that contains the short context? For example, say we want to change the r in `words` but not in `words!`. To do that we can specify an *exception* to the contextual rule. For example:

```opentype_feature_file
ignore sub w o r' d s exclam;
sub w o r' d s by r.alt;
```

The `ignore` keyword followed by a backtrack (optional), target and lookahead (optional) creates the exception.

### Common Gotcha

If you use a contextual rule or exception within a lookup, all of the rules within that lookup *must* also use the `'` on the target of the rule. For example:

```opentype_feature_file
sub a b' c by b.alt;
sub d' by d.alt;
```

## Advanced Techniques

By now we have established the rules needed to make most features that you’ll want to add to your fonts—small caps, ligatures, tabular figures, etc. But, when you want to do some more complex things, you’ll need a few more things.

### Language Systems

One of OpenType’s best attributes is the way that it handles languages and scripts. We can define rules that only apply when the user has indicated that they are writing a particular language or using a particular script. To do this, we state the script and the language that the rules apply to. After these have been made, all subsequent rules in the feature belong to this language and script unless you declare another language and script.

Let’s look at an example. Let’s say that we have a special `IJ` that should only be used when Dutch is the declared language. We need to say: when the script is latin and the language is Dutch, replace `IJ` with `IJ.alt`. Here is how we do that:

```opentype_feature_file
script latn;
language NLD;
sub IJ by IJ.dutch;
```

The script tags are defined [here](https://docs.microsoft.com/typography/opentype/spec/scripttags) and language tags are defined [here](https://docs.microsoft.com/typography/opentype/spec/languagetags).

If you add language or script specific rules you also need to register that the features include a particular language and script combination, known as a language system, before any of your feature definitions. This is the syntax:

```opentype_feature_file
languagesystem script language;
```

And in our example, we would do this:

```opentype_feature_file
languagesystem latn NLD;
```

Before you define any specific language system, you should always declare this:

```opentype_feature_file
languagesystem DFLT dflt;
```

This will register all rules for a fallback system in case an OpenType layout engine gets confused about which language or script your features apply to. Additionally, before you register a script with a specific language, you should register it with the default language for the same reason. So, the complete set of language system statements would look like this:

```opentype_feature_file
languagesystem DFLT dflt;
languagesystem latn dflt;
languagesystem latn NLD;
```

### Lookups

We studied lookups when we went through the feature processing model, but they deserve some extra emphasis. Multiple lookups are allowed in a single feature and the fact that they process an entire glyph run before moving on to the next lookup makes them incredibly useful. We can use this technique to produce some very complex behavior. For example, in a swash feature it is often best to insert swashes first at the beginning and then at the end of words in separate passes. We can do this easily with lookups.

You can also reuse lookups if they are declared outside of a feature. To do this, define your lookup like this:

```opentype_feature_file
lookup Example {
    # rules go here
} Example;
```

Then, inside of your features you can have this lookup called by referencing its name:

```opentype_feature_file
lookup Example;
```

This is useful if you want to share some rules across multiple features.

```opentype_feature_file
lookup Inferiors {
    sub @inferiorOff by @inferiorOn;
} Inferiors;

feature subs {
    lookup Inferiors;
} subs;

feature sinf {
    lookup Inferiors;
} sinf;
```
