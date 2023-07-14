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
    - init.sh: for moving `*.lp` files to this directory.
- dsl_parser: iesl parser and code generator
    - functional_base.py: experimental functional exeucution mechanism
    - functional_base.py.j2: for generating functional_base.py.j2
    - generate_code.py: for reading functional_base.py.j2 and generate python code
    - lex_yacc.py: for tokenizing and parsing iesl code (experiment)
    - Makefile: define iesl related build tasks
    - mylang.ies: iesl language specification
    - mylang.txt: legacy language specification
    - pyomo_reduce_ineqalities.py: for calculating variable bounds from a system of ineqality expressions, used by iesl
    - yacc_init.py: experimencal parser
    - your_model_name.lp: experimental model export as lp files which contains Chinese charactors
    - 柴油.ies: diesel power generator model written in iesl language
- frontend_convert_format: convert non-standard frontend data into standard model specification format, used by frontend
    - customToolbar.vue: code used by frontend, which includes logics for input data construction
    - cvt.js: non-standard input format conversion
    - error_cvt.js: error message handling (translation)
    - input_template_processed.json: example input template
    - sample_parse.json: partial cleaned non-standard input data
    - sample.json: raw non-standard input data
- logs: directory reserved for logging
    - .log: need to be touched in order to preserve this directory in release archive `release.7z`
- makefile_ninja_pytest_incremental_test
    - platform_detect_makefile: for detecting different os using makefile
        - Makefile: os detect implementation
    - construct_ninja_file.py: using package "ninja_syntax" to generate ninja.build file
    - dodo.py: experiment of package "pydo"
    - generic.py: python type system experiment
    - lfnf.py: pytest file used for testing pytest "-lfnf" commandline flag
    - Makefile.j2: test jinja template for generating Makefile
    - mytest.py: pytest file using type hints and request fixture
    - test_buffer.py: infinite loop for conda stdout buffer mechanism
    - type_check.py: multiple experiments of python type system
    - typecheck.py: 
    
- Makefile: main makefile for code generation, define build dependencies, handles and share environment variables across submake sessions.