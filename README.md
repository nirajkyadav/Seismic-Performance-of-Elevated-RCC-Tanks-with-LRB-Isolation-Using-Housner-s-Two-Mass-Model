# Seismic Performance of Elevated RCC Tanks with LRB Isolation Using Housner's Two-Mass Model

## Overview
This repository contains the numerical modeling, simulation scripts, and data analysis framework used to evaluate the seismic performance of elevated reinforced concrete (RC) water tanks under fluid-structure interaction (FSI). The project compares traditional fixed-base configurations with Lead Rubber Bearing (LRB) base-isolated systems using **Housner's two-mass approximation** (convective and impulsive components).

This research was conducted under the supervision of **Dr. Kshitiz C. Shrestha** and presented at the **KtmGeoLab Student Research Symposium (May 2026)**.

## Core Engineering Objectives
* **Fluid-Structure Interaction:** Modeled sloshing effects (convective mass) and structural hydrodynamic coupling (impulsive mass) using Python-based OpenSeesPy workflows.
* **Comparative Evaluation:** Analyzed typical 100kL and 750kL Department of Water Supply and Sewerage Management (DWSSM) standard designs.
* **Nonlinear Analysis:** Performed Nonlinear Pushover Analysis and Nonlinear Time-History Analysis (NLTHA) using ground motions spectrally matched to NBC 105:2020 provisions for Soil Type A.

## Key Findings & Engineering Insights
* **Force Reduction:** LRB base isolation successfully reduced seismic base shear by up to **30%** and overturning moments by up to **65%**.
* **Deformation Capacity:** Increased lateral drift capacity by up to **73%**.
* **Design Implications:** Developed drift-based fragility curves demonstrating that while base isolation allows for optimized, smaller staging elements and shallower foundations, it necessitates larger seismic gap designs and flexible utility/piping connections.

## Tech Stack & Libraries
* **Core Simulation:** `OpenSeesPy`
* **Data Processing & Analysis:** `NumPy`, `SciPy`, `Pandas`, `Opsvis`
* **Visualization:** `Matplotlib`
* **Signal Processing:** `SeismoMatch` / `SeismoSelect` (for ground motion matching)

## Repository Structure
* 100kL, 750kL: OpenSeesPy structural modeling scripts for fixed and isolated water tanks.
* Poster Plots: Generated fragility curves, hysteresis loops, and time-history responses.

## Citation / Contact
* **Primary Researcher:** Niraj Kumar Yadav (078bce094.niraj@pcampus.edu.np)
* **Supervisor:** Dr. Kshitiz C. Shrestha
