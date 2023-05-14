from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

UNIVERSITY_SCHEMA_PARAMETERS = [
    OpenApiParameter(name="a_param", description="QueryParam1 입니다.", required=False, type=str),
    OpenApiParameter(
        name="date_param",
        type=OpenApiTypes.DATE,
        location=OpenApiParameter.QUERY,
        description="Filter by release date",
    ),
]
