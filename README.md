# Measuring the OneWeb Satellite Network

This repository contains the code and dataset of the paper **Measuring the OneWeb Satellite Network** submitted to the *IFIP 2025 Network Traffic Measurement and Analysis Conference (TMA'25)*.

## Prerequisites

To generate the figures and results in the paper, Python and [MATLAB Satellite Communication Toolbox](https://www.mathworks.com/products/satellite-communications.html) is required.

Tested on:

- MATLAB R2024b
- Python 3.13

## Dataset

### Ethical Considerations

In this study, we anonymized the "outside-in" measurements by removing the IP addresses and GPS coordinates that could otherwise be used to associate latency measurements with individual OneWeb user terminals (UTs).
Thus, we refrain from releasing the raw dataset for "outside-in" measurements.

To obtain the pre-processed annomalized dataset, please download the dataset from [Zenodo]().

## Generate Results

We use [Poetry](https://github.com/python-poetry/poetry) to manage the Python dependencies. Please follow the installation guide on the Poetry project to install it before generating the results.

A normal installation process on Debian-based Linux distributions is as follows:

```bash
sudo apt-get update
sudo apt-get install pipx -y
pipx install poetry
```

Ensure `poetry` is installed:

```bash
which poetry
poetry --version
```

Install the dependencies:

```bash
poetry install
eval $(poetry env activate) # On Poetry 2.0 or later
```

Check each individual sub-directory for the related scripts to generate the figures and results in the paper.
