from ninja import ModelSchema, FilterSchema
from main.models import Brief

ALL = "__all__"



class BriefSchema(ModelSchema):
    class Meta:
        model = Brief
        fields = ALL