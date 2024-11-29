from huggingface_hub import InferenceClient
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatInputSerializer
#from openai import OpenAI, api_key
import os
from dotenv import load_dotenv

load_dotenv()

# client = OpenAI()
# api_key = os.getenv('OPENAI_API_KEY')
hf_api_key = os.getenv("HUGGINFACE_API_KEY")


# class Chat(APIView):
#     def post(self, request):

#         serializer = ChatInputSerializer(data=request.data)

#         if serializer.is_valid():
#             user_input = serializer.validated_data['user_input']

#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant."},
#                         {
#                             "role": "user",
#                             "content": user_input
#                         }
#                     ],
#                     max_tokens=serializer.validated_data.get('max_tokens', 100)
#                 )

#                 result = response.choices[0].message['content'].strip()
#                 return Response({'response': result}, status=status.HTTP_200_OK)
            
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Initialize the Hugging Face client 
client = InferenceClient(api_key= hf_api_key)


class ChatView(APIView):
    def post(self, request, *args, **kwargs):
        # Deserialize and validate input
        serializer = ChatInputSerializer(data=request.data)
        if serializer.is_valid():
            user_input = serializer.validated_data['user_input']

            # Prepare messages payload
            messages = [
                {"role": "user", "content": user_input}
            ]

            try:
                # Call the Hugging Face chat completion API
                completion = client.chat.completions.create(
                    model="meta-llama/Llama-3.2-3B-Instruct",
                    messages=messages,
                    max_tokens=500
                )

                # Extract the assistant's response
                if completion and "choices" in completion:
                    ai_response = completion.choices[0].message["content"]
                    return Response(ai_response, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "No response received from the model."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
