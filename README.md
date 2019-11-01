# nytwit

## Getting started
1. Copy `conf/conf.example.json` to `conf/conf.json`
2. Sign up for a New York Times [API key](https://developer.nytimes.com/)
3. Fill out the key and secret in `conf/conf.json` (`gitignore`d so no worries about checking in credentials)
4. Ignore Twitter auth stuff; decided to scrape public Twitter pages
5. In some appropriate environment (virtual or otherwise), run `pip install -e .` from the root directory of the project
6. In python, run `import nytwit`(yes, I know this is insanity, feel free to pull out into a different script)

The code currently grabs data starting from January 1, 2019 (see line 32 in `nytwit/__init.py__`
