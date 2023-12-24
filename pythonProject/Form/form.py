import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Loading necessary data files
occupation_data_df = pd.read_excel("/Users/mukulhooda/Desktop/SIH/model_and_data/Occupation Data.xlsx")
oip_transformed_df = pd.read_csv("/Users/mukulhooda/Desktop/SIH/model_and_data/oip_transformed.csv")


def calculate_riasec_scores(responses):
    riasec_mapping = {
        "R": [1, 2, 13, 24, 25, 26, 38, 49, 50, 60],
        "I": [3, 4, 15, 16, 28, 39, 40, 52, 53, 54],
        "A": [5, 6, 17, 18, 29, 30, 41, 42, 55, 56],
        "S": [7, 8, 19, 20, 31, 32, 43, 44, 57, 58],
        "E": [9, 10, 21, 22, 33, 34, 45, 46, 47, 59],
        "C": [11, 12, 14, 23, 27, 35, 36, 37, 48, 51]
    }
    riasec_scores = {key: sum(responses[val - 1] for val in values) for key, values in riasec_mapping.items()}
    return riasec_scores


def calculate_correlations(user_riasec_scores):
    user_scores_vector = np.array(list(user_riasec_scores.values()))
    correlations = {}
    for index, row in oip_transformed_df.iterrows():
        occupation_scores_vector = np.array(
            [row['Realistic'], row['Investigative'], row['Artistic'], row['Social'], row['Enterprising'],
             row['Conventional']])
        correlation = np.corrcoef(user_scores_vector, occupation_scores_vector)[0, 1]
        occupation_code = row['O*NET-SOC Code']
        correlations[occupation_code] = correlation
    return correlations


def assessment():

    st.title("📝 Interest Assessment")
    st.write("""
    Please respond to the following questions. Indicate your interest in each activity by selecting the appropriate option:
    - Strongly Dislike
    - Dislike
    - Unsure
    - Like
    - Strongly Like
    """)
    questions = [
        "Develop a new medicine",
        "Teach an individual an exercise routine",
        "Buy and sell stocks and bonds",
        "Conduct chemical experiments",
        "Draw pictures",
        "Operate a beauty salon or barber shop",
        "Install software across computers on a large network",
        "Assemble electronic parts",
        "Examine blood samples using a microsce",
        "Create special effects for mov",
        "Teach children how to play sports",
        "Develop a way to better predict the weather",
        "Teach sign language to people who are deaf or hard of hearing",
        "Represent a client in a lawsuit",
        "Instruct a class of students at school",
        "Manage Social media and public relations for an organization",
        "Study ways to reduce water pollution",
        "Help people with personal or emotional problems",
        "Manage a retail store",
        "Study the movement of planets",
        "Perform rehabilitation therapy",
        "Drive a truck to deliver packages to offices and homes",
        "Investigate the cause of a fire",
        "Do volunteer work at a non-profit organization",
        "Start your own business",
        "Calculate the wages of employees",
        "Work in a biology lab",
        "Develop a fresh fashion line",
        "Manage Social media and public relations for an organization",
        "Write books or plays or scripts for movies or television shows",
        "Develop a spreadsheet using computer software",
        "Compose or arrange music",
        "Test the quality of parts before shipment",
        "Perform various dance styles",
        "Do laboratory tests to identify diseases",
        "Play a musical instrument",
        "Repair household appliances",
        "Open an Animal husbandry",
        "Take care of children at a day-care center"
    ]
    response_mapping = {"Strongly Dislike": 0, "Dislike": 1, "Unsure": 2, "Like": 3, "Strongly Like": 4}
    responses = [st.selectbox(question, list(response_mapping.keys())) for question in questions]
    responses_scores = [response_mapping[response] for response in responses]
    riasec_scores = calculate_riasec_scores(responses_scores)
    st.subheader("Your RIASEC Scores")
    st.write(riasec_scores)



    correlations = calculate_correlations(riasec_scores)
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    num_recommendations = st.selectbox("Select the number of recommended occupations to display:", options=range(1, 21),
                                       index=4)

    top_recommendations = sorted_correlations[:num_recommendations]

    st.subheader(f"Top {num_recommendations} Recommended Occupations")
    recommended_data = []
    for occupation_code, correlation in top_recommendations:
        occupation_row = occupation_data_df[occupation_data_df['O*NET-SOC Code'] == occupation_code].iloc[0]
        occupation_name = occupation_row['Title']
        description = occupation_row['Description']
        recommended_data.append([occupation_name, description])

    recommended_df = pd.DataFrame(recommended_data, columns=['Occupation', 'Description'])
    st.table(recommended_df)


# App navigation
st.title("🧭 Career Recommendation")
# section = st.sidebar.radio("Choose a section:", ["📝 Interest Assessment"])

# if section == "📝 Interest Assessment":
assessment()
