import aiohttp
import typing, pydantic
from error import Exceptions


class CloudflarepyRequest:
    BASE = "https://api.cloudflare.com/client/v4/"

    def __init__(
            self,
            token: str,
            email: str
    ):
        self.token = token
        self.email = email
        self.zone_id = None

    async def Auth(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.BASE + "zones",
                headers={
                    "Content-Type": "application/json",
                    "X-Auth-Email": self.email,
                    "X-Auth-Key": self.token
                }
            ) as response:
                if response.status == 200:
                    response = await response.json()
                    self.zone_id =  response["result"]["id"]
                    return "성공"
                else:
                    return Exceptions(response.status)

    async def create_record(
        self,
        name : str,
        content: str,
        type : str,
        ttl: int
    ):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.BASE + f"zones/{self.zone_id}/dns_records",
                headers={
                    "Content-Type": "application/json",
                    "X-Auth-Email": self.email,
                    "X-Auth-Key": self.token
                },
                json={
                    "type": type,
                    "name": name,
                    "content": content,
                    "ttl": ttl
                }
            ) as response:
                if response.status == 200:
                    return "성공"
                else:
                    return Exceptions(response.status)