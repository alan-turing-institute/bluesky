
# Docker Build

Notes for building and publishing the BlueSky docker image to the `turinginst` DockerHub.

For this example, assume we wish to publish version `turing-1.0.0`, which has been tagged in Git. It may be best to clone a
fresh copy of the repo into a temporary directory to avoid any local changes being included in the image:

```bash
> cd ~/tmp/
> if [ -d bluesky ]; then rm -Rf bluesky ; fi
> git clone git@github.com:alan-turing-institute/bluesky.git
...
> cd bluesky/
> git checkout turing-1.0.0
```

Run our tests to verify:

```bash
> chmod +x ./install.sh
> ./install.sh --headless
> source venv/bin/activate
> pip install -r requirements-dev.txt
> pytest -sv --ignore bluesky/test/tcp/ --ignore bluesky/test/traffic -W ignore::DeprecationWarning
```

Now we can build, tag, and push the Docker image:

```bash
> docker build . --tag turinginst/bluesky:1.0.0 --tag turinginst/bluesky:latest
...
> docker push turinginst/bluesky:1.0.0
> docker push turinginst/bluesky:latest
```

## Notes and TODO

- TODO: This can be setup to run automatically via DockerHub automated builds
