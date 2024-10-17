from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from pydantic import EmailStr, Field, StringConstraints

ConstrainedStr = Annotated[str, StringConstraints(strip_whitespace=True)]
ConstrainedEmailStr = Annotated[EmailStr, StringConstraints(strip_whitespace=True)]
ConstrainedDec = Annotated[Decimal, Field(decimal_places=2, gt=0)]
TimeStamp = datetime.now(tz=UTC)
TimeStamp.strftime("%Y-%m-%d")
