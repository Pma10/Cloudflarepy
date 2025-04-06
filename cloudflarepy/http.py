import aiohttp
from cloudflarepy.error import Exceptions, CloudflarepyException


class CloudflarepyRequest:
    BASE = "https://api.cloudflare.com/client/v4/"

    def __init__(self, token: str):
        self.token = token
        self.zone_id = None
        self.domain = None

    async def Auth(self, domain: str = None):
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        self.domain = domain

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.BASE + "zones",
                    headers=headers
            ) as response:
                response_json = await response.json()

                if response.status == 200 and response_json.get("success", False):
                    if response_json.get("result") and len(response_json["result"]) > 0:
                        if domain:
                            for zone in response_json["result"]:
                                if zone["name"] == domain:
                                    self.zone_id = zone["id"]
                                    return "성공"
                            raise CloudflarepyException(f"{domain} 도메인을 찾을 수 없습니다")
                        else:
                            self.zone_id = response_json["result"][0]["id"]
                            return "성공"
                    else:
                        raise Exceptions[404]()
                else:
                    if response.status in Exceptions:
                        error_msg = response_json.get("errors", [{"message": "Unknown error"}])[0].get("message", "")
                        raise Exceptions[response.status](f"{error_msg}")
                    else:
                        raise CloudflarepyException(f"알 수 없는 에러 발생: {response.status}")

    async def get_dns_records(self, name: str = None):
        if not self.zone_id:
            raise CloudflarepyException("Auth()를 먼저 해주셔야 합니다.")

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        params = {}

        if name:
            if self.domain and "." not in name:
                full_name = f"{name}.{self.domain}"
            else:
                full_name = name
            params["name"] = full_name

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.BASE + f"zones/{self.zone_id}/dns_records",
                    headers=headers,
                    params=params
            ) as response:
                response_json = await response.json()

                if response.status == 200 and response_json.get("success", False):
                    return response_json.get("result", [])
                else:
                    if response.status in Exceptions:
                        error_msg = response_json.get("errors", [{"message": "Unknown error"}])[0].get("message", "")
                        raise Exceptions[response.status](f"{error_msg}")
                    else:
                        raise CloudflarepyException(f"알 수 없는 에러 발생: {response.status}")

    async def update_record(self, record_id: str, name: str, content: str, type: str, ttl: int, proxy: bool):
        if not self.zone_id:
            raise CloudflarepyException("Auth()를 먼저 해주셔야 합니다.")

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}

        if self.domain and "." not in name:
            full_name = f"{name}.{self.domain}"
        else:
            full_name = name

        async with aiohttp.ClientSession() as session:
            async with session.put(
                    self.BASE + f"zones/{self.zone_id}/dns_records/{record_id}",
                    headers=headers,
                    json={
                        "type": type,
                        "name": full_name,
                        "content": content,
                        "ttl": ttl,
                        "proxied": proxy
                    }
            ) as response:
                response_json = await response.json()

                if response.status == 200 and response_json.get("success", False):
                    return "성공"
                else:
                    if response.status in Exceptions:
                        error_msg = response_json.get("errors", [{"message": "Unknown error"}])[0].get("message", "")
                        raise Exceptions[response.status](f"{error_msg}")
                    else:
                        raise CloudflarepyException(f"알 수 없는 에러 발생: {response.status}")

    async def create_record(self, name: str, content: str, type: str, ttl: int, proxy: bool):
        if not self.zone_id:
            raise CloudflarepyException("Auth()를 먼저 해주셔야 합니다.")

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}

        if self.domain and "." not in name:
            full_name = f"{name}.{self.domain}"
        else:
            full_name = name

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    self.BASE + f"zones/{self.zone_id}/dns_records",
                    headers=headers,
                    json={
                        "type": type,
                        "name": full_name,
                        "content": content,
                        "ttl": ttl,
                        "proxied": proxy
                    }
            ) as response:
                response_json = await response.json()

                if response.status == 200 and response_json.get("success", False):
                    return "성공"
                else:
                    if response.status in Exceptions:
                        error_msg = response_json.get("errors", [{"message": "Unknown error"}])[0].get("message", "")
                        raise Exceptions[response.status](f"{error_msg}")
                    else:
                        raise CloudflarepyException(f"알 수 없는 에러 발생: {response.status}")

    async def create_or_update_record(self, name: str, content: str, type: str, ttl: int, proxy: bool):
        if not self.zone_id:
            raise CloudflarepyException("Auth()를 먼저 해주셔야 합니다.")

        if self.domain and "." not in name:
            full_name = f"{name}.{self.domain}"
        else:
            full_name = name

        existing_records = await self.get_dns_records(name)

        for record in existing_records:
            if record["name"] == full_name and record["type"] == type:
                return await self.update_record(record["id"], name, content, type, ttl, proxy)

        return await self.create_record(name, content, type, ttl, proxy)