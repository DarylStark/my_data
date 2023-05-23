# Branching and release strategy

This document describes the branching and release strategy for this library. In the document [Versioning](Versioning.md), you can find how versionnumbers are being generated for this library.

## Branching

This Git repository contains two important branches:
-   `dev`
-   `main`

The `dev` branch contains all work-in-progress code. When a new feature or bugfix is created, it will be created in it's own branch. After the creation is done, a GitHub Pull Request will be done to request the merging of the branch into the `dev` branch. After that is done, the `dev` branch contains the code for the new feature or bugfix and the specific branch for this feature can be closed. When all features and bugfixes for a specific version are merged into the `dev` branch and are tested, the `dev` branch will be merged into the `main` branch. The `-dev` tag will be removed from the version and the production version will be distributed.

## Release strategy

This repository used GitHub Actions as a CI/CD mechanism to run unit tests, check code quality and to publish the package to the correct repository. Within GitHub Actions, there are three workflow created (which you can find in `.github/workflows`):

-   `push-to-all-other`; this workflow gets kicked off when one or more commits in any branch, except `main` and `dev` are pushed to GitHub. Within this workflow, unit tests are run and a code quality check is done.
-   `push-to-dev`; this workflow gets kicked off when a push to `dev` is done. This workflow checks if the version-tag is `dev` and runs the unit tests and code quality tests. After that, it published the `dev` package to the correct Python repository.
-   `push-to-main`; this workflow gets kicked off when a push to `main` is done. This workflow checks if the version-tag is `final` and runs the unit tests and code quality tests. After that, it published the `final` package to the correct Python repository.

To make this work, a specific way of working is required. When starting a new feature or bugfix, you'll have to create a new branch. If it is from a GitHub issue, we use the naming convention `issue-<number>/<short-description>`. Within this branch, you make your changes to the code. After you're done making changes, you commit and push your code. The `push-to-all-other` workflow wil test the code. You can then create a Pull Reqeust to merge this code with the `dev` branch. After this is merged, the specific branch can and should be deleted.

After all changes are in `dev` that needed to be done, it has be to be merged into `main`. As of right now, this cannot be done with a Pull Request since the version will be `dev`. So, instead, you have to use the following steps:

1.  Check out the `main` branch in your local repository
2.  Fetch all changes for all branches to make sure you don't miss anything:

    ```bash
    git fetch --all --prune
    ```
3.  Merge the `dev` branch into the `main` branch:

    ```bash
    git merge dev
    ```
4.  Update the version-tag with the `bumpver` command. This command has to be installed within your Python environment first

    ```bash
    bumpver update --no-fetch --tag final --tag-commit
    ```

    A new commit will be automatically made and a Git tag will be automatically made. Make sure to sign the Git tag with your PGP key.
5.  Push the code to GitHub. The `push-to-main` workflow will be kicked off and everything should be correct now. The package will be published and user can use the library now.
6.  Create a release in GitHub by going to the tag overview and clicking on `Releases`. Click the `Add release` button and choose the newly created tag and the `main` branch for the release.
7.  Switch back to the `dev` branch. Merge the main branch into `dev` and use `bumpver` to upgrade to a new patch-level or minor-level and make sure to set the versiontag to `dev`:

    ```bash
    bumpver update --no-fetch --tag dev <--patch | --minor>
    ```
8.  Push the new `dev` branch. Everything should be correct now.