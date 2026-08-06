from litestar import Controller, get


class SystemController(Controller):
    tags = ["system"]

    @get("/health", include_in_schema=False)
    async def health(self) -> dict[str, str]:
        return {"status": "ok"}
