from django.db import models


def cleanData(model: models, data: dict):
    # print(data)
    model_fields = model._meta.get_fields()
    print(model_fields)
    cleaned_fields = [field.verbose_name for field in model_fields]
    print(cleaned_fields)
    cleaned_data = {field: data[field] for field in cleaned_fields}
    print(cleaned_data)
    return cleaned_data
