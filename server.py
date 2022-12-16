from flask import Flask, render_template, redirect, url_for
from forms import TeamForm, ProjectForm
from model import db, User, Team, Project, connect_to_db

app = Flask(__name__)
app.secret_key = "keep this secret"

user_id = 1


@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    return render_template("home.html", team_form=team_form, project_form=project_form)


@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        team_description = team_form.team_description.data
        new_team = Team(team_name, user_id, team_description=team_description)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        project_description = project_form.project_description.data
        is_completed = project_form.is_completed.data
        team_id = project_form.team_selection.data

        new_project = Project(
            project_name, is_completed, team_id, project_description=project_description
        )
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/teams")
def get_teams():
    teams = (
        db.session.query(Team)
        .filter_by(user_id=user_id)
        .order_by(Team.team_id.asc())
        .all()
    )

    team_forms = []

    for team in teams:
        team_forms.append(
            TeamForm(team_name=team.team_name, team_description=team.team_description)
        )

    return render_template("teams.html", teams=teams, team_forms=team_forms)


@app.route("/edit-team/<team_id>", methods=["POST"])
def edit_team(team_id):
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_to_update = Team.query.filter_by(team_id=team_id).first()
        team_to_update.team_name = team_form.team_name.data
        team_to_update.team_description = team_form.team_description.data
        db.session.add(team_to_update)
        db.session.commit()
        return redirect(url_for("get_teams"))
    else:
        return redirect(url_for("get_teams"))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True)
