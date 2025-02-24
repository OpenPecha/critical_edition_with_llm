from ai_critical_edition.config import ANTHROPIC_CLIENT
import time


def get_claude_response(message):
    time.sleep(3)
    response = ''
    try:
        ai_response = ANTHROPIC_CLIENT.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8192,
            temperature=0,
            messages=message
        )
        response = ai_response.content[0].text

    except Exception as e:
        print(f"Error processing translation: {e}")
    
    return response