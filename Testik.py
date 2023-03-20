import openai
import os


def Testi():
    import sqlite3
    import random

    # Connect to the database
    conn = sqlite3.connect('scenarios.db')

    # Create a table to store scenarios
    conn.execute('CREATE TABLE IF NOT EXISTS scenarios (name TEXT, transcript TEXT, positive TEXT, negative TEXT)')

    # Define a function to add a scenario to the database
    def add_scenario(name, transcript, positive_responses, negative_responses):
        positive = "\n".join(positive_responses)
        negative = "\n".join(negative_responses)
        conn.execute('INSERT INTO scenarios (name, transcript, positive, negative) VALUES (?, ?, ?, ?)',
                     (name, transcript, positive, negative))
        conn.commit()

    # Define a function to retrieve a scenario from the database
    def get_scenario(name):
        cursor = conn.execute('SELECT transcript, positive, negative FROM scenarios WHERE name = ?', (name,))
        result = cursor.fetchone()
        if result:
            transcript = result[0]
            positive_responses = result[1].split("\n")
            negative_responses = result[2].split("\n")
            return transcript, positive_responses, negative_responses
        else:
            return None

    # Ask the operator to enter a name for the scenario
    name = input("Enter a name for the scenario: ")

    # Ask the operator to enter the transcript for the scenario
    transcript = input("Enter the transcript for the scenario: ")

    # Ask the operator to enter the possible positive responses for the scenario
    positive_responses = input("Enter the possible positive responses (separated by commas): ").split(",")

    # Ask the operator to enter the possible negative responses for the scenario
    negative_responses = input("Enter the possible negative responses (separated by commas): ").split(",")

    # Add the scenario to the database
    add_scenario(name, transcript, positive_responses, negative_responses)

    # Retrieve a scenario from the database
    scenario_name = input("Enter the name of the scenario to retrieve: ")
    scenario = get_scenario(scenario_name)
    if scenario:
        transcript, positive_responses, negative_responses = scenario
        response = input(transcript)
        if response.strip().lower() in [resp.strip().lower() for resp in positive_responses]:
            print("Positive response detected")
            # Handle positive response
        elif response.strip().lower() in [resp.strip().lower() for resp in negative_responses]:
            print("Negative response detected")
            # Handle negative response
        else:
            print("Response not recognized")
    else:
        print("Scenario not found")