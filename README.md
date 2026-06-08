# The Unofficial Guide — Project 1



A Retrieval-Augmented Generation (RAG) chatbot that helps Georgia State University Computer Science students search professor reviews, course advice, workload discussions, and student recommendations using semantic search and grounded AI responses.



Technologies:

\- Python

\- ChromaDB

\- Sentence Transformers

\- Groq

\- Gradio

## Domain

This system covers Georgia State University Computer Science professor reviews and student course advice.



This knowledge is valuable because official course descriptions do not explain teaching style, exam difficulty, workload, grading policies, communication quality, or how helpful a professor is. Students typically rely on Reddit discussions, peer recommendations, and review websites to make registration decisions.



The goal of this system is to make student-generated knowledge searchable through natural language questions so students can quickly find information about professors, courses, and workload expectations.

## Document Sources



|#|Source|Type|URL or file path|
|-|-|-|-|
|1|CS Professors and Their Courses Rate|Reddit Discussion|documents/source\_01\_cs\_professors.txt|
|2|GSU CS Program Discussion|Reddit Discussion|documents/source\_02\_cs\_program.txt|
|3|Data Structures Recommendations|Reddit Discussion|documents/source\_03\_data\_structures.txt|
|4|Machine Learning Course Discussion|Reddit Discussion|documents/source\_04\_machine\_learning.txt|
|5|Professor Feedback Discussions|Reddit Discussion|documents/source\_05\_professor\_feedback.txt|
|6|Rate My Professor Review Set 1|Review Collection|documents/source\_06\_rmp\_reviews.txt|
|7|Rate My Professor Review Set 2|Review Collection|documents/source\_07\_rmp\_reviews.txt|
|8|Student Course Advice Notes|Student Advice|documents/source\_08\_course\_advice.txt|
|9|CS Registration Advice Thread|Student Advice|documents/source\_09\_registration\_advice.txt|
|10|CS Workload Discussion|Student Advice|documents/source\_10\_workload.txt|



## Chunking Strategy

**Chunk size:300 characters**

**Overlap: 50 characters**

**Why these choices fit your documents: Most documents consist of short student reviews, recommendations, and discussion posts. A 300-character chunk preserves enough context to capture a complete opinion while remaining focused enough for semantic retrieval. A 50-character overlap helps prevent information loss when important ideas occur near chunk boundaries.**

**Preprocessing:**



**Loaded plain text files from the documents folder**

**Removed empty lines**

**Preserved source metadata for retrieval attribution**



**Final chunk count: 26 chunks**



## Embedding Model

**Model used:** all-MiniLM-L6-v2 (Sentence Transformers)



I selected all-MiniLM-L6-v2 because it is lightweight, fast, free to use locally, and performs well for semantic similarity tasks. It is commonly used in retrieval-augmented generation systems because it balances retrieval quality with computational efficiency.



**Production tradeoff reflection:**



If I were deploying this system for real users and cost was not a constraint, I would evaluate larger embedding models with higher retrieval accuracy. I would consider tradeoffs including context length, multilingual support, performance on educational and review-based text, inference latency, and infrastructure cost. Larger models may improve retrieval quality but would require more compute resources and increase response time.

## Grounded Generation

**System prompt grounding instruction**:



The system prompt instructs the model to answer questions using only the retrieved context. It explicitly tells the model not to use outside knowledge, not to guess, and to respond with "I don't have enough information in the documents to answer that" whenever the retrieved context is insufficient.



Retrieved chunks are formatted into a context block and passed directly to the model. Only the top retrieved chunks are included in the prompt.



**How source attribution is surfaced in the response:**



Each retrieved chunk includes source metadata. The application displays the source document names alongside generated answers, allowing users to identify where information originated. The prompt also instructs the model to reference source documents when generating responses

## Evaluation Report

|#|Question|Expected answer|System response (summarized)|Retrieval quality|Response accuracy|
|-|-|-|-|-|-|
|1|What do students value most in CS professors?|Clear lectures, useful feedback, communication, fair exams, office hours|Reported insufficient information|Relevant|Inaccurate|
|2|What do students say about Data Structures professors?|Assignment quality, exam fairness, workload, coding support|Identified assignment quality, exam fairness, and practical coding skills|Relevant|Accurate|
|3|What makes a CS professor difficult according to students?|Unclear teaching, hard exams, poor communication, heavy workload|Reported insufficient information|Partially Relevant|Inaccurate|
|4|What do students say about Machine Learning coursework?|Projects are useful but challenging; difficulty depends on math background|Identified project usefulness and importance of feedback|Relevant|Accurate|
|5|What advice do students give for choosing CS courses?|Compare professors, manage workload, plan schedules carefully|Identified workload management, professor research, and course planning|Relevant|Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate
Overall Accuracy: 60% (3/5)



The system performed best when documents contained direct statements related to the query. Questions that required broader synthesis across multiple documents were more likely to fail because the required information was not explicitly represented in the source documents.

## Failure Case Analysis

**Question that failed:** What do students value most in CS professors?



