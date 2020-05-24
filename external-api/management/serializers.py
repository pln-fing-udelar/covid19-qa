from rest_framework import serializers


class ESQueryConfSerializer(serializers.Serializer):
    boost = serializers.IntegerField()
    minimum_should_match = serializers.IntegerField(allow_null=True, required=False)
    operator = serializers.ChoiceField(choices=['and', 'or'])
    fuzziness = serializers.IntegerField()
