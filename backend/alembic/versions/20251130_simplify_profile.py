"""Simplify profile to 2 experience fields

Revision ID: 20251130_simplify_profile
Revises: 1ff6300a0768
Create Date: 2025-11-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20251130_simplify_profile'
down_revision: Union[str, None] = '1ff6300a0768'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns as VARCHAR first (to avoid enum complications)
    op.add_column('profiles', sa.Column('ai_agents_experience', sa.String(50), nullable=True))
    op.add_column('profiles', sa.Column('robotics_hardware_experience', sa.String(50), nullable=True))
    
    # Migrate data from old columns to new columns using text comparison
    # Map old values to new (none/expert -> beginner/advanced)
    op.execute("""
        UPDATE profiles SET 
            ai_agents_experience = CASE 
                WHEN ai_ml_experience::text IN ('none', 'beginner') THEN 'beginner'
                WHEN ai_ml_experience::text = 'intermediate' THEN 'intermediate'
                ELSE 'advanced'
            END,
            robotics_hardware_experience = CASE 
                WHEN robotics_experience::text IN ('none', 'beginner') THEN 'beginner'
                WHEN robotics_experience::text = 'intermediate' THEN 'intermediate'
                ELSE 'advanced'
            END
    """)
    
    # Set defaults for any null values
    op.execute("UPDATE profiles SET ai_agents_experience = 'beginner' WHERE ai_agents_experience IS NULL")
    op.execute("UPDATE profiles SET robotics_hardware_experience = 'beginner' WHERE robotics_hardware_experience IS NULL")
    
    # Make new columns non-nullable
    op.alter_column('profiles', 'ai_agents_experience', nullable=False)
    op.alter_column('profiles', 'robotics_hardware_experience', nullable=False)
    
    # Drop old columns
    op.drop_column('profiles', 'robotics_experience')
    op.drop_column('profiles', 'programming_experience')
    op.drop_column('profiles', 'ai_ml_experience')
    op.drop_column('profiles', 'learning_goals')
    op.drop_column('profiles', 'preferred_learning_style')
    op.drop_column('profiles', 'weekly_time_commitment')


def downgrade() -> None:
    # Add old columns back as VARCHAR
    op.add_column('profiles', sa.Column('robotics_experience', sa.String(50), nullable=True))
    op.add_column('profiles', sa.Column('programming_experience', sa.String(50), nullable=True))
    op.add_column('profiles', sa.Column('ai_ml_experience', sa.String(50), nullable=True))
    op.add_column('profiles', sa.Column('learning_goals', sa.Text(), nullable=True))
    op.add_column('profiles', sa.Column('preferred_learning_style', sa.String(100), nullable=True))
    op.add_column('profiles', sa.Column('weekly_time_commitment', sa.Integer(), nullable=True))
    
    # Migrate data back
    op.execute("""
        UPDATE profiles SET 
            robotics_experience = robotics_hardware_experience,
            programming_experience = 'beginner',
            ai_ml_experience = ai_agents_experience,
            learning_goals = 'Migrated from simplified profile'
    """)
    
    # Make required columns non-nullable
    op.alter_column('profiles', 'robotics_experience', nullable=False)
    op.alter_column('profiles', 'programming_experience', nullable=False)
    op.alter_column('profiles', 'ai_ml_experience', nullable=False)
    op.alter_column('profiles', 'learning_goals', nullable=False)
    
    # Drop new columns
    op.drop_column('profiles', 'ai_agents_experience')
    op.drop_column('profiles', 'robotics_hardware_experience')
