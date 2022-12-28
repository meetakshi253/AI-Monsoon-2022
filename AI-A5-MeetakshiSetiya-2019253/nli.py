import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from fuzzywuzzy import process
import string

nltk.download('wordnet')
nltk.download('omw-1.4')

facts = []
to_assert = {'stream': False, 'semester': False, 'cgpa': False, 'corecreds': False,
             'spzlcreds': False, 'interestlist': False, 'grade': False, 'queried': False}

stream_code = {'cse': 1, 'ece': 2, 'csam': 3,
               'csd': 4, 'csai': 5, 'csb': 6, 'csss': 7}

course_code = {'ai ml': 1, 'ai/ml': 1, 'security cryptography': 2, 'algorithms': 3, 'theoretical computer science': 4, 'systems software development': 5,
               'mathematics': 6, 'computational biology': 7, 'hardware electronics': 8, 'design': 9, 'humanities social science': 10}

mandatory_courses = {1: ['Computer Networks', 'Technical Communication', 'Environmental Science'],
                     2: ['Digital Communication Systems', 'Digital Signal Processig', 'Technical Communication', 'Environmental Science'],
                     3: ['Scientific Computing', 'Probability and Random Processes', 'Linear Optimization', 'Statistical Inference', 'Technical Communication', 'Environmental Science'],
                     4: ['Computer Networks', 'Research Methods in Social Science and Design',
                         'Design of Interactive Systems', 'Technical Communication', 'Environmental Science'],
                     5: ['Machine Learning', 'Computer Networks', 'Artificial Intelligence', 'Ethics in AI',
                         'Technical Communication', 'Environmental Science'],
                     6: ['Biophysics', 'Algorithms in Computational Biology', 'Technical Communication', 'Environmental Science'],
                     7:  ['Computer Networks', 'Technical Communication', 'Environmental Science']}

elective_courses = {
    1: ['Artificial Intelligence', 'Machine Learning', 'Natural Language Processing',
        'Reinforcement Learning', 'Data Mining', 'Meta Learning', 'Edge AI',
        'Computer Vision', 'Deep Learning'],
    2: ['Foundations Of Computer Security', 'Network Anonymity & Privacy', 'Applied Cryptography',
        'Topics In Adaptive Cybersecurity', 'Topics In Cryptanalysis', 'Networks And System Security II',
        'Advanced Biometrics'],
    3: ['Modern Algorithm Design', 'Advanced Algorithms', 'Introduction to Graduate Algorithms',
        'Randomised Algorithms', 'Concurrent and Learned Data Structures', 'Approximation Algorithms',
        'Network Science'],
    4: ['Introduction to Quantum Computing', 'Theory of Computation', 'Program Verification',
        'Complexity Theory', 'Program Analysis', 'Decision Procedures'],
    5: ['Distributed Systems: Concepts & Design', 'Parallel Runtimes For Modern Processors',
        'Compilers', 'Advanced Operating Systems', 'Programmable Networking', 'Mobile Computing',
        'Software Development Using Open-Source', 'Multimedia Computing & Applications',
        'Systems Analysis, Design & Requirements Engineering'],
    6: ['Linear Optimization', 'Advanced Linear Algebra', 'Calculus in R^N', 'Scientific Computing',
        'Complex Analysis', 'Algebraic Number Theory', 'Finite & Spectral Element Methods',
        'Categorical Data Analysis'],
    7: ['Computational Gastronomy', 'Algorithms in Bioinformatics', 'Foundations of Modern Biology',
        'Biomedical Image Processing', 'Introduction to Mathematical Biology', 'Biophysics',
        'Data Science for Genomics', 'Systems and Synthetic Biology'],
    8: ['Memory Testing and Design', 'Digital Image Processing', 'Wireless System Implementation',
        'Statistical Signal Processing', 'Digital VLSI Design', 'Computer Architecture',
        'Introduction to Nanoelectronics', 'Control Theory', 'Robotics', 'Autonomous Driving'],
    9: ['Design of Interactive Systems', 'Human Centred AI', 'Introduction To Motion Graphics',
        'Introduction To Animation And Graphics', 'Game Design & Development', 'Introduction To 3D Animation',
        'Fundamentals Of Audio For Engineers', 'Advanced Topics In Human Centered Computing'],
    10: ['Game Theory', 'Foundations Of Finance', 'Industrial Organization', 'Ethics in AI',
         'Learning and Memory', 'Social Psychology', 'Entrepreneurial Kichadi', 'Philosophy of Mind',
         'Intersectionality Studies', 'Advanced Ethnographic Research Methods'],
    11: ['BTech. Project', 'Independent Project', 'Independent Study']
}


