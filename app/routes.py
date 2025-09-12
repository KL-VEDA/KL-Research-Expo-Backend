from flask import Blueprint, jsonify
from flask import request
from app.models import db, Team, Member
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return jsonify({"message": "Welcome to the Flask API!"})

@main.route("/server_status")
def server_status():
    return jsonify({"status": True, "message": "Server is running!"})



@main.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    team_name = data.get("team_name")
    paper_drive_link = data.get("paper_drive_link")
    password = data.get("password")
    members_data = data.get("members")

    if not team_name or not members_data or not password:
        return jsonify({"error": "Team name, password, and members are required"}), 400

    try:
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create team
        team = Team(
            team_name=team_name,
            paper_drive_link=paper_drive_link,
            password=hashed_password
        )
        db.session.add(team)
        db.session.flush()

        # Generate team code
        team.team_code = f"KL-RE25-{team.team_id:04d}"

        # Ensure exactly one team leader
        leaders = [m for m in members_data if m.get("is_team_leader")]
        if len(leaders) != 1:
            return jsonify({"error": "Exactly one team leader must be specified"}), 400

        # Add members
        for m in members_data:
            member = Member(
                team_id=team.team_id,
                name=m.get("name"),
                contact=m.get("contact"),
                email=m.get("email"),
                is_team_leader=m.get("is_team_leader", False),
                degree_program=m.get("degree_program"),
                year_or_status=m.get("year_or_status"),
                institution=m.get("institution"),
                role=m.get("role")
            )
            db.session.add(member)

        db.session.commit()

        return jsonify({
            "message": "Team registered successfully",
            "team_id": team.team_id,
            "team_code": team.team_code
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e.orig)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500