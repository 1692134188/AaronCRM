from KingAdmin import sites
from KingAdmin.sites import site
from KingAdmin.admin_base import BaseKingAdmin
from Student import models


site.register(models.Test)
