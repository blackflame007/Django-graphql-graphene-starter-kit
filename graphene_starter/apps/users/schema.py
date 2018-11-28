from django.contrib.auth import get_user_model
import graphene
from graphene_django.types import DjangoObjectType
import graphql_jwt


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    #2: Defines the data you can send to the server
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    #3
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)
#4
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(object):
    login = graphene.Field(UserType)
    all_users = graphene.List(UserType)

    def resolve_login(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user


    def resolve_all_users(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return get_user_model().objects.all()