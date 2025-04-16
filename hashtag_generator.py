from openai import OpenAI
import json

# Function to generate hashtags based on the explanation of an image
def generate_hashtags(explanation):
    file = open('creds.json','rb')
    CONFIG = json.load(file)
    file.close()

    # OpenAI API key setup
    # openai.api_key = CONFIG['openai']['API_KEY']
    client = OpenAI(api_key = CONFIG['openai']['API_KEY'])
    
    # Constructing the prompt for OpenAI
    prompt_text = f'''Your task is to suggest 5 hashtags for an Instagram post featuring a space education picture.
    Here are some details to consider for creating these hashtags:
    1.Focus on the theme of space education and exploration.
    2.Include popular hashtags that have proven engagement rates.
    3.Ensure the hashtags appeal to both education-focused audiences and space enthusiasts.
    
    Your final suggestions should be succinct, relevant, and innovative to maximize visibility.
    1. make sure to just tell me the hashtags, and no extra infomation.
    2. The format of the response should be like this hastag1|hastag2|hastag3|hastag4|hastag5.
    3. dont' add # symbol before the hashtags

    Here is explanation of the image:
    {explanation}
    '''
    
    # Making the API call
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Update to use a specific model suited for your use-case
            messages=[
                {"role": "system", "content": '''You are a social media strategist who has been helping individuals and brands 
    create viral content for over 10 years. Your specialty lies in crafting effective hashtags 
    tailored to various themes, ensuring that posts reach a wider audience and engage users effectively.'''},
                {"role": "user", "content": prompt_text}
            ]
            # ,
            # max_tokens=60
        )

        print(response.choices[0].message.content)
        # Processing the response to get text output
        hashtags_text = response.choices[0].message.content.strip()
        
        # Post-processing to format the hashtags
        hashtags = hashtags_text.split("|")
        formatted_hashtags = ','.join(hashtags)  # Create a comma-separated string of hashtags

        return formatted_hashtags
    except Exception as e:
        return 'nasa,apod,space,spacenerds'