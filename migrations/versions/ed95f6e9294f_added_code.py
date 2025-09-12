"""Added Code

Revision ID: ed95f6e9294f
Revises: 0a2c450f1930
Create Date: 2025-09-12 09:34:57.341046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed95f6e9294f'
down_revision = '0a2c450f1930'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('team_code', sa.String(length=64), nullable=True))
        batch_op.create_unique_constraint('uq_teams_team_code', ['team_code'])


def downgrade():
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.drop_constraint('uq_teams_team_code', type_='unique')
        batch_op.drop_column('team_code')
