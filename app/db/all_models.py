# Import all models here to ensure they are registered with SQLAlchemy
from app.db.base import Base  # noqa
from app.src.auth.models import User  # noqa
from app.src.contracts.models import Contract  # noqa
from app.src.expenses.models import Expense  # noqa
from app.src.notifications.models import Notification  # noqa
from app.src.payments.models import Payment  # noqa
from app.src.properties.models import Property  # noqa
from app.src.tenants.models import Tenant  # noqa
from app.src.units.models import Unit  # noqa
