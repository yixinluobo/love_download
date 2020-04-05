from django.contrib.sessions.serializers import JSONSerializer
import json
from django.http.response import DjangoJSONEncoder


class SessionSerializer(JSONSerializer):

    def dumps(self, obj):
        return json.dumps(obj, cls=DjangoJSONEncoder, separators=(',', ':')).encode('latin-1')

    def loads(self, data):
        return json.loads(data.decode('latin-1'))
