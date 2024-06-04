from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from llmMod.openai import OpenAiUtils


class ItemCreate(APIView):
    def post(self, request, format=None):
        user_prompt = request.data.get('prompt', '')
        session_id = request.data.get('session_id', 'default_session')

        if not user_prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            gpt_response = OpenAiUtils.globalSearch(userPrompt=user_prompt, session_id=session_id)
            return Response({"response": gpt_response}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)