import streamlit as st
from typing import Dict, List

from app_logic.content_analyser import (
    llm_call,
    summarize_content,
    extract_concepts,
    generate_flashcards,
    FlashcardGen,
)
from app_logic.tutor_assistant import (
    generate_study_plan,
    generate_quiz,
    update_mastery,
)

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

st.set_page_config(
    page_title="Insight Mentor – Your Virtual Study Buddy",
    layout="wide",
    page_icon="📚",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern dark mode styling
st.markdown("""
<style>
    /* Main theme colors - Dark Mode Optimized */
    :root {
        --primary-gradient-start: #7c3aed;
        --primary-gradient-end: #c4b5fd;
        --background-primary: #0f172a;
        --background-secondary: #1e293b;
        --background-tertiary: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #cbd5e1;
        --border-color: #475569;
        --accent-glow: rgba(124, 58, 237, 0.3);
    }
    
    /* Main app background - Dynamic gradient with attention-holding colors */
    .stApp {
        background: 
            radial-gradient(ellipse at top left, rgba(124, 58, 237, 0.15) 0%, transparent 50%),
            radial-gradient(ellipse at top right, rgba(236, 72, 153, 0.12) 0%, transparent 50%),
            radial-gradient(ellipse at bottom left, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, #0a0e27 0%, #1a1038 25%, #0f172a 50%, #1e1b4b 75%, #0d1224 100%);
        background-size: 100% 100%;
        background-attachment: fixed;
    }
    
    /* Subtle animated gradient overlay for depth */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 30%, rgba(124, 58, 237, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(196, 181, 253, 0.06) 0%, transparent 40%);
        pointer-events: none;
        animation: gradientShift 15s ease infinite;
        z-index: 0;
    }
    
    @keyframes gradientShift {
        0%, 100% {
            opacity: 0.7;
            transform: scale(1);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Content container background */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Modern card styling - Dark Mode */
    .stExpander {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.15) 0%, rgba(196, 181, 253, 0.15) 100%);
        border: 1px solid rgba(124, 58, 237, 0.3);
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .streamlit-expanderHeader {
        background: transparent;
        color: #f1f5f9 !important;
        border-radius: 16px;
        font-weight: 600;
        padding: 1rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(124, 58, 237, 0.2);
    }
    
    .streamlit-expanderContent {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 0 0 16px 16px;
        color: #cbd5e1;
    }
    
    /* Button styling - Vibrant gradient */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #c4b5fd 100%);
        color: white;
        border-radius: 30px;
        padding: 0.875rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        border: none;
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.5);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 40px rgba(196, 181, 253, 0.7);
        background: linear-gradient(135deg, #8b5cf6 0%, #ddd6fe 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* Text area styling - Dark */
    .stTextArea textarea {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 16px;
        border: 2px solid rgba(124, 58, 237, 0.3);
        color: #f1f5f9;
        transition: all 0.3s ease;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #7c3aed;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
        background: rgba(15, 23, 42, 0.95);
    }
    
    .stTextArea label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* File uploader styling - Dark */
    .stFileUploader {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 16px;
        padding: 2rem;
        border: 2px dashed rgba(124, 58, 237, 0.4);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #7c3aed;
        background: rgba(30, 41, 59, 0.8);
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.2);
    }
    
    .stFileUploader label {
        color: #e2e8f0 !important;
        font-weight: 600;
    }
    
    /* Info/Success/Warning boxes - Dark */
    .stAlert {
        border-radius: 12px;
        border: none;
        backdrop-filter: blur(10px);
    }
    
    div[data-baseweb="notification"] {
        background: rgba(30, 41, 59, 0.9);
        border-left: 4px solid #7c3aed;
        border-radius: 12px;
    }
    
    /* Progress bar - Animated gradient */
    .stProgress > div > div {
        background: linear-gradient(90deg, #7c3aed 0%, #c4b5fd 50%, #7c3aed 100%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
        border-radius: 10px;
    }
    
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    /* Headers - Glowing gradient text */
    h1 {
        font-weight: 900;
        margin-bottom: 1.5rem;
        color: #f1f5f9;
    }
    
    /* Apply gradient only to text content, not emojis */
    h1 {
        background: linear-gradient(135deg, #7c3aed 20%, #c4b5fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Restore emoji color */
    h1::before {
        -webkit-text-fill-color: initial;
    }
    
    h2, h3 {
        color: #f1f5f9;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Subheader styling */
    .stMarkdown h2, .stMarkdown h3 {
        border-bottom: 2px solid rgba(124, 58, 237, 0.3);
        padding-bottom: 0.5rem;
    }
    
    /* Sidebar styling - Deep purple gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #581c87 100%);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    /* Concept tags - Neon pills */
    code {
        background: linear-gradient(135deg, #7c3aed 0%, #c4b5fd 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: inline-block;
        margin: 0.25rem;
    }
    
    /* Radio buttons - Dark mode cards */
    .stRadio > div {
        background: rgba(30, 41, 59, 0.6);
        padding: 1rem;
        border-radius: 12px;
    }
    
    .stRadio > div > label {
        background: rgba(124, 58, 237, 0.1);
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        border: 1px solid rgba(124, 58, 237, 0.3);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stRadio > div > label:hover {
        background: rgba(124, 58, 237, 0.2);
        border-color: #7c3aed;
        transform: translateX(5px);
    }
    
    /* General text color */
    p, li, span, div {
        color: #cbd5e1;
    }
    
    /* Strong/bold text */
    strong {
        color: #f1f5f9;
        font-weight: 700;
    }
    
    /* Caption text */
    .stCaption {
        color: #94a3b8 !important;
        font-style: italic;
    }
    
    /* Divider */
    hr {
        border-color: rgba(124, 58, 237, 0.3);
        margin: 2rem 0;
    }
    
    /* Markdown lists */
    ul, ol {
        color: #cbd5e1;
    }
    
    /* Input fields */
    input {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid rgba(124, 58, 237, 0.3) !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
    }
    
    input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2) !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #7c3aed 0%, #c4b5fd 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #8b5cf6 0%, #ddd6fe 100%);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Session state helpers
# -----------------------------------------------------------------------------
def init_session_state():
    if "raw_text" not in st.session_state:
        st.session_state.raw_text = ""
    if "summary" not in st.session_state:
        st.session_state.summary = ""
    if "concepts" not in st.session_state:
        st.session_state.concepts = []  # type: List[str]
    if "flashcards" not in st.session_state:
        st.session_state.flashcards = []  # type: List[FlashcardGen]
    if "study_plan" not in st.session_state:
        st.session_state.study_plan = []
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "mastery" not in st.session_state:
        st.session_state.mastery = {}  # type: Dict[str, float]
    if "model_provider" not in st.session_state:
        st.session_state.model_provider = "Gemini"

init_session_state()

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title(" Insight Mentor")
    st.markdown(
        """
        **Tips to Get Started**

        1. Paste your notes or reading.
        2. Generate a summary & flashcards.
        3. Get a personalized study plan & quiz.
        """
    )

    st.subheader("⚙️ Model Provider")

    provider_choice = st.radio(
        "Choose your AI engine:",
        options=["OpenAI", "Gemini"],
        index=1 if st.session_state.model_provider == "Gemini" else 0,
        help="Switch between OpenAI and Gemini for summary/flashcards.",
    )
    st.session_state.model_provider = provider_choice

    st.caption(
        "Tip: OpenAI is great for very polished summaries. "
        "Gemini is much more faster."
    )

    st.markdown("A fast easy learning solution designed for students ✨")

# -----------------------------------------------------------------------------
# Main layout
# -----------------------------------------------------------------------------
# Split emoji and text to apply gradient only to text
st.markdown('<h1><span style="filter: none; -webkit-text-fill-color: initial; color: initial; background: none; -webkit-background-clip: initial; background-clip: initial;">📚</span> <span style="background: linear-gradient(135deg, #c4b5fd 0%, #f5f5f0 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Insight Mentor – Your Virtual Study Buddy</span></h1>', unsafe_allow_html=True)

col_input, col_output = st.columns([1, 1.2])

# ---------------------- Input Column ----------------------
with col_input:
    st.subheader("Drop in your study materials to get started 📥")

    # File upload option
    uploaded_file = st.file_uploader(
        label="Upload files here (PDF, Markdown, or Text):",
        type=["pdf", "md", "txt"],
        help="Upload your study material as a file",
    )

    # Handle file upload
    if uploaded_file is not None:
        try:
            if uploaded_file.type == "application/pdf":
                # For PDF files, we'll need PyPDF2 or similar
                import PyPDF2
                import io
                
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                text_from_file = ""
                for page in pdf_reader.pages:
                    text_from_file += page.extract_text()
                st.session_state.raw_text = text_from_file
                st.success(f"Loaded {len(pdf_reader.pages)} pages from PDF")
            else:
                # For txt and md files
                text_from_file = uploaded_file.read().decode("utf-8")
                st.session_state.raw_text = text_from_file
                st.success(f"Loaded {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    text = st.text_area(
        "Or paste your text here:",
        value=st.session_state.raw_text,
        height=250,
        placeholder="...paste your study notes or reading material here...",
    )

    if st.button("Generate Study Notes & Flashcards 💜"):
        if not text.strip():
            st.warning("Error‼️ Please upload your docs or paste your text first.")
        else:
            st.session_state.raw_text = text

            provider_key = (
                "openai" if st.session_state.model_provider == "OpenAI" else "gemini"
            )

            with st.spinner(
                f"Thanks! Now analyzing your content with {st.session_state.model_provider}✨… "
            ):
                summary = summarize_content(text, provider=provider_key)
                concepts = extract_concepts(text, provider=provider_key)
                flashcards = generate_flashcards(text, concepts, provider=provider_key)

            st.session_state.summary = summary
            st.session_state.concepts = concepts
            st.session_state.flashcards = flashcards

            # Initialize mastery for new concepts if not present
            for c in concepts:
                st.session_state.mastery.setdefault(c, 0.3)  # starting confidence

            st.success("Great news! Study Notes & Flashcards have been generated ☺️")

    st.markdown("---")
    st.subheader("Generate a Personalized Study Plan & a Quick Quiz")

    if st.button("🎓 Generate Study Plan & Quiz"):
        if not st.session_state.concepts:
            st.warning("Generate Study Notes first so I know what you’re studying.")
        else:
            with st.spinner("Got it! Building your personalized study plan 💜…"):
                plan = generate_study_plan(
                    st.session_state.concepts,
                    st.session_state.mastery,
                )
                quiz = generate_quiz(
                    st.session_state.concepts,
                    st.session_state.raw_text,
                )
                # Simple mastery update: treat this as a completed study session
                st.session_state.mastery = update_mastery(
                    st.session_state.mastery,
                    st.session_state.concepts,
                )

            st.session_state.study_plan = plan
            st.session_state.quiz_questions = quiz
            st.success("Your study plan & quiz have been generated!")

    # -------------------------------------------------------------------------
    # Prompt Tutor – major-specific example prompts
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("🧠 Learn2Prompt – Ask Better Questions About Your Study Notes")

    if not st.session_state.raw_text:
        st.info("Upload your study materials & generate Study Notes first to see prompt ideas.")
    else:
        st.markdown(
            "Good prompts usually include: **role + task + context + output format**.\n"
            "Pick your major (or the closest one) to see smart example prompts you can use with your notes."
        )

        major = st.selectbox(
            "Choose your major (or closest field):",
            [
                "Computer Science",
                "Nursing",
                "Business / Management",
                "Psychology",
                "Biology / Pre-Med",
                "Chemistry",
                "Math",
                "Engineering",
                "Law / Criminal Justice",
                "Arts / Humanities",
                "General / Other",
            ],
        )

        major_prompts: Dict[str, Dict[str, str]] = {
            "Computer Science": {
                "Explain core concepts simply":
                    "Explain these notes like you're a senior software engineer teaching an intern. "
                    "Use simple analogies, text-based diagrams, and real-world coding examples.",
                "Algorithms / data structures focus":
                    "Identify the algorithms or data structures mentioned in these notes and explain when to use each one. "
                    "Give at least one coding example per concept.",
                "Interview-style practice":
                    "Based on these notes, create 5 technical interview–style questions and include ideal answers with time and space complexity where relevant.",
                "System design thinking":
                    "Based on this material, describe how the concepts would fit into a real system design. Include components, data flow, and tradeoffs.",
            },
            "Nursing": {
                "Clinical explanation":
                    "Explain these notes as if you're teaching a first-year nursing student during clinicals. "
                    "Include symptoms, assessment steps, and safety precautions.",
                "NCLEX-style questions":
                    "Turn these notes into NCLEX-style multiple choice questions. For each question, provide rationales for why each answer is correct or incorrect.",
                "Care plan creation":
                    "Create a patient care plan from these notes. Include assessment, priority nursing diagnoses, interventions, and expected outcomes.",
                "Clinical scenario practice":
                    "Create a real-world clinical scenario based on these notes and ask me 3 critical thinking questions about it.",
            },
            "Business / Management": {
                "Explain with real companies":
                    "Explain the business concepts in these notes using real-world examples from well-known companies. "
                    "Keep it practical and easy to understand.",
                "Case study mode":
                    "Turn these notes into a business case study with a problem statement, stakeholders, constraints, and possible strategies.",
                "Exam-style questions":
                    "Produce 5 short-answer exam questions based on these notes, along with model answers.",
                "Cross-functional thinking":
                    "Show how these notes apply to marketing, finance, and operations. Give one concrete example for each area.",
            },
            "Psychology": {
                "Everyday behavior examples":
                    "Explain these psychological concepts using real-world behaviors and examples from everyday life.",
                "Compare and contrast theories":
                    "Identify theories in these notes that are often confused. Create a compare/contrast chart with key differences and memory tricks.",
                "Research design":
                    "Turn these notes into a research hypothesis and describe how you would design an experiment to test it.",
                "Reflective questions":
                    "Generate 3 reflective questions that help me connect these psychological concepts to personal experience.",
            },
            "Biology / Pre-Med": {
                "Analogy-based explanation":
                    "Explain these biology concepts using analogies (for example, a cell is like a factory). "
                    "Focus on what happens, where it happens, and why it matters.",
                "ASCII pathway diagram":
                    "Create a simple ASCII diagram that represents the biological process described in these notes. Label each step clearly.",
                "MCAT-style questions":
                    "Turn these notes into 3 MCAT-style questions with detailed reasoning for each answer.",
                "Pathway breakdown":
                    "Break down the biological pathway in these notes into inputs, steps, outputs, and regulation points.",
            },
            "Chemistry": {
                "Mechanism explanation":
                    "Explain the chemical reaction mechanisms in these notes using step-by-step descriptions as if drawing curly arrows.",
                "Lab prep and safety":
                    "Based on these notes, describe the key safety risks, PPE, and proper lab procedures to follow.",
                "Stoichiometry / reaction practice":
                    "Turn the concepts in these notes into 5 stoichiometry or reaction-mechanism quiz questions with answers.",
            },
            "Math": {
                "Intuitive understanding":
                    "Explain these mathematical ideas using geometric intuition and simple visual analogies.",
                "Practice problems with solutions":
                    "Generate 5 practice problems similar to the concepts in these notes and include full worked solutions.",
                "Proof techniques":
                    "Identify the proof techniques implied in these notes and show one clear example of each technique using similar content.",
            },
            "Engineering": {
                "Systems view":
                    "Explain how the concepts in these notes fit into an engineering system. Include components, forces/flows, and potential failure points.",
                "Engineering problem set":
                    "Create 3 engineering problems based on this material and include step-by-step solutions.",
                "Real-world applications":
                    "Give real-world engineering applications for each major concept in these notes.",
            },
            "Law / Criminal Justice": {
                "Plain-language explanation":
                    "Explain the legal concepts in these notes using real case examples and plain language.",
                "IRAC practice":
                    "Turn these notes into 3 IRAC-style legal analysis exercises. For each, provide a brief model answer.",
                "Essay-style exam prep":
                    "Generate 5 essay-style exam questions from these notes and include a short outline for each ideal answer.",
            },
            "Arts / Humanities": {
                "Theme interpretation":
                    "Explain the main themes in these notes and how they relate to larger historical or cultural contexts.",
                "Essay prompt and thesis help":
                    "Create 3 essay prompts based on these notes, along with sample thesis statements I could use.",
                "Compare to other works":
                    "Compare the ideas in these notes to another major work or thinker in the field, pointing out similarities and differences.",
            },
            "General / Other": {
                "Explain simply":
                    "You are a friendly tutor. Explain the most important ideas from these notes in simple terms that a first-year college student could understand. Use short bullet points and one real-life example.",
                "Exam-like practice":
                    "Create 3–5 exam-style questions based on these notes and include model answers.",
                "Flashcards from notes":
                    "Create flashcards from these notes. Format them as 'Q: ...' and 'A: ...'. Focus on one concept or definition per card.",
                "Deep dive on a confusing concept":
                    "I am confused about one key concept in these notes. Ask me which one, then explain it in three levels: ELI5, normal explanation, and exam-level detail, followed by 2 practice questions.",
            },
        }

        prompts_for_major = major_prompts.get(major, major_prompts["General / Other"])

        for label, prompt_text in prompts_for_major.items():
            with st.expander(label):
                st.code(prompt_text, language="markdown")

        st.markdown("---")
        st.markdown("### Make it your own! ✍️")

        custom_prompt = st.text_area(
            "Need help better understanding a certain topic? Ask me a question (and I'll answer it best I can using the updated docs you provided):",
            height=120,
            placeholder="Example: Explain the most confusing part of these notes and quiz me on it.",
        )

        if st.button("Help Me Learn More Using My Notes 💜"):
            if not custom_prompt.strip():
                st.warning("Write a prompt first.")
            else:
                provider_key = (
                    "openai" if st.session_state.model_provider == "OpenAI" else "gemini"
                )
                with st.spinner(
                    f"Asking {st.session_state.model_provider} using your custom prompt…"
                ):
                    system_msg = "You are a helpful study tutor for college students."
                    full_prompt = (
                        f"{custom_prompt}\n\n"
                        "Here are my notes:\n"
                        f"{st.session_state.raw_text}"
                    )
                    response = llm_call(full_prompt, system_msg, provider=provider_key)

                st.subheader("🤖 Insight Mentor's Response")
                st.write(response)

# ---------------------- Output Column ----------------------
with col_output:
    st.subheader("📌 Study Notes")
    if st.session_state.summary:
        st.write(st.session_state.summary)
    else:
        st.info("Upload your lecture notes & other topics to generate Study Notes & see it here.")

    st.subheader("🧩 Key Concepts")
    if st.session_state.concepts:
        st.markdown(", ".join(f"`{c}`" for c in st.session_state.concepts))
    else:
        st.info("Key concepts will appear here after you generate Study Notes.")

    st.subheader("🃏 Flashcards")
    if st.session_state.flashcards:
        for i, card in enumerate(st.session_state.flashcards, start=1):
            with st.expander(f"Card {i}: {card.question}"):
                st.markdown(f"**Answer:** {card.answer}")
    else:
        st.info("Flashcards will appear here after you generate Study Notes.")

    st.subheader("🗺️ Today’s Study Plan")
    if st.session_state.study_plan:
        for task in st.session_state.study_plan:
            st.markdown(f"- **{task.title}** – ⏱ {task.estimated_time}")
            if task.description:
                st.caption(task.description)
    else:
        st.info("Generate a Study Plan to see it here.")

    st.subheader("📝 Quiz")
    if st.session_state.quiz_questions:
        for i, q in enumerate(st.session_state.quiz_questions, start=1):
            st.markdown(f"**Q{i}. {q.text}**")
    else:
        st.info("Your quiz will show up here once generated.")

    st.subheader("📊 Concept Mastery (Prototype)")
    if st.session_state.mastery:
        for concept, score in st.session_state.mastery.items():
            st.write(f"{concept}: {int(score * 100)}%")
            st.progress(min(max(score, 0.0), 1.0))
    else:
        st.info("Mastery scores will appear after you generate plans & quizzes.")