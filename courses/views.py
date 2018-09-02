import uuid

from ajson import ASerializer
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from courses.models import Course, Student, Card, UpdateCard
from lp_auth.models import User
from lp_auth.permissions import IsRegular
from services.request_utils import is_upload_file, save_in_memory_file


class CourseView(ViewSet):
    permission_classes = [IsRegular]

    def list(self, request: Request):
        courses = Course.get_user_courses(request.user)
        return JsonResponse({
            "data": ASerializer().to_dict(list(courses), groups=['course_detailed', 'user_basic'])
        })

    def retrieve(self, request: Request, pk: str):
        user: User = request.user
        course: Course = Course.get_or_404(pk=request.data['course_id'], user=user)
        return JsonResponse({
            "data": ASerializer().to_dict(course, groups=['course_detailed', 'user_detailed'])
        })

    def create(self, request: Request):
        course: Course = ASerializer().from_dict(request.data, Course)
        course.teacher = request.user
        course.save()
        return JsonResponse({
            "data": ASerializer().to_dict(course, groups=['course_detailed'])
        })

    def update(self, request: Request, pk: str):
        user: User = request.user
        course: Course = Course.get_or_404(pk=request.data['course_id'], user=user)
        course.title = request.data['title']
        course.save()
        return JsonResponse({
            "data": ASerializer().to_dict(course, groups=['course_detailed', 'user_detailed'])
        })
        pass

    @action(methods=['get', 'post'], detail=True)
    def students(self, request: Request, pk=None):
        if request.method == 'GET':
            students = Student.objects.filter(course__pk=pk)
            return JsonResponse({
                "data": ASerializer().to_dict(list(students), groups=['student_basic', 'user_basic'])
            })
        else:
            user = User.objects.get(id=request.data['user_id'])
            course = Course.objects.get(id=pk)
            student = Student()
            student.user = user
            student.course = course
            student.save()
            return JsonResponse({
                "data": ASerializer().to_dict(student, groups=['student_basic', 'user_basic'])
            })


class StudentsView(ListCreateAPIView):
    permission_classes = [IsRegular]

    def list(self, request: Request, course_id: int):
        students = Student.objects.filter(course__pk=course_id)
        return JsonResponse({
            "data": ASerializer().to_dict(list(students), groups=['student_basic', 'user_basic'])
        })

    def create(self, request: Request, course_id: int):
        user = User.objects.get(id=request.data['user_id'])
        course = Course.objects.get(id=course_id)
        student = Student()
        student.user = user
        student.course = course
        student.save()
        return JsonResponse({
            "data": ASerializer().to_dict(student, groups=['student_basic', 'user_basic'])
        })


class StudentView(RetrieveUpdateAPIView):
    permission_classes = [IsRegular]

    def retrieve(self, request: Request, course_id: int, pk: int):
        student: Student = get_object_or_404(Student, course__pk=course_id, id=pk)
        return JsonResponse({
            "data": ASerializer().to_dict(student, groups=['student_detailed', 'user_detailed'])
        })

    def update(self, request: Request, course_id: int, pk: int):
        student: Student = get_object_or_404(Student, course__pk=course_id, id=pk)
        raise NotImplementedError()

    def partial_update(self, request: Request, course_id: int, pk: int):
        student: Student = get_object_or_404(Student, course__pk=course_id, id=pk)
        raise NotImplementedError()


class CardsView(ListCreateAPIView):
    permission_classes = [IsRegular]

    def list(self, request: Request, course_id: int):
        cards = Card.get_user_cards(request.user).filter(course__pk=course_id)
        return JsonResponse({
            "data": ASerializer().to_dict(list(cards), groups=['card_basic'])
        })

    def create(self, request: Request, course_id: int):
        card: Card = ASerializer().from_dict(request.data, Card)
        card.user = request.user
        card.course = Course.get_or_404(pk=request.data['course_id'], user=request.user)
        card.save()
        return JsonResponse({
            "data": ASerializer().to_dict(card, groups=['card_detailed'])
        })


class CardView(RetrieveUpdateAPIView):
    permission_classes = [IsRegular]

    def retrieve(self, request: Request, course_id: int, pk: int):
        card: Card = get_object_or_404(Card, pk=pk, user=request.user)
        return JsonResponse({
            "data": ASerializer().to_dict(card, groups=['card_detailed'])
        })

    def update(self, request: Request, course_id: int, pk: int):
        # make sure data has the right format
        card = ASerializer().from_dict(request.data, UpdateCard)
        card_data = ASerializer().to_dict(card, groups=["card_basic"])

        card: Card = get_object_or_404(Card, pk=pk, user=request.user)
        for key, value in card_data.items():
            setattr(card, key, value)

        card.course = Course.get_or_404(pk=request.data['course_id'], user=request.user)
        card.save()
        return JsonResponse({
            "data": ASerializer().to_dict(card, groups=['card_detailed'])
        })

    def partial_update(self, request: Request, course_id: int, pk: int):
        raise NotImplementedError()

    @staticmethod
    @is_upload_file
    def upload_card_sound(request: Request, file, course_id: int, pk: int):
        # todo add security here
        card: Card = get_object_or_404(Card, pk=pk, user=request.user)
        path = f'static/cards/sound_id_{uuid.uuid4()}_{pk}.m4a'
        card.sound_path = path
        save_in_memory_file(file, path)
        card.save()
        return JsonResponse({"success": True})
