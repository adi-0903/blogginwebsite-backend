from datetime import date, timedelta, time

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone

from blog.models import Category, Series, Post, Event


class Command(BaseCommand):
    help = "Seed demo data for categories, series, posts, and events"

    def handle(self, *args, **options):
        User = get_user_model()

        # Create or get demo user
        demo_user, created = User.objects.get_or_create(
            email="demo@example.com",
            defaults={
                "username": "demo",
                "first_name": "Demo",
                "last_name": "User",
                "is_staff": True,
            },
        )
        if created:
            demo_user.set_password("demo1234")
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo user (email: demo@example.com, password: demo1234)"))
        else:
            self.stdout.write("Demo user already exists")

        # Categories
        category_names = ["Culture", "Travel", "Design", "Opinion", "Personal", "Technology"]
        categories = {}
        for name in category_names:
            cat, _ = Category.objects.get_or_create(name=name)
            categories[name] = cat
        self.stdout.write(f"Ensured {len(categories)} categories")

        # Series
        series_data = [
            {
                "title": "Writers on the Road",
                "subtitle": "Stories from journeys that shaped us",
                "description": "A collection of essays about travel, identity, and creative discovery.",
                "icon": "🌍",
                "status": "active",
                "tags": "travel,identity,stories",
                "gradient": "linear-gradient(135deg, #6dd5ed, #2193b0)",
                "accent_color": "#2193b0",
            },
            {
                "title": "Design Futures",
                "subtitle": "Where craft meets technology",
                "description": "Exploring the evolving landscape of design, tools, and storytelling.",
                "icon": "🎨",
                "status": "active",
                "tags": "design,technology,craft",
                "gradient": "linear-gradient(135deg, #b993d6, #8ca6db)",
                "accent_color": "#8ca6db",
            },
        ]

        series_records = []
        for data in series_data:
            obj, _ = Series.objects.get_or_create(
                title=data["title"],
                defaults={**data, "author": demo_user},
            )
            series_records.append(obj)
        self.stdout.write(f"Ensured {len(series_records)} series")

        # Posts
        now = timezone.now()
        post_data = [
            {
                "title": "Finding Voice Between Cities",
                "excerpt": "On learning to listen to the silence between departures and arrivals.",
                "content": "Long-form story content about travel, belonging, and creative expression.",
                "icon": "📝",
                "category": categories["Travel"],
                "series": series_records[0],
                "status": "published",
                "is_featured": True,
                "read_time": 6,
                "gradient": "linear-gradient(135deg, rgba(99, 221, 190, 0.2), rgba(76, 175, 215, 0.1))",
                "published_at": now - timedelta(days=3),
            },
            {
                "title": "Sketching Tomorrow's Interfaces",
                "excerpt": "How designers can prototype feelings, not just screens.",
                "content": "Thoughts on design practice, tooling, and intentional storytelling in product work.",
                "icon": "🎨",
                "category": categories["Design"],
                "series": series_records[1],
                "status": "published",
                "is_featured": True,
                "read_time": 7,
                "gradient": "linear-gradient(135deg, rgba(181, 169, 255, 0.2), rgba(120, 88, 255, 0.1))",
                "published_at": now - timedelta(days=1),
            },
            {
                "title": "A Quiet Technology",
                "excerpt": "Building tools that disappear so stories can stay in focus.",
                "content": "Reflections on technology that supports creativity without demanding attention.",
                "icon": "💡",
                "category": categories["Technology"],
                "series": None,
                "status": "published",
                "is_featured": False,
                "read_time": 5,
                "gradient": "linear-gradient(135deg, rgba(163, 203, 255, 0.2), rgba(108, 156, 255, 0.1))",
                "published_at": now - timedelta(days=2),
            },
        ]

        for data in post_data:
            Post.objects.update_or_create(
                title=data["title"],
                defaults={**data, "author": demo_user},
            )
        self.stdout.write(f"Ensured {len(post_data)} posts")

        # Events
        today = date.today()
        event_data = [
            {
                "title": "Writing Lab: Scenes that Breathe",
                "description": "A 90-minute workshop on crafting immersive scenes and pacing.",
                "event_type": "workshop",
                "date": today + timedelta(days=5),
                "time": time(17, 0),
                "end_time": time(18, 30),
                "location": "Online",
                "is_virtual": True,
                "price": 0,
                "is_free": True,
                "max_attendees": 50,
                "gradient": "linear-gradient(135deg, rgba(255, 177, 71, 0.2), rgba(255, 87, 34, 0.1))",
                "accent_color": "#ffb147",
            },
            {
                "title": "Design Crit Night",
                "description": "Share work-in-progress and get constructive feedback from peers.",
                "event_type": "meetup",
                "date": today + timedelta(days=12),
                "time": time(19, 0),
                "location": "Creative Hub, Downtown",
                "is_virtual": False,
                "price": 15,
                "is_free": False,
                "max_attendees": 30,
                "gradient": "linear-gradient(135deg, rgba(181, 169, 255, 0.2), rgba(120, 88, 255, 0.1))",
                "accent_color": "#7858ff",
            },
        ]

        for data in event_data:
            Event.objects.update_or_create(
                title=data["title"],
                defaults={**data, "organizer": demo_user},
            )
        self.stdout.write(f"Ensured {len(event_data)} events")

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
