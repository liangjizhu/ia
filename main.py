from MFIS_Read_Functions import *


def evaluate_application(application, fuzzy_sets, rules):
    """Evaluates an application using fuzzy sets and rules."""
    results = []
    for rule in rules:
        rule_strength = 1.0

        # Calculate the strength of each rule by checking the membership degrees
        for condition in rule.antecedent:
            if condition in fuzzy_sets:
                # Find corresponding fuzzy set for this condition
                fuzzy_set = fuzzy_sets[condition]
                # Find the application data corresponding to this variable
                for var, value in application.data:
                    if var == fuzzy_set.var:
                        # Compute membership degree for the given value
                        idx = min(range(len(fuzzy_set.x)),
                                  key=lambda i: abs(
                                      fuzzy_set.x[i] - value))
                        fuzzy_set.memDegree = fuzzy_set.y[idx]
                        rule_strength = min(rule_strength,
                                            fuzzy_set.memDegree)
                        break

        # Store the rule strength as the membership degree of the consequent
        results.append((rule.consequent, rule_strength))

    # Aggregate results to produce the final risk level
    final_risk = sum([strength for _, strength in results]) / len(results)
    return final_risk


# Load the fuzzy sets, rules, and applications from respective files
fuzzy_sets_file = 'InputVarSets.txt'
fuzzy_sets = readFuzzySetsFile(fuzzy_sets_file)

rules = readRulesFile()
applications = readApplicationsFile()

# Process each application and calculate their risk levels
results = {}
for app in applications:g
    results[app.appId] = evaluate_application(app, fuzzy_sets, rules)

# Print the results or save them to Results.txt
with open('Results.txt', 'w') as result_file:
    for app_id, risk in results.items():
        result_file.write(f"{app_id}: {risk:.2f}\n")
        print(f"Application {app_id}: Risk Level = {risk:.2f}")