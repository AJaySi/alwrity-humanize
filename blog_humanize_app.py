import time #Iwish
import os
import json
import openai
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
    )
    # Remove the extra spaces from margin top.
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"""
      <style>
      [class="st-emotion-cache-7ym5gk ef3psqc12"]{{
            display: inline-block;
            padding: 5px 20px;
            background-color: #4681f4;
            color: #FBFFFF;
            width: 300px;
            height: 35px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            border-radius: 8px;’
      }}
      </style>
    """
    , unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Sidebar input for OpenAI API Key
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown(f"🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")
    
    # Title and description
    st.title("✍️ Alwrity - Humanize Your AI Content")
    with st.expander("How to Write **Great AI Content** ? 📝❗"):
        st.markdown('''
           ### Howto Proofread & Humanize AI Content Guidelines 📝✨
    ---
    **Guidelines:🗣️ ***

    1. **Identify Redundancies:** Remove repeated phrases and consolidate information for clarity.
    2. **Use Clear Language:** Opt for straightforward language, avoiding jargon and complex sentences.
    3. **Keep Sentences Concise:** Break down long sentences for improved clarity.
    4. **Trim Excess Words:** Eliminate filler words and vague phrases.
    5. **Enhance Readability:** Ensure content delivers value and engages readers effectively.
    6. **Focus on Quality:** Prioritize delivering valuable insights concisely.

    **SEO Integration: 📊 **

    - **Use Focus Keywords Seamlessly:** Integrate keywords naturally for visibility.
    - **Avoid Speculative Statements:** Present only factual evidence, avoiding exaggeration.
    - **Maintain a Calm Tone:** Use a conversational tone, avoiding exclamations.

    **Grammar and Clarity Check:🧹 **

    - **Review for Errors:** Ensure grammatical correctness and clarity.
    - **Enhance Sentence Structure:** Refine language for smooth flow.
    - **Inject Unique Voice:** Add personal insights to humanize the content.

    **Task Instructions: 💬 **

    - Rewrite provided content, ensuring originality and avoiding repetition.
    - Focus on providing concrete evidence and avoid speculative language.
    - Maintain a conversational tone and avoid corporate jargon.
    - Remove excess qualifiers for clarity.
    
    --- 
                ''')
    
    # Input section
    with st.expander("**PRO-TIP** - Read the instructions below.", expanded=True):
        input_blog = st.text_area('**Enter your Suspected AI Content Below** (Copy/Paste)')

        # Generate Blog FAQ button
        if st.button('**Humanize AI Content**'):
            with st.spinner():
                # Clicking without providing data, really ?
                if not input_blog:
                    st.error('** 🫣P Provide your blog content to humanizezze it.**')
                elif input_blog:
                    blog_content = generate_humanized_blog(input_blog)
                    if blog_content:
                        st.subheader('**👩🔬👩🔬 Your Human Sounding Content**')
                        st.markdown(blog_content)
                    else:
                        st.error("💥**Failed to Humanize given Content. Please try again!**")

    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")
    st.markdown('''
                Generate SEO optimized Blog FAQs - powered by AI (OpenAI GPT, Gemini Pro).
                Implemented by [Alwrity](https://alwrity.netlify.app).
                Know more: [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know)
                In short, write for human readers & Not for search engine. Provide value to Readers & Not hack for rankings..
                ''')



# Function to generate blog metadesc
def generate_humanized_blog(input_blog):
    """ Function to call upon LLM to get the work done. """

    # If keywords and content both are given.
    if input_blog:
        prompt = f"""As part of our continuous efforts to improve the quality and effectiveness of our blog content, we require a thorough proofreading, tailored to optimize readability, grammar, style, and seamless integration of SEO strategies. 
        Your task involves refining the provided blog post, ensuring your response reads like human written, provides more value to readers & Passes all AI content detectors.

    Follow Proofreading Guidelines:

    1). Identify Redundancies: Remove repeated phrases and consolidate information for clarity.
    2). Use Clear Language: Opt for straightforward language, avoiding jargon and complex sentences.
    3). Keep Sentences Concise: Break down long sentences for improved clarity.
    4). Trim Excess Words: Eliminate filler words and vague phrases.
    5). Enhance Readability: Ensure content delivers value and engages readers effectively.
    6). Rhetorical questions: Integrate strategically to emphasize key points and engage readers.
    7). Figures of speech: Employe selectively to captivate the reader and underscore essential points.
    8). Idiomatic expressions: Use sparingly and fittingly to inject personality and convey ideas effectively.
    9). Focus on Quality: Prioritize delivering valuable insights concisely.

    10). Avoid Speculative Statements: Present only factual evidence, avoiding exaggeration. Ensure No plagiarism.
    11). Maintain a Calm Tone: Use a conversational tone of voice, avoiding exclamations.
    12). Review for Errors: Ensure grammatical correctness and clarity.
    13). Inject Unique Voice: Add personal insights to humanize the content.

    Task Instructions:

    1). Rewrite the article with higher perplexity and burstiness, incorporating varied sentence structures.
    2). DO NOT use these negative terms: ' "It’s important to note", "Delve into", "Tapestry", "Bustling", "In summary", 
    "In conclusion", "Remember that", "Take a dive into", "Navigating", "Navigating the landscape", "Navigating the complexities of", 
    "Landscape", "The landscape of", "Testament", "a testament to", "In the world of", "Realm", "Embark", "virtuoso", "symphony", 
    "Harnessing", "Revolutionizing", "Empower", "game changing", "ever-changing", "Embrace", "Embracing", "game-changing",
    "ever-evolving", "Landscape"' etc.
    \n\nContent: '{input_blog}'
        """
        blog_humanized = openai_chatgpt(prompt)
        return blog_humanized


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", temperature=0.2, max_tokens=4096, top_p=0.9, n=1):
    """
    Wrapper function for OpenAI's ChatGPT completion.

    Args:
        prompt (str): The input text to generate completion for.
        model (str, optional): Model to be used for the completion. Defaults to "gpt-4-1106-preview".
        temperature (float, optional): Controls randomness. Lower values make responses more deterministic. Defaults to 0.2.
        max_tokens (int, optional): Maximum number of tokens to generate. Defaults to 8192.
        top_p (float, optional): Controls diversity. Defaults to 0.9.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        str: The generated text completion.

    Raises:
        SystemExit: If an API error, connection error, or rate limit error occurs.
    """
    # Wait for 10 seconds to comply with rate limits
    for _ in range(10):
        time.sleep(1)

    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
            # Additional parameters can be included here
        )
        return response.choices[0].message.content

    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"OpenAI error: {err}")



# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url


if __name__ == "__main__":
    main()
