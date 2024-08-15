from openai import ChatCompletion

async def get_gpt4_mini_response(prompt):
    try:
        completion = ChatCompletion.create(
            model="gpt-4",  # Make sure this is the correct model name for GPT-4
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,  # Adjust token limit as needed
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request."


import openai


async def get_gpt4_response(user_input: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # Specify the correct model name
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
        )
        response = completion.choices[0].message['content']
        return response
    except openai.error.InvalidRequestError as e:
        # Handle specific OpenAI API errors
        return f"API Error: {str(e)}"
    except Exception as e:
        # Handle general errors
        return f"Error: {str(e)}"

