"""create tables

Revision ID: 9d7b62a738f4
Revises: 
Create Date: 2024-04-07 12:41:48.134603

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9d7b62a738f4"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "profile",
        sa.Column("first_name", sa.String(length=20), nullable=False),
        sa.Column("last_name", sa.String(length=30), nullable=False),
        sa.Column("occupation", sa.String(length=30), nullable=True),
        sa.Column("status", sa.Text(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("phone_number", sa.String(length=11), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_table(
        "friend",
        sa.Column("profile_id", sa.UUID(), nullable=False),
        sa.Column("friend_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["friend_id"],
            ["profile.id"],
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profile.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "profile_id", "friend_id", name="idx_unique_profile_friend"
        ),
    )
    op.create_table(
        "post",
        sa.Column("header", sa.String(length=50), nullable=False),
        sa.Column("hashtag", sa.String(length=30), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("likes", sa.Integer(), nullable=False),
        sa.Column(
            "written_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("profile_id", sa.UUID(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["profile_id"], ["profile.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("post")
    op.drop_table("friend")
    op.drop_table("profile")
    # ### end Alembic commands ###
