from app import create_app, db
from app.models import User, Service



def seed_services():
    if not Service.query.first():
        mock_services = [
            Service(name="Home Cleaning", category="Cleaning", price="KSh 1500", icon="🧹"),
            Service(name="Sofa Cleaning", category="Cleaning", price="KSh 3000", icon="🛋️"),
            Service(name="Tap Repair", category="Plumbing", price="KSh 800", icon="🔧"),
            Service(name="Hair Styling", category="Beauty", price="KSh 2000", icon="💇🏽‍♀️"),
        ]
        db.session.add_all(mock_services)
        db.session.commit()
        print("✅ Mock services seeded.")

app = create_app()

with app.app_context():
    db.create_all()
    print("📦 Tables created:", db.inspect(db.engine).get_table_names())  # ADD THIS
    seed_services()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
