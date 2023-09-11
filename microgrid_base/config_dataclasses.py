from pydantic import confloat, Field
from config_utils import EnvBaseModel, Union


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
    MOCK_TEST: Union[None, str] = Field(
        default=None,
        title="If set to an nonempty string, then the server will return mock results.",
    )
    DETERMINISTIC_MOCK: bool = Field(
        default=False, title="If set to True, then the server will return deterministic mock results based on input hash."
    )


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
        default="Ctrl-d,d",
        title="Key sequence to detach from Docker container (not working on Windows)",
    )
    UNITTEST: bool = Field(
        default=False, title="Perform unittest before launching the service"
    )
    # FORCE_UPDATE: bool = Field(
    #     default=False,
    #     title="Force updating ultimate docker image even if up-to-date (not older than 7 days).",
    # )
    # UPDATE_INTERVAL_IN_DAYS: int = Field(
    #     default=7, title="Update/rebuild image interval in days"
    # )
