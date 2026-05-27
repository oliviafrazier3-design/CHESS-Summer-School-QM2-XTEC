## Create a python environment at lnx201

#### ✅ Step 1: Login to the lnx201
    ssh -Y <username>@lnx201.classe.cornell.edu

#### ✅ Step 2: Start an Interactive Job Session
    qrsh -q interactive.q -l mem_free=200G -pe sge_pe 8 

#### ✅ Step 3: Go to the fife location
        cd /nfs/chess/sw

#### ✅ Step 4: Go to the life location
        python3 -m venv <name of your python env> 
   
    Example: 
        python3 -m venv qm2_BO

#### ✅ Step 5: activate environment
        source /nfs/chess/sw/<name of your python env>/bin/activate 
    
    Example: 
        source /nfs/chess/sw/qm2_BO/bin/activate

#### ✅ Step 6: Install packages
        cd /nfs/chess/sw/<name of your python env>/
        Example
        pip install scikit-learn



## ✅ For jupyternotebook
# Go to the website : https://jupyterhub.classe.cornell.edu

Talk to beamline scientist before selecting the server

# Go to the specific folder
[ss@lnx201 ~]$ cd /nfs/chess/sw/qm2_BO

# Activate the environment
[ss@lnx201 ~]$ source /nfs/chess/sw/qm2_BO/bin/activate

# Check the python environment before moving forward
[ss@lnx201 ~]$ which python

# Install ipykernel if needed
[ss@lnx201 ~]$ pip install ipykernel

# It will create environment in the jupyterhub

[ss@lnx201 ~]$ python -m ipykernel install --user --name=my-python-env --display-name "nxs-analysis-tools"

# Creating link in the jupyterhub folder
[ss@lnx313 ~]$ ln -s /nfs/chess/id4baux/2025-3/sarker-0000-a ~/sarker-0000-a
Install your own python environments and have them added as an option when creating new notebooks.

Install anything you like in the environment, but you MUST at least install ipykernel. For example

        pip install ipykernel

Activate the new environment. If using conda, this would look something like:

        source /nfs/chess/sw/qm2_BO/bin/activate conda activate my-python-env

Add the virtual environment as a jupyter kernel using

        python -m ipykernel install --user --name=my-python-env --display-name "My Python Env"

This adds the kernel to ~/.local/share/jupyter/kernels/ and now it can be used by Jupyter. When you create a new notebook now, “My Python Env” will be one of your choices.

