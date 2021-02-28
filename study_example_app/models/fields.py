from django.db.models import CharField

from study_example_app.example_source_code.no_django_orm_example import User


class MaskingField(CharField):
    def to_python(self, value):
        # print("to_python: ",value)
        if isinstance(value, str) or value is None:
            return value
        return str(value)
        # return str("********")

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)
#
#
# user_list = list(User.objects.all())
# #
# # first_user_named_kim_ex = [user for user in user_list if user.first_name == "김예제"][0]
# #
# next((user for user in user_list if user.first_name == "김예제"), None)
#
# for user in user_list:  # 3번 로직을 QuerySet이 아닌 python 로직으로 대체
#     if user.first_name == "김예제":
#         first_user_named_kim_ex = user
#         break
