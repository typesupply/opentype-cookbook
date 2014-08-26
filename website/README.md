# Website README

The OpenType Cookbook website uses [Pelican](http://getpelican.com) as a static site generator.

## Quickstart

1. ```pip install pelican markdown```

2. Edit page content, written using markdown, in the `/content` directory.

3. Generate the static content into the output directory: ```pelican -r```. The -r flag tells pelican to autoregenerate when it detects changes.

4. Preview the output. From the output directory: ```python -m SimpleHTTPServer```. The website can be viewed at [http://localhost:8000](http://localhost:8000).

More options for publishing and previewing the website can be found in [Pelican's docs](http://docs.getpelican.com/en/3.4.0/publish.html).
