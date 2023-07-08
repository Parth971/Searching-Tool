from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.utils import html

from .models import Survey, PublicSectorLanguage, PublicSectorCountry, PublicSectorBusinessTerritory, InterestedCountry, \
    Turnover, BusinessPercentage, Industry, Category, Sector
from .utils import get_model_object


class GenericListSerializer(serializers.ListSerializer):
    child = serializers.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        for index, value in enumerate(attrs.copy()):
            obj = get_model_object(self.model, query={'name': value})
            if not obj:
                raise ValidationError(f"{value} is not valid value")
            attrs[index] = obj
        return attrs

    def to_internal_value(self, data):
        """
        List of dicts of native values <- List of dicts of primitive datatypes.
        """
        if html.is_html_input(data):
            data = html.parse_html_list(data, default=[])

        if not isinstance(data, list):
            message = "This value should be list"
            raise ValidationError(message)

        if not self.allow_empty and len(data) == 0:
            message = self.error_messages['empty']
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='empty')

        if self.max_length is not None and len(data) > self.max_length:
            message = self.error_messages['max_length'].format(max_length=self.max_length)
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='max_length')

        if self.min_length is not None and len(data) < self.min_length:
            message = self.error_messages['min_length'].format(min_length=self.min_length)
            raise ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: [message]
            }, code='min_length')

        ret = []
        errors = []

        for item in data:
            try:
                validated = self.child.run_validation(item)
            except ValidationError as exc:
                errors.append(exc.detail)
            else:
                ret.append(validated)
                errors.append({})

        if any(errors):
            raise ValidationError(errors)

        return ret


class CreateUpdateUserSurveyDataSerializer(serializers.ModelSerializer):
    country = serializers.CharField(max_length=255, required=False)
    turnover = serializers.CharField(max_length=255, required=False)
    business_percentage = serializers.CharField(max_length=255, required=False)

    public_sector_languages = GenericListSerializer(model=PublicSectorLanguage, required=False)
    public_sector_countries = GenericListSerializer(model=PublicSectorCountry, required=False)
    public_sector_business_territories = GenericListSerializer(model=PublicSectorBusinessTerritory, required=False)

    industry = serializers.CharField(max_length=255, required=False)
    category = serializers.CharField(max_length=255, required=False)
    sector = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Survey
        fields = [
            'country', 'turnover', 'business_percentage', 'public_sector_languages',
            'public_sector_countries', 'public_sector_business_territories',
            'industry', 'category', 'sector'
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not attrs:
            raise ValidationError("Data cannot be empty")

        country = attrs.get('country')
        if country:
            if obj := get_model_object(InterestedCountry, query={'name': country}):
                attrs['country'] = obj
            else:
                raise ValidationError(f"{country} is not valid country")

        turnover = attrs.get('turnover')
        if turnover:
            turnover_value = Turnover.extract_turnover(turnover)
            if turnover_value is None:
                raise ValidationError(f"{turnover} is not valid turnover")

            minimum_turnover, maximum_turnover = turnover_value
            if obj := get_model_object(
                    Turnover,
                    query={
                        'minimum_turnover': minimum_turnover,
                        'maximum_turnover': maximum_turnover
                    }
            ):
                attrs['turnover'] = obj
            else:
                raise ValidationError(f"{turnover} is not valid turnover")

        business_percentage = attrs.get('business_percentage')
        if business_percentage:
            value = BusinessPercentage.extract_value(business_percentage)
            if value is None:
                raise ValidationError(f"{business_percentage} is not valid business_percentage")

            if obj := get_model_object(BusinessPercentage, query={'value': value}):
                attrs['business_percentage'] = obj
            else:
                raise ValidationError(f"{business_percentage} is not valid business_percentage")

        industry = attrs.get('industry')
        if industry:
            if obj := get_model_object(Industry, query={'name': industry}):
                attrs['industry'] = obj
            else:
                raise ValidationError(f"{industry} is not valid industry")

        category = attrs.get('category')
        if category:
            if obj := get_model_object(Category, query={'name': category}):
                attrs['category'] = obj
            else:
                raise ValidationError(f"{category} is not valid category")

        sector = attrs.get('sector')
        if sector:
            if obj := get_model_object(Sector, query={'name': sector}):
                attrs['sector'] = obj
            else:
                raise ValidationError(f"{sector} is not valid sector")

        return attrs

    def create(self, validated_data):
        public_sector_languages = validated_data.pop('public_sector_languages', [])
        public_sector_countries = validated_data.pop('public_sector_countries', [])
        public_sector_business_territories = validated_data.pop('public_sector_business_territories', [])
        user = validated_data['user']
        if user.is_survey_completed:
            survey = user.survey
            for attr, value in validated_data.items():
                setattr(survey, attr, value)
            survey.save()
        else:
            survey = Survey.objects.create(**validated_data)
            user.is_survey_completed = True
            user.save()

        survey.public_sector_languages.set(public_sector_languages)
        survey.public_sector_countries.set(public_sector_countries)
        survey.public_sector_business_territories.set(public_sector_business_territories)

        return survey
