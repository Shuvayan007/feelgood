from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatView.as_view(), name='api_chat'),
    path('check-in/', views.CheckInView.as_view(), name='api_check_in'),
    path('conversations/', views.ConversationListView.as_view(), name='api_conversations'),
    path(
        'conversations/<int:conversation_id>/messages/',
        views.ConversationMessageView.as_view(),
        name='api_conversation_messages',
    ),
    path('proposals/', views.ProposalListView.as_view(), name='api_proposals'),
    path('proposals/<int:pk>/approve/', views.ProposalApproveView.as_view(), name='api_proposal_approve'),
    path('proposals/<int:pk>/reject/', views.ProposalRejectView.as_view(), name='api_proposal_reject'),
]
