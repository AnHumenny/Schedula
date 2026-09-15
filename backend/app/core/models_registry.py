from app.modules.directions.models import Direction                    # noqa: F401
from app.modules.profiles.models import Profile                        # noqa: F401

from app.modules.teachers.models import Teacher                        # noqa: F401
from app.modules.disciplines.models import (                           # noqa: F401
    Discipline,
    teacher_discipline,
)
from app.modules.locations.buildings.models import Building            # noqa: F401

from app.modules.groups.models import Group                            # noqa: F401
from app.modules.locations.rooms.models import Room                    # noqa: F401
from app.modules.users.models import User                              # noqa: F401

from app.modules.schedule.models import (                              # noqa: F401
    ScheduleItem,
    schedule_audience,
    schedule_groups,
)