def get_semester(line):
    global facts
    if to_assert['semester']:
        return
    for i in range(len(line)-1):
        word1, pos1 = line[i]
        word2, pos2 = line[i+1]
        if (pos1 == 'CD' and word2 == 'semester'):
            word1 = word1[:1]  # just the number
            fact = f"py_semester({word1})"
            facts.append(fact)
            to_assert['semester'] = True
        elif (pos2 == 'CD' and word1 == 'semester'):
            word2 = word2[:1]
            fact = f"py_semester({word2})"
            facts.append(fact)
            to_assert['semester'] = True


def get_stream(line):
    global facts, stream_code
    if to_assert['stream']:
        return
    for i in range(len(line)-1):
        word1, pos1 = line[i]
        word2, _ = line[i+1]
        if (pos1 == 'NN') and (word2 == 'branch' or word2 == 'stream'):
            code = stream_code[word1]
            fact = f"py_stream({code})"
            facts.append(fact)
            to_assert['stream'] = code


def get_cgpa(line):
    global facts
    if to_assert['cgpa']:
        return
    for i in range(len(line)-1):
        word1, pos1 = line[i]
        word2, pos2 = line[i+1]
        if pos1 == 'CD' and word2 == 'cgpa':
            fact = f"py_cgpa({word1})"
            facts.append(fact)
            to_assert['cgpa'] = True
        if pos2 == 'CD' and word1 == 'cgpa':
            fact = f"py_cgpa({word2})"
            facts.append(fact)
            to_assert['cgpa'] = True


def get_credits(line):
    global facts
    if to_assert['corecreds'] and to_assert['spzlcreds']:
        return
    for i in range(len(line)-1):
        word1, pos1 = line[i]
        word2, _ = line[i+1]
        if pos1 == 'CD' and word2 == 'core-credits':
            fact = f"py_corecredits({word1})"
            facts.append(fact)
            to_assert['corecreds'] = True
        if pos1 == 'CD' and (word2 == 'specialization-credits' or word2 == 'spzl-credits'):
            fact = f"py_spzlcredits({word1})"
            facts.append(fact)
            to_assert['spzlcreds'] = True


def get_interests(line):
    global facts
    if "gpa" in dict(line):
        return
    for i in line:
        word, pos = i
        if pos == "JJ" or word == "like":
            course = get_interest_name(line)
            to_assert['interestlist'] = True
            if course:
                code = course_code[course]
                fact = f"py_interests({code})"
                facts.append(fact)
                return


def get_gpa_courses_done(line):
    global facts
    for i in range(len(line)-1):
        word1, pos1 = line[i]
        word2, pos2 = line[i+1]
        if (pos1 == 'CD' and word2 == 'gpa'):
            intr = get_interest_name(line)
            if (intr):
                c, t = get_course_name(intr)
                facts.append(f"py_grade('{c}', {word1})")
                facts.append(f"py_queried('{c}')")
                facts.append(f"py_type('{c}', '{t}')")
        elif (pos2 == 'CD' and word1 == 'gpa'):
            intr = get_interest_name(line)
            if (intr):
                c, t = get_course_name(intr)
                facts.append(f"py_grade('{c}', '{word2}')")
                facts.append(f"py_queried('{c}')")
                facts.append(f"py_type('{c}', '{t}')")


