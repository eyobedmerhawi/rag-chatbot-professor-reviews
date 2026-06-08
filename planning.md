# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

\---

## Domain

My domain is Georgia State University Computer Science professor reviews.



This knowledge is valuable because official course descriptions do not explain teaching style, exam difficulty, grading policies, workload, or how helpful a professor is. Students usually rely on Reddit posts, Rate My Professor reviews, Discord conversations, and peer advice to decide which professor or course section to take.



Documents



|#|Source|Description|URL or location|
|-|-|-|-|
|1|Reddit|CS Professors and Their Courses Rate \| Student discussion about CS professors, course difficulty, and registration advice|documents/source\_01\_cs\_professors.txt|
|2|Reddit|GSU CS Program Discussion \| Student opinions about the overall CS program, internships, and self-learning|documents/source\_02\_cs\_program.txt|
|3|Reddit|Data Structures Recommendations \| Student feedback about Data Structures professors, exams, and assignments|documents/source\_03\_data\_structures.txt|
|4|Reddit|Machine Learning Course Discussion \| Student comments about machine learning workload, projects, and grading|documents/source\_04\_machine\_learning.txt|
|5|Reddit|Professor Feedback Discussions \| Student comments about office hours, communication, and assignment feedback|documents/source\_05\_professor\_feedback.txt|
|6|Rate My Professor Review Set 1|Professor review comments about clarity, difficulty, and grading|documents/source\_06\_rmp\_reviews.txt|
|7|Rate My Professor Review Set 2|Additional professor review comments about exams and workload|documents/source\_07\_rmp\_reviews.txt|
|8|Student Course Advice Notes|Informal student advice about choosing CS sections|documents/source\_08\_course\_advice.txt|
|9|CS Registration Advice Thread|Student discussion about which courses and professors to avoid or prioritize|documents/source\_09\_registration\_advice.txt|
|10|CS Workload Discussion|Student comments about workload, projects, and balancing CS courses|documents/source\_10\_workload.txt|

\---

## Chunking Strategy

**Chunk size: 300 characters**

**Overlap: 50 characters**

**Reasoning:** Most of my documents are short student reviews or informal comments. A 300-character chunk is large enough to preserve context around one opinion, such as exam difficulty, grading, or teaching style, while still being focused enough for semantic search. The 50-character overlap helps if a useful sentence or professor comment gets split between two chunks.



\---

## Retrieval Approach

**Embedding model: all-MiniLM-L6-v2 using sentence-transformers**

**Top-k: 3**

**Production tradeoff reflection: I chose all-MiniLM-L6-v2 because it runs locally, is free, and is fast enough for a student project. In production, I would compare larger embedding models for better accuracy, longer context length, stronger multilingual support, and better handling of informal student language. I would also consider cost, latency, and whether the model should run locally or through an API.**



\---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.

|#|Question|Expected answer|
|-|-|-|
|1|What do students value most in CS professors at GSU?|Students value clear lectures, useful feedback, communication, fair exams, and helpful office hours.|
|2|What do students say about Data Structures professors?|Students compare professors based on assignment quality, exam fairness, workload, and practical coding support.|
|3|What makes a CS professor difficult, according to students?|Students mention unclear teaching, heavy workload, hard exams, slow communication, and limited feedback.|
|4|What do students say about Machine Learning coursework?|Students describe projects as useful but challenging, and say the course difficulty depends on their math background and the professor's communication.|
|5|What advice do students give for choosing CS courses?|Students recommend checking reviews, comparing professors, planning workload carefully, and doing projects or internships outside class.|

\\---

## Anticipated Challenges

1. Student reviews are noisy and subjective. Different students may disagree about the same professor, so the system may retrieve conflicting opinions.
2. Some documents may be too short or too general. If chunks do not include enough context, retrieval may return broad CS program advice instead of professor-specific feedback.

\\---

## Architecture

```text

Raw student documents

\&#x20;       |

\&#x20;       v

Document Ingestion

(load .txt files from documents/)

\&#x20;       |

\&#x20;       v

Cleaning + Preprocessing

(remove empty lines, extra spaces, and unrelated text)

\&#x20;       |

\&#x20;       v

Chunking

(300 characters, 50 character overlap)

\&#x20;       |

\&#x20;       v

Embedding

(sentence-transformers: all-MiniLM-L6-v2)

\&#x20;       |

\&#x20;       v

Vector Store

(ChromaDB with source metadata)

\&#x20;       |

\&#x20;       v

Retrieval

(top-k = 3 relevant chunks)

\&#x20;       |

\&#x20;       v

Generation

(Groq llama-3.3-70b-versatile, grounded prompt with citations)

\&#x20;       |

\&#x20;       v

User Interface

(simple Gradio query app)---

## AI Tool Plan

\*\*Milestone 3 — Ingestion and chunking: I will use ChatGPT to help implement the document loading and chunking code. I will provide the Documents section, Chunking Strategy section, and Architecture diagram. I expect it to generate Python functions that load text files, clean them, and split them into 300-character chunks with 50-character overlap. I will verify the output by inspecting sample chunks and confirming they are readable and self-contained.\*\*

\*\*Milestone 4 — Embedding and retrieval: I will use ChatGPT to help implement ChromaDB storage and retrieval. I will provide the Retrieval Approach section and ask for code that embeds chunks using all-MiniLM-L6-v2, stores metadata, and retrieves the top 3 most relevant chunks. I will verify the output by testing retrieval on my evaluation questions.\*\*

\*\*Milestone 5 — Generation and interface: I will use ChatGPT to help implement grounded response generation and a Gradio interface. I will provide the grounding requirements from the project instructions and ask for code that uses Groq to answer questions only from retrieved context. I will verify this by testing both in-scope and out-of-scope questions.\*\*


