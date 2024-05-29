from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import openai
from flask_login import login_user, logout_user, current_user, login_required
import torch
from model.journal import Message
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model_name = "gpt2-medium"  # Choose model size
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

mental_api = Blueprint('mental_api', __name__, url_prefix='/api/mental')
api = Api(mental_api)

class MentalAPI:

    class _AI(Resource):
        def post(self):
            data = request.get_json()
            message = data.get('message', '')

            # Set the context by including the purpose in the prompt
            prompt = f"The user is writing about their life and stress do not judge and just give advice, no personal stories:\n{message}\n\nAI Response:"

            # Call OpenAI GPT-3 API to generate a response
            response = generate_response(prompt)

            return jsonify({"response": response})
        
    class _Journal(Resource):
        def post(self, current_user, Message):
            body = request.get_json()
            
            Journal_Content = body.get('message')
            
            message = Message(uid=current_user.uid, message=Journal_Content)
            
            try:
                created_log = message.create()
                return jsonify(created_log.read()), 201
            except Exception as e:
                return {'message': f'Error: {e}'}, 500
            
        def get(self):
            logs = Message.query.all()
            json_ready = [message.read() for message in logs]
            return jsonify(json_ready)
    
    class _Send(Resource):
        def post(self):
            body = request.get_json()
            # Fetch data from the form
            uid = body.get('uid')
            message = body.get('message')
            if uid is not None:
                new_message = Message(uid=uid, message=message)
            message = new_message.create()
            if message:
                return message.read()
            return {'message': f'Processed {uid}, either a format error or User ID {uid} is duplicate'}, 400
            
        

def generate_response(prompt, max_length=1000, temperature=1.0):
    # Tokenize the user-provided story prompt and convert it into input_ids
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    # Generate a story based on the input_ids (prompt)
    output = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        num_return_sequences=1,  # Generate a single sequence
        pad_token_id=50256,      # Specify the padding token ID for GPT-2
        do_sample=True,          # Allow for sampling to introduce randomness
    )
    
    # Decode the generated output into human-readable text, skipping special tokens
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

api.add_resource(MentalAPI._AI, '/ai')
api.add_resource(MentalAPI._Journal, '/journal')
api.add_resource(MentalAPI._Send, '/send')
