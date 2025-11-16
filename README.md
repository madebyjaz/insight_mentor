# 📚 Insight Mentor 

<br/>


**Insight Mentor** is an AI-powered study companion that transforms dense class materials into clear, actionable learning resources.  
Upload your PDFs, lecture slides, or text — and Insight Mentor instantly generates:

-  Clean study notes  
-  Flashcards  
-  Quizzes  
-  Personalized study plans  


Built for college students, self-learners, and anyone who wants to study smarter, *not longer*.

---

## 🚀 Features

### 📝 Automatic Clean Study Notes  
Upload PDFs or text files and Insight Mentor breaks them down into clear, structured explanations.  
Perfect for long chapters, dense slides, and confusing textbook content.

### 🃏 Auto-Generated Flashcards  
Flashcards are created directly from your uploaded materials.  
Expand cards to reveal definitions, examples, and explanations.

### 🙋‍♀️ Mentor Mode  
Ask contextual questions like:  
> “Explain the most confusing concepts and quiz me on them.”

Insight Mentor uses your uploaded materials to teach *in context* — like a personal AI tutor.

### 📅 Personalized Study Plans  
Daily study plans are generated based on your weaknesses, mastery levels, and topic complexity.

### 🧠 Concept Mastery Tracking  
Track your progress across topics you upload (e.g., Networking, Biology, Accounting).

### 📤 Upload Support  
- PDFs  
- PowerPoints (exported to PDF)  
- Markdown  
- Plain text  

---
## 🧪 Using Insight Mentor
Not sure how a feature works? 

[Visit the project’s GitBook for full documentation →](https://insightmentor.gitbook.io/insightmentor-docs/)

---

## 🧩 How Does Insight Mentor Work?

### 1. **File Extraction**  
Insight Mentor accepts multiple file formats (PDF, Markdown, Text) and intelligently extracts raw text content. For PDFs, it uses **PyPDF2** to parse each page and concatenate the text, preserving structure while removing formatting artifacts. This ensures that lecture slides, textbooks, and study guides are ready for AI processing.

### 2. **Semantic Chunking & Structure Detection**  
The extracted text is analyzed to identify key structural elements—headings, bullet points, definitions, and concepts. This allows Insight Mentor to:
- Recognize topic boundaries and hierarchies
- Identify core concepts vs. supporting details
- Maintain context when breaking down long documents
- Preserve relationships between related ideas

### 3. **AI Generation** — Notes, Flashcards, Quizzes  
Using **OpenAI GPT-4o-mini** and **Google Gemini**, Insight Mentor generates three core study resources:

- **Study Notes**: Concise summaries that distill dense material into clear, digestible explanations
- **Flashcards**: Question-answer pairs focused on key concepts, definitions, and relationships
- **Quizzes**: Contextual questions designed to test understanding and reinforce learning

Each generation is powered by carefully crafted prompts that instruct the AI to act as an expert tutor, ensuring high-quality, educational output.

### 4. **Contextual Retrieval (Learn2Prompt Tutor Mode)**  
The **Prompt Tutor** feature provides major-specific prompt templates tailored to 11+ academic fields (Computer Science, Nursing, Business, Psychology, Biology, Chemistry, Math, Engineering, Law, Arts, and more). 

Students can:
- Select their major to see example prompts designed for their field
- Use custom prompts to ask questions about their uploaded materials
- Get contextual AI responses that reference their specific study content
- Learn effective prompting strategies (role + task + context + output format)

This transforms Insight Mentor into a personalized AI tutor that understands both the *subject matter* and the *student's field of study*.

### 5. **Mastery Model**  
Insight Mentor tracks your understanding of each concept through a **dynamic mastery scoring system**:
- Concepts start at 30% mastery when first extracted
- Generating study plans and completing quizzes updates mastery scores
- Progress bars visualize your confidence level for each topic
- The system prioritizes weaker concepts in future study plans


### 6. **Model Switching (OpenAI / Gemini)**  
Flexibility is built into the core architecture. Insight Mentor supports **dual AI providers**:
- **Google Gemini** (`gemini-flash-latest`) — Fast, cost-effective, set as default
- **OpenAI** (`gpt-4o-mini`) — High-quality fallback option

The system automatically handles API calls, rate limiting, and error recovery. Users can switch providers via the sidebar, and the app gracefully falls back to the alternative if one provider encounters issues.

---



## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Frontend UI | Streamlit |
| Backend | Python |
| AI Models | OpenAI GPT-4x, Gemini |
| Extraction | PyPDF, Unstructured |
| Embeddings | Local vector store |
| Deployment | Streamlit Cloud / Local |

---

## 🌍 Who Is This For?

- Students 
  - High School
  - College ( Pre-med, CS, Business, Nursing, etc. )
- Online learners 
- Educators 
- Bootcamps    

---

## 📈 Insight Mentor’s Impact 

- Cuts study prep time by 50–70%
    - One-click notes turn long PDFs/slides into 10–15 minute study blocks
    - Semantic chunking lets you study between classes, shifts, or club meetings

- Improves comprehension and retention
    - Mastery-aware flashcards evolve from definitions to application as you progress
    - Quizzes surface misconceptions; Mentor Mode explains concepts in plain language with examples

- Reduces stress and study burnout
    - Personalized plans stack realistic 10–20 minute tasks with clear priorities
    - Progress bars and trend arrows show momentum and growth over time

- Fits real student life
    - Accepts PDFs, exported slides, Markdown, and plain text—keep all materials in one place
    - Major-aware prompts tailor explanations to your field (CS, Nursing, Business, etc.)
    - Contextual retrieval focuses answers on your uploaded content, not generic web info

- Converts overwhelm into a clear learning path
    - “What to study next” is always visible; weaker concepts are auto-prioritized
    - Structured notes (Section → Key Idea → Explanation) keep review focused

- Polished, practical UX
    - Clean UI with quick regenerate options for notes, flashcards, and quizzes
    - Reliable model switching and transparent logs keep sessions stable and recoverable


---

## 🙏 Acknowledgments

Thanks to:

- CS Girlies  
- Gitbook
- GitHub Copilot
- OpenAI & Google AI APIs  


Feel free to reach out for collaborations or improvements! 💜
