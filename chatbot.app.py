import streamlit as st
import joblib
import random

# Load the trained model and vectorizer
clf = joblib.load('chatbot_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Define the intents (same as in your model training script)
intents = [
    {"tag": "account_opening", 
     "patterns": ["How do I open an account?", "Can I open an account online?", "What do I need to open an account?"], 
     "responses": ["You can open an account online or visit a branch. Required documents may include a valid ID, proof of address, and an                     initial deposit.", "To open an account, visit our website or a nearby branch with your identification and proof of                         residence."]
    },
    {"tag": "account_balance",
     "patterns": ["What is my account balance?", "How do I check my balance?", "Can you tell me my balance?"], 
     "responses": ["You can check your balance through our mobile app, online banking, or by visiting a branch.",
                   "Log in to your account online or use our automated phone service to check your balance."]
    },
    {"tag": "loan_inquiry", 
     "patterns": ["How can I apply for a loan?", "What are the requirements for a loan?", "Tell me about loan options."], 
     "responses": ["We offer personal, home, and business loans. Visit our website or a branch to apply.",
                   "Loan requirements include a good credit score, proof of income, and collateral (if applicable)."]
    },
     {
        "tag": "loan_repayment",
        "patterns": ["How do I repay my loan?", "What are my loan repayment options?", "Can I pay off my loan early?"],
        "responses": ["You can repay your loan through automatic deductions, online banking, or at a branch.",
                      "Yes, early loan repayment is possible, but check if there are any prepayment penalties."]
    },
    {
        "tag": "fraud_alert",
        "patterns": ["I think my account has been hacked.", "What do I do if I notice fraud?", "How do I report suspicious activity?"],
        "responses": ["If you suspect fraud, immediately contact our customer support and secure your account.",
                      "You can report fraudulent activity through our online banking portal or by calling our fraud department."]
    },
    {
        "tag": "credit_card",
        "patterns": ["How can I apply for a credit card?", "What are the benefits of your credit cards?", "What is the credit limit?"],
        "responses": ["You can apply for a credit card online or at a branch. Benefits include cashback, rewards, and low-interest                               rates.", "Your credit limit depends on your credit score and financial history."]
    },
    {
        "tag": "investment_options",
        "patterns": ["What investment options do you offer?", "How can I invest my money?", "Tell me about savings and investment                               plans."],
        "responses": ["We offer savings accounts, fixed deposits, mutual funds, and stock market investments. Visit our website for                              details.", "Investment options vary based on your risk appetite. Speak to a financial advisor for personalized                             recommendations."]
    },
    {
        "tag": "money_transfer",
        "patterns": ["How do I send money to another account?", "Can I transfer money internationally?", "What are the transfer fees?"],
        "responses": ["You can transfer money using online banking, our mobile app, or by visiting a branch.",
                      "Yes, international transfers are available. Fees and processing times vary based on the destination country."]
    },
    {
        "tag": "fixed_deposit",
        "patterns": ["What is a fixed deposit?", "How much interest do fixed deposits offer?", "Can I withdraw my fixed deposit early?"],
        "responses": ["A fixed deposit is a savings option that offers higher interest rates than regular savings accounts.",
                      "Interest rates vary based on the duration of the deposit. Early withdrawal may incur penalties."]
    },
    {
        "tag": "debit_card_issues",
        "patterns": ["My debit card is not working.", "How do I activate my new debit card?", "What should I do if my card is lost?"],
        "responses": ["If your card is not working, check if it is activated or contact customer support.",
                      "To activate your new debit card, use an ATM or online banking. Report lost cards immediately for security."]
    },
    {
        "tag": "mortgage",
        "patterns": ["How do I apply for a mortgage?", "What are the interest rates for mortgages?", "Do you offer home loans?"],
        "responses": ["We offer home loans with competitive interest rates. Visit a branch or apply online.",
                      "Mortgage interest rates depend on your credit score and loan duration. Contact our loan officers for details."]
    },
    {
        "tag": "customer_support",
        "patterns": ["How do I contact customer support?", "What are your support hours?", "I need assistance with my account."],
        "responses": ["You can reach our support team via phone, email, or live chat on our website.",
                      "Our customer support is available 24/7 for urgent issues. Visit our website for contact details."]
    },
    {
        "tag": "greeting",
        "patterns": ["Hi", "Hello", "Hey", "How are you", "What's up"],
        "responses": ["Hi there", "Hello", "Hey", "I'm fine, thank you"]
    },
    {
        "tag": "goodbye",
        "patterns": ["Bye", "See you later", "Goodbye", "Take care"],
        "responses": ["Goodbye", "See you later", "Take care", "Thank you for chatting with me. Have a great day!"]
    },
    {
        "tag": "thanks",
        "patterns": ["Thank you", "Thanks", "Thanks a lot", "I appreciate it"],
        "responses": ["You're welcome", "No problem", "Glad I could help"]
    },
    {
        "tag": "about",
        "patterns": ["What can you do", "Who are you", "What are you", "What is your purpose"],
        "responses": ["I am a chatbot", "My purpose is to assist you", "I can answer questions and provide assistance"]
    },
    {
        "tag": "help",
        "patterns": ["Help", "I need help", "Can you help me", "What should I do"],
        "responses": ["Sure, what do you need help with?", "I'm here to help. What's the problem?", "How can I assist you?"]
    },
    {
        "tag": "age",
        "patterns": ["How old are you", "What's your age"],
        "responses": ["I don't have an age. I'm a chatbot.", "I was just born in the digital world.", "Age is just a number for me."]
    },
    {
        "tag": "savings_account",
        "patterns": ["How do I open a savings account?", "What are the benefits of a savings account?", "What is the minimum balance for                       a savings account?"],
        "responses": ["You can open a savings account online or at any of our branches with a valid ID and an initial deposit.",
                      "A savings account helps you earn interest on your money while keeping it accessible.",
                      "The minimum balance requirement depends on the type of savings account. Please check our website for details."]
    },
    {
        "tag": "business_loans",
        "patterns": ["Do you offer business loans?", "How can I get a loan for my business?", "What are the requirements for a business                        loan?"],
        "responses": ["Yes, we offer business loans with flexible repayment options. Visit a branch or apply online.",
                      "To apply for a business loan, you'll need to provide business financial statements, proof of income, and                                  collateral (if required)."]
    },
    {
        "tag": "debit_card_application",
        "patterns": ["How do I apply for a debit card?", "Can I get a replacement debit card?", "What should I do if my debit card is                           lost or stolen?"],
        "responses": ["You can apply for a debit card when you open an account or request one online.",
                      "If your card is lost or stolen, immediately report it to our support team to prevent unauthorized transactions."]
    },
    {
        "tag": "interest_rates",
        "patterns": ["What are your current interest rates?", "How much interest do I earn on my savings?", "Do you offer competitive                           interest rates?"],
        "responses": ["Our interest rates vary based on the type of account or loan. Visit our website or contact our support team for                           details.", "Yes, we offer competitive interest rates on savings, loans, and fixed deposits."]
    },
    {
        "tag": "online_banking",
        "patterns": ["How do I register for online banking?", "What services are available through online banking?", "Can I pay my bills                        online?"],
        "responses": ["You can register for online banking on our website using your account details.",
                      "Online banking allows you to check your balance, transfer funds, pay bills, and more.",
                      "Yes, you can pay utility bills, loans, and credit card bills using our online banking service."]
    },
    {
        "tag": "mobile_banking",
        "patterns": ["Do you have a mobile banking app?", "How do I download your mobile banking app?", "Can I transfer money using                             mobile banking?"],
        "responses": ["Yes, we have a mobile banking app available on iOS and Android. Download it from the App Store or Google Play.",
                      "You can use our mobile banking app to transfer funds, check balances, and pay bills conveniently."]
    },
    {
        "tag": "tax_information",
        "patterns": ["Do you provide tax filing assistance?", "Can I get my tax statement from the bank?", "How do I download my annual                         tax summary?"],
        "responses": ["We provide tax statements that you can access through online banking or request at a branch.",
                      "Log in to your online banking account and go to the tax section to download your annual tax summary."]
    },
    {
        "tag": "atm_locations",
        "patterns": ["Where is the nearest ATM?", "How can I find an ATM near me?", "Do you have ATMs in my city?"],
        "responses": ["You can find the nearest ATM using our website's branch locator or mobile banking app.",
                      "Visit our website and enter your location to find the closest ATM."]
    },
    {
        "tag": "overdraft_protection",
        "patterns": ["Do you offer overdraft protection?", "What happens if I overdraft my account?", "How can I avoid overdraft fees?"],
        "responses": ["Yes, we offer overdraft protection to help prevent declined transactions and fees.",
                      "If you overdraft your account, you may incur a fee unless you have overdraft protection.",
                      "To avoid overdraft fees, consider setting up alerts for low balances or linking your savings account for automatic                        transfers."]
    },
    {
        "tag": "foreign_exchange",
        "patterns": ["What are your foreign exchange rates?", "Can I exchange currency at the bank?", "Do you offer international money                         exchange services?"],
        "responses": ["You can check our latest foreign exchange rates on our website or by visiting a branch.",
                      "Yes, we offer foreign currency exchange services at select branches."]
    },
    {
        "tag": "wire_transfers",
        "patterns": ["How do I send a wire transfer?", "How long does a wire transfer take?", "Are there fees for wire transfers?"],
        "responses": ["You can send a wire transfer online, through mobile banking, or by visiting a branch.",
                      "Domestic wire transfers typically take 1-2 business days, while international transfers may take longer.",
                      "Wire transfer fees depend on the destination and transfer method. Check our website for details."]
    },
    {
        "tag": "financial_advice",
        "patterns": ["Can I speak to a financial advisor?", "Do you offer financial planning services?", "How do I manage my finances                           better?"],
        "responses": ["Yes, we offer financial advisory services to help you with investments, savings, and retirement planning.",
                      "Our financial advisors can guide you on managing your money effectively. Schedule an appointment online or at a                           branch."]
    },
    {
        "tag": "retirement_planning",
        "patterns": ["How do I start planning for retirement?", "Do you offer retirement accounts?", "What are the best retirement                              savings options?"],
        "responses": ["We offer retirement accounts such as IRAs and pension plans to help you save for the future.",
                      "It's never too early to start planning for retirement. Speak to a financial advisor to explore your options."]
    },
    {
        "tag": "bank_hours",
        "patterns": ["What are your branch hours?", "Are you open on weekends?", "When does the bank close?"],
        "responses": ["Our branch hours vary by location. Please check our website for specific hours.",
                      "Some branches may be open on weekends. Visit our website to find weekend banking locations."]
    },
    {
        "tag": "identity_verification",
        "patterns": ["Why do I need to verify my identity?", "How do I verify my identity for online banking?", "What documents are                             needed for identity verification?"],
        "responses": ["Identity verification helps ensure the security of your account and prevent fraud.",
                      "To verify your identity, you may need to provide a government-issued ID, proof of address, and account details."]
    },
    {
    "tag": "unrelated_questions",
    "patterns": ["Tell me a joke", "What's the weather like?", "Who won the football match?", "How do I cook pasta?"],
    "responses": ["I'm here to help with financial services. If you need banking assistance, feel free to ask!",
                  "I specialize in banking and finance. Let me know if you have any questions about your account, loans, or savings."]
}
]

# Function to get a response from the chatbot
def chatbot_response(user_text):
    user_text = vectorizer.transform([user_text])
    tag = clf.predict(user_text)[0]
    for intent in intents:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Streamlit app interface
st.set_page_config(page_title="Chatbot Application", page_icon="🤖")

# Custom CSS to improve UI
st.markdown("""
    <style>
    .main {
        background-color: #D3D3D3;
        color: #333;
    }
    .stTextArea label {
        display: none;
    }
    .stTextInput input {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("Chatbot Settings")
st.sidebar.markdown("Adjust the chatbot's settings here.")

# App title and description
st.title("🤖 Chatbot")
st.write("Welcome to the chatbot. Please type a message and press Enter to start the conversation.")

# Input text box for user input
user_input = st.text_input("You: ", key="user_input")

if user_input:
    response = chatbot_response(user_input)
    st.session_state.chat_history.append({"user": user_input, "bot": response})

    if response.lower() in ['goodbye', 'bye']:
            st.write("Thank you for chatting with me. Have a great day!")
            st.stop()
        
# Display chat history
for chat in st.session_state.chat_history:
    st.write(f"**You:** {chat['user']}")
    st.write(f"**Bot:** {chat['bot']}")

if __name__ == "__main__":
    chatbot_response("")
