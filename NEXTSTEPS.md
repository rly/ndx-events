# Next Steps for ndx-events Extension for NWB:N

## Creating Your Extension

1. In a terminal, change directory into the new ndx-events directory.

2. Add any packages required by your extension to `requirements.txt` and `setup.py`.

3. Run `python -m pip install -r requirements.txt` to install the `pynwb` package
and any other packages required by your extension.

4. Modify `src/create_extension_spec.py` to define your extension.

    - If you want to create any custom classes for interacting with the extension,
      add them to the `src/pynwb`.
      - If present, the `src/pynwb` folder MUST contain the following:
        - `ndx-events` - Folder with the sources of the NWB extension
        - `ndx-events/__init__.py` - Python file that may be empty
      - If present, the `src/pynwb` folder MAY contain the following files/folders:
        - `test` - Folder for unit tests for the extensions
        - `jupyter_widgets` - Optional package with custom widgets for use with Jupyter

5. Run `python src/spec/create_extension_spec.py` to generate the
`spec/ndx-events.namespace.yaml` and
`spec/ndx-events.extensions.yaml` files.

6. You may need to modify `setup.py` and re-run `python setup.py install` if you
use any dependencies.


## Documenting and Publishing Your Extension to the Community

1. Install the latest release of hdmf_docutils: `python -m pip install hdmf-docutils`

2. Start a git repository for your extension directory ndx-events
 and push it to GitHub. You will need a GitHub account.
    - Follow these directions:
  https://help.github.com/en/articles/adding-an-existing-project-to-github-using-the-command-line

3. Change directory into `docs`.

4. Run `make html` to generate documentation for your extension based on the YAML files.

5. Read `docs/README.md` for instructions on how to customize documentation for
your extension.

6. Modify `README.md` to describe this extension for interested developers.

7. Add a license file. Permissive licenses should be used if possible. **A [BSD license](https://opensource.org/licenses/BSD-3-Clause) is recommended.**

8. Make a release for the extension on GitHub with the version number specified. e.g. if version is 0.1.0, then this page should exist: https://github.com/rly/ndx-events/releases/tag/0.1.0 . For instructions on how to make a release on GitHub see [here](https://help.github.com/en/github/administering-a-repository/creating-releases).

9. Publish your updated extension on PyPi.
    - Follow these directions: https://packaging.python.org/tutorials/packaging-projects/
    - You may need to modify `setup.py`
    - If your extension version is 0.1.0, then this page should exist: https://pypi.org/project/ndx-events/0.1.0

   Once your GitHub release and ``setup.py`` are ready, publishing on PyPi:
    ```bash
    python setup.py sdist bdist_wheel
    twine upload dist/*
    ```

10. Go to https://github.com/nwb-extensions/staged-extensions and fork the
repository.

11. Clone the fork onto your local filesystem.

12. Copy the directory `staged-extensions/example` to a new directory
`staged-extensions/ndx-events`:

    ```bash
    cp -r staged-extensions/example staged-extensions/ndx-events
    ```

13. Edit `staged-extensions/ndx-events/ndx-meta.yaml`
with information on where to find your NWB extension.
    - The YAML file MUST contain a dict with the following keys:
      - name: extension namespace name
      - version: extension version
      - src: URL for the main page of the public repository (e.g. on GitHub, BitBucket, GitLab) that contains the sources of the extension
      - pip: URL for the main page of the extension on PyPI
      - license: name of the license of the extension
      - maintainers: list of GitHub
      usernames of those who will reliably maintain the extension
    -

  You may copy and modify the following YAML that was auto-generated:
```yaml
name: ndx-events
version: 0.1.0
src: https://github.com/rly/ndx-events
pip: https://pypi.org/project/ndx-events/
license: BSD 3-Clause
maintainers:
  - rly
```

14. Edit `staged-extensions/ndx-events/README.md`
to add information about your extension. You may copy it from
`ndx-events/README.md`.

  ```bash
cp ndx-events/README.md staged-extensions/ndx-events/README.md
```

15. Add and commit your changes to Git and push your changes to GitHub.
```
cd staged-extensions
git add ndx-events
git commit -m "Add new catalog entry for ndx-events" .
git push
```

16. Open a pull request. Building of your extension will be tested on Windows,
Mac, and Linux. The technical team will review your extension shortly after
and provide feedback and request changes, if any.

17. When your pull request is merged, a new repository, called
ndx-events-feedstock will be created in the nwb-extensions
GitHub organization and you will be added as a maintainer for that repository.


## Updating Your Published Extension

1. Update your ndx-events GitHub repository.

2. Publish your updated extension on PyPi.

3. Fork the ndx-events-feedstock repository on GitHub.

4. Open a pull request to test the changes automatically. The technical team
will review your changes shortly after and provide feedback and request changes,
 if any.

5. Your updated extension is approved.
