from rest_framework.renderers import JSONRenderer
import json


class UserRenderer(JSONRenderer):

    charset = "utf-8"

    def render(self, data, media_type=None, render_context=None):
        errors = '',
        response = json.dumps({"user": data})

        if isinstance(data, list):
            return json.dumps({"users": data})

        errors = data.get('errors', None)

        if errors is not None:
            # As mentioned about, we will let the default JSONRenderer handle
            # rendering errors.
            return super(UserRenderer, self).render(data)

        # Finally, we can render our data under the "user" namespace.
        return response
