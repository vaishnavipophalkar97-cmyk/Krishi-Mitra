# 🌾 KrishiAI Pro: Advanced Farm Intelligence Hub

KrishiAI Pro is an AI-powered, localized digital assistant hub engineered to empower farmers with real-time, actionable insights. Built for a 5-hour hackathon, this application integrates multimodal computer vision for plant pathology, localized predictive climate threat analysis, and a stateful contextual chat engine—all tailored dynamically to the farmer's profile.

---

## 🚀 Core Features

* **📸 Vision Diagnostics (Plant Pathology):** Upload leaf sample images to instantly analyze crop health. Powered by `gemini-2.5-flash`, the system returns structural diagnosis, concrete treatment protocols, and a numerical model confidence percentage.
* **🌤️ Predictive Weather Advisory:** Analyzes current meteorological anomalies against the farmer's specific crop and location, generating immediate emergency field directives and irrigation adjustments.
* **💬 Contextual Knowledge Agent (Chatbot):** A stateful chat companion that remembers historical conversation threads and automatically personalizes its agricultural advice based on the farmer's profile data.
* **🌐 Multi-Language Localization:** Supports dynamic interface switching between English, Hindi, Punjabi, and Spanish.
* **🗄️ Cloud Profile Persistence:** Uses Firebase Firestore to store and update unique user metrics (soil variant, region, primary crop) which are automatically injected into the AI context window.

---

## 🏗️ Technical Architecture & Data Flow

1.  **User Authentication & Session:** The application loads a unique Farmer ID via the Streamlit interface.
2.  **Profile Synchronization:** Profile edits (e.g., changing soil type from Loam to Clay) are committed via the `firebase-admin` SDK to an online cloud Google Firestore database instance.
3.  **Context-Aware AI Generation:** When generating weather updates or chatting, the backend fetches the user's latest cloud profile data, bundles it as a system instruction metadata block, and pipes it directly into the Gemini API.
4.  **Structured JSON Pipelines:** The application forces Gemini to return strict, unmarred JSON schemas, allowing the frontend to cleanly map metrics, severity levels, and arrays into customized UI container cards.

---
## 🏗️ System Architecture

KrishiMitra follows a lightweight, modular AI-assisted architecture built with Python and Streamlit.

```text
                    ┌─────────────────────────┐
                    │       👨‍🌾 Farmer        │
                    │   Web-based Interface   │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     🌾 Streamlit UI     │
                    │                         │
                    │ • Farmer Profile        │
                    │ • Disease Detection     │
                    │ • Weather Advisory      │
                    │ • AI Chat Companion     │
                    └────────────┬────────────┘
                                 │
                 ┌───────────────┼────────────────┐
                 │               │                │
                 ▼               ▼                ▼
        ┌────────────────┐ ┌──────────────┐ ┌────────────────┐
        │ 🩺 Crop Health │ │ 🌦️ Weather   │ │ 🤖 KrishiAI    │
        │    Analyzer    │ │   Advisory   │ │     Chat       │
        └───────┬────────┘ └──────┬───────┘ └───────┬────────┘
                │                 │                 │
                └─────────────────┼─────────────────┘
                                  ▼
                    ┌─────────────────────────┐
                    │       🧠 Gemini AI      │
                    │                         │
                    │ • Image Analysis        │
                    │ • Advisory Generation   │
                    │ • Conversational AI     │
                    └─────────────────────────┘

                         Farmer Profile
                              │
                              ▼
                    ┌─────────────────────────┐
                    │    🔥 Firebase          │
                    │       Firestore         │
                    │                         │
                    │ • Farmer Information    │
                    │ • Region                │
                    │ • Primary Crop          │
                    │ • Soil Type             │
                    └─────────────────────────┘
