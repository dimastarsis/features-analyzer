import aiohttp
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instances[cls]


class ApiHandler(metaclass=Singleton):

    def __init__(self):
        self.session: aiohttp.ClientSession() = None
        self.semaphore = asyncio.Semaphore(10)

    def set_session(self) -> None:
        if not self.session:
            self.session = aiohttp.ClientSession()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5))
    async def get(self, url: str, headers: dict = None) -> str:
        if not self.session:
            raise ConnectionError("Сессия не была открыта")
        async with self.semaphore:
            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()  # eсли 4xx/5xx -> будет повторный запрос
                return await response.text()

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()


API = ApiHandler()
