# gdapi-diff

Compares the API JSON dump of different Godot Engine versions.
For help, see `python gdapi-diff.py --help`.

Rough initial implementation. :)

For simple use, just calling `python gdapi-diff.py` should be enough.
Dump files are placed in `dumps/`.
To generate dump files, use the below commands with a Godot Engine executable:

- `godot --dump-extension-api` (for Godot 4.0 and later)
- `godot --gdnative-generate-json-api api.json` (for Godot 3.x)

Output path and format are currently ignored and STDOUT is used, pipe to file manually for now.
For example output see [here](https://gist.github.com/mhilbrunner/9dee280293b4c8063f5ce97e38173430).

Requires Python 3 and optionally Numpy for edit distance calculations.
