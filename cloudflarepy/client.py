import cloudflarepy.http as http


class Cloudflarepy():
    def __init__(self, api_key: str, domain: str = None):
        self.api_key = api_key
        self.domain = domain
        self.request = http.CloudflarepyRequest(api_key)

    async def login(self):
        return await self.request.Auth(self.domain)

    async def create_record(self, name: str, content: str, type: str, ttl: int):
        return await self.request.create_record(name, content, type, ttl)

    async def update_record(self, record_id: str, name: str, content: str, type: str, ttl: int):
        return await self.request.update_record(record_id, name, content, type, ttl)

    async def get_dns_records(self, name: str = None):
        return await self.request.get_dns_records(name)

    async def create_or_update_record(self, name: str, content: str, type: str, ttl: int, proxy: bool = False):
        return await self.request.create_or_update_record(name, content, type, ttl, proxy)