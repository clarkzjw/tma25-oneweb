![](https://img.shields.io/badge/TMA'25-Paper-blue)

[Author version PDF](https://pan.uvic.ca/~clarkzjw/tma25.pdf)

**Note**: This repository is currently working in progress. The complete dataset will be uploaded to Zenodo very soon.

# Measuring the OneWeb Satellite Network

This repository contains the code and dataset of the paper **Measuring the OneWeb Satellite Network** accepted in the *IFIP 2025 Network Traffic Measurement and Analysis Conference (TMA'25)*.

## 📖 Abstract

OneWeb, the second largest low-Earth-orbit (LEO) satellite constellation, predominantly serves enterprise and government markets, presenting challenges for researchers trying to assess its network performance in practical scenarios. Consequently, the research community lacks a comprehensive understanding of the OneWeb system beyond the constellation parameters detailed in its regulatory filings and constrained simulation-based analysis. In this paper, we conduct a comprehensive network measurement study of the OneWeb satellite network, using both "inside-out" measurements for controlled user terminals (UTs) and "outside-in" measurements targeting publicly accessible UTs on the Internet. We present real-world measurements of the antenna signal-to-interference-and-noise-ratio (SINR), network latency, and throughput performance of different transport layer protocols and congestion control algorithms. Additionally, we utilize UT antenna tracking logs of connected satellites for cross-layer analysis. Our findings indicate that, while OneWeb generally fulfills its throughput service-level agreement (SLA) for enterprise and government customers, its latency performance is profoundly impacted by its constellation design. While latency remains relatively stable with minimal fluctuations during most inter-beam and inter-satellite handovers, notable latency variations occur during satellite network portal (SNP) handover events in certain geographical areas. This issue is partly due to the absence of inter-satellite links (ISLs), which presents a significant obstacle to OneWeb’s pursuit of seamless global coverage and robust network resilience.

## 💾 Dataset

### Ethical Considerations

In this study, we anonymized the "outside-in" measurements by removing the IP addresses and GPS coordinates that could otherwise be used to associate latency measurements with individual OneWeb user terminals (UTs).
Thus, we refrain from releasing the raw dataset for "outside-in" measurements.

To obtain the pre-processed annomalized dataset, please download the dataset from [Zenodo]() (**To be uploaded**).

## 📊 Reproducibility

### Prerequisites

To generate the figures and results in the paper, Python and [MATLAB Satellite Communication Toolbox](https://www.mathworks.com/products/satellite-communications.html) is required.

Tested on:

- MATLAB R2024b
- Python 3.13

### Generate Results

We use [Poetry](https://github.com/python-poetry/poetry) to manage Python dependencies. Please follow the installation guide on the Poetry project to install it before generating the results.

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
