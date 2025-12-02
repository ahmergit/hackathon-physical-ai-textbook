"""Add Better Auth support - extend profiles with new fields

Revision ID: 20251202_add_better_auth_profile_fields
Revises: 20251130_simplify_profile
Create Date: 2025-12-02 01:54:28.000000

This migration:
1. Creates new enum types for skill levels and device types
2. Adds 4 new columns to profiles table
3. Migrates existing data from old columns to new columns
4. Drops old columns

New profile fields:
- hardware_skill: beginner | intermediate | expert
- programming_skill: beginner | intermediate | expert
- ai_ml_skill: beginner | intermediate | expert
- current_device: cloud_laptop | rtx_gpu | physical_robot
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = '20251202_add_better_auth_profile_fields'
down_revision = '20251130_simplify_profile'
branch_labels = None
depends_on = None

# Define enum types
skill_level_enum = postgresql.ENUM('beginner', 'intermediate', 'expert', name='skill_level')
device_type_enum = postgresql.ENUM('cloud_laptop', 'rtx_gpu', 'physical_robot', name='device_type')


def upgrade():
    """
    Apply migration: Add new profile fields for Better Auth integration
    """
    # Create enum types
    skill_level_enum.create(op.get_bind(), checkfirst=True)
    device_type_enum.create(op.get_bind(), checkfirst=True)

    # Add new columns to profiles table (nullable initially for data migration)
    op.add_column('profiles', sa.Column('hardware_skill', skill_level_enum, nullable=True))
    op.add_column('profiles', sa.Column('programming_skill', skill_level_enum, nullable=True))
    op.add_column('profiles', sa.Column('ai_ml_skill', skill_level_enum, nullable=True))
    op.add_column('profiles', sa.Column('current_device', device_type_enum, nullable=True))

    # Migrate existing data from old columns to new columns
    # Map old experience levels to new skill levels:
    # - ADVANCED → expert
    # - INTERMEDIATE → intermediate
    # - BEGINNER → beginner
    # - Default programming_skill to beginner (new field)
    # - Default current_device to cloud_laptop (new field)
    op.execute("""
        UPDATE profiles
        SET
            hardware_skill = CASE
                WHEN robotics_hardware_experience = 'ADVANCED' THEN 'expert'::skill_level
                WHEN robotics_hardware_experience = 'INTERMEDIATE' THEN 'intermediate'::skill_level
                ELSE 'beginner'::skill_level
            END,
            programming_skill = 'beginner'::skill_level,
            ai_ml_skill = CASE
                WHEN ai_agents_experience = 'ADVANCED' THEN 'expert'::skill_level
                WHEN ai_agents_experience = 'INTERMEDIATE' THEN 'intermediate'::skill_level
                ELSE 'beginner'::skill_level
            END,
            current_device = 'cloud_laptop'::device_type
        WHERE hardware_skill IS NULL
    """)

    # Make new columns NOT NULL after data migration
    op.alter_column('profiles', 'hardware_skill', nullable=False)
    op.alter_column('profiles', 'programming_skill', nullable=False)
    op.alter_column('profiles', 'ai_ml_skill', nullable=False)
    op.alter_column('profiles', 'current_device', nullable=False)

    # Drop old columns (no longer needed)
    op.drop_column('profiles', 'ai_agents_experience')
    op.drop_column('profiles', 'robotics_hardware_experience')


def downgrade():
    """
    Rollback migration: Restore old profile structure
    """
    # Add old columns back
    op.add_column('profiles', sa.Column('ai_agents_experience', sa.String(50), nullable=True))
    op.add_column('profiles', sa.Column('robotics_hardware_experience', sa.String(50), nullable=True))

    # Migrate data back from new columns to old columns
    op.execute("""
        UPDATE profiles
        SET
            robotics_hardware_experience = CASE
                WHEN hardware_skill = 'expert' THEN 'ADVANCED'
                WHEN hardware_skill = 'intermediate' THEN 'INTERMEDIATE'
                ELSE 'BEGINNER'
            END,
            ai_agents_experience = CASE
                WHEN ai_ml_skill = 'expert' THEN 'ADVANCED'
                WHEN ai_ml_skill = 'intermediate' THEN 'INTERMEDIATE'
                ELSE 'BEGINNER'
            END
    """)

    # Drop new columns
    op.drop_column('profiles', 'hardware_skill')
    op.drop_column('profiles', 'programming_skill')
    op.drop_column('profiles', 'ai_ml_skill')
    op.drop_column('profiles', 'current_device')

    # Drop enum types
    skill_level_enum.drop(op.get_bind(), checkfirst=True)
    device_type_enum.drop(op.get_bind(), checkfirst=True)
