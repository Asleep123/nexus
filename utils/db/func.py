from prisma.errors import PrismaError
from .register import db
from .classes import Guild, User
import datetime
from typing import Union

class Guilds:

    async def create(self, id: int, channelId: int = None, webhook: str = None) -> Guild | PrismaError:
        _resp = await Guild.prisma().create(
            data={
                "channelId": channelId,
                "guildId": id,
                "webhook": webhook
            }
        )
        return _resp
    
    async def update(self, guildId: int, channelId: int = None, webhook: str = None, locked: bool = None, linkedOn: datetime.datetime = None) -> Guild | PrismaError:
        _find = await Guild.prisma().find_unique(
            where={
                "guildId": guildId
            }
        )
        if channelId is None:
            channelId = _find.channelId
        elif webhook is None:
            webhook = _find.webhook
        elif locked is None:
            locked = _find.locked
        elif linkedOn is None:
            linkedOn = _find.linkedOn

        _resp = await Guild.prisma().update(
            where={
                "guildId": guildId
            },
            data={
                "channelId": channelId,
                "webhook": webhook,
                "locked": locked,
                "linkedOn": linkedOn
            }
        )
        return _resp

    async def suspend(self, guildId: int = None, userId: int = None, ends: datetime.datetime, reason: str = None, type: Union["user", "guild"]) -> Guild | PrismaError:
        if type == "guild":
            _resp = await Guild.prisma().update(
                where={
                    "guildId": guildId
                },
                data={
                    "suspended": True,
                    "suspensions": {
                        "create": [
                            {
                                "endsOn": ends,
                                "reason": reason
                            }
                        ]
                    }
                }
            )
        elif type == "user":
            _resp = await User.prisma().update(
                where={
                    "userId": userId
                },
                data={
                    "suspended": True,
                    "suspensions": {
                        "create": [
                            {
                                "endsOn": ends,
                                "reason": reason
                            }
                        ]
                    }
                }
            )
        return _resp