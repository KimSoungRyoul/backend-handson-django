from ninja import NinjaAPI

ninja_api = NinjaAPI(
    title="백엔드 개발을 위한 핸즈온 장고 NINJA SAMPLE API 문서",
    description="[한빛 미디어] 백엔드 개발을 위한 핸즈온 장고 실습예제 입니다.",
)


@ninja_api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}
