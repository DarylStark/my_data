# Versioning

For this library is chosen to use incremental version numbering with the version pattern `MAJOR.MINOR.PATCH[-TAG]`. The `MAJOR` starts at `1` and is only increased when there is a new version that causes major breaking of code that is dependent on this library. This version will almost never, if ever, increase. The `MINOR` is increased when new features are added to the library. If this version will break anything, it will be in the release notes. The `PATCH` is increased when there are bugfixes in the code. This should never break any dependent code.

The `-TAG` defines what kind of library this is. For this library, the tag can be either nothing, meaning it is a final release, or `dev`, meaning the release is still in development. If the tag is `dev`, there is a likely chance that this version will change overtime. You cannot use this kind of version for production workloads.

## Release notes

The releasenotes for this library will be placed at two places; in the repository in a file called `CHANGELOG.md` and on GitHub at the releases page. Both should be the same at all time and should contain all changes for all versions, including the date of the release. Both locations will only contain the changes in final released, not in dev releases.