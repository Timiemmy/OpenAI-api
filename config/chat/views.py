from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatInputSerializer
from openai import OpenAI, api_key
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
api_key = os.getenv('OPENAI_API_KEY')


class Chat(APIView):
    def post(self, request):

        serializer = ChatInputSerializer(data=request.data)

        if serializer.is_valid():
            user_input = serializer.validated_data['user_input']

            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ],
                    max_tokens=serializer.validated_data.get('max_tokens', 100)
                )

                result = response.choices[0].message['content'].strip()
                return Response({'response': result}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        