# m2pi-2023---Awesense
The final results of Team Awesense's 2023 [Math to Power Industry](https://m2pi.ca/) project: [how do Time of Use (ToU) tariffs affect peak electrical usage](https://m2pi.ca/project/2023/awesense/).

## Overview 

We worked with [Awesense's](https://www.awesense.com/) Sandbox Environment (the `awefice` simulated grid "located" in Vancouver). Note that to use this API, you need an Awesense account. You can [contact Awesense to request a demo](https://www.awesense.com/contact/).

Time of Use tariffs are set by utility companies making electricity more expensive at certain times to encourage consumers to spread their usage to different times of day in order to put less stress on the electrical grid and "flatten the curve." 

Here are some resources for further reading:

* [The "duck curve" and daily usage](https://insideenergy.org/2014/10/02/ie-questions-why-is-california-trying-to-behead-the-duck/)
* [US DoE page on demand response](https://www.energy.gov/oe/demand-response)
* [Ontario Energy Board on Time of Use](https://www.oeb.ca/consumer-information-and-protection/electricity-rates)

## The Data and method

In this data, the hourly usage is stored meter-by-meter. 
Because we're looking at the load on the grid as a whole, we aggregate by timestamp. 
In particular, we focus on *residential* meters, as both business and industry consumers are frequently billed differently than residential consumers, and would have different behavior under ToU tariffs.

We consider a weekly shift: that is, that consumers may choose to move some of their usage to different times of day AND different days of the week (eg, choosing to charge their EV in the middle of the night, and choosing to do their laundry on Saturday instead of Wednesday). Although Awesense has hourly EV charger usage data, we don't have appliance level granularity, so for simplicity, we've worked with "shiftable percentages" estimates to account for the fact that some electricity usage must be used at certain times.

#### A side note: Daylight Savings Time

Because we are considering hourly usage over the course of a week, there are two weeks of the year that cause problems: the 167 hour week in March when we "spring forward" and lose an hour and the 169 hour week in November when we "fall back" and gain an hour.

There are several options to deal with this, but we choose the simplest option: we drop the duplicate hour in November and fill the missing hour in March with a 0. 
We acknowledge that this means our work is less accurate, however, given that we're interested in peak usage and that these hours are in neither the summer (air conditioning) nor the winter (heating) use seasons, we feel that this is an acceptable compromise.


## The files

This repository contains

* `mograph.py`: functions for graphing usage so that they're all consistent in both color and layout
* `data_management_functions.py`: functions to manipulate our `pandas` data frames, selecting and aggregating certain data
* `Awesense_ToU_Demo.ipynb`: a model of Time of Use tariffs including choosing peak hours to define the tariff
* `Team1Awesense.pdf`: our M2PI final report with more background and in-depth discussion of the method (to come)