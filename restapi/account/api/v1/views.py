from rest_framework.decorators import  api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer

from rest_framework.decorators import permission_classes

from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([])
def signup(request):
    data = {'data': '', 'status': ''}

    user_serializer = UserSerializer(data=request.data)

    if user_serializer.is_valid():
        user_serializer.save()
        print("user ->", user_serializer.data)

        data['data'] = {
            'user': user_serializer.data,
            'token': Token.objects.get(user__username=user_serializer.data.get('username')).key,
            'message': 'Created'
        }
        data['status'] = status.HTTP_201_CREATED
    else:
        data['data'] = user_serializer.errors
        data['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**data)