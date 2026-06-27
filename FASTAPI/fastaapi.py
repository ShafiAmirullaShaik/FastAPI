from fastapi import FastAPI

app = FastAPI()

Items = [
    {
        'ID': 'COMP101',
        'name': 'Introduction to Computer Science',
        'description': 'Fundamentals of programming, algorithms, and data structures. This course covers basic programming concepts, problem-solving techniques, and introduction to data structures like arrays, linked lists, and trees.'
    },
    {
        'ID': 'WEB201',
        'name': 'Full Stack Web Development',
        'description': 'Learn to build modern web applications using HTML, CSS, JavaScript, and backend technologies. Covers responsive design, API development, and database integration.'
    },
    {
        'ID': 'DATA301',
        'name': 'Data Science and Machine Learning',
        'description': 'Explore data analysis, visualization, and machine learning algorithms. Includes practical projects using Python, pandas, scikit-learn, and TensorFlow.'
    },
    {
        'ID': 'CLOUD401',
        'name': 'Cloud Computing and DevOps',
        'description': 'Master cloud platforms (AWS, Azure, GCP), containerization with Docker, Kubernetes, CI/CD pipelines, and infrastructure as code.'
    },
    {
        'ID': 'SEC201',
        'name': 'Cybersecurity Fundamentals',
        'description': 'Learn security principles, encryption, network security, ethical hacking basics, and best practices for protecting applications and data.'
    }
]

@app.get("/")
def read_root():
    message = "Welcome to the FastAPI application!"
    return {"notification": message}

@app.get("/about")
def read_about():
    message = "This is a simple FastAPI application that demonstrates basic routing. You can access the root endpoint to see a welcome message, and the /about endpoint to learn more about this application."
    return {"about": message}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    item = next((i for i in Items if i['ID'] == item_id), None)
    if item:
        return {"item": item}
    else:
        return {"error": "Course not found."}