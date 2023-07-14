# Microgrid Algorithm Service

The main objective of this directory is to model an IES system and optimize its operation.

User defines topology, in which devices such as loads, grids, energy sources and generators are.

Inputs and outputs follow a standard format. Modeling language “IESLang” is used to describe the system.

## Roadmap

* [x ] create algorithm service
* [x ] parse input parameters from excel
* [x ] create name mapping table
* [x ] define port types and connectivity matrix
* [x ] generate model code using jinja2 and macros
* [x ] prepare generative tests
* [ ] define and parse `*.ies` DSL

## File Structure

- cplex_convex_debug: test files for debugging cplex solver
    - init.sh: 