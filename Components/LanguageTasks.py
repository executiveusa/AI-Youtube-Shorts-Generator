from pydantic import BaseModel,Field
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API")

# Zero-secrets mode: Allow running without OpenAI API key
STUB_MODE = api_key is None or api_key == "" or api_key == "DISABLED"

if STUB_MODE:
    print("⚠️  ZERO-SECRETS MODE: OpenAI API not configured")
    print("    Manual highlight selection will be used instead of AI")
    api_key = None  # Explicitly set to None for safety

class JSONResponse(BaseModel):
    """
    The response should strictly follow the following structure: -
     [
        {
        start: "Start time of the clip",
        content: "Highlight Text",
        end: "End Time for the highlighted clip"
        }
     ]
    """
    start: float = Field(description="Start time of the clip")
    content: str= Field(description="Highlight Text")
    end: float = Field(description="End time for the highlighted clip")

system = """

Based on the Transcription user provides with start and end, Highilight the main parts in less then 1 min which can be directly converted into a short. highlight it such that its intresting and also keep the time staps for the clip to start and end. only select a continues Part of the video

Follow this Format and return in valid json 
[{{
start: "Start time of the clip",
content: "Highlight Text",
end: "End Time for the highlighted clip"
}}]
it should be one continues clip as it will then be cut from the video and uploaded as a tiktok video. so only have one start, end and content
Make sure that the content's length doesn't go beyond 60 seconds.

Dont say anything else, just return Proper Json. no explanation etc


IF YOU DONT HAVE ONE start AND end WHICH IS FOR THE LENGTH OF THE ENTIRE HIGHLIGHT, THEN 10 KITTENS WILL DIE, I WILL DO JSON['start'] AND IF IT DOESNT WORK THEN...

<TRANSCRIPTION>
{Transcription}

"""

# User = """
# Example
# """




def GetHighlight(Transcription):
    """
    Extract video highlight timestamps.
    
    In ZERO-SECRETS MODE (when OPENAI_API is not set):
    - Prompts user for manual start/end timestamps
    
    In NORMAL MODE (when OPENAI_API is configured):
    - Uses GPT-4 to automatically identify interesting segments
    """
    if STUB_MODE:
        # Manual mode: User provides timestamps
        print("\n" + "="*60)
        print("MANUAL HIGHLIGHT SELECTION MODE")
        print("="*60)
        print("\nTranscription preview (first 500 chars):")
        print(Transcription[:500] + "..." if len(Transcription) > 500 else Transcription)
        print("\n" + "-"*60)
        
        while True:
            try:
                print("\nEnter the highlight timestamps for your short:")
                start_input = input("Start time (in seconds): ").strip()
                end_input = input("End time (in seconds): ").strip()
                
                Start = int(float(start_input))
                End = int(float(end_input))
                
                if Start >= 0 and End > Start and (End - Start) <= 120:
                    duration = End - Start
                    print(f"\n✓ Selected highlight: {Start}s to {End}s (duration: {duration}s)")
                    confirm = input("Confirm this selection? (y/n): ").lower()
                    if confirm == 'y':
                        return Start, End
                    else:
                        print("Let's try again...")
                else:
                    print("❌ Invalid timestamps. Please ensure:")
                    print("   - Start is >= 0")
                    print("   - End is greater than Start")
                    print("   - Duration is <= 120 seconds")
            except ValueError:
                print("❌ Invalid input. Please enter numeric values.")
            except KeyboardInterrupt:
                print("\n\n❌ Operation cancelled by user.")
                return 0, 0
    
    else:
        # AI mode: Use OpenAI GPT-4
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-4o-2024-05-13",
            temperature=0.7,
            api_key = api_key
        )

        from langchain.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",system),
                ("user",Transcription)
            ]
        )
        chain = prompt |llm.with_structured_output(JSONResponse,method="function_calling")
        response = chain.invoke({"Transcription":Transcription})
        Start,End = int(response.start), int(response.end)
        # print(f"Start is {Start}")
        # print(f"End is {End}\n\n")
        if Start==End:
            Ask = input("Error - Get Highlights again (y/n) -> ").lower()
            if Ask == "y":
                Start, End = GetHighlight(Transcription)
            return Start, End
        return Start,End

if __name__ == "__main__":
    print(GetHighlight(User))
