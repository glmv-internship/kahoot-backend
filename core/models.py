# --- START: IMPORTS

# built-in
import uuid


# django-specific
from django.db import models
from django.utils import timezone

# other/external
# --- END: IMPORTS


class BaseManager(models.Manager):
    """
    Our basic manager is used to order all child models of BaseLayer
    to be ordered by created time (descending), therefore it creates a LIFO order,
    causing the recent ones appear first in results.
    """
    use_for_related_fields = True

    def get_queryset(self):
        super(BaseManager, self).get_queryset().order_by('-created_time')


class BaseLayer(models.Model):
    """
    This layer makes system-wide sonfigurations which tends to be effective for every single model.
    It is used as a parent class for all other models.
    """

    # let's configure managers
    default_manager = BaseManager
    objects = BaseManager
    all_objects = models.Manager

    # all models are going to have following two fields
    created_time = models.DateTimeField(default=timezone.now)
    last_updated_time = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, *args, **kwargs):
        now = timezone.now()
        obj = cls(
            *args,
            **kwargs,
            created_time=now,
            last_updated_time=now
        )
        obj.save()
        return obj

    def save(self, *args, **kwargs):
        self.last_updated_time = timezone.now()
        return super(BaseLayer, self).save(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return cls.objects.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None

    @classmethod
    def all(cls, *args, **kwargs):
        return cls.objects.all()

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    class Meta:
        abstract = True


class User(BaseLayer):
    """
    To store users
    """
    uid = models.IntegerField(unique=True)
    uuid = models.UUIDField(null=True, blank=True, default=None)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    temp_data = models.TextField(null=True, blank=True)
    # welcome_message_id = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=5, default='en')
    def __str__(self):
        return f"{self.nickname or ''} {self.uid}".lstrip()

    class Meta:
        db_table = 'users'

class Quiz(BaseLayer):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='quizzes')
    name = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField()
    number_of_questions = models.IntegerField(default=0)
    duration = models.IntegerField(default=60)
    class Meta:
        db_table = 'quizzes'
class Poll(BaseLayer):
    """
    A simple quiz model to store quizzes
    """
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, related_name='polls')
    question = models.TextField()
    tip = models.TextField(null=True, blank=True)
    # duration = models.IntegerField(default=60)

    def __str__(self):
        return f"{''.join([self.question[:30], ['', '...'][len(self.question) > 30]])}"

    class Meta:
        db_table = 'polls'


class PollOption(BaseLayer):
    """
    A single quiz can have multiple options/answers.
    So, we are using ManyToOne relation
    """
    poll = models.ForeignKey(Poll, on_delete=models.SET_NULL, null=True, related_name='options')
    text = models.TextField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return f"{''.join([self.text[:30], ['', '...'][len(self.text) > 30]])}"

    class Meta:
        db_table = 'options'

class Game(BaseLayer):
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True, related_name='games')
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='games')
    join_code = models.CharField(max_length=6, unique=True)
    is_active = models.BooleanField(default=True)
    players = models.ManyToManyField(User, related_name='games')
    started_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.join_code} {self.quiz.name}"
    
class UserResult(BaseLayer):
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, related_name='results')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='results')
    score = models.IntegerField(default=0)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    joined_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.nickname or ''} {self.score}".lstrip()






