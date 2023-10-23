from log_utils import logger_print

from pydantic import confloat, Field  # , validator, ValidationError
from config_utils import EnvBaseModel, Union
from typing import Literal, Optional


class IESEnv(EnvBaseModel):
    """
    IES algorithm program configurations.
    """

    VAR_INIT_AS_ZERO: Union[None, str] = Field(
        default=None,
        title="If set to an nonempty string, then all variables will be initialized as zero, otherwise left uninitialized.",
    )
    UNIT_WARNING_AS_ERROR: bool = Field(
        default=False,
        title="Treat unit related warnings as errors, such as percentage related warnings.",
    )
    PERCENT_WARNING_THRESHOLD: confloat(gt=0) = Field(
        default=1,
        title="Emit warnings when any percentage values is less than given value.",
    )
    STATIC_MOCK: Union[None, str] = Field(
        default=None,
        title="If set to an nonempty string, then the server will return static mock results.",
    )
    GENERATED_MOCK: bool = Field(
        default=False,
        title="If set to True, the server will generate mock results by analyzing the input parameters (if MOCK_TEST is False))",
    )
    DETERMINISTIC_MOCK: bool = Field(
        default=False,
        title="If set to True, then the server will return deterministic synthetic mock results based on input hash.",
    )

    MOCK_DATA_THRESHOLD: float = Field(
        default=0.001,
        title="Threshold for mock data manipulation, under which will not change.",
    )
    ANSWER_TO_THE_UNIVERSE: int = Field(
        default=42,
        title="Answer to the universe (value related to randomness restoration)",
    )

    FAILSAFE: bool = Field(
        default=False,
        title="Enable failsafe mode, which guarantees that task output will be generated in any condition.",
    )

    DETERMINISTIC_FAILSAFE: bool = Field(
        default=False, title="Ensure determinism in failsafe mode."
    )

    INFEASIBILITY_DIAGNOSTIC: bool = Field(
        default=False,
        title="Enable infeasibility diagnostic mode, which will perform various tests to detect and analyze infeasibility, before and after accessing the solver.",
    )

    DYNAMIC_TYPE_VERIFICATION: bool = Field(
        default=False,
        # default = True,
        title="Enable dynamic type verification on topology.",
    )

    ADDER_ERROR_COMPENSATION: Literal[
        "none", "positive", "negative", "combined"
    ] = Field(
        default="none",
        title="Mode for adder error compensation, 'none' for no compensation, 'positive' for too much input, 'negative' for too little input, and 'combined' for both.",
    )

    IGNORE_ANCHOR_EXCEPTIONS: bool = Field(
        default=True, title="Ignore exceptions raised by anchors in topology checks."
    )

    ADDER_ERROR_WEIGHT: float = Field(
        default=1e9, 
        # default=1e20, 
        # default=1e7, 
        title="Weight of adder error in objective passed to solver."
    )

    PROLOG_STACK_LIMIT:Optional[int] = Field(default=None, title = 'Prolog stack limit in gigabytes.')

    # @validator("MOCKGEN")
    # def validate_mockgen(cls, values, v):
    #     mock_test = values.get("MOCK_TEST", None)
    #     if v is True:
    #         if mock_test is None:
    #             raise ValidationError(
    #                 "MOCKGEN shall not be set to True if MOCK_TEST is not set."
    #             )


class DockerLauncherConfig(IESEnv):
    """
    IES Docker launcher configurations.

    Also parse algorithm related configs.
    """

    NO_HALFDONE: bool = Field(
        default=False,
        title="Disable pulling half-done images from Dockerhub and build from ubuntu base image.",
    )
    JUST_BUILD: bool = Field(
        default=False, title="Just build docker image, don't run service."
    )
    TERMINATE_ONLY: bool = Field(
        default=False, title="Only terminate all running containers and exit."
    )
    DETACH_KEYS: str = Field(
        default="ctrl-d,d",
        title="Key sequence to detach from Docker container (not working on Windows)",
    )
    UNITTEST: bool = Field(
        default=False, title="Perform unittest before launching the service"
    )
    FINAL_IMAGE_TAG: str = Field(
        default="latest",
        title='Tag name(setting anything other than "latest" will skip image building and run final image with that tag instead)',
    )
    # FORCE_UPDATE: bool = Field(
    #     default=False,
    #     title="Force updating ultimate docker image even if up-to-date (not older than 7 days).",
    # )
    # UPDATE_INTERVAL_IN_DAYS: int = Field(
    #     default=7, title="Update/rebuild image interval in days"
    # )
