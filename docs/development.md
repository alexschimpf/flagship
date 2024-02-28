# Development

If you are interested in contributing to this project, please email me at <a href="mailto:aschimpf1@gmail.com">aschimpf1@gmail.com</a>.

<hr>

## Notes

- There are a number of Makefiles with most of the commands you'd need.
- `make help` will give you information about the available Makefile commands
- The `docker` folder's Makefile has various commands for running Flagship
    - `make -c docker dev` will run all necessary containers with auto-reload and debug ports
- If you're planning to contribute, you'll want to run: `make setup-dev`
    - This will install the pre-commit hook and install all necessary packages
- You'll want to use the latest version of node for UI dev
- You'll want to use Python 3.12+ for Admin API and Flags API dev
