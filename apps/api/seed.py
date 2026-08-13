import asyncio
from database import AsyncSessionLocal
from models import Institution, Programme, CompetencyUnit, User, Placement, EvidenceSubmission, Assessment
from security import hash_password
from models import UserRole

async def seed():
    async with AsyncSessionLocal() as session:
        # Create an institution
        institution = Institution(name="THe Kiambu National Polytechnic")
        session.add(institution)
        await session.commit()

        # Create a programme
        programme = Programme(institution_id = institution.id ,name="Computer Science Level 6",)
        session.add(programme)
        await session.commit()

        # Create competency units
        competency_unit1 = CompetencyUnit(programme_id = programme.id, code = "CSC101", name = "Introduction to Programming")

        competency_unit2 = CompetencyUnit(programme_id = programme.id, code = "CSC102", name = "Data Structures and Algorithms")

        competency_unit3 = CompetencyUnit(programme_id = programme.id, code = "CSC103", name ="Networking and Distributed Systems")

        competency_unit4 = CompetencyUnit(programme_id = programme.id, code = "CSC104", name = "Database Management Skills")

        competency_unit5 = CompetencyUnit(programme_id = programme.id, code = "CSC105", name = "Develop an Information System")

        # Adding the competency units to the session
        session.add_all([competency_unit1, competency_unit2, competency_unit3, competency_unit4, competency_unit5])
        # Commit the changes to the database
        await session.commit()

        # Create a user
        user = User(institution_id = institution.id, email = "victor@kiambupoly.ac.ke", hashed_password = hash_password("password123"), full_name = "Victor Wanjala", role = UserRole.SUPERVISOR)
        session.add(user)
        await session.commit()

        # TODO: Create 2 student Users, then Placement
        # Placement needs student.id and supervisor.id - commit users first