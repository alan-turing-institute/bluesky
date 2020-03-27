
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Git tags are prefixed with `turing-` to avoid clashes with any upstream tags. This prefix is assumed for all versions
referenced in this file.

## [Unreleased]

-

## [1.4.1] - 2020-03-27

- Fix remaining issues with msgpack 1.0.0

## [1.4.0] - 2020-03-27

- Upgrade msgpack to v1.0.0, and fix encoding changes
- Add client echo response to DTMULT command
- Disable auto-start of simulation when aircraft are added

## [1.3.0] - 2020-01-01

### Added

- TravisCI: Add pip cache, build on all branches, and add the Docker build as part of the test
- Added a `--build-caches` option, to pre-build the Navdatabase cache files. This reduces the start-up time of the Docker container

## [1.2.3] - 2019-10-08

### Added

- Add `LISTAC` stack command

## [1.2.2] - 2019-08-09

### Removed

- Removed `pyopengl-accelerate` dependency

## [1.2.1] - 2019-07-12

### Added

- Reloaded scenario files added to .gitignore

### Fixed

- Create the directory for new scenarios if it doesn't exist

## [1.2.0] - 2019-06-28

### Added

- `STEP` command added to server and simulation

### Fixed

- Return to previous `DTMULT` value after simulation is resumed
- Add PyQtWebEngine to requirements - fixes 'Bluesky needs pyqt5' error

## [1.1.1] - 2019-05-16

### Fixed

- Added proper handling of Ctrl+C and QUIT events

## [1.1.0] - 2019-05-16

### Added

- New server command to allow uploading of a scenario file

### Changed

- Try and find scenario files in `settings.scenario_path` if they can't be located in the given path
- Add pip upgrade to Dockerfile

### Fixed

- Fixed typo in client class

## [1.0.5] - 2019-04-17

### Added

- `semver` added to headless requirements file

### Fixed

- Fixed handling of client/host version checking before 1.0.4

## [1.0.4] - 2019-04-15

### Added

- Add `VERSION` file and `semver` package
- Emit host version on client connection. Can be used by clients to determine forwards/backwards compatibility.  

## [1.0.3] - 2019-04-08

### Added

- Created `test-scenario.scn` for Turing demo
- Add aircraft type to `send_aircraft_data` method

## [1.0.2] - 2019-03-26

### Added

- Travis CI configuration
- Allow extra wait time for tests when running under CI
- Handle missing scenario file in `stack.py`
- Add `requirements-dev.txt` containing development packages

## [1.0.1] - 2019-02-20

- First tag since forking from upstream - additions and changes are relative to
[this](https://github.com/TUDelft-CNS-ATM/bluesky/commit/cf7de6c5b4f487275759e93720bd6856b04f6bec) commit.

### Added

- Notes on startup process
- Small test scripts to investigate client/server communication
- Utility `get_hexid` method, used to convert the client_id and host_id fields into a human-readable format
- Optional timeout to client connection
- Client tests
- Install script, headless mode, requirements file, Docker support
- CLI argument to connect to remote simulation (temp. fix)
- Pulled in changes from `upstream/master`

### Changed

- Main window title changed to 'RedSky' (mostly a joke, but also useful to quickly see which version of the sim is running) 

[Unreleased]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.4.1...develop
[1.4.1]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.4.0...turing-1.4.1
[1.4.0]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.3.0...turing-1.4.0
[1.3.0]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.2.3...turing-1.3.0
[1.2.3]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.2.2...turing-1.2.3
[1.2.2]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.2.1...turing-1.2.2
[1.2.1]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.2.0...turing-1.2.1
[1.2.0]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.1.1...turing-1.2.0
[1.1.1]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.1.0...turing-1.1.1
[1.1.0]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.0.5...turing-1.1.0
[1.0.5]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.0.4...turing-1.0.5
[1.0.4]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.0.3...turing-1.0.4
[1.0.3]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.0.2...turing-1.0.3
[1.0.2]: https://github.com/alan-turing-institute/bluesky/compare/turing-1.0.1...turing-1.0.2
[1.0.1]: https://github.com/alan-turing-institute/bluesky/releases/tag/turing-1.0.1
