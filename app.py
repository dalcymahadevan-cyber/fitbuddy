from flask import Flask, render_template, request, redirect, url_for
from database import init_db, SessionLocal, User, WorkoutPlan
from ai_services import generate_fitness_plan

app = Flask(__name__)
init_db()  # Database tables initialisation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    db = SessionLocal()
    try:
        # 1. Form values-a get pannadhal
        name = request.form.get('name', 'User')
        age = request.form.get('age')
        weight = request.form.get('weight')
        fitness_goal = request.form.get('fitness_goal')
        intensity = request.form.get('intensity')

        # 2. User-a Database-la save pannanum
        new_user = User(
            name=name,
            age=int(age) if age else None,
            weight=int(weight) if weight else None,
            fitness_goal=fitness_goal,
            intensity=intensity
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # 3. AI response generate pannanum
        user_info = f"Name: {name}, Age: {age}, Weight: {weight}kg, Goal: {fitness_goal}, Intensity: {intensity}"
        ai_response = generate_fitness_plan(user_info)

        # 4. Workout plan-a Database-la save pannanum
        new_plan = WorkoutPlan(
            user_id=new_user.id,
            plan_content=ai_response,
            nutrition_tip="Eat balanced protein and stay hydrated!"  # Optional Tip
        )
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        # 5. Data-va HTML template-ukku pass pannanum
        return render_template('plan.html', user=new_user, plan=new_plan)

    finally:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)