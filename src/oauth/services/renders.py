import json
from rest_framework.renderers import JSONRenderer

from src.oauth.services.google import log_function_call


class UserJSONRenderer(JSONRenderer):
    charset = "utf-8"

    @log_function_call
    def render(self, data, media_type=None, renderer_context=None):
        # Check if the view returns an error
        errors = data.get("errors", None)

        # Check for token byte object and decode if present
        token = data.get("token", None)
        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data["token"] = token.decode("utf-8")

        # Render data under 'user' namespace
        return json.dumps({"user": data})
