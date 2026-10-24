from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Conversation, Message, Proposal
from .serializers import ConversationSerializer, MessageSerializer, ProposalSerializer


# ── API Views ────────────────────────────────────────────────────


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content', '').strip()
        if not content:
            return Response(
                {'detail': 'Message content is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation_id = request.data.get('conversation_id')
        if conversation_id:
            conversation = get_object_or_404(
                Conversation, id=conversation_id, user=request.user
            )
        else:
            conversation = Conversation.objects.create(
                user=request.user, purpose=Conversation.Purpose.GENERAL
            )

        Message.objects.create(
            conversation=conversation, role=Message.Role.USER, content=content
        )

        # Stub: return a canned mentor response
        mentor_reply = (
            "Thank you for sharing that. I'm here to help you turn your goals "
            "into actionable steps. Could you tell me more about what you'd like "
            "to work on?"
        )
        assistant_msg = Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content=mentor_reply,
        )

        return Response({
            'conversation_id': conversation.id,
            'message': MessageSerializer(assistant_msg).data,
        }, status=status.HTTP_201_CREATED)


class CheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation = Conversation.objects.create(
            user=request.user, purpose=Conversation.Purpose.CHECK_IN
        )
        mentor_reply = (
            "Good to see you! Let's review your day. "
            "What did you accomplish since we last spoke?"
        )
        assistant_msg = Message.objects.create(
            conversation=conversation,
            role=Message.Role.ASSISTANT,
            content=mentor_reply,
        )
        return Response({
            'conversation_id': conversation.id,
            'message': MessageSerializer(assistant_msg).data,
        }, status=status.HTTP_201_CREATED)


class ConversationListView(ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)


class ConversationMessageView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation = get_object_or_404(
            Conversation,
            id=self.kwargs['conversation_id'],
            user=self.request.user,
        )
        return Message.objects.filter(conversation=conversation)


class ProposalListView(ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Proposal.objects.filter(
            user=self.request.user, status=Proposal.Status.PENDING
        )


class ProposalApproveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        proposal = get_object_or_404(Proposal, pk=pk, user=request.user)
        if proposal.status != Proposal.Status.PENDING:
            return Response(
                {'detail': 'Proposal is no longer pending.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        proposal.status = Proposal.Status.APPROVED
        proposal.resolved_at = timezone.now()
        proposal.save()
        return Response(ProposalSerializer(proposal).data)


class ProposalRejectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        proposal = get_object_or_404(Proposal, pk=pk, user=request.user)
        if proposal.status != Proposal.Status.PENDING:
            return Response(
                {'detail': 'Proposal is no longer pending.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        proposal.status = Proposal.Status.REJECTED
        proposal.resolved_at = timezone.now()
        proposal.save()
        return Response(ProposalSerializer(proposal).data)


# ── Frontend Views ───────────────────────────────────────────────


@login_required
def chat_view(request, conversation_id=None):
    conversations = Conversation.objects.filter(user=request.user).order_by('-last_message_at')
    messages = []
    current_conversation = None

    if conversation_id:
        current_conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user
        )
        messages = current_conversation.messages.all()

    return render(request, 'mentor/chat.html', {
        'conversations': conversations,
        'current_conversation': current_conversation,
        'messages': messages,
    })


@login_required
def onboarding_view(request):
    return render(request, 'mentor/onboarding.html')
