import pytz
from enum import IntEnum
from typing import Annotated
from pydantic import Field
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

HEX_COLOR_PATTERN = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
DISCORDCHANNELNAME_PATTERN = r"^[a-z0-9-]{1,100}$"
HANDLE_PATTERN = r"^[a-zA-Z0-9\-]+$"

Handle = Annotated[str, Field(pattern=HANDLE_PATTERN, max_length=24)]
HexColor = Annotated[str, Field(pattern=HEX_COLOR_PATTERN)]
# we'll need to store snowflakeid as TEXT into sqlite
UnixTimestamp = Annotated[int, Field(strict=True, gt=0)]
SnowflakeId = Annotated[int, Field(strict=True, gt=0, lt=2**64 - 1)]
DiscordChannelName: str = Field(..., pattern=r"^[a-z0-9-]{1,100}$")
DiscordRoleId = SnowflakeId
DiscordUserId = SnowflakeId
DiscordCategoryId = SnowflakeId
DiscordChannelId = SnowflakeId

class User_Level(IntEnum):
    Superadmin = 0
    Full = 10
    Trusted = 20
    Public = 99

    def __str__(self):
        return self.name

class Competition_Type(IntEnum):
    Men = 0
    Women = 1

    def __str__(self):
        return self.name

class Match_Status(IntEnum):
    Pending = 0     # Match in scheduled but not yet reached match's hours_before_kickoff
    Ready = 1       # We reached match's hours_before_kickoff, channel should be created
    Active = 2      # Match in progress
    Completed = 3   # Match reached match's hours_after_kickoff, time to cleanup

    def __str__(self):
        return self.name

class TimeZone:
    def __init__(self, tz: str):
        if not self.validate_timezone(tz):
            raise ValueError(f"Invalid time zone: {tz}")
        self.tz = tz

    def __str__(self):
        return self.tz

    def validate_timezone(self, tz: str) -> bool:
        return tz in pytz.all_timezones

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        def validate(value: str) -> "TimeZone":
            return cls(value)
        return core_schema.no_info_plain_validator_function(validate)
