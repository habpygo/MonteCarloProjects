# Monte Carlo Simulation Project 
Initially this project was never intended to become open source until 2016. This folder is a compilation from some of the Python projects I did between 2006 and 2010.
## CLI implementataion - some history
The project was abandoned in 2010, but hopefully some day I will find time to finish it with other interested coders by making it robust and create a proper Web-UI around it. At first I have been tinkering with the possibility to feed the data via a spreadsheet, but I now believe that it should be a web-ui from where the app can pick up the values from a form.

The CLI implementation though has been used to value biotech start-ups and real estate. 

**NOTE:** I don't know whether this implementation still works. Probably not! Also, I don't knwow if there are any files missing. Last time I used it was in 2010. So don't waste too much time on it to get it running. I just put this up on GitHub today for people interested in a Python code sample ... for whatever reason...

Below the rationale why I wrote this.

## Problem - How to value a start-up company?
The one major mistake some people make when trying to value a start-up is utilizing static data. They put in specific estimates for Revenue, fixed costs, variable costs as a % of Revenue, tax etc. into a spreadsheet and obtain a Net Present Value (NPV) or IRR. Although usually some attempt is made by them to cater for various scenario's, i.e. changing start values, growth rates, costs -- called sensitivity analysis-- this is not the correct way to value a start-up. I will not go into the reasons for this, but for those interested I would encourage them to read the excelent book by Yale Professor Anrew Metric, *"Venture Capital and the Finance of Innovation."* 

To cut a long story short, to correctly value a start-up, one should be using a technique called, Monte Carlo Simuation (MCS). In MCS all independent varaibles get assigned a distribution, with a mean and standard deviation (std), from which a value is drawn n times and a calculation is performed to obtain an NPV. The mean of all the n NPVs is the proper value of the start-up company and the standard deviation (std) the risk. From this the conclusion can be drawn that, for example, after 100.000 draws the start-up is worth $(mean of n NPV) with a x%, y% or z% chance that it could be worth the NPV + one, two or three times the std respectively. Vice versa, a probablitiy of company failure could be obtained or with this information the conclusion by the investor or owner of the start-up can be drawn to continue or abondon the project.

The current version of mcsim uses four distributions, i.e. the *normal*, *lognormal*, *triangular* and *uniform* distributions. This is thought to be more than sufficient for financial valuations.

## TODO
Probably start project from scratch (Golang implementation?), write a proper manual/tutorial, and implement some tests.



