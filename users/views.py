from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializers import UserRegisterSerializer


class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
    