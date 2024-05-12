#!/usr/bin/env python3

import numpy as np
import skfuzzy as skf
from MFIS_Classes import FuzzySetsDict, FuzzySet, RuleList, Rule, Application
from MFIS_Read_Functions import readFuzzySetsFile, readRulesFile, readApplicationsFile

# Step 1: Load Fuzzy Sets and Rules
fuzzySetsDict = readFuzzySetsFile('InputVarSets.txt')
riskSetsDict = readFuzzySetsFile('Risks.txt')
fuzzySetsDict.update(riskSetsDict)
rules = readRulesFile()

# Print fuzzy sets for debugging
print("Loaded fuzzy sets:")
fuzzySetsDict.printFuzzySetsDict()

# Step 2: Load Applications
applications = readApplicationsFile()

def fuzzify(application, fuzzySetsDict):
    """
    Fuzzify the input values of an application.
    """
    for var, value in application.data:
        for fuzzySet in fuzzySetsDict.values():
            if fuzzySet.var == var:
                fuzzySet.memDegree = skf.interp_membership(fuzzySet.x, fuzzySet.y, value)

def apply_rules(rules, fuzzySetsDict):
    """
    Apply the rules to the fuzzy sets to infer the risk level.
    """
    for rule in rules:
        min_strength = min([fuzzySetsDict[antecedent].memDegree for antecedent in rule.antecedent])
        rule.strength = min_strength
        if rule.consequent in fuzzySetsDict:
            fuzzySetsDict[rule.consequent].memDegree = max(fuzzySetsDict[rule.consequent].memDegree, min_strength)

def defuzzify(fuzzySetsDict):
    """
    Defuzzify the output fuzzy set to get a crisp value.
    """
    # Debugging: Print 'risk' fuzzy set details
    print("Defuzzifying 'risk' fuzzy set")
    combined_x = None
    combined_y = None
    for label in ['Risk=LowR', 'Risk=MediumR', 'Risk=HighR']:
        if label in fuzzySetsDict:
            fs = fuzzySetsDict[label]
            if combined_x is None:
                combined_x = np.linspace(fs.x[0], fs.x[-1], 1000)
                combined_y = np.zeros_like(combined_x)
            fs_y_interp = skf.interp_membership(fs.x, fs.y, combined_x)
            combined_y = np.fmax(combined_y, fs_y_interp)
    if combined_x is not None and combined_y is not None:
        return skf.defuzz(combined_x, combined_y, 'centroid')
    else:
        raise ValueError("Risk fuzzy sets not defined in fuzzySetsDict")

def process_applications(applications, fuzzySetsDict, rules):
    results = []
    for application in applications:
        # Reset membership degrees before processing each application
        for fuzzySet in fuzzySetsDict.values():
            fuzzySet.memDegree = 0
        fuzzify(application, fuzzySetsDict)
        apply_rules(rules, fuzzySetsDict)
        risk = defuzzify(fuzzySetsDict)
        results.append((application.appId, risk))
    return results

# Process applications and output results
results = process_applications(applications, fuzzySetsDict, rules)

with open('Results.txt', 'w') as outputFile:
    for appId, risk in results:
        outputFile.write(f"{appId}, {risk}\n")
