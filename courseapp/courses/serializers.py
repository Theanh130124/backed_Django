# Viết  Restful
from courses.models import Category, Course, Tag, Lesson , User , Comment
from rest_framework import serializers



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url

        return req

class LessonSerializer(ItemSerializer):

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_date']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields =['id','name']


class AuthenticatedLessonDetailsSerializer(LessonDetailsSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request:
            return lesson.like_set.filter(user=request.user, active=True).exists()

    class Meta:
        model = LessonDetailsSerializer.Meta.model
        fields = LessonDetailsSerializer.Meta.fields + ['liked']

#Gom nhóm những thằng có chung thuộc tính :
class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSerializer(many=True)
    def get_image(self, course):

        if course.image:
            request = self.context.get('request')
            if request:
                return  request.build_absolute_uri('/static/%s' % course.image.name)
            return  '/static/%s' % course.image.name

class CourseSerializer(BaseSerializer):
    #Xử lý hình ảnh hiện trên đó -> vì phải có static
#-> Đã đưa lên baseserializer
    # Có dòng này thì course sẽ đỗ dữ liệu của Tag ra
    # Lấy tags đúng tên trong models của course
#-> Đã đưa lên baseserializer
    class Meta:
        model = Course
        # lấy ra
        fields = '__all__'


class LessonSerializer(BaseSerializer):
    # Nữa làm thì truong fields chỉ lấu những cái cần
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'content','created_date','updated_date']

class LessonDetailSerializer(LessonSerializer):
    liked = serializers.SerializerMethodField()
    #Muốn biết bài học đc like hay chưa
    def get_liked(self, lesson):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return lesson.like_set.filter(active =True).exists()
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # User là có sẳn của django rồi
        model = User
        fields = ['first_name' ,'last_name', 'username','password' , 'email','avatar']
        extra_kwargs = {
            'password':{
                'write_only' : True
            }

        }
    def create(self, validated_data):
        data = validated_data.copy() #validatae là các trường fields
        # tự gán first_name = "TheAnh"
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content','user']


