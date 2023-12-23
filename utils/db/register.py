from prisma import Prisma
from prisma import register


db = Prisma()
register(db)