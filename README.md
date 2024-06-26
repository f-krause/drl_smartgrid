# Reinforcement Learning Demo

From a joint effort of Sina Henning, Felix Krause and Johannes Spieß 

Mandatory assignment 1 for Artificial Intelligence for Energy Informatics at University of Oslo (UiO) Autumn 2023.

![project6](https://github.com/f-krause/drl_smartgrid/assets/93521294/1ccc8ca8-ec35-4e84-acfb-184e66414977)

## Setup
### Environment setup

Create new environment "venv"
```shell
python -m venv venv
```

Activate env in bash:
```bash
source venv/bin/activate
```

Install packages in venv
```bash
pip install -r requirements.txt
```

Add virtual environment to kernel
```bash
python -m ipykernel install --user --name=venv
```

### Provide Datasets
**For the demo, there is already all data needed in the data/directory.** 

**For full replication** (and more freedom regarding the energy demand), put the following datasets into a folder "/data" in this repo
* [SolarIrradiance.csv](https://drive.google.com/file/d/1SUjtybPtUzwSEDQoqXbMNijEeDi8QF8m/view)
* [rate_consumption_charge.csv/electricity price](https://drive.google.com/file/d/1uxM9TC401TBwjcdxe3i7TAxSo9tPNWi1/view)
* [WindSpeed.csv](https://drive.google.com/file/d/1X87VRm88-Tp2cs9zjmOB0R6wTxJl8QBf/view)

And put the "BASE" profiles in a folder "/data/residential_load_data_base"
* **[Residential load profiles](https://data.openei.org/files/153/RESIDENTIAL_LOAD_DATA_E_PLUS_OUTPUT.zip)**: Check out data source [here](https://data.openei.org/submissions/153)


## Run training
Open the notebook ["notebooks/RL_smartgrid_demo.ipynb"](notebooks/RL_smartgrid_demo.ipynb) and follow instructions for 
a simple code demonstration.

For advanced replication with more options, open the notebook ["notebooks/1_training.ipynb"](notebooks/1_training.ipynb) 
and follow instructions. This needs the full datasets provided in the "data" folder.


## Analysis of results
Open the notebook ["notebooks/2_result_viz.ipynb"](notebooks/2_result_viz.ipynb).


## Conventions
* The main unit used for energy is kWh
* The used time frame is an hour


## Possible future work
In another iteration, one could try to improve the reward function, e.g.:
- penalizing switching energy sources on that are not optimal (i.e. solar on although there is no solar irradience, e.g. during night)
- including opportunity cost concept: negative reward proportional to "lost" money because a more expensive energy source was used than a cheap alternative (e.g. buying energy from grid although high solar irradience)
