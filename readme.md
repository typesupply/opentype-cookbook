Welcome to The Unofficial OpenType Cookbook. Feel free to peruse this information in its raw state here. But, it's much nicer in its compiled form on [opentypecookbook.com](http://opentypecookbook.com).

## Getting started

The OpenType Cookbook website uses [Pelican](http://getpelican.com) as a static site generator, which compiles the source Markdown and theme files into plain HTML, CSS, and JavaScript. This is published to [Surge.sh](https://surge.sh) via [Travis CI](http://travis-ci.org) each time a change is pushed to the `master` branch of this repository on GitHub.

This means that, if you spot something you’d like to fix, you can open a Pull Request right from GitHub and have the changed merged and published—all without ever needing to run anything locally.

If you _would_ like to run the project locally yourself:

1. Run `pip install pelican markdown` with Python 2.7 installed

2. Edit page content, written using markdown, in the `/content` directory.

3. Generate the static content into the output directory: ```pelican -r```. The `-r` flag tells pelican to autoregenerate when it detects changes.

4. Preview the output. From the output directory: `python -m SimpleHTTPServer`. The website can be viewed at [http://localhost:8000](http://localhost:8000).

More options for publishing and previewing the website can be found in [Pelican's docs](http://docs.getpelican.com/en/3.4.0/publish.html).
