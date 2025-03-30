import openai
import json
import os
import re
from datetime import datetime

openai.api_key=""
def get_response(messages):
    response=openai.chat.completions.create(
        model = 'gpt-4o',
        messages = messages
        )
    return response.choices[0].message.content

def AI_Summarize(user_input):
    entries = load_entries()

    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent assistant that analyzes a user's diary (in JSON format) and their request.\n"
                "Your task is to return a JSON object with two keys:\n"
                "1. 'relevant_ids': a list of diary entry IDs that match the user's request. You must match based on title, date, or content. In case of lack of detail like specific dates, use all entry ids, since the user asked general question\n"
                "2. 'task': a clear rephrasing of the user’s request into an actionable task with exact numbers (e.g., 'Summarize April 2024 entries' or 'Summarize 2024 then give 3 interesting moments' - gives exactly 3 as requested by user).\n\n"
                "**Important Instructions - Special Cases:**\n"
                "- If user requests a date range partially or completely outside available entries, give the closest matching entries' ids.\n"
                "- If user says something like 'my 2024 highlights', return all entries' ids from 2024.\n"
                "- If nothing matches, return an empty list.\n"
                "- DO NOT include anything else in your response — only the JSON object."
            )
        },
        {
            "role": "user",
            "content": f"Diary Entries: {json.dumps(entries, indent=2)}"
        },
        {
            "role": "user",
            "content": f"User Request: {user_input}"
        }
    ]

    response = get_response(messages)

    try:
        # Clean up markdown-style code block if GPT returns one
        if response.startswith("```"):
            response = re.sub(r"```(?:json)?\s*", "", response)
            response = response.rstrip("```").strip()

        parsed = json.loads(response)
        relevant_ids = parsed.get("relevant_ids", [])
        task = parsed.get("task", "")

        # Pass this structured info to summarization function
        if relevant_ids:
            entries = load_entries()
            filtered_entries = [entry for entry in entries if entry["id"] in relevant_ids]

            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful AI. You will be given a list of diary entries (as JSON) and a user request. Respond only based on the entries provided and task requested. Be concise and answer to the request with response to question why. Your response should not exceed the maximum 2 sentences length"
                },
                {
                    "role": "user",
                    "content": f"Request: {task}"
                },
                {
                    "role": "user",
                    "content": f"Diary Entries: {json.dumps(filtered_entries, indent=2)}"
                }
            ]

            print("Matching Entry IDs:", relevant_ids)
            print("Task:", task)
            print("Summarizing Matching Entries...")
            print(get_response(messages))
        else:
            print("No matching entries found.")
    except Exception as e:
        print("Error parsing AI response:", e)
        print("Raw response:", response)


# Welcome to the Personal Diary
print("Welcome to the Personal Diary, to create a new diary memory input your message!")



diary_file = "diary.json"


def load_entries():
    if os.path.exists(diary_file):
        with open(diary_file, "r") as file:
            return json.load(file)
    return []


def save_entries(entries):
    with open(diary_file, "w") as file:
        json.dump(entries, file, indent=4)


def add_entry():
    title = input("Enter title: ")
    content = input("Enter content: ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entries = load_entries()
    entry = {"id": len(entries) + 1, "title": title, "date": date, "content": content}
    entries.append(entry)
    save_entries(entries)
    print("Entry added successfully!")


def list_entries():
    entries = load_entries()
    if not entries:
        print("No diary entries found.")
        return
    for entry in entries:
        print(f"[{entry['id']}] {entry['date']} - {entry['title']}")


def view_entry():
    entry_id = int(input("Enter entry ID: "))
    entries = load_entries()
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if entry:
        print(f"\nTitle: {entry['title']}\nDate: {entry['date']}\nContent: {entry['content']}\n")
    else:
        print("Entry not found.")


def update_entry():
    entry_id = int(input("Enter entry ID to update: "))
    entries = load_entries()
    for entry in entries:
        if entry["id"] == entry_id:
            entry["title"] = input("Enter new title: ") or entry["title"]
            entry["content"] = input("Enter new content: ") or entry["content"]
            save_entries(entries)
            print("Entry updated successfully!")
            return
    print("Entry not found.")


def delete_entry():
    entry_id = int(input("Enter entry ID to delete: "))
    entries = load_entries()
    entries = [e for e in entries if e["id"] != entry_id]
    save_entries(entries)
    print("Entry deleted successfully!")


def main():
    while True:
        print("\nPersonal Diary - Spectrum Team")
        print("1. Create Entry")
        print("2. List Entries")
        print("3. View (display) Entry")
        print("4. Update Entry")
        print("5. Delete Entry")
        print("6. AI summarize")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_entry()
        elif choice == "2":
            list_entries()
        elif choice == "3":
            view_entry()
        elif choice == "4":
            update_entry()
        elif choice == "5":
            delete_entry()
        elif choice == "6":
            user_request = input("Your request: ")
            AI_Summarize(user_request)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()



