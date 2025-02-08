# RAG System - Superteam Vietnam AI Assistant

## 🎯 Objective

Superteam Vietnam currently relies on **manual effort** to manage its communication channels like **Telegram and Twitter**. This project aims to develop an **AI-driven solution** to **automate, enhance, and streamline** content creation, management, and community interactions. 

This **MVP solution** lays the **foundation for a fully-fledged AI system**. The winner of this bounty will have a strong chance of securing a contract to **build the complete solution**.

---

## ✅ How This RAG System Addresses the Requirements

### 📌 1. **Telegram Knowledge Portal Bot**
✔ **Solution Implemented:**
- Developed a **Telegram bot** that acts as a **knowledge base** for Superteam Vietnam.
- Uses **Retrieval-Augmented Generation (RAG)** to ensure **accurate responses**.
- Ensures **no hallucinations**—the bot **confidently says "NO"** if it does not find a relevant answer.
- Integrated **Admin UI** for document uploads to continuously train and improve the bot.

---

### 📌 3. **Twitter Management & Content Advisor Assistant**
✔ **Solution Implemented:**
- The AI integrates with **Superteam Vietnam’s Twitter account** to:
  - **Propose tweets** for human approval.
  - **Help refine drafts** by:
    - Suggesting **keywords**.
    - Correcting **Twitter handles** based on **Superteam VN’s followed accounts**.
  - **Finalize and publish** tweets.
  - Uses **local AI models** for faster & more relevant suggestions.

---

### 📌 4. **Local LLM Deployment**
✔ **Solution Implemented:**
- **Deployed & runs locally** to ensure **data privacy**.
- Uses **Ollama** to run **LLM models** on local machines.

**Installation Steps:**
```sh
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  

# Pull the Llama model
ollama pull llama3.2:1b

# Run the model
ollama run llama3.2:1b
```
🔗 **[Admin UI Installation Guide](https://github.com/skushagra9/rag-pdf/blob/master/admin-ui/README.md)**  
🔗 **[Telegram Stack Installation Guide](https://github.com/skushagra9/rag-pdf/tree/master/telegram-stack/Readme.md)**  
🔗 **[Python Backend Installation Guide](https://github.com/skushagra9/rag-pdf/blob/master/rag_backend/Readme.md)**  