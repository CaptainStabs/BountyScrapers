class JSONOpen:
    def __init__(self, url):
        self.url = url
        self.file = None
        self.session = None

    async def __aenter__(self):
        if self.url.startswith('http') or self.url.startswith('https'):
            self.session = aiohttp.ClientSession()
            async with self.session.get(self.url) as response:
                if response.status == 200:
                    if self.url.endswith('.gz'):
                        self.file = gzip.GzipFile(fileobj=await response.read(), mode=self.mode, *self.args, **self.kwargs)
                    else:
                        self.file = await response.read()
                else:
                    raise Exception(f'Error: {response.status}')
        else:
            if
            self.file = open(self.url, self.mode, *self.args, **self.kwargs)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        if self.file:
            self.file.close()
