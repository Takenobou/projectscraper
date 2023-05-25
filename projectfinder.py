import json
import os
import subprocess


class ProjectFinder:
    def __init__(self, data_file):
        self.data_file = data_file
        if not os.path.exists(self.data_file):
            self.generate_data_file()

    def generate_data_file(self):
        print('projects.json not found. Running projectscraper.py...')
        subprocess.call(['python', 'projectscraper.py'])

    def load_data(self):
        with open(self.data_file, 'r') as f:
            self.data = json.load(f)

    def search_by_supervisor(self):
        print("\n----Search by Supervisor----")
        supervisors = input(
            'Enter the IDs of the supervisors you are interested in (separated by commas if more than one): ').split(
            ',')
        supervisors = [supervisor.strip() for supervisor in supervisors]
        filtered_projects = [project for project in self.data if
                             any(supervisor in project['info'].get('Supervisor', '') for supervisor in supervisors)]

        if filtered_projects:
            print("\nHere are the projects supervised by the specified supervisors:\n")
            for project in filtered_projects:
                print(
                    f"Project Title: {project['title']}\nLink: {project['link']}\nSupervisor: {project['info'].get('Supervisor', '')}\n")
        else:
            print("\nNo projects found for the specified supervisors.\n")

    def search_by_keywords(self):
        print("\n----Search by Keywords----")
        keywords = input('Enter the keywords you want to search for (separated by commas): ').split(',')
        keywords = [keyword.strip() for keyword in keywords]
        filtered_projects = [project for project in self.data if any(keyword.lower() in (
                    project['info'].get('Aims of project', '') + project['info'].get('Prerequisites', '') + project[
                'title']).lower() for keyword in keywords)]

        if filtered_projects:
            print("\nHere are the projects that match your keywords:\n")
            for project in filtered_projects:
                print(f"Project Title: {project['title']}\nLink: {project['link']}\nKeywords: {', '.join(keywords)}\n")
        else:
            print("\nNo projects found for the specified keywords.\n")


def main():
    print("Welcome to the Project Finder!")
    project_finder = ProjectFinder('projects.json')

    while True:
        print("\nWhat do you want to do?")
        print("1. Search projects by supervisor")
        print("2. Search projects by keywords")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")
        if choice == '1':
            project_finder.load_data()
            project_finder.search_by_supervisor()
        elif choice == '2':
            project_finder.load_data()
            project_finder.search_by_keywords()
        elif choice == '3':
            print("Thank you for using Project Finder. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
