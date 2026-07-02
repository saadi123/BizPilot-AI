# 🚀 BizPilot AI

> **An AI-powered Multi-Agent Business Formation & Finance Architect built using Google ADK, MCP, and Large Language Models.**

BizPilot AI helps entrepreneurs design the optimal legal entity, tax strategy, accounting architecture, compliance roadmap, workforce model, and QuickBooks-ready financial setup—all through an intelligent multi-agent workflow.

---

# 📌 Problem Statement

Starting a business involves numerous decisions that require expertise from accountants, tax advisors, attorneys, and operations consultants.

Entrepreneurs often struggle with questions such as:

* Which legal entity should I choose?
* What registrations are required?
* Which tax forms must be filed?
* Which authorities receive each filing?
* Which accounting software should I use?
* Should I hire employees or contractors?
* How should my Chart of Accounts be structured?
* How do all my systems integrate?

BizPilot AI automates these decisions using a collaborative AI agent architecture.

---

# 🎯 Features

## ✅ Business Formation Advisor

* Business profile analysis
* Entity recommendation
* LLC vs Corporation guidance
* Multi-owner recommendations
* State-aware incorporation guidance

---

## ✅ Tax Strategy Agent

* Federal filing requirements
* State filing requirements
* Sales tax guidance
* EIN requirements
* Estimated tax recommendations
* Filing authority identification
* Processing time estimation
* Compliance checklist

---

## ✅ Accounting Architecture

* Accounting software recommendation
* Chart of Accounts generation
* QuickBooks Online compatible COA export
* Bookkeeping workflow design

---

## ✅ Workforce Planning

* Employee vs Contractor recommendations
* Payroll readiness
* Workforce compliance guidance

---

## ✅ Integration Architecture

Automatically recommends integration flow between platforms such as:

* Shopify
* Stripe
* QuickBooks Online
* Banks
* Payment processors

---

## ✅ Document Package Generator

Automatically generates:

* Business Blueprint
* Incorporation Checklist
* Tax Readiness Checklist
* Accounting Setup Guide
* Integration Workflow
* Compliance Documentation

---

## ✅ State-specific Incorporation Guidance

Provides:

* State filing authority
* Incorporation forms
* Filing links
* Estimated processing times

---

## ✅ Risk Assessment

Analyzes business profile and generates:

* Risk score
* Risk level
* Recommendations

---

## ✅ Security Guardrails

Detects sensitive information including:

* Social Security Numbers
* Credit Card Numbers
* Bank Account Numbers
* API Keys

Rejects unsafe inputs before processing.

---

## ✅ STRIDE Security Review

Threat modeling implemented using STRIDE methodology covering:

* Spoofing
* Tampering
* Repudiation
* Information Disclosure
* Denial of Service
* Elevation of Privilege

---

# 🏗 System Architecture

```
                        User

                         │

                 Streamlit Interface

                         │

                  Security Guardrails

                         │

               Multi-Agent Orchestrator

        ┌─────────┬─────────┬──────────┬─────────┬──────────┐
        │         │         │          │         │
   Entity     Tax Agent  Accounting Workforce Documents
    Agent                    Agent      Agent      Agent

                         │

                  MCP Tool Layer

                         │

         Business Rules + Specialized Skills

                         │

                LLM Router (Provider Agnostic)

                  ┌──────────────┐
                  │              │
               Gemini        Groq
              (Primary)    (Fallback)

                         │

                Business Blueprint Output
```

---

# 🤖 Multi-Agent Architecture

BizPilot AI consists of specialized AI agents working collaboratively.

## Entity Agent

Responsible for:

* Entity recommendation
* Ownership analysis
* Business structure

---

## Tax Agent

Responsible for:

* Tax planning
* Compliance
* Filing requirements

---

## Accounting Agent

Responsible for:

* Accounting stack
* COA generation
* Financial architecture

---

## Workforce Agent

Responsible for:

* Hiring strategy
* Payroll recommendations

---

## Integration Agent

Responsible for:

* Platform integrations
* Workflow architecture

---

## Document Agent

Responsible for:

* Business blueprint generation
* Compliance documentation

---

# 🔌 MCP Integration

BizPilot AI implements an MCP server exposing reusable business tools.

Current MCP Tools include:

* Entity Structure Recommendation
* Accounting Stack Recommendation
* Workforce Recommendation
* Tax Checklist Generator
* Integration Map Generator

The orchestrator invokes these tools during blueprint generation.

---

# 🧠 Google ADK

The project uses Google ADK concepts for:

* Agent orchestration
* Tool execution
* Modular agent design
* Skills organization

---

# 🛡 Guardrails

Input validation prevents accidental processing of sensitive information.

Examples:

* SSNs
* Credit cards
* Bank account numbers
* API keys

Unsafe requests are rejected before reaching the LLM.

---

# 🔐 STRIDE Security

Threat modeling documentation is located in:

```
security/
    stride.md
```

Implemented controls include:

* Input validation
* Error handling
* Secret management
* Principle of least privilege
* API key isolation

---

# 📁 Project Structure

```
BizPilot AI/

├── agents/
├── config/
├── documents/
├── mcp_server/
├── security/
├── skills/
├── utils/
├── app.py
├── requirements.txt
└── README.md
```

---

# 🛠 Technologies Used

### AI

* Google ADK
* Google Gemini API
* Groq API
* Llama 3.3

### Backend

* Python
* Streamlit

### Agent Framework

* Google ADK
* MCP

### Security

* STRIDE
* Guardrails

### Data

* JSON
* Python Dataclasses

---

# 🚀 Local Installation

## Clone Repository

```bash
git clone https://github.com/saadi123/BizPilot-AI.git

cd BizPilot-AI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

Example:

```env
GEMINI_API_KEY=YOUR_GEMINI_KEY

GROQ_API_KEY=YOUR_GROQ_KEY
```

---

## Run the Application

```bash
streamlit run app.py
```

---

# ☁ Deployment

BizPilot AI is deployed using Streamlit Community Cloud.

Deployment steps:

1. Push code to GitHub.
2. Connect repository to Streamlit Community Cloud.
3. Configure Secrets:

```
GEMINI_API_KEY=...

GROQ_API_KEY=...
```

4. Deploy.

---

# 📸 Application Workflow

1. User enters business details.
2. Guardrails validate input.
3. Orchestrator dispatches tasks.
4. MCP tools execute.
5. Specialized agents analyze.
6. Gemini processes prompts.
7. Groq serves as fallback.
8. Business Blueprint is generated.

---

# 📈 Future Improvements

* Oracle NetSuite integration
* Xero support
* AI financial forecasting
* Business valuation
* Cash flow projections
* Banking integrations
* Payroll automation
* RAG knowledge base
* Multi-language support

---

# 👨‍💻 Author

**Muhammad Saad Haque**

BizPilot AI was developed as a competition project demonstrating modern AI agent architecture using Google ADK, MCP, LLM orchestration, and secure AI application design.

---

# 📄 License

This project is licensed under the MIT License.
