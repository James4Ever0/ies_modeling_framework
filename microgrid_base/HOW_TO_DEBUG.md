# Debugging MILP Models

## Configuration

You can configure the program in the following ways:

1. Setting environmental variables with corresponding name
2. Pass configuration as commandline options (the syntax is different, so use `--help` to learn it first)
3. Write configuration in an dotenv formatted file and pass the path of that file into either as environment variable or commandline option

## Debugging Preference

Small models are always preferred since they are fast and concise. If one big model is troublesome and hard to analyze, you can either reduce the iteration size or submodel count.

## Modeling Preference

When you want to model some logical non-linearities (like disjunctions), the GDP method (`pyomo.gdp`) is always preferred over manual Big-M definitions. This can minimize error, ensure clarity and reduce cognitive loads.

## Error Tracking

To learn more about error logs, we need to create a mapping between the line number, the file name and the variables being defined. Once the variable/constraint name is found in the error log, we can reference the source and learn more abount the cause of the error.

We can categorize and sort errors by importance (like violation degree) and relevance.

### Infeasibility or Unbounded variables

To know more of the cause of the error, we need to set the objective function to a constant, so if in this way the model is still not valid, it must be infeasible, or having contradictive constraints.

To use this feature, set `INFEASIBILITY_DIAGNOSTIC=True` in configuration.

### Feasopt

When the model is hard to reduce, and must be analyzed in detail, we can use the `feasopt` option to find the violated constraints.

Feasopt is part of the failsafe protocols. Set `FAILSAFE=True` in configuration to enable it.

More options like `FEASOPT_TIMELIMIT` can be found as constants in file `failsafe_utils.py`.

In case you may want more specific relaxation targets than all constraints, you can tweak the adders, device count bounds and more.

One common routine is that first relax all adder constraints and add the sum of all adder errors into target, then locate the error, create isolated models which enforce error must be fulfilled and relax constraints like device count bounds, also we can locate the conflicting code location within the device model.
