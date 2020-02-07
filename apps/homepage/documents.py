from django.contrib.auth.models import User
from django_elasticsearch_dsl.documents import DocType
from django_elasticsearch_dsl import Index, fields

from ..post.models import Post
from ..channel.models import Channel
from ..account.models import Profile

posts = Index('posts')


@posts.doc_type
class PostDocument(DocType):
    class Django:
        model = Post

        fields = [
            'body',
            'title'
        ]
        ignore_signals = False
        auto_refresh = True


channels = Index('channels')


@channels.doc_type
class ChannelDocument(DocType):
    class Django:
        model = Channel
        fields = [
            'title',
            'subject',
            'description',
        ]


profiles = Index('profile')


@profiles.doc_type
class ProfileDocument(DocType):
    user = fields.ObjectField(properties={
        'username': fields.TextField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
        'email': fields.TextField(),
    })

    class Django:
        model = Profile
        fields = [
            'age',
        ]
        related_models = [User]

    def get_queryset(self):
        return super(ProfileDocument, self).get_queryset().select_related(
            'manufacturer'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.profile
