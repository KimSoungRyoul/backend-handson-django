from rest_framework.fields import CharField


class MaskingDRFField(CharField):
    def to_internal_value(self, data):
        # We're lenient with allowing basic numerics to be coerced into strings,
        # but other types should fail. Eg. unclear if booleans should represent as `true` or `True`,
        # and composites such as lists are likely user error.
        if isinstance(data, bool) or not isinstance(
            data,
            (
                str,
                int,
                float,
            ),
        ):
            self.fail("invalid")
        value = str(data)
        return value.strip() if self.trim_whitespace else value

    def to_representation(self, value):
        print("to_representation: ", value)
        return "*****"
        # return str(value)
