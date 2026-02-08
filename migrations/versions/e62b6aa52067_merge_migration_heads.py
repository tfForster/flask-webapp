"""merge migration heads

Revision ID: e62b6aa52067
Revises: 3019194c706d, c033a3336a08
Create Date: 2025-12-27 00:55:16.342204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e62b6aa52067'
down_revision = ('3019194c706d', 'c033a3336a08')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
