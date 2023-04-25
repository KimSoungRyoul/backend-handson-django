from datetime import date
from unittest import TestCase

from study_example_app.models import Company, Department, Employee
from study_example_app.serializers.serializer_structure_analysis import (
    EmployeeWithCustomDepartmentSerializer,
)


class EmployeeWithCustomDepartmentSerializerTest(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(company_number="111-22-33333", name="(주) 해피물산")
        self.department = Department.objects.create(
            name="기술연구소",
            description="사업에 필요한 기술을 연구하고 개발하는 부서입니다.",
        )
        self.employee = Employee.objects.create(
            name="김홍홍", age=27, birth_date=date(1997, 5, 12), company=self.company, department=self.department
        )

    def test_serializer(self):
        request_body = {
            "name": "string",
            "age": 0,
            "company": {
                "id": self.company.id,
            },
            "is_deleted": False,
            "birth_date": "2022-01-02",
            "employment_period": 0,
            "programming_language_skill": ["string"],
            "department": {
                "name": "인적자원부",
                "description": "인재 채용 관리를 담당하는 부서입니다.",
            },
        }

        serializer = EmployeeWithCustomDepartmentSerializer(data=request_body)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.assertTrue(Department.objects.filter(name="인적자원부").exists())
        self.assertEqual(serializer.data["company"]["company_number"], self.company.com)
