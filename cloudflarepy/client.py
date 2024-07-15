import cloudflarepy.http as http


class Cloudflarepy():
    def __init__(self, api_key: str, email: str):
        self.api_key = api_key
        self.email = email
        self.request = http.CloudflarepyRequest(api_key, email)

    async def login(self):
        return await self.request.Auth()

    async def create_record(self, name: str, content: str, type: str, ttl: int):
        return await self.request.create_record(name, content, type, ttl)