def get_course_name(course):
    global facts
    maxscore = 0
    bestcourse = ""
    besttype = ""
    if to_assert['stream']:
        for k in elective_courses.keys():
            courselist = elective_courses[k]
            c, s = process.extractOne(course, courselist)
            if s > maxscore:
                maxscore = s
                bestcourse = c
                besttype = "Elective per Interest"
        for k in mandatory_courses.keys():
            courselist = mandatory_courses[k]
            c, s = process.extractOne(course, courselist)
            if s >= maxscore:
                maxscore = s
                bestcourse = c
                if not besttype == "Department Mandatory":
                    besttype = "Elective per Interest"
                if k == to_assert['stream']:
                    besttype = "Department Mandatory"
        return bestcourse, besttype


def get_interest_name(line):
    intr = ""
    for i in range(len(line)-1, -1, -1):
        (word, pos) = line[i]
        if pos == "NN" or pos == "NNP" or pos == "NNS":
            intr = f"{word} {intr}"
        elif word == "theoretical" and intr.strip() == "computer science":
            intr = f"{word} {intr}"
        elif word == "computational" and intr.strip() == "biology":
            intr = f"{word} {intr}"
        elif word == "social" and "science" in intr.strip():
            intr = f"{word} {intr}"
        else:
            break
    if len(intr) > 0:
        return intr.strip()


def pos_tagging(tokenised_lines):
    tagged = []
    for l in tokenised_lines:
        tagged.append(nltk.pos_tag(l))
    return tagged


def preprocess(lines):
    # tokenize and remove stop words
    stop_words = set(stopwords.words('english'))
    tokenized_lines = []
    for line in lines:
        line = line.lower().strip()
        tokens = word_tokenize(line)
        cleaned_tokens = [t for t in tokens if not t in stop_words]
        cleaned_tokens = list(
            filter(lambda t: t not in string.punctuation, cleaned_tokens))
        tokenized_lines.append(cleaned_tokens)
    return tokenized_lines


def make_facts(tagged_lines):
    for i in tagged_lines:
        get_stream(i)

    if not to_assert['stream']:
        st = int(input("Enter your stream code: "))
        fact = f"py_stream({st})"
        facts.append(fact)
        to_assert['stream'] = st

    for i in tagged_lines:
        get_semester(i)
        get_cgpa(i)
        get_credits(i)
        get_interests(i)
        get_gpa_courses_done(i)
    # semester, gpa etc also'
    if not to_assert['semester']:
        sem = int(input("Enter the current semester of study: "))
        fact = f"py_semester({sem})"
        facts.append(fact)
        to_assert['semester'] = True

    if not to_assert['cgpa']:
        cg = float(input("Enter your current CGPA: "))
        fact = f"py_cgpa({cg})"
        facts.append(fact)
        to_assert['cgpa'] = True

    if to_assert['stream'] and to_assert['stream'] > 2:
        if not to_assert['spzlcreds']:
            spc = int(input("Enter the number of specialization credits done: "))
            fact = f"py_spzlcredits({spc})"
            facts.append(fact)
            to_assert['spzlcreds'] = True

    if not to_assert['corecreds']:
        cc = int(input("Enter the number of core credits done: "))
        fact = f"py_corecredits({cc})"
        facts.append(fact)
        to_assert['corecreds'] = True

    assert to_assert['interestlist'] == True, "Enter some interests and restart."


def main():
    lines = []
    with open("input.txt") as fileptr:
        lines = fileptr.readlines()
    preprocessed_lines = preprocess(lines)
    tagged_lines = pos_tagging(preprocessed_lines)
    make_facts(tagged_lines)
    with open("facts.pl", "w") as fileptr:
        facts.sort()
        for i in facts:
            fileptr.write(f"{i}.\n")


main()
