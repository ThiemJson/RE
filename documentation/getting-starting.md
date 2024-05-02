Some notes, because we keep on struggling to get treqs to run locally. 

# Try out if your system already works

Run 

        pip install -e .

If there is no error, run 'treqs'.

If there is still no error, enjoy .

# If it does not...

## Perhaps you have done all the steps below previously...

Then, load the virtual environment for treqs and start using it:

        source treqs_env/bin/activate

On my machine, that folder is just next to the git repository... if you want to stop using the treqs_env, deactivate it by typing:

        deactivate

## Create the virtual python environment

If you do not have the treqs_env as described above, the following should work:

        python3 -m venv treqs_env
        source treqs_env/bin/activate

If not, continue reading...

## Do you have the correct python installed?

Run 

        python --version

If it starts with a 2, you may need to install python3. Try:

        python3 --version

## Is there a problem with Sphinx?

Then, likely the setup is a bit shady. Consider reading:
https://stackoverflow.com/questions/43694823/python-no-module-named-sphinx-error

> pyenv might not really be needed, I guess. We appear to be using venv instead!!!

In a nutshell: Get a virtual environment setup to install treqs and all dependencies into. Go to 
https://github.com/pyenv/pyenv

and install/configure pyenv. 

### Now, create a virtual environment

https://packaging.python.org/tutorials/installing-packages/#requirements-for-installing-packages

Is venv installed? Where to put those folders? What are the exact commands to execute?

> I think venv is part of python3. No need to install pyenv as described above.


