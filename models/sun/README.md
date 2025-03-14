# Python implementation of the SUN saliency model

The original SUN saliency model is implemented in MATLAB.
This is a python implementation of that model.
There are **no guarantees** that this implementation is fully consistent with the original MATLAB version.

## Running the model FastAPI app

  * `devbox shell` (devbox required: https://www.jetify.com/docs/devbox/installing_devbox/)
  * `souce .venv/bin/activate`
  * `pip install -r requirements.txt`
  * `uvicorn main:app --host 0.0.0.0 --port 8080 --reload`


## Running the model by itself

There are hardcoded paths to input and output directories in `SUN_test.py`.

Execute these to run the model:
  * `devbox shell` (devbox required: https://www.jetify.com/docs/devbox/installing_devbox/)
  * `souce .venv/bin/activate`
  * `pip install -r requirements.txt`
  * `cd app/saliency && python SUN_test.py` <= **HARDCODED** IMAGE PATHS IN `SUN_test.py`
