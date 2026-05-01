import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- CONFIGURATION ---
# It is best practice to set this in your terminal or a .env file, 
# but for testing, you can uncomment the line below and paste your key.
# os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"

def generate_notes(transcript, external_context=None, model_name="gemini-2.5-flash"):
    """
    Feeds the transcript and optional scraped context to the Gemini API
    to generate structured, markdown-formatted notes.
    """
    
    # Verify the API key is present
    if "GOOGLE_API_KEY" not in os.environ:
        print("Error: GOOGLE_API_KEY environment variable not found.")
        print("Please set it using: os.environ['GOOGLE_API_KEY'] = 'your_key'")
        return None

    print(f"Connecting to Gemini API ({model_name})...")
    
    # Initialize the Gemini Model
    # temperature=0.2 keeps the AI focused and factual rather than overly creative
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
    
    # Define how the AI should behave and format the output
    template = """
    You are an expert academic assistant. Your task is to extract the most important 
    information from the provided video transcript.
    
    {context_instruction}
    
    Here is the video transcript:
    <transcript>
    {transcript}
    </transcript>
    
    Please provide the output in the following Markdown format:
    # [Video Title / Main Topic]
    ## Executive Summary
    (A 2-3 sentence summary of the entire video)
    
    ## Key Concepts
    (Bullet points of the main ideas discussed)
    
    ## Actionable Insights / Formulas / Definitions
    (Extract any specific rules, definitions, or actionable advice)
    """
    
    # Handle the optional web-scraped context
    context_instruction = ""
    if external_context:
        context_instruction = f"""
        Additionally, use this external context scraped from a linked resource to enrich your notes:
        <external_context>
        {external_context}
        </external_context>
        Ensure you integrate facts from this external context into your final notes.
        """
        
    # Build the LangChain pipeline
    prompt = PromptTemplate(
        template=template,
        input_variables=["transcript", "context_instruction"]
    )
    
    # Chain: Prompt -> LLM -> String Output
    chain = prompt | llm | StrOutputParser()
    
    try:
        print("Sending data to Gemini. Waiting for response...")
        result = chain.invoke({
            "transcript": transcript,
            "context_instruction": context_instruction
        })
        print("Notes generation complete!")
        return result
        
    except Exception as e:
        print(f"Error during note generation: {e}")
        return None

# --- Test the script ---
if __name__ == "__main__":
    # Ensure you set your API key before running the test
    # os.environ["GOOGLE_API_KEY"] = "YOUR_KEY"
    
    sample_transcript = "In this lecture, we discussed neural networks. A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of data through a process that mimics the way the human brain operates."
    sample_context = "Neural networks were first proposed in 1944 by Warren McCulloch and Walter Pitts."
    
    final_notes = generate_notes(sample_transcript, sample_context)
    
    if final_notes:
        print("\n--- Final Generated Notes ---")
        print(final_notes)
