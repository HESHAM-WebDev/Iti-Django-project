from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pinterest.models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission


class UserCanDeleteMovie(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Can_Delete').exists():
            return True
        return False

from rest_framework.authentication import TokenAuthentication
#
# Available RESTAPI Permission
# 1- AllowAny
# 2- IsAuthenticated
# 3- IsAdminUser
# 4- IsAuthenticatedReadOnly
# 5-DjangoModelPermissionsOrAnonReadOnly


@api_view(['GET'])
@permission_classes([IsAdminUser])
def hello(request, mykey):
    data = {'message': 'Hell from rest api your key is ->  {}'.format(mykey)}
    if mykey == 'yes':
        return Response(data=data, status=status.HTTP_200_OK)

    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_list(request):
    movies = Movie.objects.all()
    serialized_movies = MovieSerializer(instance=movies, many=True)
    return Response(data=serialized_movies.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_create(request):
    serialized_movies = MovieSerializer(data=request.data)
    if serialized_movies.is_valid():
        serialized_movies.save()
    else:
        return Response(data=serialized_movies.errors, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'message': 'success',
        'data': {'id': serialized_movies.data.get('id')}

    }

    return Response(data=data, status=status.HTTP_201_CREATED)


# @api_view(['GET'])
# def movie_detail(request, pk):
#     movie_obj = Movie.objects.filter(pk=pk)
#     if movie_obj.exists():
#         pass
#     else:
#         return Response(data={'message': 'failed movie doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
#
#     serialized_movies = MovieSerializer(instance=movie_obj)
#
#     return Response(data=serialized_movies.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request, pk):
    response = {}
    movie_obj = Movie.objects.filter(pk=pk)
    if movie_obj.exists():
        movie_obj = movie_obj.first()
        serialized_movie = MovieSerializer(instance=movie_obj)

        response['data'] = serialized_movie.data
        response['status'] = status.HTTP_200_OK
    else:
        response['data'] = {'message': 'failed Movie does not exist'}
        response['status'] = status.HTTP_400_BAD_REQUEST

    return Response(**response)


@api_view(['DELETE'])
@permission_classes([UserCanDeleteMovie])
def movie_delete(request, pk):
    response = {}
    try:
        movie_obj = Movie.objects.get(pk=pk)
        movie_obj.delete()
        response['data'] = {'message': 'Successfully Deleted Movie'}
        response['status'] = status.HTTP_200_OK
    except Exception as e:
        response['data'] = {'message': 'Error While Deleting Movie {}'.format(str(e))}
        response['status'] = status.HTTP_400_BAD_REQUEST

    print("Result -> ", response)

    return Response(**response)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def movie_update(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Exception as e:
       return Response(data={'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='PUT':
        serialized_movies = MovieSerializer(instance=movie, data=request.data)
    elif request.method == 'PATCH':
        serialized_movies = MovieSerializer(instance=movie, data=request.data, partial=True)

    if serialized_movies.is_valid():
        serialized_movies.save()
        return Response(data=serialized_movies.data, status=status.HTTP_200_OK)

    return Response(data=serialized_movies.errors, status=status.HTTP_400_BAD_REQUEST)
