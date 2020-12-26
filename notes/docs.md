Create a folder docs in the root path.

pip install sphinx recommonmark

By default, Jekyll does not build any files or directories with underscore. Include an empty .nojekyll file in the docs folder to turn off Jekyll.

In the docs folder, create an index.html file and redirect to ./html/index.html for example like this:

<meta http-equiv="refresh" content="0; url=./build/html/index.html" />

Change the Sphinx build directory to docs in your Makefile for example as follows:
BUILDDIR  = build



Add modules.rst to index.rst

```
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules.rst
```

Add extensions to sphinx conf.py
```
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.todo',
              'sphinx.ext.autosummary', 'sphinx.ext.viewcode', 'sphinx.ext.coverage',
              'sphinx.ext.doctest', 'sphinx.ext.ifconfig', 'sphinx.ext.mathjax',
              'sphinx.ext.napoleon', 'recommonmark']

```

sphinx-apidoc -o . ../fhiry

uncomment and modify conf.py. For this example, sys.path.insert(0, os.path.abspath('mymodule'))
re-run make html


Run make html then add, commit and push the repo.

In your project config, choose to use the docs folder for your GitHub Pages.

visit https://<username>.github.io/<repo>
