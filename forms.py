from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length


class TeamForm(FlaskForm):
    team_name = StringField(
        "Team name", validators=[DataRequired(), Length(min=4, max=255)]
    )
    team_description = TextAreaField("Team description")
    submit = SubmitField("Submit")


class ProjectForm(FlaskForm):
    project_name = StringField(
        "Project name", validators=[DataRequired(), Length(min=4, max=255)]
    )
    project_description = TextAreaField("Project description")
    is_completed = BooleanField("Is it completed?")
    team_selection = SelectField("Team")
    submit = SubmitField("Submit")

    def update_teams(self, teams):
        self.team_selection.choices = [(team.team_id, team.team_name) for team in teams]
