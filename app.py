from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Interview Chatbot", page_icon="🤖")
st.title("Interview Chatbot 🤖")
MAX_QUESTIONS = 5

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-3.5-turbo"
if "feedback_response" not in st.session_state:
    st.session_state.feedback_response = None

def complete_setup():
    st.session_state.setup_complete = True


@st.dialog("Feedback")
def show_feedback_dialog():
    if st.session_state.feedback_response is None:
        conversation_history = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
        feedback_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        system_prompt = """
You are an HR expert providing feedback on interviewee performance.
Follow this format:
Overall Score: //Your score \n
Feedback: //Your feedback
Give only the feedback without any additional commentary or explanations."""

        feedback_prompt = f"""
This is the interview you need to evaluate.
Keep in mind that you are only a tool and should not engage in any conversation. {conversation_history}"""

        try:
            with st.spinner("Generating your feedback..."):
                response = feedback_client.chat.completions.create(
                    model=st.session_state.openai_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": feedback_prompt},
                    ],
                    max_tokens=500,
                )
            st.session_state.feedback_response = response.choices[0].message.content
        except Exception as e:
            st.error(f"Failed to generate feedback: {e}")

    if st.session_state.feedback_response:
        st.write(st.session_state.feedback_response)

    if st.button("Close"):
        st.rerun()

if not st.session_state.setup_complete:
    st.subheader("Personal Information" , divider="rainbow")

    if "name" not in st.session_state: st.session_state.name = ""
    if "age" not in st.session_state: st.session_state.age = None
    if "experience" not in st.session_state: st.session_state.experience = "" 
    if "skills" not in st.session_state: st.session_state.skills = ""

    st.session_state.name = st.text_input(label="Name",max_chars=40, placeholder="Enter your name")
    st.session_state.age = st.number_input(label="Age", min_value=18, max_value=100, step=1, placeholder="Enter your age")
    st.session_state.experience = st.text_area(label="Experience", height=None, max_chars=200, placeholder="Describe your work experience")
    st.session_state.skills = st.text_area(label="Skills", height=None, max_chars=200, placeholder="List your skills")

    st.subheader("Company and Role Information" , divider="rainbow")

    if "level" not in st.session_state: st.session_state.level = "Entry-level"
    if "role" not in st.session_state: st.session_state.role = "Software Engineer"
    if "company" not in st.session_state: st.session_state.company = "Google"

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.level = st.radio("Choose level", key="visibility", options=["Entry-level", "Mid-level", "Senior-level"])
    with col2:
        st.session_state.role = st.selectbox("Choose role", options=["Software Engineer", "Data Scientist", "Product Manager"])

    st.session_state.company = st.selectbox("Choose company", options=["Google", "Amazon", "Microsoft", "Facebook", "Apple"])

    name_filled = bool(st.session_state.name.strip())

    if st.button("Start Interview Preparation", disabled=not name_filled):
        complete_setup()
        st.rerun()
    if not name_filled:
        st.warning("Please enter your name to continue.")
    if not st.session_state.experience.strip() or not st.session_state.skills.strip():
        st.warning("Filling in experience and skills will improve the quality of your interview preparation.")

    # Keep setup and chat modes strictly separate within a single run.
    st.stop()


if st.session_state.setup_complete:
    st.info("""
        Start by introducing yourself and providing some background information. 
        Then, you can ask me specific questions about interview preparation, 
            such as common interview questions for your role, tips for answering behavioral questions, 
            or advice on how to research the company before your interview. 
        I'm here to help you feel confident and prepared for your upcoming interview!""", icon="💡")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "system", 
             "content": 
             f"You are an HR executive preparing a candidate for an interview. "
             f"The candidate's name is {st.session_state.name}, they are {st.session_state.age} years old, "
             f"with experience in {st.session_state.experience} and skills in {st.session_state.skills}. "
             f"They are applying for a {st.session_state.level} {st.session_state.role} position at {st.session_state.company}. "
             f"Provide interview preparation advice and answer any questions they have about the interview process. "}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    can_ask = st.session_state.user_message_count < MAX_QUESTIONS
    input_placeholder = st.empty()
    prompt = None

    if can_ask:
        prompt = input_placeholder.chat_input(
            "Ask me anything about interview preparation!",
            max_chars=500,
        )

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state.openai_model,
                    messages=[
                        {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                    ],
                    stream=True,
                    max_tokens=500,
                )

                response = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.user_message_count += 1
        except Exception as e:
            st.error(f"Failed to get a response: {e}")

    can_ask = st.session_state.user_message_count < MAX_QUESTIONS
    if not can_ask:
        input_placeholder.empty()
        st.info("Interview complete. Review the conversation, then click Provide Feedback.")

        if st.button("Provide Feedback"):
            show_feedback_dialog()

if st.session_state.setup_complete:
    st.caption(f"Questions used: {st.session_state.user_message_count} / {MAX_QUESTIONS}")
