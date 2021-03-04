# VMT
Volume Massing Tool

## Introduction

This is an introduction to the codebase/API involved in the thesis project titled: "High Performance Computing for Evaluating Volume Massing Designs". The codebase is intended to work as a standalone API executable. The codebase is supplemented by a thesis report with litterature study and a walkthrough of the engines used in the codebase and their validation work. Examples of thesis report ready text can be found here:

[Week 4 report ready text](https://perkinswillinc-my.sharepoint.com/:b:/g/personal/top_shl_dk/EfJjjpM6rDFItiNq6uQFj8sBO2jztBHUwOrbb-Ry2CcxRQ?e=HuQMz2)


[Week 5 report ready text](https://perkinswillinc-my.sharepoint.com/:b:/g/personal/top_shl_dk/EWFAPr3lD-ROrrbdw8O0_7MBLMSQlsNh_VmRaYMKImmFlg?e=w7Xr9h)


## API structure overview

The main goal of the API is to serve as a tool for conducting volume massing design studies. A volume massing design study is an architectural process of defining the polygon boundaries of a new building within an existing building context, based on building performance simulations. The structure of the API is originally inspired by: https://pure.au.dk/portal/da/publications/building-performance-simulation-supporting-typical-design-activities-the-case-of-volume-massing(1b3a413f-bf5d-4b28-94ab-6e287939f4d9).html

The general structure of the API is as follows:

* Radiation analysis:   "How much solar radiation is recieved on all the facades"
* Zone placement:       "Based radiation analysis, placement of representative zones"
* Daylight analysis:    "For each zone, run an annual daylight simulation"
* Energy analysis:      "For each zone, run an annual energy simulation"


## Innovations

One of the main innovations from this API compared to previous work and other related software packages is the use of GPU based raytracing. Furthermore the API will work out of the box and not require any detailed knowledge about the underlying engines (the API makes justifiable assumptions for you). The API will be CAD agnostic working as an independant executable. Lastly several "experimental" approaches for speeding up computation time is implemented as laid out by the version overview/roadmap below.

## Engines

* [Radiance](https://www.radiance-online.org/)

Validated lighting simulation tool. Using CPU based raytracing.

* [Accelerad](https://nljones.github.io/Accelerad/)

Modelled after Radiance. Using GPU based raytracing.

* [ICEbear](http://www.idbuild.dk/icebear)

Whole building energy simulation. Based on ISO 13790.

* [EnergyPlus](https://energyplus.net/)

Extensive simulation engine, with possibilities for modelling with a high level of detail, at the cost of speed.

## Versioning (roadmap)

This is a development roadmap of the API versions. The reasoning behind developing the API with multiple versions is to be able to narrate the changes in implementation and their effect on speed.

### Version 0.0.0 (Baseline implementation)

Implementation of the conventional approach to volume massing design. The daylight analysis and radiation analysis is based on Radiance. The energy analysis is based on EnergyPlus. That is - all computations are CPU based.

This implementation will serve as a benchmarking baseline in terms of speed for the other versions. Also this implementation will serve a as basis for comparing results.

### Version 0.0.1 

Same as version 0.0.0 except, changing Radiance function calls (CPU based raytracing) to Accelerad function calls (GPU based raytracing).

### Version 0.0.2

Same as version 0.0.1 except, sharing octree and ambient file between daylight calculations for different zones.

### Version 0.0.3

Same as version 0.0.2 except, creating a database of precomputed s-matrices (annual perez all weather model, tregenza discretized sky models). 

### Version 0.0.4

Same as version 0.0.3 except, running matrix multiplication on GPU using CUDA - replacing Radiance dctimestep and rmtxop function calls. Using 1 color channel instead of 3. 

### Version 0.0.5

Same as version 0.0.4 except, keeping output from Accelerad (Optix) rfluxmtx call in GPU memory instead of writing it to disk.

### Version 0.0.6

Same as version 0.0.5 except, displaying result from each ambient bounce in the ambient daylight calculation interatively (progressive raytracing).

### Version 0.0.7

Same as version 0.0.6 except, using ICEbear instead of EnergyPlus. This also entails outputting solar heat gain through the window from Accelerad computations. 