**What the system returned:** "I don't have enough information in the documents to answer that."



**Root cause (tied to a specific pipeline stage):**



The retrieval stage returned partially relevant chunks, but none of the source documents explicitly summarized what students value most in professors. The information existed indirectly across multiple documents, but not in a single chunk. Because the generation stage was instructed not to infer beyond retrieved evidence, it correctly refused to answer.

**What you would change to fix it:** I would add additional source documents containing direct student discussions about professor preferences and improve chunking to preserve more context. I would also experiment with retrieving more than three chunks to improve evidence coverage.



## Spec Reflection

Reflect on how planning.md shaped your implementation.

**One way the spec helped you during implementation:** The planning.md document helped define the architecture, chunking strategy, evaluation questions, and retrieval approach before implementation began. Having these decisions documented made it easier to generate and verify code for each stage of the pipeline.

**One way your implementation diverged from the spec, and why:** My original plan assumed that retrieval alone would provide enough information for all evaluation questions. During testing, I discovered that some questions failed because the source documents lacked explicit information. As a result, I expanded the document collection and adjusted the evaluation expectations to better reflect the available evidence.



## AI Usage

**Instance 1**

* *What I gave the AI:* **I provided the Chunking Strategy section from planning.md and described my requirement for 300-character chunks with 50-character overlap.**
* *What it produced:* **The AI generated a chunk\_text() function that split documents into overlapping character-based chunks.**
* *What I changed or overrode:* **I reviewed the output and tested it on my documents to ensure chunks were being generated correctly and preserved enough context for retrieval.**

**Instance 2**

* *What I gave the AI:* **I provided the Retrieval Approach section and requested code that used ChromaDB and all-MiniLM-L6-v2 embeddings to perform semantic retrieval.**
* *What it produced:* **The AI-generated code for embedding, storing, and retrieving chunks from a vector database.**
* *What I changed or overrode:* **I modified the retrieval workflow to include source metadata and tested retrieval quality using the evaluation questions defined in planning.md.**




#### **ALSO**



Sample Chunks



Chunk 1 — source\_01\_cs\_professors.txt



Students discussed their experiences with Georgia State CS professors and courses. Common themes included exam difficulty, teaching quality, workload, attendance requirements, and grading policies.



Chunk 2 — source\_03\_data\_structures.txt



Students frequently compare instructors based on assignment quality and exam fairness. Practical coding assignments are valued more than theoretical lectures.



Chunk 3 — source\_04\_machine\_learning.txt



Students value professors who provide detailed project feedback. Projects are often described as the most useful part of the course.



Chunk 4 — source\_08\_course\_advice.txt



Do not take multiple heavy programming courses during the same semester unless you have strong time management skills.



Chunk 5 — source\_10\_workload.txt



Data Structures is frequently described as one of the most time-consuming courses. Students recommend starting assignments early.







Retrieval Test Results



Query 1



Question:

What do students say about Data Structures professors?



Top Retrieved Chunks:



\* source\_03\_data\_structures.txt

\* source\_06\_rmp\_reviews.txt

\* source\_10\_workload.txt



Why Retrieval Was Relevant:

The returned chunks contained direct references to Data Structures instructors, assignment quality, exam fairness, workload, and practical coding skills.



Query 2



Question:

What advice do students give for choosing CS courses?



Top Retrieved Chunks:



\* source\_08\_course\_advice.txt

\* source\_09\_registration\_advice.txt

\* source\_10\_workload.txt



Why Retrieval Was Relevant:

The retrieved chunks directly discussed course selection, workload management, registration planning, and professor research.



Query 3



Question:

What do students value most in CS professors?



Top Retrieved Chunks:



\* source\_01\_cs\_professors.txt

\* source\_02\_cs\_program.txt

\* source\_10\_workload.txt



Result:

The retrieval was only partially successful because none of the documents explicitly summarized what students value most in professors.





Example Responses



Example Response 1



Question:

What do students say about Data Structures professors?



Response:

Students frequently compare instructors based on assignment quality and exam fairness. Students also value practical coding skills and real-world examples.



Sources:



\* source\_03\_data\_structures.txt

\* source\_06\_rmp\_reviews.txt



Example Response 2



Question:

What advice do students give for choosing CS courses?



Response:

Students recommend researching professors before registration, balancing difficult courses with lighter electives, and avoiding too many heavy programming classes in one semester.



Sources:



\* source\_08\_course\_advice.txt

\* source\_09\_registration\_advice.txt



Out-of-Scope Query



Question:

Who won the 2025 Super Bowl?



Response:

I don't have enough information in the documents to answer that.



Reason:

The question is outside the scope of the professor review document collection.





Query Interface



Input:



\* User question textbox



Output:



\* Generated answer

\* Source document list



Sample Interaction:



User:

What do students say about Machine Learning coursework?



System:

Students describe projects as useful but challenging and appreciate professors who provide detailed project feedback.



Sources:



\* source\_04\_machine\_learning.txt

\* source\_06\_rmp\_reviews.txt



