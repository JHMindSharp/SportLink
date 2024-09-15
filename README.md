![SportLink Logo](https://image.noelshack.com/fichiers/2024/37/7/1726398352-sportlink.jpg
)

# SportLink

## Connect, Engage, Exercise, and Book with Similar Partners! (English)

SportLink is an app designed for amateur athletes and sports enthusiasts, allowing them to find sports partners, book equipment and venues, track their health, and organize activities effortlessly.

### Main Features:

1. **Health and Performance Tracking**:
   - Track sports performance and health statistics, inspired by Strava.
   - Get partner recommendations based on performance and sports profiles.

2. **Profile Creation and Networking**:
   - Users can create personal profiles with their sports preferences.
   - A 5-star rating system to evaluate users after sports meetups, assessing their reliability and social skills.
   - Search for sports partners in the local area based on shared activities and similar performance goals.

3. **Organize Sports Activities**:
   - Plan sports activities based on users' availability in the upcoming days.
   - Find sports facilities or nearby locations suitable for specific sports activities.
   - Built-in messaging system to contact other users and plan meetups.

4. **Equipment and Venue Booking**:
   - Book sports venues (fields, courts, gyms) and equipment.
   - Search for nearby facilities that don’t require reservations for sports activities without special equipment.

5. **Integrated Payments**:
   - Secure payments directly through the app for venue and equipment bookings, with PayPal and Apple Pay integration.

### Technologies Used:

- **Backend**: Flask
- **Frontend**: React Native
- **Database**: MongoDB
- **Internal APIs**: Health statistics tracking and profile management
- **Real-Time Messaging**: WebSocket
- **Payments**: Integrated with PayPal and Apple Pay
- **Deployment**: GitHub Actions and AWS
- **Testing**: `pytest` for backend, `Jest` for frontend

### Getting Started:

1. Clone the repository:
   ```bash
   git clone https://github.com/JHMindSharp/sportlink.git
   cd sportlink
   ```

2. Install dependencies:
   - Backend (Flask):
     ```bash
     pip install -r requirements.txt
     ```
   - Frontend (React Native):
     Follow the React Native setup instructions [here](https://reactnative.dev/docs/environment-setup).

3. Configure environment variables in `.env`:
   - Flask secret key
   - MongoDB database connection
   - PayPal and Apple Pay API keys
   - Email settings for Flask-Mail

4. Run the application:
   - Backend:
     ```bash
     flask run
     ```
   - Frontend:
     ```bash
     npm start
     ```

### Running Tests:

- Backend unit tests with `pytest`:
  ```bash
  pytest
  ```

- Frontend tests with `Jest`:
  ```bash
  npm test
  ```

### Deployment:

- The project uses GitHub Actions for continuous deployment to AWS.

### Contribution:

Contributions are welcome! If you have ideas or improvements, feel free to open an issue or submit a pull request.

---

# SportLink

## Connectez-vous, engagez, faites du sport et réservez avec des partenaires similaires ! (Français)

SportLink est une application destinée aux athlètes amateurs et passionnés de sport, leur permettant de trouver des partenaires sportifs, réserver des équipements et terrains, suivre leur santé, et organiser des activités en toute simplicité.

### Fonctionnalités principales :

1. **Suivi de la santé et des performances** :
   - Suivi des performances sportives et des statistiques de santé, inspiré de Strava.
   - Recommandations basées sur les performances et le profil sportif.

2. **Création de profil et mise en relation** :
   - Les utilisateurs peuvent créer un profil personnel avec leurs préférences sportives.
   - Système de notation à 5 étoiles permettant de savoir si une personne est fiable et socialement adaptée après chaque rencontre.
   - Recherche de partenaires sportifs dans la région, basés sur des activités communes et des objectifs de performance similaires.

3. **Organisation d'activités sportives** :
   - Planification d'activités sportives en fonction des disponibilités des utilisateurs dans les jours à venir.
   - Recherche d'infrastructures sportives ou de lieux de pratique proches pour des activités sportives spécifiques.
   - Messagerie intégrée pour contacter d'autres utilisateurs et organiser les rencontres.

4. **Réservation d'équipements et de terrains** :
   - Réservation d'infrastructures sportives (terrains, salles, etc.) et d'équipements.
   - Recherche d'infrastructures sans besoin de réservation pour les sports ne nécessitant pas de matériel spécifique.

5. **Paiements intégrés** :
   - Paiements sécurisés via l'application pour les réservations de terrains et d'équipements, avec intégration de PayPal et Apple Pay.

### Technologies utilisées :

- **Backend** : Flask
- **Frontend** : React Native
- **Base de données** : MongoDB
- **API internes** : Suivi des statistiques de santé et gestion des profils
- **Messagerie en temps réel** : WebSocket
- **Paiements** : PayPal et Apple Pay intégrés
- **Déploiement** : GitHub Actions et AWS
- **Tests** : `pytest` pour le backend et `Jest` pour le frontend

### Démarrer le projet :

1. Clonez le dépôt Git :
   ```bash
   git clone https://github.com/JHMindSharp/sportlink.git
   cd sportlink
   ```

2. Installez les dépendances :
   - Backend (Flask) :
     ```bash
     pip install -r requirements.txt
     ```
   - Frontend (React Native) :
     Suivez les instructions de configuration pour React Native [ici](https://reactnative.dev/docs/environment-setup).

3. Configurez les variables d'environnement dans le fichier `.env` :
   - Clé secrète Flask
   - Informations de connexion à la base de données MongoDB
   - Clés API pour PayPal et Apple Pay
   - Paramètres de messagerie pour Flask-Mail

4. Démarrez l'application :
   - Backend :
     ```bash
     flask run
     ```
   - Frontend :
     ```bash
     npm start
     ```

### Tests :

- Lancez les tests unitaires pour le backend avec `pytest` :
  ```bash
  pytest
  ```

- Lancez les tests pour le frontend avec `Jest` :
  ```bash
  npm test
  ```

### Déploiement :

- Le projet utilise GitHub Actions pour un déploiement continu vers AWS.

### Contribution :

Les contributions sont les bienvenues ! Si vous avez des idées ou des améliorations, n'hésitez pas à ouvrir une issue ou soumettre une pull request.

---

**SportLink** - Connect with sports partners, organize activities, and book equipment in just a few clicks!
