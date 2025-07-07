import pandas as pd
from datetime import datetime, time, timedelta
from django.utils.timezone import localtime, now

# Generate time slots with custom slot length (30 minutes)
def generate_time_slots(start_time, end_time, slot_minutes=30):
    slots = []
    current = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)
    while current + timedelta(minutes=slot_minutes) <= end:
        slots.append(current.time())
        current += timedelta(minutes=slot_minutes)
    return slots

# Format time as string
def format_time(t):
    return t.strftime("%I:%M %p")

# Configuration
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
TIME_SLOTS = generate_time_slots(time(8, 0), time(17, 0), slot_minutes=30)  # 30-minute slots
MAX_SESSION_MINUTES = 120  # 1.5 hours
BLOCK_SIZE = 30
MAX_SESSION_BLOCKS = MAX_SESSION_MINUTES // BLOCK_SIZE  # 3 blocks

# Subject list
subjects = [
    {"name": "Math", "hours_per_week": 6, "instructor": "Mr. Smith", "section": "Grade 7-A"},
    {"name": "Science", "hours_per_week": 3, "instructor": "Ms. Johnson", "section": "Grade 7-A"},
    {"name": "English", "hours_per_week": 4.5, "instructor": "Mr. Lee", "section": "Grade 8-B"},
    {"name": "PE", "hours_per_week": 1.5, "instructor": "Ms. Garcia", "section": "Grade 7-A"},
    {"name": "History", "hours_per_week": 3, "instructor": "Mr. Brown", "section": "Grade 8-B"}
]

# Allowed rooms per subject
room_subjects = {
    "Room A": ["Math", "History"],
    "Room B": ["Science", "English"],
    "Room C": ["English", "Math"],
    "Room D": ["PE"]
}

# Build subject-to-rooms mapping
subject_rooms = {}
for room, allowed_subjects in room_subjects.items():
    for subj in allowed_subjects:
        subject_rooms.setdefault(subj, []).append(room)

# Sort to prioritize subjects with fewer room options
subjects.sort(key=lambda s: len(subject_rooms.get(s['name'], [])))

# Trackers
schedule = []
used_slots = set()               # (day, time, room)
instructor_busy = set()          # (day, time, instructor)
section_busy = set()             # (day, time, section)
subject_daily_minutes = {}       # (subject, day) => minutes

# Scheduling logic
for subj in subjects:
    name = subj["name"]
    instructor = subj["instructor"]
    section = subj["section"]
    total_minutes = int(subj["hours_per_week"] * 60)
    allowed_rooms = subject_rooms.get(name, [])
    scheduled_minutes = 0

    for day in DAYS:
        if scheduled_minutes >= total_minutes:
            break

        for i in range(len(TIME_SLOTS)):
            if scheduled_minutes >= total_minutes:
                break

            for session_blocks in reversed(range(1, MAX_SESSION_BLOCKS + 1)):
                if i + session_blocks > len(TIME_SLOTS):
                    continue

                slot_block = TIME_SLOTS[i:i + session_blocks]
                session_minutes = session_blocks * BLOCK_SIZE

                if subject_daily_minutes.get((name, day), 0) + session_minutes > MAX_SESSION_MINUTES:
                    continue

                # Check instructor and section availability
                conflict = False
                for slot in slot_block:
                    if (day, slot, instructor) in instructor_busy or (day, slot, section) in section_busy:
                        conflict = True
                        break
                if conflict:
                    continue

                # Check room availability
                for room in allowed_rooms:
                    if all((day, slot, room) not in used_slots for slot in slot_block):
                        start_time = slot_block[0]
                        end_time = (datetime.combine(datetime.today(), slot_block[-1]) + timedelta(minutes=BLOCK_SIZE)).time()

                        schedule.append({
                            "Section": section,
                            "Subject": name,
                            "Instructor": instructor,
                            "Room": room,
                            "Day": day,
                            "Start Time": format_time(start_time),
                            "End Time": format_time(end_time),
                            "Hours": session_minutes / 60
                        })

                        for slot in slot_block:
                            used_slots.add((day, slot, room))
                            instructor_busy.add((day, slot, instructor))
                            section_busy.add((day, slot, section))

                        subject_daily_minutes[(name, day)] = subject_daily_minutes.get((name, day), 0) + session_minutes
                        scheduled_minutes += session_minutes
                        break  # room assigned
                if scheduled_minutes >= total_minutes:
                    break

# Export result


current_time = localtime(now())
print(current_time)
df = pd.DataFrame(schedule)
print(df)
df.to_excel("schedule_1_5_hour_blocks.xlsx", index=False)