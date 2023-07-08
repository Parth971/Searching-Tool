import re

from rest_framework import serializers

from accounts.constants import (
    SPECIAL_SYMBOL_REGEX, PASSWORD_SPECIAL_SYMBOL_ERROR, DIGIT_REGEX, PASSWORD_DIGIT_ERROR, UPPERCASE_LETTER_REGEX,
    PASSWORD_UPPERCASE_LETTER_ERROR, LOWERCASE_LETTER_REGEX, PASSWORD_LOWERCASE_LETTER_ERROR, FIRST_NAME_MINIMUM_LENGTH,
    FIRST_NAME_MAXIMUM_LENGTH, FIRST_NAME_LENGTH_ERROR, USER_NAME_REGEX, FIRST_NAME_ERROR, LAST_NAME_MINIMUM_LENGTH,
    LAST_NAME_MAXIMUM_LENGTH, LAST_NAME_LENGTH_ERROR, LAST_NAME_ERROR, PHONE_NUMBER_REGEX, INVALID_PHONE_NUMBER
)


def validate_password(password):
    if not re.match(SPECIAL_SYMBOL_REGEX, password):
        raise serializers.ValidationError(PASSWORD_SPECIAL_SYMBOL_ERROR)

    if not re.match(DIGIT_REGEX, password):
        raise serializers.ValidationError(PASSWORD_DIGIT_ERROR)

    if not re.match(UPPERCASE_LETTER_REGEX, password):
        raise serializers.ValidationError(PASSWORD_UPPERCASE_LETTER_ERROR)

    if not re.match(LOWERCASE_LETTER_REGEX, password):
        raise serializers.ValidationError(PASSWORD_LOWERCASE_LETTER_ERROR)


def validate_first_name(first_name):
    if not (FIRST_NAME_MINIMUM_LENGTH <= len(first_name) <= FIRST_NAME_MAXIMUM_LENGTH):
        raise serializers.ValidationError(FIRST_NAME_LENGTH_ERROR)

    if not re.match(USER_NAME_REGEX, first_name):
        raise serializers.ValidationError(FIRST_NAME_ERROR)


def validate_last_name(last_name):
    if not (LAST_NAME_MINIMUM_LENGTH <= len(last_name) <= LAST_NAME_MAXIMUM_LENGTH):
        raise serializers.ValidationError(LAST_NAME_LENGTH_ERROR)

    if not re.match(USER_NAME_REGEX, last_name):
        raise serializers.ValidationError(LAST_NAME_ERROR)


def validate_mobile_number(mobile_number):
    if not re.match(PHONE_NUMBER_REGEX, mobile_number):
        raise serializers.ValidationError(INVALID_PHONE_NUMBER)
