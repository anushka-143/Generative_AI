import streamlit as st
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Set up the Streamlit app
st.title("🌍 Travel Expert Assistant")
st.markdown("Plan your perfect trip with our AI-powered travel experts!")

# Sidebar for user inputs
with st.sidebar:
    st.header("Trip Details")
    from_city = st.text_input("Traveling from", "India")
    destination_city = st.text_input("Destination city", "Rome")
    date_from = st.text_input("Arrival Date", "1st March 2025")
    date_to = st.text_input("Departure Date", "7th March 2025")
    interests = st.text_input("Your interests", "sight seeing and good food")
    submit_button = st.button("Plan My Trip")


# Initialize Gemini LLM
def get_gemini_llm():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("Google API key not found in .env file")
        st.stop()
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=google_api_key,
        temperature=0.7
    )


# Initialize agents and tools only once
@st.cache_resource
def initialize_agents():
    # Web search tool
    @tool
    def search_web_tool(query: str):
        """Searches the web and returns results."""
        search_tool = DuckDuckGoSearchResults(num_results=5)
        return search_tool.run(query)

    # Get Gemini LLM instance
    llm = get_gemini_llm()

    # Agent: City Local Guide Expert
    guide_expert = Agent(
        role="City Local Guide Expert",
        goal="Provides information on things to do in the city based on the user's interests.",
        backstory="A local expert with a passion for sharing the best experiences and hidden gems of their city.",
        tools=[search_web_tool],
        verbose=True,
        max_iter=5,
        llm=llm,
        allow_delegation=False,
    )

    # Agent: Travel Trip Expert
    location_expert = Agent(
        role="Travel Trip Expert",
        goal="Gather helpful information about the destination city including accommodations, weather, and travel logistics.",
        backstory="A seasoned traveler who has explored various destinations and knows the ins and outs of travel logistics.",
        tools=[search_web_tool],
        verbose=True,
        max_iter=5,
        llm=llm,
        allow_delegation=False,
    )

    # Agent: Travel Planning Expert
    planner_expert = Agent(
        role="Travel Planning Expert",
        goal="Compiles all gathered information to provide a comprehensive travel plan.",
        backstory="An organizational wizard who can turn a list of possibilities into a seamless itinerary.",
        tools=[search_web_tool],
        verbose=True,
        max_iter=5,
        llm=llm,
        allow_delegation=False,
    )

    return guide_expert, location_expert, planner_expert


# Initialize agents
guide_expert, location_expert, planner_expert = initialize_agents()


def create_tasks(from_city, destination_city, date_from, date_to, interests):
    # Location Task
    location_task = Task(
        description=f"""
        This task involves gathering essential information about the destination.
        Traveling from: {from_city}
        Destination city: {destination_city}
        Arrival Date: {date_from}
        Departure Date: {date_to}

        Research and compile details on:
        - Accommodations (budget to luxury)
        - Cost of living estimates
        - Transportation options
        - Visa requirements
        - Travel advisories
        - Weather forecast for travel dates
        - Relevant events during the trip period
        """,
        expected_output="""
        A detailed markdown report with:
        - Recommended places to stay
        - Daily living expenses breakdown
        - Practical travel tips
        - Weather forecast
        - Local events during the travel period
        """,
        agent=location_expert,
        output_file='city_report.md',
    )

    # Guide Task
    guide_task = Task(
        description=f"""
        Create an engaging guide to the city's attractions tailored to the traveler's interests: {interests}.
        Destination city: {destination_city}
        Arrival Date: {date_from}
        Departure Date: {date_to}

        Focus on:
        - Cultural landmarks and historical spots
        - Entertainment venues
        - Dining experiences
        - Outdoor activities
        - Seasonal events and festivals
        """,
        expected_output="""
        A personalized itinerary of activities and attractions with:
        - Descriptions
        - Locations
        - Reservation/ticket information if needed
        """,
        agent=guide_expert,
        output_file='guide_report.md',
    )

    # Planner Task
    planner_task = Task(
        description=f"""
        Create a comprehensive travel plan for:
        Destination city: {destination_city}
        Interests: {interests}
        Arrival Date: {date_from}
        Departure Date: {date_to}

        Include:
        - Introduction to the city (3 paragraphs)
        - Day-by-day itinerary
        - City layout and transportation tips
        """,
        expected_output="""
        A rich markdown document with:
        # Welcome to {destination_city}:
        - City introduction
        - Daily expenses overview
        - Key spots to visit

        # Travel Plan:
        - Detailed daily schedule
        - Time allocations
        - Activity details
        """,
        context=[location_task, guide_task],
        agent=planner_expert,
        output_file='travel_plan.md',
    )

    return location_task, guide_task, planner_task


if submit_button:
    with st.spinner("Creating your personalized travel plan..."):
        try:
            # Create tasks
            location_task, guide_task, planner_task = create_tasks(
                from_city, destination_city, date_from, date_to, interests
            )

            # Create and run crew
            crew = Crew(
                agents=[location_expert, guide_expert, planner_expert],
                tasks=[location_task, guide_task, planner_task],
                process=Process.sequential,
                verbose=True
            )

            result = crew.kickoff()

            # Display results
            st.success("Your travel plan is ready!")
            st.markdown(result)

            # Option to download the plan
            st.download_button(
                label="Download Travel Plan",
                data=result,
                file_name=f"{destination_city}_travel_plan.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your .env file and ensure your Google API key is valid")