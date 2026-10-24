from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer


# ── API Views ────────────────────────────────────────────────────


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        UserProfile.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {'id': user.id, 'email': user.email},
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response(
                {'detail': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {'id': user.id, 'email': user.email},
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
        })


class LogoutView(APIView):
    def post(self, request):
        return Response({'detail': 'Logged out.'}, status=status.HTTP_200_OK)


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            from goals.models import Goal
            active_goals = Goal.objects.filter(
                user=request.user, status='active'
            ).count()
        except Exception:
            active_goals = 0

        try:
            from habits.models import Habit
            habits_today = Habit.objects.filter(
                user=request.user, is_active=True
            ).count()
        except Exception:
            habits_today = 0

        return Response({
            'active_goals': active_goals,
            'habits_today': habits_today,
            'recent_progress': [],
            'mentor_suggestion': 'Set your first goal to get started.',
        })


# ── Frontend Views ───────────────────────────────────────────────


def index_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'index.html')


@login_required
def dashboard_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    try:
        from goals.models import Goal
        goals = Goal.objects.filter(user=request.user, status='active').order_by('-updated_at')[:5]
    except Exception:
        goals = []
    try:
        from habits.models import Habit
        habits = Habit.objects.filter(user=request.user, is_active=True)
    except Exception:
        habits = []
    return render(request, 'dashboard.html', {
        'profile': profile,
        'goals': goals,
        'habits': habits,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        error = 'Invalid email or password.'
    return render(request, 'core/login.html', {'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        if password != password_confirm:
            error = 'Passwords do not match.'
        elif User.objects.filter(email=email).exists():
            error = 'An account with this email already exists.'
        else:
            user = User.objects.create_user(email=email, password=password)
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('onboarding')
    return render(request, 'core/register.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    saved = False
    if request.method == 'POST':
        profile.display_name = request.POST.get('display_name', profile.display_name)
        profile.age_range = request.POST.get('age_range', profile.age_range)
        profile.timezone = request.POST.get('timezone', profile.timezone)
        profile.schedule_type = request.POST.get('schedule_type', profile.schedule_type)
        hours = request.POST.get('available_hours_per_week')
        if hours:
            try:
                profile.available_hours_per_week = float(hours)
            except ValueError:
                pass
        profile.save()
        saved = True
    return render(request, 'core/profile.html', {'profile': profile, 'saved': saved})
