import sys
sys.path.append('../')
from System_formulations.two_harvesters_coop_noise import fish_game
from rhodium import * 
#from j3 import J3

model = Model(fish_game)

model.parameters = [Parameter("vars"),
                    Parameter("a"),
                    Parameter("b"),
                    Parameter("c"),
                    Parameter("d"),
                    Parameter("h"),
                    Parameter("K"),
                    Parameter("m"),
                    Parameter("sigmaX"),
                    Parameter("sigmaY")]

model.responses = [Response("NPV_a", Response.MAXIMIZE),
                   Response("NPV_b", Response.MAXIMIZE),
                   Response("PreyDeficit", Response.MINIMIZE),
#                   Response("ConsLowHarvest", Response.MINIMIZE),
#                   Response("WorstHarvest", Response.MAXIMIZE),
                   Response("PredatorExtinction", Response.MINIMIZE)]

model.constraints = []#Constraint("PredatorExtinction < 1")]

model.uncertainties = [UniformUncertainty("a", 0.002, 2),
                       UniformUncertainty("b", 0.005, 1),
                       UniformUncertainty("c", 0.2, 1),
                       UniformUncertainty("d", 0.05, 0.2),
                       UniformUncertainty("h", 0.001, 1),
                       UniformUncertainty("K", 100, 5000),
                       UniformUncertainty("m", 0.1, 1.5),
                       UniformUncertainty("sigmaX", 0.001, 0.01),
                       UniformUncertainty("sigmay", 0.001, 0.01)]

model.levers = [RealLever("vars", 0.0, 1.0, length = 8)]

output = optimize(model, "NSGAII", 700)

fig = parallel_coordinates(model, output, colormap="Blues", c= "NPV_a", target="top")
#
#J3(output.as_dataframe(list(model.responses.keys())))
#
#SOWs = sample_lhs(model, 1000)
#policy = output.find_max("NPV_a")
#results = evaluate(model, update(SOWs, policy))
##
#result = sa(model, "NPV", policy=policy, method="sobol", nsamples=1000)
#
#classification = results.apply("'Survival' if PredatorExtinction < 1 else 'Extinction'")
#p = Prim(results, classification, include=model.uncertainties.keys(), coi="Survival")
#box = p.find_box()
#fig = box.show_tradeoff()
#
#c = Cart(results, classification, include=model.uncertainties.keys(), min_samples_leaf=50)
#c.show_tree()