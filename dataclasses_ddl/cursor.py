from psycopg2.extras import RealDictCursor


def model_cursor_factory(model_type=None):
    def factory(*args, **kwargs):
        return ModelCursor(model_type, *args, **kwargs)

    return factory


class ModelCursor(RealDictCursor):
    """
    A cursor that allows users to set the model type. Accepted either from constructor or via the attribute.
    """

    def __init__(self, model_type, *args, **kwargs):
        self.model_type = model_type
        super().__init__(*args, **kwargs)

    def fetchone(self):
        res = super().fetchone()
        if not self.model_type:
            raise NotImplementedError("model_type not set")
        return self.model_type(**res)
