---

> ## Challenge Advisor: Update & Finalize Your Project Overview
>
> > 💡 **These grey text instructions are just for you, the team's Challenge Advisor; please delete them once you have completed the steps below.**
>
> We've pre-populated this Challenge Project Overview page — which is what will be shared with your Break Through Tech student team in August — using the details from your submission form. You should have received an email inviting you to join this repo as a Collaborator, enabling you to add files and make edits.
> 
> In order for your project to be finalized and assigned to a team, please:
> 1. **Review all sections below** and update or expand any content as needed, making sure to address the SME Feedback in the section immediately below. Look for square brackets to find the places below that require additional inputs from you (e.g., "About [Company / Org Name]").
> 2. **Add your dataset** to the [data folder](data) in this repo.
> 3. **Close the Issue assigned to you in this repo** to let us know that you have made your edits and the overview page is ready for final review. You can do this by going to the _Issues_ tab in the top left section of the menu above, add a comment that says "CA review complete", and click the button to Close the Issue. 
>
> If you're unfamiliar with how to edit a page like this in GitHub, check out [this tutorial](https://ubc-lib-geo.github.io/gis-workshop-waml-template/content/handson/edit-readme.html) for a quick overview (start with step 2 and only edit this page), and [this guide](https://ubc-lib-geo.github.io/gis-workshop-waml-template/content/markdown.html) on how to use Markdown to compose text.
>
>
> ❌ Remember that this is a public repo. Do NOT include: Proprietary data, PII, API keys, credentials, or anything confidential.

---
## 📋 BTT Internal Evaluation Notes
*(This section is for BTT staff only — remove before sharing with students)*

| Check | Status | Notes |
|-------|--------|-------|
| Python Compatibility | 🟢 | The tech stack is centered on Python and uses established ML libraries for classification, regression, NLP, and time series analysis. |
| Data Readiness |  🟢 | The dataset is publicly available and under 1GB, ensuring it is manageable and ready for use without extensive cleansing. |
| Resource Check | 🟢 |  While the project is designed for free-tier environments like Google Colab, students may need to explore open-source alternatives if they choose to incorporate LLMs |

**Student Fit Score:** 8/10  
**Technical Depth Score:** 7/10  
**Overall Recommendation:** REVISE

**Advisor Feedback Draft:**
The project represents a timely and impactful area of exploration, allowing students to leverage a mix of ML techniques in a significant domain. However, consider two adjustments: refine the success metrics to prioritize actionable insights over purely numerical outcomes, and ensure that all team members have a sufficient understanding of advanced techniques such as LLMs before implementation. Let's leverage this project to deepen Fellow's understanding of the real-world applications of ML in supply chain management.

# Predict the Supply Chain disruptions

**Company / Org:** Accenture  
**Challenge Advisor:** Ashok Shivarajan, ashok27kumar@gmail.com  
**Program:** Break Through Tech AI Studio - Fall 2026

---

## 🏢 About Accenture

Accenture is a global professional services company providing a broad range of services across strategy, consulting, digital, technology, and operations. Our focus is on leveraging innovative technologies to help organizations improve their performance and deliver value to their customers.

---

## 🎯 The Challenge

### Project Summary
Build an AI system that can predict supply chain disruptions and recommend mitigation actions using operational + contextual data.

### Success Criteria
Model Performance (30%): Classification (ROC-AUC/F1-score), Regression (RMSE/MAE); Resilience Intelligence (25%): Quality of risk scoring; Business Impact (20%): Cost reduction, Service level improvement; Explainability & Storytelling (15%): Executive narrative, Visual dashboards; Innovation (10%): Graph ML/simulation models, Scenario planning.

**Model Performance (30%)**   
- Classification: ROC-AUC / F1-score
- Regression: RMSE / MAE

**Resilience Intelligence (25%)**   
Quality of risk scoring   
Ability to:
- Identify high-risk suppliers/routes
- Detect early warning signals

**Business Impact (20%)**
Clear articulation of:
- Cost reduction
- Service level improvement

**Explainability & Storytelling (15%)**
Executive narrative
Visual dashboards (aligns with your AI4BI focus)

**Innovation (10%)**
Use of:
- Graph ML / simulation models
- Scenario planning

### Stretch Goals
The stretch goal will be to provided recommended actions based on the supply chain disruptions. This may not be completed within the three months window.

### Project Milestones

Use these milestones to guide your work. Your team will create a **GitHub Projects board** to track tasks within each milestone.

| Month | Milestone | Key Activities |
|-------|-----------|----------------|
| **September** | Data Understanding | Explore dataset, handle missing values, document findings |
| **October** | Model Development | Train baseline model, experiment with approaches, iterate |
| **November** | Evaluation & Presentation | Finalize model, prepare presentation, document results |

> **Note for the team:** Please create a GitHub Projects board in this repository to break these milestones into weekly tasks. Go to the **Projects** tab → **New project** → Choose **Board** → Add columns for each month.

---

## 📊 Dataset

**Name and Source:** Supply Chain Data from Kaggle  
**Format:** CSV  
**Size:** under 1gb  
**Location:** https://www.kaggle.com/competitions/datathon-2022-upc-accenture/overview

### Key Details
- Numerical / Quantitative and Time Series data stored in CSV/TSV format. 
- [Any known limitations or preprocessing needed]
- [Link to data dictionary or documentation, if available]

---

## 🛠️ Suggested Approach

**ML Problem Type:** Classification, Regression, NLP, Time Series Analysis

**Recommended Libraries:**
- [e.g., pandas, scikit-learn, TensorFlow, Hugging Face]

**Evaluation Metrics:**
- ROC-AUC, F1-score, RMSE, MAE

---

## 📚 Resources to Get Started

The following resources will help your team understand the problem space and potential technical approaches for this project:

**Background Reading:**
- [e.g., Link to an article or blog post about the problem domain]
- [e.g., Link to an industry report or case study]

**Technical Tutorials:**
- [e.g., Link to a free tutorial on the ML technique(s) involved]
- [e.g., Link to documentation for a key library or tool]

**Code Examples:**
- [e.g., Link to a relevant GitHub repo]
- [e.g., Link to a sample implementation or starter code]

**Other:**
- [Links to any additional resources — e.g., papers, videos, podcasts, etc.]

*Feel free to explore beyond these, and share anything interesting you find with me!*

---

## 🤝 How We'll Work Together

**Official check-ins:** During our biweekly 45-minute AI Studio Lab Section meeting block (2nd and 4th week of every month)

 **Other ways to reach out to me with questions:** 
* [e.g., Your team's channel within Break Through Tech’s Discord space]
* [e.g., Email; please copy your teammates and AI Studio Coach]
* [e.g., Request a team check-in on Zoom]
* [Note: I will aim to respond within 48 hours. Please reach out to your AI Studio Coach with urgent questions.]

> 💡 **Challenge Advisor: Please update the above based on your availability and preference. If you are not able to answer questions or meet with fellows outside of the biweekly Lab Section check-ins, simply write in "N/A (only available during the official check-in times)"**

**Recommended free coding / collaboration tools**
* […]
* […]

---

## 🚀 Getting Started

1. **Review this overview document** and note any questions for our first meeting
2. **Begin reviewing the dataset** using the link above
3. **Read the GitHub Projects documentation** [here](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)

I’m excited to work with you!

---

## ❓ Questions?

Please bring any questions to our first meeting during the week of August 24th (Break Through Tech’s Bridge to Studio - Session C). 
