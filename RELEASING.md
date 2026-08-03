# Releasing

This project uses [semantic versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`), with git tags in the form `1.2.3` (no `v` prefix, to match the existing `1.0.0` and `1.0.1` tags).

## Steps

1. Update the version in `pyproject.toml`:

   ```toml
   [project]
   version = "1.2.3"
   ```

2. Commit the version bump directly to `main`, or through a pull request if the change should go through CI first:

   ```shell
   git add pyproject.toml
   git commit -m "Bump version to 1.2.3"
   git push origin main
   ```

3. Tag the commit and push the tag:

   ```shell
   git tag 1.2.3
   git push origin 1.2.3
   ```

4. Create the GitHub release from the tag, with notes summarising the changes since the last release:

   ```shell
   gh release create 1.2.3 --title 1.2.3 --generate-notes
   ```

   Edit the generated notes if they need more context, then publish.

## When to bump which part

- **Patch** (`1.2.3` → `1.2.4`): bug fixes, dependency bumps, robustness improvements, no behaviour change for existing users.
- **Minor** (`1.2.3` → `1.3.0`): new features or options that don't break existing configs or command-line usage.
- **Major** (`1.2.3` → `2.0.0`): breaking changes, such as a different `config.ini` format or a dropped command-line argument.
