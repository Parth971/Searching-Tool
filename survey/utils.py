

def get_model_object(model_class, query):
    return model_class.objects.filter(**query).first()
