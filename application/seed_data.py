import os
import django
import random
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

# Import des modèles après la configuration Django
from regions.models import Region
from lodge.models import Lodge
from accommodations.models import Accommodation, CategoryAccommodation, RoomType
from activities.models import Activity, ActivityCategory
from tourist_places.models import TouristPlace
from transports.models import Transport, TransportCategory
from reservations.models import Reservation
from blog.models import BlogPost

fake = Faker(['fr_FR'])  # Utilisation du français

def create_users(num_users=10):
    """Création des utilisateurs"""
    User = get_user_model()
    users = []
    
    # Créer un superuser si nécessaire
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@syllatah.com',
            password='admin123'
        )
    
    # Créer des utilisateurs normaux
    for _ in range(num_users):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number()
        )
        users.append(user)
    return users

def create_regions(num_regions=10):
    """Création des régions"""
    regions = []
    region_names = [
        'Conakry', 'Kindia', 'Boké', 'Mamou', 'Labé',
        'Kankan', 'Faranah', 'N\'Zérékoré', 'Siguiri', 'Guéckédou'
    ]
    
    for name in region_names[:num_regions]:
        region = Region.objects.create(
            name=name,
            description=fake.text(max_nb_chars=200),
            image=f'regions/{name.lower()}.jpg'
        )
        regions.append(region)
    return regions

def create_lodges(num_lodges=10):
    """Création des lodges"""
    lodges = []
    for _ in range(num_lodges):
        lodge = Lodge.objects.create(
            name=fake.company(),
            description=fake.text(max_nb_chars=200),
            address=fake.address(),
            phone=f'+224{fake.msisdn()[4:]}',  # Numéro guinéen
            email=fake.company_email(),
            type=random.choice(['hotel', 'resort', 'guesthouse']),
            is_active=True
        )
        lodges.append(lodge)
    return lodges

def create_categories_and_room_types(num_each=5):
    """Création des catégories et types de chambres"""
    categories = []
    room_types = []
    
    category_names = ['Luxe', 'Standard', 'Économique', 'Suite', 'VIP']
    room_type_names = ['Simple', 'Double', 'Triple', 'Familiale', 'Suite Présidentielle']
    
    for name in category_names[:num_each]:
        cat = CategoryAccommodation.objects.create(
            name=name
        )
        categories.append(cat)
    
    for name in room_type_names[:num_each]:
        room_type = RoomType.objects.create(
            name=name
        )
        room_types.append(room_type)
    
    return categories, room_types

def create_accommodations(num_accommodations=10, categories=None, room_types=None):
    """Création des hébergements"""
    accommodations = []
    for _ in range(num_accommodations):
        price = random.randint(50000, 500000)  # Prix en francs guinéens
        accommodation = Accommodation.objects.create(
            name=f"Chambre {fake.word().title()}",
            location=fake.address(),
            description=fake.text(max_nb_chars=200),
            price_per_night=price,
            capacity=random.randint(1, 6),
            category=random.choice(categories) if categories else None,
            room_types=random.choice(room_types) if room_types else None,
            amenities=fake.text(max_nb_chars=100)
        )
        accommodations.append(accommodation)
    return accommodations

def create_activity_categories(num_categories=5):
    """Création des catégories d'activités"""
    categories = []
    category_names = ['Sport', 'Culture', 'Bien-être', 'Aventure', 'Gastronomie']
    
    for name in category_names[:num_categories]:
        category = ActivityCategory.objects.create(
            name=name,
            description=fake.text(max_nb_chars=200)
        )
        categories.append(category)
    return categories

def create_activities(num_activities=10, categories=None):
    """Création des activités"""
    activities = []
    activity_types = ['Randonnée', 'Piscine', 'Spa', 'Restaurant', 'Sport']
    difficulty_choices = ['beginner', 'intermediate', 'advanced', 'expert']
    
    for _ in range(num_activities):
        duration_hours = random.randint(1, 8)
        activity = Activity.objects.create(
            name=f"{random.choice(activity_types)} {fake.word().title()}",
            category=random.choice(categories) if categories else None,
            description=fake.text(max_nb_chars=200),
            location=fake.address(),
            duration=timedelta(hours=duration_hours),
            difficulty=random.choice(difficulty_choices),
            min_participants=random.randint(1, 4),
            max_participants=random.randint(5, 20),
            price=Decimal(str(random.randint(10000, 100000))),
            equipment_provided=random.choice([True, False]),
            equipment_required=fake.text(max_nb_chars=100) if random.choice([True, False]) else '',
            age_restriction=random.randint(0, 18) if random.choice([True, False]) else None,
            fitness_level=random.randint(1, 5)
        )
        activities.append(activity)
    return activities

def create_tourist_places(num_places=10, regions=None):
    """Création des lieux touristiques"""
    places = []
    for _ in range(num_places):
        place = TouristPlace.objects.create(
            name=fake.city(),
            description=fake.text(max_nb_chars=200),
            region=random.choice(regions) if regions else None,
            image=f'tourist_places/place_{random.randint(1, 10)}.jpg'
        )
        places.append(place)
    return places

