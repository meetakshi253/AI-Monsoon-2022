from durable.lang import *
from colors import *

'''
scores:

interest: +2
branch preferred: +1
courses taken: +1 per course if avg gpa >= 8.5 (for > 2 courses)
courses taken: +0.5 per course if avg gpa < 8.5 and >= 7 (for > 2 courses)
internship done: +5 per
btp publication and grade>=9: +5 per publication
ip publication and grade>=9: +3 per publication
grade>=9 but no btp publication: +2
grade>=9 but no ip_publication: +1
'''

recommendations = {}

career_stream_mapping = {
    "cse": ["software developer", "security engineer", "ai/ml engineer", "researcher"],
    "csam": ["software developer", "data scientist", "researcher"],
    "csd": ["software developer", "graphic designer", "researcher"],
    "csai": ["software developer", "data scientist", "ai/ml engineer", "researcher"],
    "csss": ["software developer", "consultant", "researcher"],
    "csb": ["software developer", "computational biologist", "researcher"],
    "ece": ["hardware engineer", "researcher"],
}

career_courses_mapping = {
    "software developer": ["software development using open-source", "data structures and algorithms", "advanced programming", "fundamentals of database management systems"],
    "security engineer": ["foundations of computer security", "security engineering", "computer networks", "network security"],
    "ai/ml engineer": ["machine learning", "artificial intelligence", "deep learning", "human-centered ai"],
    "data scientist": ["data science", "machine learning", "big data analytics", "data mining"],
    "graphic designer": ["design processes and prespectives", "human computer interaction", "inclusive design & accessibility", "introduction to animation and graphics"],
    "consultant": ["game theory", "foundation of finance", "market design", "industrial organisation"],
    "computational biologist": ["introduction to quantitative biology", "computer aided drug design", "algorithms in computational biology", "cell biology and biochemistry"],
    "hardware engineer": ["embedded logic design", "memory testing and design", "digital hardware design", "digital circuits"],
}


def give_recommendations():
    global recommendations
    count = 0
    sorted_recommendations = sort_dictionary(recommendations)
    print(color("\n\nand done! here are future career paths the ai suggests for you: ",
          fg="blue", style="bold"))
    print(color("-------------------------------------------------------------", fg="blue"))
    for k, v in sorted_recommendations.items():
        if v >= 3:
            count += 1
            print(color(f"preference {count}: {k}", fg="green"))
    if count == 0:
        print(color("enough data not available to make relevant recommendation.", fg="red"))


def pathwise_course_gpa(path, priority):
    print(color(f"\n==== evaluating career path {path} ====", fg="cyan"))
    print(
        color(f"path relevant courses: {career_courses_mapping[path]}", fg="purple"))
    num_courses = int(input(
        "\nenter the number of courses you have done out of the ones shown above? "))
    assert num_courses >= 0 and num_courses < 5, "wrong number of courses"
    avg_gpa = float(input(
        "enter your average gpa in the courses you had taken out of the above (0 if not applicable): "))
    assert avg_gpa >= 0 and avg_gpa <= 10, "invalid gpa"
    fact = {"courses_taken": num_courses, "course_path": path,
            "avg_gpa": avg_gpa, "path_priority": priority}
    return fact


def sort_dictionary(dictionary):
    sorted_dictionary = []
    values = list(dictionary.values())
    values.sort(reverse=True)
    for i in range(len(values)):
        for key, value in dictionary.items():
            if value == values[i] and (key, value) not in sorted_dictionary:
                sorted_dictionary.append((key, value))
    sorted_dictionary = dict(sorted_dictionary)
    return sorted_dictionary


with ruleset('preferred_courses'):

    @when_all((m.path == "software developer"))
    def softwareDev(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "security engineer"))
    def securityEngg(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "data scientist"))
    def dataScientist(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "ai/ml engineer"))
    def aimlEngg(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "consultant"))
    def consultant(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "hardware engineer"))
    def hardwareEngg(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "computational biologist"))
    def compBiologist(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "graphic designer"))
    def graphicDes(c):
        fact = pathwise_course_gpa(c.m.path, c.m.priority)
        c.assert_fact("update_priorities", fact)

    @when_all((m.path == "researcher"))
    def researcher(c):
        print(
            color(f"\n==== evaluating career path {c.m.path} ====", fg="cyan"))
        btp_grade = 0
        ip_grade = [0, 0]
        btp_publications = 0
        ip_publications = [0, 0]
        btp = input("did you take any btp? (y/n) ")
        if btp == "y":
            btp_grade += int(input("what was your btp grade? "))
            btp_publications += int(
                input("how many publications did you get out of your btp? "))
        ips = int(input("how many ip(s) did you do? (0/1/2) "))
        for i in range(ips):
            ipg = int(input(f"what was your grade in ip{i+1}? "))
            ip_grade[i] = ipg
            ipp = int(
                input(f"how many publications did you get out of this ip{i+1}? "))
            ip_publications[i] = ipp
        fact = {"course_path": c.m.path, "path_priority": c.m.priority, "btp_grade": btp_grade, "btp_pub": btp_publications,
                "ip_grade1": ip_grade[0], "ip_pub1": ip_publications[0], "ip_grade2": ip_grade[1], "ip_pub2": ip_publications[1]}
        c.assert_fact("update_priorities", fact)


