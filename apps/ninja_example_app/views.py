from django.forms import model_to_dict
from ninja import NinjaAPI
from ninja.responses import NinjaJSONEncoder

from aggregate.stores.models import Store

# Create your views here.
NinjaJSONEncoder

ninja_api = NinjaAPI(title="django Ninja API 예시")


@ninja_api.get("/stores")
def store_list_api(request):
    # 상점 목록을 조회하는 코드 개발자가 직접구현
    return 200, list(Store.objects.all())


@ninja_api.get("stores/{pk}")
def store_retrieve_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    store = Store.objects.get(id=pk)
    return 200, model_to_dict(store)


@ninja_api.post("/stores")
def store_create_api(request):
    # 상점을 생성하는 코드 개발자가 직접 구현
    return 200, {"detail": "상점 생성이 완료됐습니다."}


@ninja_api.put("stores/{pk}")
def store_partial_update_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    return 200, {"detail": "상점 일부정보 수정이 완료됐습니다."}


@ninja_api.patch("stores/{pk}")
def store_partial_update_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    return 200, {"detail": "상점정보 수정이 완료됐습니다."}


@ninja_api.delete("stores/{pk}")
def store_partial_update_api(request, pk: int):
    # 상점 정보를 수정하는 코드 개발자가 직접구현
    return 200, {"detail": "상점 삭제가 완료됐습니다."}
