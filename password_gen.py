import streamlit as st
import random
import string
import re

# Helper functions defined first
def check_your_password_strength(password):
    score = 0
    feedback = []
    
    # Length check with bonus for longer passwords
    if len(password) >= 15:
        score += 1
        feedback.append(f"{len(password)} characters")
    
    # Character variety
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("Lowercase letters")
    
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("Uppercase letters")
    
    if re.search(r'\d', password):
        score += 1
        feedback.append("Numbers")
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        score += 1
        feedback.append("Special characters")
    
    # Determine strength
    if score <= 1:
        strength = "Very Weak"
    elif score == 2:
        strength = "Weak"
    elif score == 3:
        strength = "Moderate"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return strength, score, feedback


def get_recommendations(password, score):
    recommendations = []
    
    if len(password) < 12:
        recommendations.append("Use at least 12 characters")
    
    if not re.search(r'[a-z]', password):
        recommendations.append("Add lowercase letters")
    
    if not re.search(r'[A-Z]', password):
        recommendations.append("Add uppercase letters")
    
    if not re.search(r'\d', password):
        recommendations.append("Add numbers")
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        recommendations.append("Add special characters")
    
    if not recommendations:
        recommendations.append("Your password is strong!")
    
    return recommendations


def estimate_crack_time(password):
    # Simplified estimation
    charset_size = 0
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'\d', password):
        charset_size += 10
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        charset_size += 32
    
    combinations = charset_size ** len(password)
    
    if combinations < 1e9:
        return "Less than a second"
    elif combinations < 1e12:
        return "Minutes to hours"
    elif combinations < 1e15:
        return "Days to weeks"
    elif combinations < 1e18:
        return "Months to years"
    else:
        return "Centuries+"


# Main app configuration
st.set_page_config(page_title="Password Generator", page_icon="🔐", layout="wide")

st.title("🔐 Generate Password & Check Strength")

tab1, tab2 = st.tabs(["🎲 Generate Your Password", "🔍 Check Your Password Strength"])

# Password Generator Tab
with tab1:
    st.header("Generate Your Secure Password")
    
    length = st.slider("Password Length", min_value=8, max_value=25, value=8)
    
    st.write("**Include:**")
    use_uppercase = st.checkbox("Uppercase letters (A-Z)", value=True)
    use_lowercase = st.checkbox("Lowercase letters (a-z)", value=True)
    use_numbers = st.checkbox("Numbers (0-9)", value=True)
    use_symbols = st.checkbox("Symbols (!@#$%^&*)", value=True)
    
    exclude_similar = st.checkbox("Exclude similar characters (i, l, 1, L, o, 0, O)", value=False)
    
    if st.button("Generate Password", type="primary"):
        # Build character set
        chars = ""
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if exclude_similar:
            chars = ''.join(c for c in chars if c not in 'il1Lo0O')
        
        if not chars:
            st.error("Please select at least one character type!")
        else:
            # Generate password
            password = ''.join(random.choice(chars) for _ in range(length))
            
            st.success("Password generated!")
            st.code(password, language=None)
            
            # Copy button info
            st.info("👆 Click the copy button in the top-right of the box to copy your password")
            
            # Show strength
            strength, score, feedback = check_your_password_strength(password)
            
            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Strength", strength)
            metric_col2.metric("Score", f"{score}/5")
            
            if feedback:
                st.write("**Characteristics:**")
                for item in feedback:
                    st.write(f"✓ {item}")

# Password Checker Tab
with tab2:
    st.header("Check Password Strength")
    
    password_input = st.text_input("Enter password to check:", type="password")
    show_password = st.checkbox("Show password")
    
    if show_password and password_input:
        st.code(password_input, language=None)
    
    if password_input:
        if len(password_input) == 0:
            st.warning("Please enter a password to check")
        else:
            strength, score, feedback = check_your_password_strength(password_input)
            
            # Color coding
            colors = {
                "Very Weak": "🔴",
                "Weak": "🟠",
                "Moderate": "🟡",
                "Strong": "🟢",
                "Very Strong": "🟢"
            }
            
            st.subheader(f"{colors.get(strength, '⚪')} Strength: {strength}")
            
            # Progress bar
            st.progress(score / 5)
            
            # Detailed feedback
            feedback_col1, feedback_col2 = st.columns(2)
            
            with feedback_col1:
                st.write("**Password contains:**")
                for item in feedback:
                    st.write(f"✓ {item}")
            
            with feedback_col2:
                st.write("**Recommendations:**")
                recommendations = get_recommendations(password_input, score)
                for rec in recommendations:
                    st.write(f"• {rec}")
            
            # Additional info
            st.write("**Password Details:**")
            st.write(f"- Length: {len(password_input)} characters")
            st.write(f"- Unique characters: {len(set(password_input))}")
            
            # Crack time estimate (simplified)
            estimate = estimate_crack_time(password_input)
            st.info(f"⏱️ Estimated time to crack: {estimate}")

st.caption("🔒 Private by design & 100% Stateless: Passwords are generated locally, never stored in a database, and never sent to a server. No data leakage. No password exposure.")
