import pyomo
import pyomo.core.base.block as block

# TODO: add support for unicode export "*.lp" files in `solve_model.py``

assert (pyomo_version := pyomo.__version__) == (
    expected_pyomo_version := "6.5.0"
), f"Expected Pyomo version: {expected_pyomo_version}\nActual: {pyomo_version}"


def write(self, filename=None, format=None, solver_capability=None, io_options={}):
    """
    Write the model to a file, with a given format.
    """
    #
    # Guess the format if none is specified
    #
    if (filename is None) and (format is None):
        # Preserving backwards compatibility here.
        # The function used to be defined with format='lp' by
        # default, but this led to confusing behavior when a
        # user did something like 'model.write("f.nl")' and
        # expected guess_format to create an NL file.
        format = block.ProblemFormat.cpxlp
    if filename is not None:
        try:
            _format = block.guess_format(filename)
        except AttributeError:
            # End up here if an ostream is passed to the filename argument
            _format = None
        if format is None:
            if _format is None:
                raise ValueError(
                    "Could not infer file format from file name '%s'.\n"
                    "Either provide a name with a recognized extension "
                    "or specify the format using the 'format' argument." % filename
                )
            else:
                format = _format
        elif format != _format and _format is not None:
            block.logger.warning(
                "Filename '%s' likely does not match specified "
                "file format (%s)" % (filename, format)
            )
    problem_writer = block.WriterFactory(format)
    if problem_writer is None:
        raise ValueError(
            "Cannot write model in format '%s': no model "
            "writer registered for that format" % str(format)
        )

    if solver_capability is None:

        def solver_capability(x):
            return True

    # TODO: fix a bug over io_options
    if "io_options" in io_options.keys():
        io_options = io_options["io_options"]
    (filename, smap) = problem_writer(self, filename, solver_capability, io_options)
    smap_id = id(smap)
    if not hasattr(self, "solutions"):
        # This is a bit of a hack.  The write() method was moved
        # here from PyomoModel to support the solution of arbitrary
        # blocks in a hierarchical model.  However, we cannot import
        # PyomoModel at the beginning of the file due to a circular
        # import.  When we rearchitect the solution writers/solver
        # API, we should revisit this and remove the circular
        # dependency (we only need it here because we store the
        # SymbolMap returned by the writer in the solutions).
        from pyomo.core.base.PyomoModel import ModelSolutions

        self.solutions = ModelSolutions(self)
    self.solutions.add_symbol_map(smap)

    if block.is_debug_set(block.logger):
        block.logger.debug(
            "Writing model '%s' to file '%s' with format %s",
            self.name,
            str(filename),
            str(format),
        )
    return filename, smap_id


from types import MethodType

# to override instance methods.
block._BlockData.write = MethodType(write, block._BlockData)