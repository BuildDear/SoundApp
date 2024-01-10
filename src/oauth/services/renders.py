import json
from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # If we get the 'token' key as part of the response, it might be a bytes object.
        # Bytes objects don't serialize well, so we need to decode them before rendering the User object.
        token = data.get('token', None)

        if token is not None and isinstance(token, bytes):
            # As mentioned above, decode the token if it's of type bytes.
            data['token'] = token.decode('utf-8')

        # Finally, we can map our data into the 'user' namespace.
        return json.dumps({
            'user': data
        })