def create_transport_categories(num_categories=4):
    """Création des catégories de transport"""
    categories = []
    category_names = ['Taxi', 'Bus', 'Minibus', 'Voiture']
    
    for name in category_names[:num_categories]:
        category = TransportCategory.objects.create(
            name=name,
            description=fake.text(max_nb_chars=200)
        )
        categories.append(category)
    return categories

def create_transports(num_transports=10, categories=None):
    """Création des moyens de transport"""
    transports = []
    vehicle_types = ['Standard', 'Premium', 'VIP', 'Economique']
    languages = ['Français', 'Anglais', 'Soussou', 'Malinké', 'Poular']
    
    for _ in range(num_transports):
        num_languages = random.randint(1, 3)
        selected_languages = random.sample(languages, num_languages)
        
        transport = Transport.objects.create(
            company_name=fake.company(),
            transport_type=random.choice(['Taxi', 'Bus', 'Minibus', 'Voiture']),
            category=random.choice(categories) if categories else None,
            vehicle_type=random.choice(vehicle_types),
            capacity=random.randint(4, 50),
            luggage_capacity=random.randint(2, 100),
            air_conditioned=random.choice([True, False]),
            wifi_available=random.choice([True, False]),
            driver_languages=selected_languages,
            insurance_included=True,
            cancellation_policy=fake.text(max_nb_chars=200),
            schedule=f"{fake.time()} - {fake.time()}",
            price=Decimal(str(random.randint(50000, 500000))),
            description=fake.text(max_nb_chars=200),
            status=random.choice(['available', 'maintenance', 'booked', 'inactive'])
        )
        transports.append(transport)
    return transports

def create_reservations(num_reservations=10, users=None, accommodations=None, activities=None, transports=None):
    """Création des réservations"""
    reservations = []
    for _ in range(num_reservations):
        check_in = timezone.now() + timedelta(days=random.randint(1, 30))
        check_out = check_in + timedelta(days=random.randint(1, 7))
        base_price = Decimal(str(random.randint(100000, 500000)))
        taxes = base_price * Decimal('0.18')  # 18% TVA
        
        reservation = Reservation.objects.create(
            user=random.choice(users) if users else None,
            accommodation=random.choice(accommodations) if accommodations else None,
            reservation_number=f'RES-{fake.unique.random_number(digits=8)}',
            status='confirmed',
            payment_status='paid',
            check_in_date=check_in,
            check_out_date=check_out,
            base_price=base_price,
            taxes=taxes,
            total_price=base_price + taxes,
            amount_paid=base_price + taxes,
            number_of_guests=random.randint(1, 4),
            special_requests=fake.text(max_nb_chars=100) if random.choice([True, False]) else ''
        )
        
        if activities:
            reservation.activity = random.choice(activities)
        
        if transports:
            reservation.transport = random.choice(transports)
        
        reservation.save()
        reservations.append(reservation)
    return reservations

def create_blog_posts(num_posts=10, users=None):
    """Création des articles de blog"""
    posts = []
    for _ in range(num_posts):
        post = BlogPost.objects.create(
            title=fake.sentence(),
            content=fake.text(max_nb_chars=1000),
            author=random.choice(users) if users else None,
            image=f'blog/post_{random.randint(1, 10)}.jpg'
        )
        posts.append(post)
    return posts

def main():
    """Fonction principale pour créer toutes les données"""
    print("Création des données de test...")
    
    # Création dans l'ordre des dépendances
    users = create_users()
    print("✓ Utilisateurs créés")
    
    regions = create_regions()
    print("✓ Régions créées")
    
    lodges = create_lodges()
    print("✓ Lodges créés")
    
    categories, room_types = create_categories_and_room_types()
    print("✓ Catégories et types de chambres créés")
    
    accommodations = create_accommodations(
        categories=categories,
        room_types=room_types
    )
    print("✓ Hébergements créés")
    
    activity_categories = create_activity_categories()
    print("✓ Catégories d'activités créées")
    
    activities = create_activities(categories=activity_categories)
    print("✓ Activités créées")
    
    tourist_places = create_tourist_places(regions=regions)
    print("✓ Lieux touristiques créés")
    
    transport_categories = create_transport_categories()
    print("✓ Catégories de transport créées")
    
    transports = create_transports(categories=transport_categories)
    print("✓ Transports créés")
    
    reservations = create_reservations(
        users=users,
        accommodations=accommodations,
        activities=activities,
        transports=transports
    )
    print("✓ Réservations créées")
    
    blog_posts = create_blog_posts(users=users)
    print("✓ Articles de blog créés")
    
    print("\nToutes les données de test ont été créées avec succès!")
    print("\nVous pouvez vous connecter avec:")
    print("Admin - username: admin, password: admin123")
    print("Utilisateur test - username: (voir premier utilisateur créé), password: password123")

if __name__ == "__main__":
    main()
