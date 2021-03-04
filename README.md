# VMT
## Introduction

This notebook gives an introduction and overview of the codebase/API involved in the thesis project titled: "High Performance Computing for Evaluating Volume Massing Designs". The codebase is intended to work as a standalone API executable so the reasoning behind this jupyter notebook is to provide a transparent overview of the APIs capabilities. The codebase is supplemented by a thesis report with litterature study and a walkthrough of the engines used in the codebase. Examples of thesis report ready text can be found here:

Week 4 report ready text: https://1drv.ms/b/s!ArT2Rk1rI-5viIZ8DYLSjZLuU3-yng?e=SwQXpJ

Week 5 report ready text: https://1drv.ms/b/s!ArT2Rk1rI-5viIkdBSnb9n6r9rLXmg?e=ZmfKBs

## API structure overview

The main goal of the API is to serve as a tool for conducting volume massing design studies. A volume massing design study is an architectural process of defining the polygon boundaries of a new building within an existing building context, based on building performance simulations. The structure of the API is originally inspired by: https://pure.au.dk/portal/da/publications/building-performance-simulation-supporting-typical-design-activities-the-case-of-volume-massing(1b3a413f-bf5d-4b28-94ab-6e287939f4d9).html

The general structure of the API is as follows:

* Radiation analysis: "How much solar radiation is recieved on all the facades"
* Zone placement: "Based radiation analysis, placement of representative zones"
* Daylight analysis: "For each zone, run an annual daylight simulation"
* Energy analysis: "For each zone, run an annual energy simulation"
