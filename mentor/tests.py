from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.html import parse_html
from django.urls import reverse
from django.utils import timezone

from .models import Conversation, Message

User = get_user_model()


def find_by_id(node, element_id):
    if isinstance(node, str):
        return None
    if dict(node.attributes).get('id') == element_id:
        return node
    for child in node.children:
        found = find_by_id(child, element_id)
        if found is not None:
            return found
    return None


class ConversationDeleteTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email='owner@example.com', password='pw-12345')
        self.other = User.objects.create_user(email='other@example.com', password='pw-12345')
        self.conversation = Conversation.objects.create(user=self.owner)
        Message.objects.create(
            conversation=self.conversation, role=Message.Role.USER, content='hi'
        )
        self.url = reverse('api_conversation_delete', args=[self.conversation.id])

    def test_owner_can_delete_conversation_and_its_messages(self):
        self.client.force_login(self.owner)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Conversation.objects.filter(pk=self.conversation.pk).exists())
        self.assertFalse(Message.objects.filter(conversation_id=self.conversation.pk).exists())

    def test_cannot_delete_another_users_conversation(self):
        self.client.force_login(self.other)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Conversation.objects.filter(pk=self.conversation.pk).exists())

    def test_requires_authentication(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 401)
        self.assertTrue(Conversation.objects.filter(pk=self.conversation.pk).exists())


class ChatPageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='chat@example.com', password='pw-12345')
        self.client.force_login(self.user)

    def test_history_renders_in_order_inside_the_message_container(self):
        conversation = Conversation.objects.create(user=self.user)
        for role, text in [('user', 'first'), ('assistant', 'second'), ('user', 'third')]:
            Message.objects.create(conversation=conversation, role=role, content=text)

        response = self.client.get(reverse('chat_conversation', args=[conversation.id]))

        # The JS appends new messages to #chat-messages, so the history has to live there too.
        container = find_by_id(parse_html(response.content.decode()), 'chat-messages')
        bubbles = [str(child) for child in container.children if not isinstance(child, str)]
        self.assertEqual(len(bubbles), 3)
        for bubble, text in zip(bubbles, ['first', 'second', 'third']):
            self.assertIn(text, bubble)
        # Chat messages must not leak into the Django messages-framework alerts.
        self.assertNotContains(response, 'class="alert')

    def test_new_chat_placeholder_can_be_removed_by_the_script(self):
        response = self.client.get(reverse('chat'))

        container = find_by_id(parse_html(response.content.decode()), 'chat-messages')
        self.assertIsNotNone(find_by_id(container, 'chat-empty'))

    def test_every_history_item_has_a_delete_button(self):
        conversations = [Conversation.objects.create(user=self.user) for _ in range(2)]

        response = self.client.get(reverse('chat'))

        for conversation in conversations:
            self.assertContains(response, f'data-delete-conversation="{conversation.id}"')

    @patch('mentor.views.MentorOrchestrator')
    def test_replying_in_a_conversation_moves_it_to_the_top_of_history(self, orchestrator):
        orchestrator.return_value.process_message.return_value = {'response': 'ok'}
        older = Conversation.objects.create(user=self.user)
        Conversation.objects.create(user=self.user)
        Conversation.objects.filter(pk=older.pk).update(
            last_message_at=timezone.now() - timedelta(days=1)
        )

        self.client.post(
            reverse('api_chat'),
            {'content': 'hello', 'conversation_id': older.id},
            content_type='application/json',
        )

        response = self.client.get(reverse('chat'))
        self.assertEqual(response.context['conversations'][0].id, older.id)
