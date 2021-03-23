from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import DecimalField
from django.db.models import DurationField
from django.db.models import FloatField
from django.db.models import ForeignKey
from django.db.models import IntegerChoices
from django.db.models import IntegerField
from django.db.models import Model
from django.db.models import TextChoices


class ExampleUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)


class DjangoModel(Model):
    class Alphabet(TextChoices):
        """
        django3.0 에 생긴 기능이다.
        django에서는 python Enum대신 이걸 사용한다 생각하면된다.

        TextChoices, IntegerChoices 두가지 타입을 지원한다.

        변수명 = "실제db에들어가는 값", "라벨값(사람이 읽기 편한 값 ex:한국어)"

        위와 같은 방식으로 선언해주면된다.
        """

        AA = 'aaa', '에이에이'
        BB = 'bb', '비비'

    class JobType(TextChoices):
        DEV = 'developer', '개발자'
        SALES = 'sales', '세일즈'
        HR = 'human resource', '인사'
        MARKETING = 'marketing', '마케팅'
        FINANCIAL = 'financial', '회계'

    class NumberChoices(IntegerChoices):
        ONE = 1, '일'
        TWO = 2, '이'
        THREE = 3, '삼'

    str_field = CharField(
        help_text='주석을 대체하는 Argument다. DB에 영향을 전혀 주지않는다.',
        blank=True,  # 빈문자열 ""을 저장하는 것을 허용할것인가?
        max_length=127,  # 문자열 최대길이
        null=False,  # database에 null 허용여부
        primary_key=False,  # True인 경우 해당 필드를 기본키로 사용 (거의 사용안함)
        unique=False,  # True인 경우 db Unique 제약(Constraint) 생성
        db_index=False,  # True인 경우 db Index 생성
        default='값을 채우지 않으면 이 값을 db을 채운다.',
        choices=Alphabet.choices,
        db_column='str_field',  # Model의 Field 변수명과 db Table의 column명을 다르게 주고싶은경우 이 값을 사용
        validators=(),  # 해당 필드 값의 유효성 검증이 필요한 경우 사용 3장에서 자세히 설명함
        error_messages={  # 해당 필드에 불순한값이 들어온 경우 어떤 에러메시지를 보낼지 여기서 재정의 가능 아래 값들은 django가 제공하는 기본 에러메시지
            'invalid_choice': 'Value %(value)r is not a valid choice.',
            'null': 'This field cannot be null.',
            'blank': 'This field cannot be blank.',
            'unique': '%(model_name)s with this %(field_label)s ' 'already exists.',
        },
    )

    int_field = IntegerField(
        help_text='주석을 대체하는 Argument다. DB에 영향을 전혀 주지않는다.',
        null=False,
        primary_key=False,  # True인 경우 해당 필드를 기본키로 사용 (거의 사용안함)
        unique=False,  # True인 경우 db Unique 제약(Constraint) 생성
        db_index=False,  # True인 경우 db Index 생성
        default=0,  # 값을 채우지 않으면 이 값을 db을 채운다.
        choices=NumberChoices.choices,  # NumberChoices에 정의되지 않는 값을 넣을수없게 제약한다.
        error_messages={'invalid': "'%(value)s' value must be an integer."},
    )
    float_field = FloatField()  # IntegerField와 Argument 포함+ 부동소수점을 사용해서 실수를 저장
    decimal_field = DecimalField(  # IntegerField와 Argument 포함 + 고정소수점을 사용함 DecimalField
        help_text='5(max_digits)개의 자릿수를 저장하고 소숫점2(decimal_places)번째까지 저장 (999.00 ~ 000.00)',
        max_digits=5,
        decimal_places=2,
    )

    bool_field = BooleanField(
        help_text="True False 뿐만 아니라 문자열 't' '1'을 True로 인식하고 'f','0'을 False로 인식한다. ",
        error_messages={
            'invalid': '“%(value)s” value must be either True or False.',
            'invalid_nullable': '“%(value)s” value must be either True, False, or None.',
        },
    )

    date_field = DateField(
        help_text='auto_now가 True이면 해당 모델이 .save()될때 마다 최신날짜로 값을 자동으로 갱신해준다.'
        'auto_now_add가  True이면 해당모델이 .create()되는 최초1회만 날짜값을 최신날짜를 채워준다.'
        '이런 옵션들은 주로 생성날짜, 최근수정날짜를 로깅할때 사용한다.',
        auto_now=True,
        # auto_now_add=True,
        error_messages={
            'invalid': '“%(value)s” value has an invalid format. It must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.',
            'invalid_date': '“%(value)s” value has the correct format (YYYY-MM-DD) but it is an invalid date.',
        },
    )
    datetime_field = DateTimeField(  # date_field와 동일
        error_messages={
            # date_field와 동일하며 아래 한개가 더 추가됨
            'invalid_datetime': '“%(value)s” value has the correct format (YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]) but it is an invalid date/time.',
        },
    )
    duration_field = DurationField(
        help_text='python의 timedelta(days=3)를 저장할 수 있다.',
        error_messages={
            'invalid': '“%(value)s” value has an invalid format. It must be in [DD] [[HH:]MM:]ss[.uuuuuu] format.',
        },
    )
    # https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-types 더 다양한 장고의 필드들을 보고싶다면 공식문서 참고
