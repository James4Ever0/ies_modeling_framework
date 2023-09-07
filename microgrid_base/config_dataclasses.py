from pydantic import confloat, Field
from config_utils import EnvBaseModel, Union

class IESEnv(EnvBaseModel):
    VAR_INIT_AS_ZERO:Union[None, str] = None
    # VAR_INIT_AS_ZERO: bool = False
    UNIT_WARNING_AS_ERROR: bool = False
    PERCENT_WARNING_THRESHOLD: confloat(gt=0) = 1
    MOCK_TEST: Union[None, str] = None


class DockerLauncherConfig(IESEnv):
    NO_HALFDONE: bool = Field(
        default=False,
        title="Disable pulling half-done images from Dockerhub and build from ubuntu base image.",
    )
    JUST_BUILD: bool = Field(
        default=False, title="Just build docker image, don't run service."
    )
    TERMINATE_ONLY:bool=Field(default=False, title="Only terminate all running containers and exit.")
    # FORCE_UPDATE: bool = Field(
    #     default=False,
    #     title="Force updating ultimate docker image even if up-to-date (not older than 7 days).",
    # )
    # UPDATE_INTERVAL_IN_DAYS: int = Field(
    #     default=7, title="Update/rebuild image interval in days"
    # )

