from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Movie, UserCreationFormEdit, MovieSerializer, UserSerializer, GroupSerializer
from .forms import MovieForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins, generics

# Create your views here.


@login_required
@permission_required(["movie.add_movie", "movie.view_movie", ])
def index(request):
    get_movies = Movie.objects.all()
    return render(request, "movie/index.html", {
        "movies": get_movies,
    })


@login_required
@permission_required(["movie.view_movie", ])
def show(request, id):
    get_movie = Movie.objects.get(pk=id)
    return render(request, "movie/show.html", {
        "movies": get_movie,
    })


@login_required
@permission_required(["movie.add_movie", "movie.view_movie", ])
def create(request):
    form = MovieForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("index")
    return render(request, "movie/create.html", {
        "form": form,
    })


@login_required
@permission_required(["movie.change_movie", "movie.view_movie", ])
def update(request, id):
    get_movie = Movie.objects.get(pk=id)
    form = MovieForm(request.POST or None, request.FILES or None, instance=get_movie)
    if form.is_valid():
        form.save()
        return redirect("index")
    return render(request, "movie/edit.html", {
        "form": form,
        "movie": get_movie,
    })


@login_required
@permission_required(["movie.delete_movie", "movie.view_movie", ])
def delete(request, id):
    get_movie = Movie.objects.get(pk=id)
    get_movie.delete()
    return redirect("index")


def signup(request):
    form = UserCreationFormEdit(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
    return render(request, "registration/signup.html", {
        "form": form,
    })


def simple_middleware(get_response):
    # One-time configuration and initialization.
    print("hello from middleware")

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # content_type = ContentType.objects.get_for_model(Movie)
        # permission = Permission.objects.create(
        #     codename='can_publish',
        #     name='Can Publish Posts',
        #     content_type=content_type,
        # )

        # get_user = User.objects.get(username='user-2')
        # test = User.objects.all()
        # print(test)
        # get_permission_1 = Permission.objects.get(codename='view_movie')
        # get_permission_2 = Permission.objects.get(codename='add_movie')
        # get_user.user_permissions.add(get_permission_1)
        # get_user.user_permissions.add(get_permission_2)
        # user = User.objects.create_user('user-3', 'lennon@thebeatles.com', 'me+you=love4ever')
        get_user = User.objects.get(username='user-3')
        # permissions = Permission.objects.all()
        # print(permissions)
        my_permissions = {'view_movie': 'view_movie', 'add_movie': 'add_movie', }
        for permission in my_permissions:
            get_permission = Permission.objects.get(codename=my_permissions[permission])
            get_user.user_permissions.add(get_permission)

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # works fine
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # works fine
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # works fine
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


@api_view(['GET', ])
def api_index(request):
    # works fine
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def api_show(request, id):
    # works fine
    if request.method == 'GET':
        get_movie = Movie.objects.get(pk=id)
        serializer = MovieSerializer(get_movie, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'PUT', ])
def api_create(request):
    # unexpected output
    if request.method == 'POST' or request.method == 'PUT':
        serializer = MovieSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST', 'PUT', ])
def api_update(request, id):
    """
    Retrieve, update or delete a code snippet.
    'GET',   'PUT',    'DELETE'
    """
    # unexpected output
    if request.method == 'POST' or request.method == 'PUT':
        get_movie = Movie.objects.get(pk=id)
        serializer = MovieSerializer(get_movie, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE', ])
def api_delete(request, id):
    # works fine
    if request.method == 'DELETE':
        get_movie = Movie.objects.get(pk=id)
        get_movie.delete()
        return Response(status=status.HTTP_200_OK)


class ApiIndex(APIView):
    # works fine
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiShow(APIView):
    # works fine
    def get(self, request, id):
        get_movie = Movie.objects.get(pk=id)
        serializer = MovieSerializer(get_movie, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApiCreate(APIView):
    # unexpected output
    def post(self, request):
        form = MovieForm(request.POST or None, request.FILES or None)
        serializer = MovieSerializer(form, data=request.data, context={'request': request})
        if serializer.is_valid():
            form.save()
            return redirect("index")
        return render(request, "movie/create.html", {
            "form": form,
        })


class ApiUpdate(APIView):
    # unexpected output
    def post(self, request, id):
        """
        Retrieve, update or delete a code snippet.
        'GET',   'PUT',    'DELETE'
        """
        get_movie = Movie.objects.get(pk=id)
        serializer = MovieSerializer(get_movie, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApiDelete(APIView):
    # works fine
    def delete(self, request, id):
        get_movie = Movie.objects.get(pk=id)
        get_movie.delete()
        return Response(status=status.HTTP_200_OK)

# ----------------------------Mixins---------------------------- #


class ApiIndexMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)


class ApiShowMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ApiCreateMixins(mixins.CreateModelMixin, generics.GenericAPIView):
    # works fine
    movies = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ApiUpdateMixins(mixins.UpdateModelMixin, generics.GenericAPIView):
    # works fine
    get_movie = Movie.objects.all()
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ApiDeleteMixins(mixins.DestroyModelMixin, generics.GenericAPIView):
    # not working
    get_movie = Movie.objects.all()
    serializer_class = MovieSerializer

# ----------------------------Generics---------------------------- #


class ApiIndexGenerics(generics.ListAPIView):
    # unexpected output
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ApiShowGenerics(generics.ListAPIView):
    # not working
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ApiCreateGenerics(generics.CreateAPIView):
    # works fine
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ApiUpdateGenerics(generics.UpdateAPIView):
    # unexpected output
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ApiDeleteGenerics(generics.DestroyAPIView):
    # unexpected output
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
