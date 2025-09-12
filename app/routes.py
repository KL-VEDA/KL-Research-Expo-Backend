from flask import Blueprint, jsonify
from flask import request
from app.models import db, Team, Member
from sqlalchemy.exc import IntegrityError

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

    # Validate input
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    team_name = data.get("team_name")
    paper_drive_link = data.get("paper_drive_link")
    members_data = data.get("members")

    if not team_name or not members_data:
        return jsonify({"error": "Team name and members are required"}), 400

    try:
        # Create team without team_code initially
        team = Team(team_name=team_name, paper_drive_link=paper_drive_link)
        db.session.add(team)
        db.session.flush()  # Get team.team_id before committing

        # Generate the team_code in the format KL-RE25-xxxx
        team.team_code = f"KL-RE25-{team.team_id:04d}"

        # Validate only one team leader
        leaders = [m for m in members_data if m.get("is_team_leader")]
        if len(leaders) != 1:
            return jsonify({"error": "Exactly one team leader must be specified"}), 400

        # Create member records
        for m in members_data:
            member = Member(
                team_id=team.team_id,
                name=m.get("name"),
                contact=m.get("contact"),
                email=m.get("email"),
                is_team_leader=m.get("is_team_leader", False)
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
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
