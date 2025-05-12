import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_gpa(scores):
    credit = [3, 3, 3, 4, 3, 3, 4, 2, 2, 2]
    credit_sum = sum(credit)
    
    grade = []
    grade_distribution = {
        "Below 40 (0.00)": 0,
        "40-44 (2.25)": 0,
        "45-49 (2.50)": 0,
        "50-54 (2.75)": 0,
        "55-59 (3.00)": 0,
        "60-64 (3.25)": 0,
        "65-69 (3.50)": 0,
        "70-74 (3.75)": 0,
        "75-100 (4.00)": 0
    }
    
    for r in scores:
        if 40 <= r <= 44:
            grade.append(2.25)
            grade_distribution["40-44 (2.25)"] += 1
        elif 45 <= r <= 49:
            grade.append(2.50)
            grade_distribution["45-49 (2.50)"] += 1
        elif 50 <= r <= 54:
            grade.append(2.75)
            grade_distribution["50-54 (2.75)"] += 1
        elif 55 <= r <= 59:
            grade.append(3.00)
            grade_distribution["55-59 (3.00)"] += 1
        elif 60 <= r <= 64:
            grade.append(3.25)
            grade_distribution["60-64 (3.25)"] += 1
        elif 65 <= r <= 69:
            grade.append(3.50)
            grade_distribution["65-69 (3.50)"] += 1
        elif 70 <= r <= 74:
            grade.append(3.75)
            grade_distribution["70-74 (3.75)"] += 1
        elif 75 <= r <= 100:
            grade.append(4.00)
            grade_distribution["75-100 (4.00)"] += 1
        else:
            grade.append(0)
            grade_distribution["Below 40 (0.00)"] += 1
    
    product = [credit[c] * grade[c] for c in range(len(credit))]
    return sum(product) / credit_sum, grade_distribution

def reset_form():
    st.session_state.submitted = False
    for i in range(10):
        st.session_state[f"score_{i}"] = 0

def main():
    st.title("GPA Calculator")
    
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    
    with st.form("gpa_form"):
        st.header("Enter Scores")
        scores = []
        
        for i in range(10):
            score = st.number_input(
                f"Score {i+1}:",
                min_value=0,
                max_value=100,
                value=st.session_state.get(f"score_{i}", 0),
                key=f"score_{i}"
            )
            scores.append(score)
        
        col1, col2 = st.columns([1, 6])
        with col1:
            submitted = st.form_submit_button("Calculate GPA")
        with col2:
            st.form_submit_button("Reset", on_click=reset_form)

    if submitted:
        if len(scores) != 10 or any(s < 0 or s > 100 for s in scores):
            st.error("Please enter valid scores (0-100) for all 10 subjects")
        else:
            st.session_state.submitted = True
            gpa, grade_distribution = calculate_gpa(scores)
    
    if st.session_state.submitted:
        st.success(f"Your GPA: {gpa:.2f}")
        st.write("---")
        
        # Grade Distribution Visualization
        st.subheader("Grade Distribution")
        
        # Create DataFrame for visualization
        df = pd.DataFrame(
            list(grade_distribution.items()),
            columns=["Grade Range", "Count"]
        ).set_index("Grade Range")
        
        # Bar Chart
        col1, col2 = st.columns([3, 1])
        with col1:
            st.bar_chart(df)
        
        # Data Table
        with col2:
            st.write("**Distribution Table**")
            st.dataframe(df.T, use_container_width=True)
        
        # Pie Chart
        st.write("---")
        st.subheader("Grade Proportion")
        
        fig, ax = plt.subplots()
        ax.pie(
            df["Count"],
            labels=df.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")  # Equal aspect ratio ensures pie is drawn as circle
        st.pyplot(fig)

        # Calculate Again button
        st.write("---")
        if st.button("Calculate Again"):
            reset_form()

if __name__ == "__main__":
    main()