with ruleset('update_priorities'):

    @when_all((m.courses_taken > 2) & (m.avg_gpa >= 8.5))
    def update(c):
        new_priority = c.m.courses_taken + c.m.path_priority
        fact = {"final_path": c.m.course_path, "final_priority": new_priority}
        c.assert_fact("update_priorities", fact)

    @when_all((m.courses_taken > 2) & (m.avg_gpa < 8.5) & (m.avg_gpa >= 7))
    def update(c):
        new_priority = 0.5*c.m.courses_taken + c.m.path_priority
        fact = {"final_path": c.m.course_path, "final_priority": new_priority}
        c.assert_fact("update_priorities", fact)

    @when_all((m.courses_taken <= 2) | (m.avg_gpa < 7))
    def update(c):
        fact = {"final_path": c.m.course_path,
                "final_priority": c.m.path_priority}
        c.assert_fact("update_priorities", fact)

    @when_all((m.course_path == "researcher"))
    def update(c):
        add_priority = 0
        if c.m.btp_grade >= 9:
            add_priority += c.m.btp_pub*5 if c.m.btp_pub > 0 else 2
        if c.m.ip_grade1 >= 9:
            add_priority += c.m.ip_pub1*3 if c.m.ip_pub1 > 0 else 1
        if c.m.ip_grade2 >= 9:
            add_priority += c.m.ip_pub2*3 if c.m.ip_pub2 > 0 else 1
        new_priority = c.m.path_priority + add_priority
        fact = {"final_path": c.m.course_path,
                "final_priority": new_priority}
        c.assert_fact("update_priorities", fact)

    @when_all((+m.final_path))
    def push_to_dict(c):
        recommendations[c.m.final_path] = c.m.final_priority


def main():
    priorities = {}
    internships = []
    interests = []

    print(color("-- CAREER ADVISORY SYSTEM FOR GRADUATING IIITD STUDENTS --",
          style="bold", fg="blue"))

    stream = input("\nenter the stream you are enrolled in: ")
    assert stream in ["cse", "csam", "ece", "csd",
                      "csss", "csb", "csai"], "incorrect stream"

    paths = ["software developer", "security engineer", "data scientist", "ai/ml engineer", "consultant", "hardware engineer",
             "computational biologist", "graphic designer", "researcher"]
    print(color(f"\npotential career paths: {paths}", fg="purple"))
    num_interests = int(
        input("how many career paths out of the above are you open to exploring? "))
    assert num_interests >= 0 and num_interests <= 9, "invalid number of paths"

    for i in range(num_interests):
        interest = input(
            f"enter path{i+1} you are interested in from the above list (as is). ")
        assert interest in paths, "path does not exist in the knowledge base"
        assert interest not in interests, "please enter a path only once"
        interests.append(interest)

    num_internships = int(input("\nhow many internship(s) have you done? "))
    for i in range(num_internships):
        internship_path = input(
            f"enter the career path your internship{i+1} was based on: ")
        assert internship_path in paths, "path does not exist in the knowledge base"
        internships.append(internship_path)

    for i in paths:
        priority = 0
        if i in interests:
            priority += 2
        if i in career_stream_mapping[stream]:
            priority += 1
        if i in internships:
            priority += 5
        priorities[i] = priority

    post('preferred_courses', {
        "path": "software developer", "priority": priorities["software developer"]})
    post('preferred_courses', {
        "path": "security engineer", "priority": priorities["security engineer"]})
    post('preferred_courses', {
        "path": "data scientist", "priority": priorities["data scientist"]})
    post('preferred_courses', {
        "path": "ai/ml engineer", "priority": priorities["ai/ml engineer"]})
    post('preferred_courses', {
        "path": "consultant", "priority": priorities["consultant"]})
    post('preferred_courses', {
        "path": "hardware engineer", "priority": priorities["hardware engineer"]})
    post('preferred_courses', {
        "path": "computational biologist", "priority": priorities["computational biologist"]})
    post('preferred_courses', {
        "path": "graphic designer", "priority": priorities["graphic designer"]})
    post('preferred_courses', {
        "path": "researcher", "priority": priorities["researcher"]})
    give_recommendations()


main()
