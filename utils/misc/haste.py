import aiohttp
import environs

env = environs.Env()
env.read_env()

async def upload(content: str):
    async with aiohttp.ClientSession() as s:
        token = env.str("HASTEBIN_TOKEN")
        async with s.post(f"https://hst.sh/documents", data=content, headers={ "Authorization": f"Bearer {token}", "Content-Type": "text/plain" }) as resp:
            if not resp.ok:
                return resp.status
            json = await resp.json()
            code = json["key"]
            return f"https://hst.sh/raw/{code}"