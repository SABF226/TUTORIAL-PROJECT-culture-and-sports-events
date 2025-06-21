import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json
import csv
from PIL import Image, ImageTk
import os
from datetime import datetime
import re
import uuid
import shutil

FICHIER_JSON = "evenements.json"

# Constantes de couleurs pour une cohérence visuelle
COLORS = {
    "primary": "#0077B6",        # Bleu vif (principal)
    "primary_dark": "#023E8A",   # Bleu foncé pour hover
    "secondary": "#47b1e8",      # vif pour les accents
    "accent": "#4b48e0",         # Orange profond pour éléments spéciaux
    "success": "#14aee6",        # Vert moderne (inchangé)
    "warning": "#0567E7",        # Jaune-orangé pour avertissements
    "danger": "#EF233C",         # Rouge vif pour danger
    "light": "#F1FAEE",          # Blanc cassé très doux (bleuté)
    "lighter": "#E0E1DD",        # Gris très clair moderne
    "white": "#ffffff",          # Blanc pur
    "dark": "#22223B",           # Bleu nuit/gris foncé moderne
    "text_primary": "#1a202c",   # Texte principal très foncé
    "text_secondary": "#495662", # Texte secondaire (bleu-gris)
    "gradient_start": "#00B4D8", # Début du dégradé (bleu clair)
    "gradient_end": "#03FBFF"    # Fin du dégradé (orange)
}
# Traductions
TRANSLATIONS = {
    "fr": {
        "app_title": "FASO SPORT & CULTURE EVENTS",
        "menu": "MENU",
        "create_event": "Créer un événement",
        "reserve_place": "Réserver une place",
        "events_news": "Actualités des événements",
        "promote_event": "Promouvoir un événement",
        "welcome": "Bienvenue sur FeastAppFaso",
        "book_place": "Réserver une place",
        "search_placeholder": "Rechercher un événement...",
        "discover_events": "Découvrir les événements en vedette",
        "no_events": "Aucun événement disponible",
        "register": "S'inscrire",
        "export_list": "Exporter la liste",
        "pay_online": "Payer en ligne",
        "my_reservations": "Mes réservations",
        "event_info": "Informations de l'événement",
        "member_info": "Informations du membre",
        "event_name": "Nom de l'événement",
        "location": "Lieu",
        "date_time": "Date et heure (AAAA-MM-JJ HH:MM)",
        "price": "Prix par ticket",
        "capacity": "Nombre de places disponibles",
        "image_path": "Chemin de l'image (optionnel)",
        "next": "Suivant →",
        "back": "Retour",
        "add_member": "Ajouter un membre",
        "save_event": "Sauvegarder l'événement",
        "member_name": "Nom du membre",
        "role": "Rôle",
        "email": "Email",
        "type": "Type",
        "name": "Nom",
        "date": "Date",
        "place": "Lieu",
        "price_label": "Prix",
        "capacity_label": "Capacité",
        "participants": "participant(s)",
        "no_image": "[Pas d'image]",
        "image_not_found": "[Image non trouvée]",
        "fields_incomplete": "Veuillez remplir tous les champs obligatoires.",
        "invalid_date": "La date doit être au format AAAA-MM-JJ HH:MM\nExemple: 2024-03-20 14:30",
        "invalid_price": "Le prix doit être un nombre positif.",
        "invalid_capacity": "La capacité doit être un nombre entier positif.",
        "success": "Succès",
        "error": "Erreur",
        "event_created": "L'événement '{}' a été créé avec succès!",
        "member_added": "Le membre {} ({}) a été ajouté avec succès.",
        "incomplete_fields": "Veuillez remplir tous les champs.",
        "invalid_contact": "Le contact doit être un email valide.",
        "event_type": "Type d'événement",
        "event_location": "Lieu de l'événement",
        "event_date_time": "Date et heure de l'événement",
        "event_price": "Prix par ticket",
        "event_capacity": "Nombre de places disponibles",
        "event_image": "Chemin de l'image (optionnel)",
        "staff_member_name": "Nom du membre",
        "staff_member_role": "Rôle du membre",
        "staff_member_email": "Email du membre",
        "logo_error": "[Erreur de logo]",
        "image_error": "[Erreur de chargement de l'image]",
        "image_not_found_error": "[Image non trouvée]",
        "export_success": "Liste exportée avec succès",
        "export_error": "Erreur lors de l'exportation",
        "payment_success": "Paiement effectué avec succès",
        "payment_error": "Erreur lors du paiement",
        "reservation_success": "Réservation effectuée avec succès",
        "reservation_error": "Erreur lors de la réservation",
        "no_events": "Aucun événement disponible",
        "no_events_for_export": "Aucun événement disponible pour l'exportation",
        "no_events_for_payment": "Aucun événement disponible pour le paiement",
        "no_events_for_reservation": "Aucun événement disponible pour la réservation",
        "event_full": "Désolé, cet événement est complet",
        "invalid_email": "Email invalide",
        "enter_valid_email": "Veuillez entrer un email valide",
        "enter_name": "Veuillez entrer votre nom",
        "enter_phone": "Veuillez entrer votre numéro de téléphone",
        "invalid_phone": "Le numéro de téléphone doit être au format +226 00 00 00 00",
        "promotion_success": "Merci {} !\nNous vous contacterons au {} pour discuter de la promotion de votre événement",
        "promotion_error": "Erreur lors de la soumission de la promotion",
        "no_reservations": "Vous n'avez aucune réservation",
        "reservations_title": "Mes réservations",
        "enter_email_for_reservations": "Veuillez entrer votre email",
        "export_list_title": "Exporter la liste",
        "save_list_title": "Enregistrer la liste",
        "online_payment_title": "Paiement en ligne",
        "pay_button": "Payer",
        "export_button": "Exporter",
        "register_button": "S'inscrire",
        "back_button": "Retour",
        "next_button": "Suivant",
        "add_member_button": "Ajouter un membre",
        "save_event_button": "Sauvegarder l'événement",
        "ok_button": "OK",
        "cancel_button": "Annuler",
        "delete_event": "Supprimer l'événement",
        "delete_confirmation": "Êtes-vous sûr de vouloir supprimer l'événement '{}' ?",
        "delete_success": "L'événement '{}' a été supprimé avec succès",
        "delete_error": "Erreur lors de la suppression de l'événement",
        "delete_button": "Supprimer",
        "confirm_delete": "Êtes-vous sûr de vouloir supprimer cet événement ?"
    },
    "en": {
        "app_title": "FASO SPORT & CULTURE EVENTS",
        "menu": "MENU",
        "create_event": "Create an Event",
        "reserve_place": "Book a Place",
        "events_news": "Event News",
        "promote_event": "Promote an Event",
        "welcome": "Welcome to feastAppFaso",
        "book_place": "Book a Place",
        "search_placeholder": "Search for an event...",
        "discover_events": "Discover featured events",
        "no_events": "No events found.",
        "register": "Register",
        "export_list": "Export List",
        "pay_online": "Pay Online (Simulation)",
        "my_reservations": "My Bookings",
        "event_info": "Event Information",
        "member_info": "Member Information",
        "event_name": "Event Name",
        "location": "Location",
        "date_time": "Date and Time (YYYY-MM-DD HH:MM)",
        "price": "Price per Ticket",
        "capacity": "Available Seats",
        "image_path": "Image Path (Optional)",
        "next": "Next →",
        "back": "← Back",
        "add_member": "Add Member",
        "save_event": "Save Event",
        "member_name": "Member Name",
        "role": "Role",
        "email": "Email",
        "type": "Type",
        "name": "Name",
        "date": "Date",
        "place": "Location",
        "price_label": "Price",
        "capacity_label": "Capacity",
        "participants": "participant(s)",
        "no_image": "[No Image]",
        "image_not_found": "[Image Not Found]",
        "fields_incomplete": "Please fill in all required fields.",
        "invalid_date": "Date must be in YYYY-MM-DD HH:MM format\nExample: 2024-03-20 14:30",
        "invalid_price": "Price must be a positive number.",
        "invalid_capacity": "Capacity must be a positive integer.",
        "success": "Success",
        "error": "Error",
        "event_created": "Event '{}' has been created successfully!",
        "member_added": "Member {} ({}) has been added successfully.",
        "incomplete_fields": "Please fill in all fields.",
        "invalid_contact": "Contact must be a valid email address.",
        "event_type": "Event Type",
        "event_location": "Event Location",
        "event_date_time": "Event Date and Time",
        "event_price": "Price per Ticket",
        "event_capacity": "Available Seats",
        "event_image": "Image Path (Optional)",
        "staff_member_name": "Staff Member Name",
        "staff_member_role": "Staff Member Role",
        "staff_member_email": "Staff Member Email",
        "logo_error": "[Logo Error]",
        "image_error": "[Error Loading Image]",
        "image_not_found_error": "[Image Not Found]",
        "export_success": "List exported successfully",
        "export_error": "Error exporting list",
        "payment_success": "Payment successful",
        "payment_error": "Error processing payment",
        "reservation_success": "Reservation completed successfully",
        "reservation_error": "Error during reservation",
        "no_events": "No events available",
        "no_events_for_export": "No events available for export",
        "no_events_for_payment": "No events available for payment",
        "no_events_for_reservation": "No events available for booking",
        "event_full": "Event is full.",
        "invalid_email": "Invalid email address",
        "enter_valid_email": "Please enter a valid email address",
        "enter_name": "Please enter your name",
        "enter_phone": "Please enter your phone number",
        "invalid_phone": "Phone number must be in format +226 00 00 00 00",
        "promotion_success": "Thank you {}!\nWe will contact you at {} to discuss promoting your event",
        "promotion_error": "Error submitting promotion request",
        "no_reservations": "You have no bookings",
        "reservations_title": "My Bookings",
        "enter_email_for_reservations": "Please enter your email",
        "export_list_title": "Export List",
        "save_list_title": "Save List",
        "online_payment_title": "Online Payment",
        "pay_button": "Pay",
        "export_button": "Export",
        "register_button": "Register",
        "back_button": "Back",
        "next_button": "Next",
        "add_member_button": "Add Member",
        "save_event_button": "Save Event",
        "ok_button": "OK",
        "cancel_button": "Cancel",
        "delete_event": "Delete Event",
        "delete_confirmation": "Are you sure you want to delete the event '{}'?",
        "delete_success": "Event '{}' has been deleted successfully",
        "delete_error": "Error deleting event",
        "delete_button": "Delete",
        "already_registered": "You are already registered for this event"
    }
}

def generer_id_unique():
    """Génère un ID unique pour un événement."""
    return str(uuid.uuid4())

def valider_evenement(evenement):
    """Valide tous les champs d'un événement."""
    erreurs = []
    
    # Validation du titre (nom)
    title = evenement.get('title') or evenement.get('nom')
    if not title or len(title.strip()) < 3:
        erreurs.append("Le titre de l'événement doit contenir au moins 3 caractères")
    
    # Validation du type
    if not evenement.get('type') or len(evenement['type'].strip()) < 2:
        erreurs.append("Le type d'événement doit contenir au moins 2 caractères")
    
    # Validation du lieu
    location = evenement.get('location') or evenement.get('lieu')
    if not location or len(location.strip()) < 3:
        erreurs.append("Le lieu doit contenir au moins 3 caractères")
    
    # Validation de la date
    date_str = evenement.get('date', '')
    time_str = evenement.get('time', '')
    
    if date_str and time_str:
        try:
            datetime_str = f"{date_str} {time_str}"
            date_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            # Vérifier que la date n'est pas dans le passé
            if date_obj < datetime.now():
                erreurs.append("La date de l'événement ne peut pas être dans le passé")
        except ValueError:
            erreurs.append("La date doit être au format AAAA-MM-JJ HH:MM (exemple: 2024-03-20 14:30)")
    else:
        erreurs.append("La date et l'heure de l'événement sont obligatoires")
    
    # Validation du prix
    price = evenement.get('price') or evenement.get('prix', 0)
    try:
        prix = float(price)
        if prix < 0:
            erreurs.append("Le prix ne peut pas être négatif")
        elif prix > 10000:
            erreurs.append("Le prix ne peut pas dépasser 10 000 €")
    except (ValueError, TypeError):
        erreurs.append("Le prix doit être un nombre valide")
    
    # Validation de la capacité
    capacity = evenement.get('capacity') or evenement.get('capacite', 0)
    try:
        capacite = int(capacity)
        if capacite <= 0:
            erreurs.append("La capacité doit être supérieure à 0")
        elif capacite > 10000:
            erreurs.append("La capacité ne peut pas dépasser 10 000 personnes")
    except (ValueError, TypeError):
        erreurs.append("La capacité doit être un nombre entier valide")
    
    # Validation du staff
    if not evenement.get('staff') or len(evenement['staff']) == 0:
        erreurs.append("Au moins un membre du staff doit être ajouté")
    else:
        for i, membre in enumerate(evenement['staff']):
            if not membre.get('nom') or len(membre['nom'].strip()) < 2:
                erreurs.append(f"Le nom du membre {i+1} doit contenir au moins 2 caractères")
            if not membre.get('rôle') or len(membre['rôle'].strip()) < 2:
                erreurs.append(f"Le rôle du membre {i+1} doit contenir au moins 2 caractères")
            if not membre.get('contact') or '@' not in membre['contact']:
                erreurs.append(f"L'email du membre {i+1} n'est pas valide")
    
    # Validation du chemin d'image (optionnel)
    if evenement.get('image_path'):
        if not os.path.exists(evenement['image_path']):
            erreurs.append("Le fichier image spécifié n'existe pas")
    
    # Validation de l'ID unique
    if not evenement.get('id'):
        erreurs.append("L'événement doit avoir un ID unique")
    
    return erreurs

def charger_evenements():
    """Charge les événements depuis le fichier JSON."""
    try:
        with open(FICHIER_JSON, "r", encoding='utf-8') as f:
            evenements = json.load(f)
            # Vérifier que chaque événement a un ID
            for evenement in evenements:
                if 'id' not in evenement:
                    evenement['id'] = generer_id_unique()
            return evenements
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Erreur lors de la lecture du fichier JSON. Création d'un nouveau fichier.")
        return []

def sauvegarder_evenements(evenements):
    """Sauvegarde les événements dans le fichier JSON."""
    try:
        # S'assurer que chaque événement a un ID
        for evenement in evenements:
            if 'id' not in evenement:
                evenement['id'] = generer_id_unique()
        
        # Créer une sauvegarde avant d'écrire
        if os.path.exists(FICHIER_JSON):
            backup_file = f"{FICHIER_JSON}.backup"
            with open(FICHIER_JSON, "r", encoding='utf-8') as f:
                backup_data = f.read()
            with open(backup_file, "w", encoding='utf-8') as f:
                f.write(backup_data)
        
        # Sauvegarder les événements
        with open(FICHIER_JSON, "w", encoding='utf-8') as f:
            json.dump(evenements, f, indent=2, ensure_ascii=False)
        
        print(f"Sauvegarde réussie de {len(evenements)} événements")
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False

def trouver_evenement_par_id(evenements, event_id):
    """Trouve un événement par son ID."""
    for evenement in evenements:
        if evenement.get('id') == event_id:
            return evenement
    return None

def supprimer_evenement_par_id(evenements, event_id):
    """Supprime un événement par son ID."""
    for i, evenement in enumerate(evenements):
        if evenement.get('id') == event_id:
            return evenements.pop(i)
    return None

def valider_telephone(telephone):
    """Valide le format d'un numéro de téléphone international."""
    pattern = r'^\+\d{1,4}\s*\d{2}\s*\d{2}\s*\d{2}\s*\d{2}$'
    return re.match(pattern, telephone) is not None

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(TRANSLATIONS["fr"]["app_title"])
        self.geometry("1080x720")
        self.configure(bg="#c3d7da")
        self.iconbitmap("feastApp.ico")

        # Variables
        self.lang = "fr"
        self.open_windows = []  # Liste pour garder une trace des fenêtres ouvertes

        # En-tête
        header_frame = tk.Frame(self, bg=COLORS["primary"], height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        # Boutons de langue
        btn_fr = tk.Button(header_frame, text="FR", font=("Arial", 10, "bold"), 
                          bg=COLORS["white"], fg=COLORS["primary"], command=lambda: self.set_lang("fr"))
        btn_fr.pack(side=tk.RIGHT, padx=10)
        btn_en = tk.Button(header_frame, text="EN", font=("Arial", 10, "bold"), 
                          bg=COLORS["white"], fg=COLORS["primary"], command=lambda: self.set_lang("en"))
        btn_en.pack(side=tk.RIGHT)

        # Logo
        try:
            logo_path = "logo.jpg"
            logo_image_pil = Image.open(logo_path)
            logo_image_pil = logo_image_pil.resize((60, 60), Image.Resampling.LANCZOS)
            self.logo_image_tk = ImageTk.PhotoImage(logo_image_pil)
            logo_label = tk.Label(header_frame, image=self.logo_image_tk, bg=COLORS["primary"])
            logo_label.pack(side=tk.LEFT, padx=20)
        except Exception as e:
            print(f"Erreur lors du chargement du logo: {e}")
            logo_placeholder = tk.Label(header_frame, text=self.get_text("logo_error"), 
                                      font=("Arial", 10), fg=COLORS["white"], bg=COLORS["primary"])
            logo_placeholder.pack(side=tk.LEFT, padx=20)

        # Titre
        self.title_label = tk.Label(header_frame, text="feastAppFaso", 
                                  font=("Georgia", 20, "bold"), fg=COLORS["white"], bg=COLORS["primary"])
        self.title_label.pack(side=tk.LEFT, padx=20)

        # Conteneur principal
        container = tk.Frame(self)
        container.pack(side="bottom", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Créer les frames
        for F in (AccueilFrame, ReservePlaceFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Créer CreateEventFrame séparément
        create_event_frame = CreateEventFrame(container, self, self.lang)
        self.frames["CreateEventFrame"] = create_event_frame
        create_event_frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("AccueilFrame")

    def set_lang(self, lang):
        """Change la langue de l'application."""
        print(f"Changing language to: {lang}")  # Debug log
        self.lang = lang
        self.title(TRANSLATIONS[lang]["app_title"])
        
        # Mettre à jour le titre de l'en-tête
        self.title_label.config(text=TRANSLATIONS[lang]["app_title"])
        
        # Mettre à jour les frames principales
        for frame_name, frame in self.frames.items():
            print(f"Updating frame: {frame_name}")  # Debug log
            if hasattr(frame, 'update_texts'):
                frame.update_texts()
        
        # Mettre à jour toutes les fenêtres ouvertes
        print(f"Updating {len(self.open_windows)} open windows")  # Debug log
        for window in self.open_windows:
            if hasattr(window, 'update_texts'):
                window.update_texts()
            else:
                # Mettre à jour les widgets dans les fenêtres modales
                self.update_modal_window_texts(window)
        
        # Forcer la mise à jour de l'affichage
        self.update_idletasks()
        self.update()

    def update_modal_window_texts(self, window):
        """Met à jour les textes dans une fenêtre modale."""
        print(f"Updating modal window: {window.title()}")  # Debug log
        
        # Mettre à jour le titre de la fenêtre
        if hasattr(window, 'title_key'):
            new_title = self.get_text(window.title_key)
            window.title(new_title)
            print(f"Updated window title to: {new_title}")  # Debug log

        # Mettre à jour tous les widgets dans la fenêtre
        for widget in window.winfo_children():
            if isinstance(widget, tk.Label):
                if hasattr(widget, 'text_key'):
                    new_text = self.get_text(widget.text_key)
                    widget.configure(text=new_text)
                    print(f"Updated label text to: {new_text}")  # Debug log
            elif isinstance(widget, tk.Button):
                if hasattr(widget, 'text_key'):
                    new_text = self.get_text(widget.text_key)
                    widget.configure(text=new_text)
                    print(f"Updated button text to: {new_text}")  # Debug log
            elif isinstance(widget, tk.Entry):
                if hasattr(widget, 'placeholder_key'):
                    current_text = widget.get()
                    placeholder_fr = self.get_text(widget.placeholder_key, lang="fr")
                    placeholder_en = self.get_text(widget.placeholder_key, lang="en")
                    if current_text == placeholder_fr or current_text == placeholder_en:
                        new_placeholder = self.get_text(widget.placeholder_key)
                        widget.delete(0, tk.END)
                        widget.insert(0, new_placeholder)
                        print(f"Updated entry placeholder to: {new_placeholder}")  # Debug log
            elif isinstance(widget, tk.Frame):
                # Récursivement mettre à jour les widgets dans les frames
                self.update_widgets_in_frame(widget)

    def update_widgets_in_frame(self, frame):
        """Met à jour récursivement tous les widgets dans une frame."""
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label):
                if hasattr(widget, 'text_key'):
                    new_text = self.get_text(widget.text_key)
                    widget.configure(text=new_text)
                    print(f"Updated frame label text to: {new_text}")  # Debug log
            elif isinstance(widget, tk.Button):
                if hasattr(widget, 'text_key'):
                    new_text = self.get_text(widget.text_key)
                    widget.configure(text=new_text)
                    print(f"Updated frame button text to: {new_text}")  # Debug log
            elif isinstance(widget, tk.Entry):
                if hasattr(widget, 'placeholder_key'):
                    current_text = widget.get()
                    placeholder_fr = self.get_text(widget.placeholder_key, lang="fr")
                    placeholder_en = self.get_text(widget.placeholder_key, lang="en")
                    if current_text == placeholder_fr or current_text == placeholder_en:
                        new_placeholder = self.get_text(widget.placeholder_key)
                        widget.delete(0, tk.END)
                        widget.insert(0, new_placeholder)
                        print(f"Updated frame entry placeholder to: {new_placeholder}")  # Debug log
            elif isinstance(widget, tk.Frame):
                # Récursivement mettre à jour les widgets dans les sous-frames
                self.update_widgets_in_frame(widget)
            elif isinstance(widget, tk.Listbox):
                # Mettre à jour les éléments de la liste si nécessaire
                pass  # Les listbox contiennent généralement des données, pas des textes à traduire

    def get_text(self, key, lang=None):
        """Récupère le texte traduit."""
        if lang is None:
            lang = self.lang
        text = TRANSLATIONS[lang].get(key, key)
        print(f"Getting text for key '{key}' in language '{lang}': '{text}'")  # Debug log
        return text

    def show_frame(self, page_name):
        """Affiche la frame spécifiée."""
        frame = self.frames[page_name]
        frame.tkraise()

    def load_event_image(self, image_path, size=(160, 120)):
        """Charge et redimensionne une image."""
        try:
            img = Image.open(image_path)
            img_resized = img.resize(size, Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_resized)
            return img_tk
        except Exception as e:
            print(f"Erreur lors du chargement de l'image {image_path}: {e}")
            return None

    def save_event(self, event):
        """Sauvegarde un événement avec validation (méthode legacy - utiliser save_events)"""
        # Charger les événements existants
        events = self.load_events()
        
        # Valider l'événement avant la sauvegarde
        erreurs = valider_evenement(event)
        if erreurs:
            messagebox.showerror(
                self.get_text("error"),
                "Erreurs de validation:\n" + "\n".join(erreurs),
                parent=self
            )
            return False
        
        # Générer un ID unique si l'événement n'en a pas
        if 'id' not in event:
            event['id'] = generer_id_unique()
        
        # Vérifier si l'événement existe déjà (par ID)
        existing_event = None
        for i, existing in enumerate(events):
            if existing.get('id') == event['id']:
                existing_event = existing
                events[i] = event  # Mettre à jour l'événement existant
                break
        
        if not existing_event:
            # Ajouter le nouvel événement
            events.append(event)
        
        # Sauvegarder dans le fichier JSON
        if self.save_events(events):
            print(f"Événement sauvegardé avec succès. ID: {event['id']}")
            return True
        else:
            messagebox.showerror(
                self.get_text("error"),
                "Erreur lors de la sauvegarde de l'événement",
                parent=self
            )
            return False

    def delete_event_by_id(self, event_id):
        """Supprime un événement par son ID (méthode legacy)"""
        events = self.load_events()
        event = None
        
        for i, existing in enumerate(events):
            if existing.get('id') == event_id:
                event = events.pop(i)
                break
        
        if event:
            if self.save_events(events):
                print(f"Événement supprimé avec succès. ID: {event_id}")
                return True
            else:
                messagebox.showerror(
                    self.get_text("error"),
                    "Erreur lors de la suppression de l'événement",
                    parent=self
                )
                return False
        return False

    def get_event_by_id(self, event_id):
        """Récupère un événement par son ID."""
        return trouver_evenement_par_id(self.evenements, event_id)

    def register_window(self, window):
        """Enregistre une fenêtre pour la mise à jour des traductions."""
        self.open_windows.append(window)
        window.protocol("WM_DELETE_WINDOW", lambda: self.unregister_window(window))

    def unregister_window(self, window):
        """Désenregistre une fenêtre."""
        if window in self.open_windows:
            self.open_windows.remove(window)
        window.destroy()

    def load_events(self):
        """Charge les événements depuis le fichier JSON"""
        try:
            with open('evenements.json', 'r', encoding='utf-8') as f:
                events = json.load(f)
                return events
        except FileNotFoundError:
            print("Fichier evenements.json non trouvé, création d'un nouveau fichier")
            return []
        except json.JSONDecodeError as e:
            print(f"Erreur de décodage JSON: {e}")
            return []
        except Exception as e:
            print(f"Erreur lors du chargement des événements: {e}")
            return []

    def save_events(self, events):
        """Sauvegarde les événements dans le fichier JSON"""
        try:
            # Créer une sauvegarde
            if os.path.exists('evenements.json'):
                shutil.copy2('evenements.json', 'evenements.json.backup')
            
            with open('evenements.json', 'w', encoding='utf-8') as f:
                json.dump(events, f, ensure_ascii=False, indent=2)
            print("Événements sauvegardés avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False

    def delete_event(self, event):
        """Supprime un événement"""
        try:
            events = self.load_events()
            # Trouver et supprimer l'événement par son ID
            events = [e for e in events if e.get('id') != event.get('id')]
            self.save_events(events)
            
            # Afficher un message de confirmation
            messagebox.showinfo(self.get_text("event_deleted"), self.get_text("event_deleted"))
            
            # Mettre à jour l'affichage
            if hasattr(self, 'current_frame') and hasattr(self.current_frame, 'update_events_list'):
                self.current_frame.update_events_list()
                
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")

    def reserve_event(self, event):
        """Réserve une place pour un événement avec les informations de l'utilisateur"""
        try:
            # Vérifier si l'événement n'est pas complet
            current_registrations = len(event.get('inscrits', []))
            capacity = event.get('capacity', 0)
            
            if current_registrations >= capacity:
                messagebox.showwarning(self.get_text("event_full"), self.get_text("event_full"))
                return
            
            # Créer une fenêtre pour saisir les informations de réservation
            reservation_window = tk.Toplevel()
            reservation_window.title("Réservation d'événement")
            reservation_window.geometry("400x350")
            reservation_window.configure(bg=COLORS["light"])
            
            # Titre
            title_label = tk.Label(reservation_window, text=f"Réservation - {event.get('title', '')}", 
                                 font=("Arial", 14, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
            title_label.pack(pady=20)
            
            # Informations de l'événement
            event_info = tk.Frame(reservation_window, bg=COLORS["light"])
            event_info.pack(pady=10)
            
            event_text = f"📅 {event.get('date', '')} à {event.get('time', '')}\n📍 {event.get('location', '')}\n💰 {event.get('price', '0')}€"
            event_label = tk.Label(event_info, text=event_text, 
                                 font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_secondary"])
            event_label.pack()
            
            # Formulaire de réservation
            form_frame = tk.Frame(reservation_window, bg=COLORS["light"])
            form_frame.pack(pady=20)
            
            # Nom
            name_label = tk.Label(form_frame, text="Nom complet:", bg=COLORS["light"], fg=COLORS["text_primary"])
            name_label.pack(anchor=tk.W)
            name_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
            name_entry.pack(pady=5)
            
            # Email
            email_label = tk.Label(form_frame, text="Email:", bg=COLORS["light"], fg=COLORS["text_primary"])
            email_label.pack(anchor=tk.W)
            email_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
            email_entry.pack(pady=5)
            
            # Téléphone
            phone_label = tk.Label(form_frame, text="Téléphone:", bg=COLORS["light"], fg=COLORS["text_primary"])
            phone_label.pack(anchor=tk.W)
            phone_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
            phone_entry.pack(pady=5)
            
            def confirm_reservation():
                # Valider les champs
                name = name_entry.get().strip()
                email = email_entry.get().strip()
                phone = phone_entry.get().strip()
                
                if not name or not email or not phone:
                    messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs")
                    return
                
                # Valider le format de l'email
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    messagebox.showwarning("Email invalide", "Veuillez entrer un email valide")
                    return
                
                # Vérifier si l'utilisateur est déjà inscrit
                events = self.load_events()
                for e in events:
                    if e.get('id') == event.get('id'):
                        inscrits = e.get('inscrits', [])
                        for inscrit in inscrits:
                            if isinstance(inscrit, dict) and inscrit.get('email') == email:
                                messagebox.showwarning("Déjà inscrit", "Vous êtes déjà inscrit à cet événement")
                                reservation_window.destroy()
                                return
                        break
                
                # Créer la réservation
                from datetime import datetime
                reservation_data = {
                    'nom': name,
                    'email': email,
                    'telephone': phone,
                    'date_reservation': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'status': 'Confirmée'
                }
                
                # Ajouter la réservation à l'événement
                for e in events:
                    if e.get('id') == event.get('id'):
                        if 'inscrits' not in e:
                            e['inscrits'] = []
                        e['inscrits'].append(reservation_data)
                        break
                
                # Sauvegarder les modifications
                self.save_events(events)
                
                messagebox.showinfo("Réservation réussie", 
                                  f"Votre réservation pour '{event.get('title', '')}' a été confirmée !\n\n"
                                  f"Un email de confirmation sera envoyé à {email}")
                
                reservation_window.destroy()
                
                # Mettre à jour l'affichage si nécessaire
                if hasattr(self, 'current_frame') and hasattr(self.current_frame, 'update_events_list'):
                    self.current_frame.update_events_list()
            
            # Boutons
            buttons_frame = tk.Frame(reservation_window, bg=COLORS["light"])
            buttons_frame.pack(pady=20)
            
            confirm_btn = tk.Button(buttons_frame, text="Confirmer la réservation", command=confirm_reservation,
                                  font=("Arial", 12, "bold"), bg=COLORS["success"], fg=COLORS["white"], 
                                  relief=tk.FLAT, padx=15, pady=8)
            confirm_btn.pack(side=tk.LEFT, padx=5)
            
            cancel_btn = tk.Button(buttons_frame, text="Annuler", command=reservation_window.destroy,
                                 font=("Arial", 12, "bold"), bg=COLORS["danger"], fg=COLORS["white"], 
                                 relief=tk.FLAT, padx=15, pady=8)
            cancel_btn.pack(side=tk.LEFT, padx=5)
            
            # Permettre la confirmation avec Entrée
            name_entry.bind('<Return>', lambda e: email_entry.focus())
            email_entry.bind('<Return>', lambda e: phone_entry.focus())
            phone_entry.bind('<Return>', lambda e: confirm_reservation())
            
            # Focus sur le premier champ
            name_entry.focus()
            
        except Exception as e:
            print(f"Erreur lors de la réservation: {e}")
            messagebox.showerror("Erreur", self.get_text("reservation_error"))

class AccueilFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["light"])

        main_layout_frame = tk.Frame(self, bg=COLORS["light"])
        main_layout_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        menu_frame = tk.Frame(main_layout_frame, bg=COLORS["lighter"], width=220)
        menu_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        menu_frame.pack_propagate(False)

        content_frame = tk.Frame(main_layout_frame, bg=COLORS["white"])
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.menu_label = tk.Label(menu_frame, text=self.controller.get_text("menu"), 
                                 font=("Arial", 14, "bold"), bg=COLORS["lighter"], fg=COLORS["dark"])
        self.menu_label.pack(pady=(20, 10))

        self.btn_create = tk.Button(menu_frame, text=self.controller.get_text("create_event"), 
                                  command=lambda: controller.show_frame("CreateEventFrame"), 
                                  font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"], width=20, height=1, relief=tk.FLAT)
        self.btn_create.pack(pady=8)

        self.btn_reserve = tk.Button(menu_frame, text=self.controller.get_text("reserve_place"), 
                                   command=lambda: controller.show_frame("ReservePlaceFrame"), 
                                   font=("Arial", 12, "bold"), bg=COLORS["accent"], fg=COLORS["white"], width=20, height=1, relief=tk.FLAT)
        self.btn_reserve.pack(pady=8)

        self.btn_news = tk.Button(menu_frame, text=self.controller.get_text("events_news"), 
                                command=self.show_events_news, 
                                font=("Arial", 12, "bold"), bg=COLORS["secondary"], fg=COLORS["white"], width=20, height=1, relief=tk.FLAT)
        self.btn_news.pack(pady=8)

        self.btn_promote = tk.Button(menu_frame, text=self.controller.get_text("promote_event"), 
                                   command=self.promote_event, 
                                   font=("Arial", 12, "bold"), bg=COLORS["success"], fg=COLORS["white"], width=20, height=1, relief=tk.FLAT)
        self.btn_promote.pack(pady=8)

        self.welcome_label = tk.Label(content_frame, text=self.controller.get_text("welcome"), 
                                    font=("Arial", 24, "bold"), bg=COLORS["white"], fg=COLORS["text_primary"])
        self.welcome_label.pack(pady=50)

        images_frame = tk.Frame(content_frame, bg=COLORS["white"])
        images_frame.pack(pady=20)

        image1_path = "faso-foot.jpg"
        try:
            loaded_image1 = self.controller.load_event_image(image1_path, size=(420, 500))
            if loaded_image1:
                label_image1 = tk.Label(images_frame, image=loaded_image1, bg=COLORS["white"])
                label_image1.image = loaded_image1
                label_image1.pack(side=tk.LEFT, padx=10)
            else:
                label_image1 = tk.Label(images_frame, text=self.controller.get_text("image_not_found"), font=("Arial", 10), fg=COLORS["danger"], bg=COLORS["white"])
                label_image1.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image 1: {e}")
            label_image1 = tk.Label(images_frame, text=self.controller.get_text("image_error"), font=("Arial", 10), fg=COLORS["danger"], bg=COLORS["white"])
            label_image1.pack(side=tk.LEFT, padx=10)

        image2_path = "festibro.jpg"
        try:
            loaded_image2 = self.controller.load_event_image(image2_path, size=(500, 500))
            if loaded_image2:
                label_image2 = tk.Label(images_frame, image=loaded_image2, bg=COLORS["white"])
                label_image2.image = loaded_image2
                label_image2.pack(side=tk.LEFT, padx=10)
            else:
                label_image2 = tk.Label(images_frame, text=self.controller.get_text("image_not_found"), font=("Arial", 10), fg=COLORS["danger"], bg=COLORS["white"])
                label_image2.pack(side=tk.LEFT, padx=10)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image 2: {e}")
            label_image2 = tk.Label(images_frame, text=self.controller.get_text("image_error"), font=("Arial", 10), fg="#dc3545", bg="#ffffff")
            label_image2.pack(side=tk.LEFT, padx=10)

    def update_texts(self):
        """Met à jour les textes selon la langue sélectionnée."""
        self.menu_label.config(text=self.controller.get_text("menu"))
        self.btn_create.config(text=self.controller.get_text("create_event"))
        self.btn_reserve.config(text=self.controller.get_text("reserve_place"))
        self.btn_news.config(text=self.controller.get_text("events_news"))
        self.btn_promote.config(text=self.controller.get_text("promote_event"))
        self.welcome_label.config(text=self.controller.get_text("welcome"))

    def show_events_news(self):
        """Affiche la liste des événements créés avec possibilité de suppression."""
        # Créer une nouvelle fenêtre
        news_window = tk.Toplevel(self)
        news_window.title_key = "events_news"
        news_window.title(self.controller.get_text("events_news"))
        news_window.geometry("800x600")
        news_window.configure(bg=COLORS["light"])
        news_window.transient(self)
        news_window.grab_set()
        
        # Enregistrer la fenêtre pour les mises à jour de traduction
        self.controller.register_window(news_window)

        # Titre
        title_label = tk.Label(news_window, text=self.controller.get_text("events_news"), 
                             font=("Arial", 16, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
        title_label.pack(pady=20)

        # Créer un cadre pour la liste des événements
        events_frame = tk.Frame(news_window, bg=COLORS["light"])
        events_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Créer un Canvas avec Scrollbar
        canvas = tk.Canvas(events_frame, bg=COLORS["white"])
        scrollbar = tk.Scrollbar(events_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS["white"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Charger les événements depuis le fichier JSON
        events = self.controller.load_events()

        if not events:
            # Message si aucun événement
            no_events_label = tk.Label(scrollable_frame, 
                                     text="Aucun événement créé pour le moment", 
                                     font=("Arial", 14), bg=COLORS["white"], fg=COLORS["text_secondary"])
            no_events_label.pack(pady=50)
        else:
            # Afficher les événements avec le nouveau design
            for event in events:
                # Carte d'événement avec design moderne
                event_frame = tk.Frame(scrollable_frame, bg=COLORS["white"], relief=tk.RAISED, bd=2)
                event_frame.pack(fill=tk.X, padx=10, pady=5)

                # En-tête de la carte
                header_frame = tk.Frame(event_frame, bg=COLORS["primary"], height=40)
                header_frame.pack(fill=tk.X)
                header_frame.pack_propagate(False)

                # Titre de l'événement
                title = event.get('title', event.get('nom', 'Sans titre'))
                title_label = tk.Label(header_frame, text=title, 
                                     font=("Arial", 14, "bold"), bg=COLORS["primary"], fg=COLORS["white"])
                title_label.pack(side=tk.LEFT, padx=10, pady=5)

                # Badge de type d'événement
                event_type = event.get('type', 'Autre')
                type_bg = COLORS["accent"] if event_type == "Sport" else COLORS["secondary"]
                type_label = tk.Label(header_frame, text=event_type, font=("Arial", 10, "bold"), 
                                     bg=type_bg, fg=COLORS["white"], padx=8, pady=2)
                type_label.pack(side=tk.RIGHT, padx=10, pady=5)

                # Contenu de la carte
                content_frame = tk.Frame(event_frame, bg=COLORS["light"])
                content_frame.pack(fill=tk.X, padx=10, pady=10)

                # Informations de l'événement
                info_frame = tk.Frame(content_frame, bg=COLORS["light"])
                info_frame.pack(fill=tk.X, pady=5)

                # Date et heure
                date_time = f"{event.get('date', 'Date non spécifiée')} à {event.get('time', 'Heure non spécifiée')}"
                date_label = tk.Label(info_frame, text=f"📅 {date_time}", 
                                     font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
                date_label.pack(anchor=tk.W)

                # Lieu
                location = event.get('location', event.get('lieu', 'Lieu non spécifié'))
                location_label = tk.Label(info_frame, text=f"📍 {location}", 
                                         font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
                location_label.pack(anchor=tk.W)

                # Prix et capacité
                price = event.get('price', event.get('prix', 0))
                capacity = event.get('capacity', event.get('capacite', 0))
                nb_inscrits = len(event.get('inscrits', []))
                price_capacity_text = f"💰 Prix: {price}€ | 👥 Capacité: {nb_inscrits}/{capacity}"
                price_capacity_label = tk.Label(info_frame, text=price_capacity_text, 
                                              font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
                price_capacity_label.pack(anchor=tk.W)

                # Description
                description = event.get('description', 'Aucune description')
                desc_label = tk.Label(info_frame, text=f"📝 {description[:100]}{'...' if len(description) > 100 else ''}", 
                                     font=("Arial", 10), bg=COLORS["light"], fg=COLORS["text_secondary"], wraplength=400)
                desc_label.pack(anchor=tk.W, pady=(5, 0))

                # Boutons d'action
                buttons_frame = tk.Frame(content_frame, bg=COLORS["light"])
                buttons_frame.pack(fill=tk.X, pady=10)

                # Bouton Voir détails
                details_btn = tk.Button(buttons_frame, text="Voir détails", 
                                      command=lambda e=event: self.show_event_details(e),
                                      font=("Arial", 11, "bold"), bg=COLORS["accent"], fg=COLORS["white"], 
                                      relief=tk.FLAT, padx=15, pady=5)
                details_btn.pack(side=tk.LEFT, padx=(0, 10))

                # Bouton Supprimer (seulement dans les actualités)
                delete_btn = tk.Button(buttons_frame, text=self.controller.get_text("delete"), 
                                     command=lambda e=event, w=news_window: self.delete_event_from_news(e, w),
                                     font=("Arial", 11, "bold"), bg=COLORS["danger"], fg=COLORS["white"], 
                                     relief=tk.FLAT, padx=15, pady=5)
                delete_btn.pack(side=tk.LEFT)

        # Ajuster l'empaquetage
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Bouton fermer
        close_btn = tk.Button(news_window, text="Fermer", command=news_window.destroy,
                            font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"], 
                            relief=tk.FLAT, padx=20, pady=10)
        close_btn.pack(pady=20)

    def show_event_details(self, event):
        """Affiche les détails complets d'un événement"""
        try:
            details_window = tk.Toplevel(self)
            details_window.title("Détails de l'événement")
            details_window.geometry("600x500")
            details_window.configure(bg=COLORS["light"])
            
            # Titre
            title = event.get('title', event.get('nom', 'Sans titre'))
            title_label = tk.Label(details_window, text=title, 
                                 font=("Arial", 16, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
            title_label.pack(pady=20)
            
            # Contenu
            content_frame = tk.Frame(details_window, bg=COLORS["white"], relief=tk.RAISED, bd=2)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Informations détaillées
            details_text = f"""
Type: {event.get('type', 'Non spécifié')}
Date: {event.get('date', 'Non spécifiée')}
Heure: {event.get('time', 'Non spécifiée')}
Lieu: {event.get('location', event.get('lieu', 'Non spécifié'))}
Prix: {event.get('price', event.get('prix', 0))}€
Capacité: {event.get('capacity', event.get('capacite', 0))} personnes
Inscrits: {len(event.get('inscrits', []))}
Description: {event.get('description', 'Aucune description')}

Membres du staff ({len(event.get('staff', []))}):
"""
            
            # Ajouter les membres du staff
            for i, member in enumerate(event.get('staff', []), 1):
                details_text += f"{i}. {member.get('nom', '')} - {member.get('rôle', '')} ({member.get('contact', '')})\n"
            
            details_label = tk.Label(content_frame, text=details_text, 
                                   font=("Arial", 11), bg=COLORS["white"], fg=COLORS["text_primary"], 
                                   justify=tk.LEFT, wraplength=550)
            details_label.pack(padx=20, pady=20)
            
            # Bouton fermer
            close_btn = tk.Button(details_window, text="Fermer", command=details_window.destroy,
                                font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"], 
                                relief=tk.FLAT, padx=20, pady=10)
            close_btn.pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des détails: {e}")

    def delete_event_from_news(self, event, window):
        """Supprime un événement depuis la fenêtre des actualités."""
        # Demander confirmation
        title = event.get('title', event.get('nom', 'Cet événement'))
        confirmation = messagebox.askyesno(
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer l'événement '{title}' ?\n\nCette action est irréversible.",
            parent=window
        )
        
        if confirmation:
            try:
                # Charger les événements
                events = self.controller.load_events()
                
                # Trouver et supprimer l'événement par son ID
                events = [e for e in events if e.get('id') != event.get('id')]
                
                # Sauvegarder les modifications
                if self.controller.save_events(events):
                    messagebox.showinfo(
                        "Succès",
                        f"L'événement '{title}' a été supprimé avec succès",
                        parent=window
                    )
                    # Fermer et rouvrir la fenêtre pour mettre à jour la liste
                    window.destroy()
                    self.show_events_news()
                else:
                    messagebox.showerror(
                        "Erreur",
                        "Erreur lors de la suppression de l'événement",
                        parent=window
                    )
            except Exception as e:
                messagebox.showerror(
                    "Erreur",
                    f"Erreur lors de la suppression: {e}",
                    parent=window
                )

    def promote_event(self):
        """Demande les informations du promoteur et affiche un message de confirmation."""
        # Demander le nom du promoteur
        promoter_name = simpledialog.askstring(
            self.controller.get_text("promote_event"),
            self.controller.get_text("enter_name"),
            parent=self
        )
        if not promoter_name:
            return

        # Demander le numéro de téléphone
        promoter_phone = simpledialog.askstring(
            self.controller.get_text("promote_event"),
            self.controller.get_text("enter_phone"),
            parent=self
        )
        if not promoter_phone:
            return

        # Vérifier le format du téléphone
        if not valider_telephone(promoter_phone):
            messagebox.showwarning(
                self.controller.get_text("error"),
                self.controller.get_text("invalid_phone"),
                parent=self
            )
            return

        # Afficher un message de confirmation
        messagebox.showinfo(
            self.controller.get_text("success"),
            self.controller.get_text("promotion_success").format(promoter_name, promoter_phone),
            parent=self
        )

class ReservePlaceFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=COLORS["white"])

        # Bouton de retour (flèche)
        btn_back = tk.Button(self, text=self.controller.get_text("back"), command=lambda: controller.show_frame("AccueilFrame"),
                           font=("Arial", 14), bg=COLORS["white"], bd=0, relief=tk.FLAT, fg=COLORS["primary"])
        btn_back.place(x=10, y=10)
        btn_back.text_key = "back"

        # Titre
        label = tk.Label(self, text=self.controller.get_text("book_place"), font=("Arial", 18, "bold"), bg=COLORS["white"], fg=COLORS["text_primary"])
        label.pack(pady=20)
        label.text_key = "book_place"

        # Barre de recherche
        search_frame = tk.Frame(self, bg=COLORS["white"])
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_events)

        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=40, font=("Arial", 10))
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.insert(0, self.controller.get_text("search_placeholder"))
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) if search_entry.get() == self.controller.get_text("search_placeholder") else None)
        search_entry.bind("<FocusOut>", lambda e: search_entry.insert(0, self.controller.get_text("search_placeholder")) if not search_entry.get() else None)
        search_entry.placeholder_key = "search_placeholder"

        # Boutons d'action
        action_frame = tk.Frame(self, bg=COLORS["white"])
        action_frame.pack(fill=tk.X, padx=20, pady=5)

        btn_export = tk.Button(action_frame, text=self.controller.get_text("export_list"), command=self.export_list,
                             font=("Arial", 10, "bold"), bg=COLORS["accent"], fg=COLORS["white"], relief=tk.FLAT)
        btn_export.pack(side=tk.LEFT, padx=5)
        btn_export.text_key = "export_list"

        btn_pay = tk.Button(action_frame, text=self.controller.get_text("pay_online"), command=self.pay_online,
                          font=("Arial", 10, "bold"), bg=COLORS["success"], fg=COLORS["white"], relief=tk.FLAT)
        btn_pay.pack(side=tk.LEFT, padx=5)
        btn_pay.text_key = "pay_online"

        btn_my_reservations = tk.Button(action_frame, text=self.controller.get_text("my_reservations"), command=self.show_my_reservations,
                                      font=("Arial", 10, "bold"), bg=COLORS["secondary"], fg=COLORS["white"], relief=tk.FLAT)
        btn_my_reservations.pack(side=tk.LEFT, padx=5)
        btn_my_reservations.text_key = "my_reservations"

        # Stocker les références pour la mise à jour
        self.btn_back = btn_back
        self.title_label = label
        self.search_entry = search_entry
        self.btn_export = btn_export
        self.btn_pay = btn_pay
        self.btn_my_reservations = btn_my_reservations

        # Liste des événements
        self.events_frame = tk.Frame(self, bg=COLORS["white"])
        self.events_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Créer un Canvas avec Scrollbar
        self.canvas = tk.Canvas(self.events_frame, bg=COLORS["white"])
        scrollbar = tk.Scrollbar(self.events_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["white"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Ajuster l'empaquetage
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Mettre à jour la liste des événements
        self.update_events_list()

    def update_texts(self):
        """Met à jour les textes selon la langue sélectionnée."""
        print("Updating ReservePlaceFrame texts")  # Debug log
        
        # Mettre à jour le bouton de retour
        if hasattr(self, 'btn_back'):
            self.btn_back.config(text=self.controller.get_text("back"))
        
        # Mettre à jour le titre
        if hasattr(self, 'title_label'):
            self.title_label.config(text=self.controller.get_text("book_place"))
        
        # Mettre à jour la barre de recherche
        if hasattr(self, 'search_entry'):
            current_text = self.search_entry.get()
            placeholder_fr = self.controller.get_text("search_placeholder", lang="fr")
            placeholder_en = self.controller.get_text("search_placeholder", lang="en")
            if current_text == placeholder_fr or current_text == placeholder_en:
                new_placeholder = self.controller.get_text("search_placeholder")
                self.search_entry.delete(0, tk.END)
                self.search_entry.insert(0, new_placeholder)
        
        # Mettre à jour les boutons d'action
        if hasattr(self, 'btn_export'):
            self.btn_export.config(text=self.controller.get_text("export_list"))
        if hasattr(self, 'btn_pay'):
            self.btn_pay.config(text=self.controller.get_text("pay_online"))
        if hasattr(self, 'btn_my_reservations'):
            self.btn_my_reservations.config(text=self.controller.get_text("my_reservations"))

        # Mettre à jour la liste des événements
        self.update_events_list()

    def update_events_list(self):
        """Met à jour la liste des événements avec le nouveau design"""
        # Supprimer les anciens widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Charger les événements
        events = self.controller.load_events()
        
        if not events:
            # Message si aucun événement
            no_events_label = tk.Label(self.scrollable_frame, 
                                     text=self.controller.get_text("no_events"), 
                                     font=("Arial", 14), bg=COLORS["white"], fg=COLORS["text_secondary"])
            no_events_label.pack(pady=50)
            return

        # Créer les cartes d'événements
        for event in events:
            self.create_event_card(event, self.scrollable_frame)

    def filter_events(self, *args):
        """Filtre les événements selon la recherche"""
        search_term = self.search_var.get().lower()
        
        # Supprimer les anciens widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Charger et filtrer les événements
        events = self.controller.load_events()
        filtered_events = []
        
        for event in events:
            if (search_term in event.get('title', '').lower() or 
                search_term in event.get('description', '').lower() or
                search_term in event.get('location', '').lower() or
                search_term in event.get('type', '').lower()):
                filtered_events.append(event)

        if not filtered_events:
            # Message si aucun résultat
            no_results_label = tk.Label(self.scrollable_frame, 
                                      text=self.controller.get_text("no_results"), 
                                      font=("Arial", 14), bg=COLORS["white"], fg=COLORS["text_secondary"])
            no_results_label.pack(pady=50)
            return

        # Créer les cartes d'événements filtrés
        for event in filtered_events:
            self.create_event_card(event, self.scrollable_frame)

    def create_event_card(self, event, parent):
        """Crée une carte d'événement avec un design moderne et attrayant"""
        # Carte principale avec bordure et ombre
        card_frame = tk.Frame(parent, bg=COLORS["white"], relief=tk.RAISED, bd=2)
        card_frame.pack(fill=tk.X, padx=10, pady=5)

        # En-tête de la carte avec dégradé
        header_frame = tk.Frame(card_frame, bg=COLORS["primary"], height=40)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Titre de l'événement
        title_label = tk.Label(header_frame, text=event.get('title', 'Sans titre'), 
                              font=("Arial", 14, "bold"), bg=COLORS["primary"], fg=COLORS["white"])
        title_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Badge de type d'événement
        event_type = event.get('type', 'Autre')
        type_bg = COLORS["accent"] if event_type == "Sport" else COLORS["secondary"]
        type_label = tk.Label(header_frame, text=event_type, font=("Arial", 10, "bold"), 
                             bg=type_bg, fg=COLORS["white"], padx=8, pady=2)
        type_label.pack(side=tk.RIGHT, padx=10, pady=5)

        # Contenu de la carte
        content_frame = tk.Frame(card_frame, bg=COLORS["light"])
        content_frame.pack(fill=tk.X, padx=10, pady=10)

        # Informations de l'événement
        info_frame = tk.Frame(content_frame, bg=COLORS["light"])
        info_frame.pack(fill=tk.X, pady=5)

        # Date et heure
        date_time = f"{event.get('date', 'Date non spécifiée')} à {event.get('time', 'Heure non spécifiée')}"
        date_label = tk.Label(info_frame, text=f"📅 {date_time}", 
                             font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
        date_label.pack(anchor=tk.W)

        # Lieu
        location = event.get('location', 'Lieu non spécifié')
        location_label = tk.Label(info_frame, text=f"📍 {location}", 
                                 font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
        location_label.pack(anchor=tk.W)

        # Description
        description = event.get('description', 'Aucune description')
        desc_label = tk.Label(info_frame, text=f"📝 {description[:100]}{'...' if len(description) > 100 else ''}", 
                             font=("Arial", 10), bg=COLORS["light"], fg=COLORS["text_secondary"], wraplength=400)
        desc_label.pack(anchor=tk.W, pady=(5, 0))

        # Boutons d'action
        buttons_frame = tk.Frame(content_frame, bg=COLORS["light"])
        buttons_frame.pack(fill=tk.X, pady=10)

        # Bouton Réserver (seulement dans la page de réservation)
        btn_reserve = tk.Button(buttons_frame, text=self.controller.get_text("reserve"), 
                               command=lambda: self.reserve_place(event),
                               font=("Arial", 11, "bold"), bg=COLORS["success"], fg=COLORS["white"], 
                               relief=tk.FLAT, padx=15, pady=5)
        btn_reserve.pack(side=tk.LEFT)

        return card_frame

    def reserve_place(self, event):
        """Réserve une place pour un événement"""
        self.controller.reserve_event(event)

    def delete_event(self, event):
        """Supprime un événement"""
        # Demander confirmation avant suppression
        if messagebox.askyesno(self.controller.get_text("confirm_delete"), self.controller.get_text("confirm_delete")):
            self.controller.delete_event(event)
            self.update_events_list()

    def export_list(self):
        """Exporte la liste des événements en CSV"""
        try:
            events = self.controller.load_events()
            if not events:
                messagebox.showwarning("Export", "Aucun événement à exporter")
                return
            
            # Demander où sauvegarder le fichier
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Sauvegarder la liste des événements"
            )
            
            if filename:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['Titre', 'Type', 'Date', 'Heure', 'Lieu', 'Description', 'Prix', 'Capacité', 'Inscrits']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for event in events:
                        writer.writerow({
                            'Titre': event.get('title', ''),
                            'Type': event.get('type', ''),
                            'Date': event.get('date', ''),
                            'Heure': event.get('time', ''),
                            'Lieu': event.get('location', ''),
                            'Description': event.get('description', ''),
                            'Prix': event.get('price', ''),
                            'Capacité': event.get('capacity', ''),
                            'Inscrits': len(event.get('inscrits', []))
                        })
                
                messagebox.showinfo("Export réussi", f"Liste exportée vers {filename}")
        except Exception as e:
            messagebox.showerror("Erreur d'export", f"Erreur lors de l'export: {e}")

    def pay_online(self):
        """Simule un système de paiement en ligne"""
        try:
            events = self.controller.load_events()
            if not events:
                messagebox.showwarning("Paiement", "Aucun événement disponible pour le paiement")
                return
            
            # Créer une fenêtre de sélection d'événement
            payment_window = tk.Toplevel(self)
            payment_window.title("Paiement en ligne")
            payment_window.geometry("500x400")
            payment_window.configure(bg=COLORS["light"])
            
            # Titre
            title_label = tk.Label(payment_window, text="Sélectionner un événement pour le paiement", 
                                 font=("Arial", 14, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
            title_label.pack(pady=20)
            
            # Liste des événements
            events_frame = tk.Frame(payment_window, bg=COLORS["light"])
            events_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Scrollbar pour la liste
            canvas = tk.Canvas(events_frame, bg=COLORS["white"])
            scrollbar = tk.Scrollbar(events_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=COLORS["white"])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            
            # Afficher les événements avec prix
            for event in events:
                if event.get('price'):
                    event_frame = tk.Frame(scrollable_frame, bg=COLORS["white"], relief=tk.RAISED, bd=1)
                    event_frame.pack(fill=tk.X, padx=5, pady=5)
                    
                    # Informations de l'événement
                    info_text = f"{event.get('title', 'Sans titre')} - {event.get('price', '0')}€"
                    info_label = tk.Label(event_frame, text=info_text, 
                                        font=("Arial", 11), bg=COLORS["white"], fg=COLORS["text_primary"])
                    info_label.pack(side=tk.LEFT, padx=10, pady=5)
                    
                    # Bouton de paiement
                    pay_btn = tk.Button(event_frame, text="Payer", 
                                      command=lambda e=event: self.process_payment(e, payment_window),
                                      font=("Arial", 10, "bold"), bg=COLORS["success"], fg=COLORS["white"], 
                                      relief=tk.FLAT, padx=15, pady=3)
                    pay_btn.pack(side=tk.RIGHT, padx=10, pady=5)
            
            # Bouton fermer
            close_btn = tk.Button(payment_window, text="Fermer", command=payment_window.destroy,
                                font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"], 
                                relief=tk.FLAT, padx=20, pady=10)
            close_btn.pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture du système de paiement: {e}")

    def process_payment(self, event, window):
        """Traite le paiement pour un événement spécifique"""
        try:
            # Simuler le processus de paiement
            payment_window = tk.Toplevel(window)
            payment_window.title("Paiement")
            payment_window.geometry("400x300")
            payment_window.configure(bg=COLORS["light"])
            
            # Titre
            title_label = tk.Label(payment_window, text=f"Paiement - {event.get('title', '')}", 
                                 font=("Arial", 14, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
            title_label.pack(pady=20)
            
            # Montant
            amount_label = tk.Label(payment_window, text=f"Montant: {event.get('price', '0')}€", 
                                  font=("Arial", 12), bg=COLORS["light"], fg=COLORS["text_primary"])
            amount_label.pack(pady=10)
            
            # Informations de paiement
            payment_frame = tk.Frame(payment_window, bg=COLORS["light"])
            payment_frame.pack(pady=20)
            
            # Numéro de carte
            card_label = tk.Label(payment_frame, text="Numéro de carte:", bg=COLORS["light"], fg=COLORS["text_primary"])
            card_label.pack(anchor=tk.W)
            card_entry = tk.Entry(payment_frame, width=30)
            card_entry.pack(pady=5)
            
            # Date d'expiration
            exp_label = tk.Label(payment_frame, text="Date d'expiration (MM/AA):", bg=COLORS["light"], fg=COLORS["text_primary"])
            exp_label.pack(anchor=tk.W)
            exp_entry = tk.Entry(payment_frame, width=10)
            exp_entry.pack(pady=5)
            
            # CVV
            cvv_label = tk.Label(payment_frame, text="CVV:", bg=COLORS["light"], fg=COLORS["text_primary"])
            cvv_label.pack(anchor=tk.W)
            cvv_entry = tk.Entry(payment_frame, width=5)
            cvv_entry.pack(pady=5)
            
            # Boutons
            buttons_frame = tk.Frame(payment_window, bg=COLORS["light"])
            buttons_frame.pack(pady=20)
            
            def confirm_payment():
                # Simuler un paiement réussi
                messagebox.showinfo("Paiement réussi", "Paiement traité avec succès !")
                payment_window.destroy()
                window.destroy()
            
            confirm_btn = tk.Button(buttons_frame, text="Confirmer le paiement", command=confirm_payment,
                                  font=("Arial", 12, "bold"), bg=COLORS["success"], fg=COLORS["white"], 
                                  relief=tk.FLAT, padx=15, pady=8)
            confirm_btn.pack(side=tk.LEFT, padx=5)
            
            cancel_btn = tk.Button(buttons_frame, text="Annuler", command=payment_window.destroy,
                                 font=("Arial", 12, "bold"), bg=COLORS["danger"], fg=COLORS["white"], 
                                 relief=tk.FLAT, padx=15, pady=8)
            cancel_btn.pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du traitement du paiement: {e}")

    def show_my_reservations(self):
        """Affiche les réservations de l'utilisateur basées sur son email"""
        try:
            # Créer une fenêtre pour demander l'email
            email_window = tk.Toplevel(self)
            email_window.title("Mes réservations")
            email_window.geometry("400x200")
            email_window.configure(bg=COLORS["light"])
            
            # Titre
            title_label = tk.Label(email_window, text="Entrez votre email pour voir vos réservations", 
                                 font=("Arial", 14, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
            title_label.pack(pady=20)
            
            # Frame pour l'email
            email_frame = tk.Frame(email_window, bg=COLORS["light"])
            email_frame.pack(pady=20)
            
            # Label et champ email
            email_label = tk.Label(email_frame, text="Email:", bg=COLORS["light"], fg=COLORS["text_primary"])
            email_label.pack(anchor=tk.W)
            email_entry = tk.Entry(email_frame, width=40, font=("Arial", 12))
            email_entry.pack(pady=10)
            email_entry.focus()
            
            def search_reservations():
                email = email_entry.get().strip()
                if not email:
                    messagebox.showwarning("Email requis", "Veuillez entrer votre email")
                    return
                
                # Valider le format de l'email
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, email):
                    messagebox.showwarning("Email invalide", "Veuillez entrer un email valide")
                    return
                
                # Fermer la fenêtre de saisie d'email
                email_window.destroy()
                
                # Afficher les réservations
                self.display_user_reservations(email)
            
            # Boutons
            buttons_frame = tk.Frame(email_window, bg=COLORS["light"])
            buttons_frame.pack(pady=20)
            
            search_btn = tk.Button(buttons_frame, text="Rechercher", command=search_reservations,
                                 font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"], 
                                 relief=tk.FLAT, padx=20, pady=8)
            search_btn.pack(side=tk.LEFT, padx=5)
            
            cancel_btn = tk.Button(buttons_frame, text="Annuler", command=email_window.destroy,
                                 font=("Arial", 12, "bold"), bg=COLORS["danger"], fg=COLORS["white"], 
                                 relief=tk.FLAT, padx=20, pady=8)
            cancel_btn.pack(side=tk.LEFT, padx=5)
            
            # Permettre la recherche avec la touche Entrée
            email_entry.bind('<Return>', lambda e: search_reservations())
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ouverture des réservations: {e}")

    def display_user_reservations(self, user_email):
        """Affiche les réservations d'un utilisateur spécifique"""
        try:
            # Charger tous les événements
            events = self.controller.load_events()
            
            # Trouver les événements où l'utilisateur est inscrit
            user_reservations = []
            for event in events:
                inscrits = event.get('inscrits', [])
                for inscrit in inscrits:
                    if isinstance(inscrit, dict) and inscrit.get('email') == user_email:
                        # Ajouter les informations de réservation
                        reservation_info = {
                            'event_title': event.get('title', 'Sans titre'),
                            'event_type': event.get('type', ''),
                            'date': event.get('date', ''),
                            'time': event.get('time', ''),
                            'location': event.get('location', ''),
                            'price': event.get('price', '0'),
                            'reservation_date': inscrit.get('date_reservation', ''),
                            'status': inscrit.get('status', 'Confirmée'),
                            'event_id': event.get('id', ''),
                            'user_info': inscrit
                        }
                        user_reservations.append(reservation_info)
            
            # Créer une fenêtre pour afficher les réservations
            reservations_window = tk.Toplevel(self)
            reservations_window.title(f"Réservations - {user_email}")
            reservations_window.geometry("700x600")
            reservations_window.configure(bg=COLORS["light"])
            
            # Titre
            title_label = tk.Label(reservations_window, text=f"Mes réservations ({user_email})", 
                                 font=("Arial", 16, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
            title_label.pack(pady=20)
            
            # Informations de l'utilisateur
            if user_reservations:
                user_info = user_reservations[0]['user_info']
                user_name = user_info.get('nom', 'Non spécifié')
                user_phone = user_info.get('telephone', 'Non spécifié')
                
                info_text = f"👤 {user_name} | 📧 {user_email} | 📞 {user_phone}"
                info_label = tk.Label(reservations_window, text=info_text, 
                                    font=("Arial", 12), bg=COLORS["light"], fg=COLORS["text_secondary"])
                info_label.pack(pady=10)
            
            # Frame pour les réservations
            reservations_frame = tk.Frame(reservations_window, bg=COLORS["light"])
            reservations_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Scrollbar pour la liste
            canvas = tk.Canvas(reservations_frame, bg=COLORS["white"])
            scrollbar = tk.Scrollbar(reservations_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=COLORS["white"])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            scrollbar.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            
            if not user_reservations:
                no_reservations_label = tk.Label(scrollable_frame, text="Aucune réservation trouvée pour cet email", 
                                               font=("Arial", 14), bg=COLORS["white"], fg=COLORS["text_secondary"])
                no_reservations_label.pack(pady=50)
            else:
                for reservation in user_reservations:
                    # Carte de réservation
                    reservation_frame = tk.Frame(scrollable_frame, bg=COLORS["white"], relief=tk.RAISED, bd=2)
                    reservation_frame.pack(fill=tk.X, padx=10, pady=5)
                    
                    # En-tête avec statut
                    header_frame = tk.Frame(reservation_frame, bg=COLORS["primary"], height=35)
                    header_frame.pack(fill=tk.X)
                    header_frame.pack_propagate(False)
                    
                    # Titre de l'événement
                    title_label = tk.Label(header_frame, text=reservation['event_title'], 
                                         font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"])
                    title_label.pack(side=tk.LEFT, padx=10, pady=5)
                    
                    # Badge de statut
                    status_color = COLORS["success"] if reservation['status'] == 'Confirmée' else COLORS["warning"]
                    status_label = tk.Label(header_frame, text=reservation['status'], 
                                          font=("Arial", 10, "bold"), bg=status_color, fg=COLORS["white"], 
                                          padx=8, pady=2)
                    status_label.pack(side=tk.RIGHT, padx=10, pady=5)
                    
                    # Contenu
                    content_frame = tk.Frame(reservation_frame, bg=COLORS["light"])
                    content_frame.pack(fill=tk.X, padx=10, pady=10)
                    
                    # Détails de l'événement
                    details_frame = tk.Frame(content_frame, bg=COLORS["light"])
                    details_frame.pack(fill=tk.X, pady=5)
                    
                    # Date et heure
                    date_time_text = f"📅 {reservation['date']} à {reservation['time']}"
                    date_label = tk.Label(details_frame, text=date_time_text, 
                                        font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
                    date_label.pack(anchor=tk.W)
                    
                    # Lieu
                    location_text = f"📍 {reservation['location']}"
                    location_label = tk.Label(details_frame, text=location_text, 
                                            font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
                    location_label.pack(anchor=tk.W)
                    
                    # Prix
                    price_text = f"💰 Prix: {reservation['price']}€"
                    price_label = tk.Label(details_frame, text=price_text, 
                                         font=("Arial", 11), bg=COLORS["light"], fg=COLORS["text_primary"])
                    price_label.pack(anchor=tk.W)
                    
                    # Date de réservation
                    if reservation['reservation_date']:
                        reservation_date_text = f"📝 Réservé le: {reservation['reservation_date']}"
                        reservation_date_label = tk.Label(details_frame, text=reservation_date_text, 
                                                         font=("Arial", 10), bg=COLORS["light"], fg=COLORS["text_secondary"])
                        reservation_date_label.pack(anchor=tk.W, pady=(5, 0))
                    
                    # Boutons d'action
                    buttons_frame = tk.Frame(content_frame, bg=COLORS["light"])
                    buttons_frame.pack(fill=tk.X, pady=10)
                    
                    # Bouton Annuler réservation
                    cancel_btn = tk.Button(buttons_frame, text="Annuler réservation", 
                                         command=lambda r=reservation: self.cancel_reservation(r, user_email, reservations_window),
                                         font=("Arial", 10, "bold"), bg=COLORS["danger"], fg=COLORS["white"], 
                                         relief=tk.FLAT, padx=15, pady=5)
                    cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
                    
                    # Bouton Voir détails
                    details_btn = tk.Button(buttons_frame, text="Voir détails", 
                                          command=lambda r=reservation: self.show_reservation_details(r),
                                          font=("Arial", 10, "bold"), bg=COLORS["accent"], fg=COLORS["white"], 
                                          relief=tk.FLAT, padx=15, pady=5)
                    details_btn.pack(side=tk.LEFT)
            
            # Bouton fermer
            close_btn = tk.Button(reservations_window, text="Fermer", command=reservations_window.destroy,
                                font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"], 
                                relief=tk.FLAT, padx=20, pady=10)
            close_btn.pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des réservations: {e}")

    def cancel_reservation(self, reservation, user_email, window):
        """Annule une réservation"""
        try:
            # Demander confirmation
            if not messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir annuler cette réservation ?"):
                return
            
            # Charger les événements
            events = self.controller.load_events()
            
            # Trouver l'événement et supprimer la réservation
            for event in events:
                if event.get('id') == reservation['event_id']:
                    inscrits = event.get('inscrits', [])
                    # Supprimer l'inscription de cet utilisateur
                    event['inscrits'] = [inscrit for inscrit in inscrits 
                                       if not (isinstance(inscrit, dict) and inscrit.get('email') == user_email)]
                    break
            
            # Sauvegarder les modifications
            self.controller.save_events(events)
            
            messagebox.showinfo("Réservation annulée", "Votre réservation a été annulée avec succès")
            
            # Fermer la fenêtre et rouvrir les réservations
            window.destroy()
            self.display_user_reservations(user_email)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'annulation de la réservation: {e}")

    def show_reservation_details(self, reservation):
        """Affiche les détails d'une réservation"""
        try:
            details_window = tk.Toplevel(self)
            details_window.title("Détails de la réservation")
            details_window.geometry("500x400")
            details_window.configure(bg=COLORS["light"])
            
            # Titre
            title_label = tk.Label(details_window, text="Détails de la réservation", 
                                 font=("Arial", 16, "bold"), bg=COLORS["light"], fg=COLORS["text_primary"])
            title_label.pack(pady=20)
            
            # Contenu
            content_frame = tk.Frame(details_window, bg=COLORS["white"], relief=tk.RAISED, bd=2)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Informations détaillées
            details_text = f"""
Événement: {reservation['event_title']}
Type: {reservation['event_type']} 
Date: {reservation['date']}
Heure: {reservation['time']}
Lieu: {reservation['location']}
Prix: {reservation['price']}€
Statut: {reservation['status']}
Date de réservation: {reservation['reservation_date']}

Informations personnelles:
Nom: {reservation['user_info'].get('nom', 'Non spécifié')}
Email: {reservation['user_info'].get('email', 'Non spécifié')}
Téléphone: {reservation['user_info'].get('telephone', 'Non spécifié')}
            """
            
            details_label = tk.Label(content_frame, text=details_text, 
                                   font=("Arial", 11), bg=COLORS["white"], fg=COLORS["text_primary"], 
                                   justify=tk.LEFT, wraplength=450)
            details_label.pack(padx=20, pady=20)
            
            # Bouton fermer
            close_btn = tk.Button(details_window, text="Fermer", command=details_window.destroy,
                                font=("Arial", 12, "bold"), bg=COLORS["primary"], fg=COLORS["white"], 
                                relief=tk.FLAT, padx=20, pady=10)
            close_btn.pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des détails: {e}")

class CreateEventFrame(tk.Frame):
    def __init__(self, parent, controller, lang):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#ffffff")

        # Bouton de retour (flèche)
        btn_back = tk.Button(self, text=self.controller.get_text("back"), command=lambda: controller.show_frame("AccueilFrame"),
                           font=("Arial", 14), bg="#ffffff", bd=0, relief=tk.FLAT)
        btn_back.place(x=10, y=10)
        btn_back.text_key = "back"

        # Liste pour stocker temporairement les membres du staff ajoutés
        self.staff_members = []
        self.current_staff_index = 0

        label = tk.Label(self, text=self.controller.get_text("create_event"), font=("Arial", 18, "bold"), bg="#ffffff")
        label.pack(pady=20)
        label.text_key = "create_event"

        # Cadre principal pour les deux sections
        self.main_frame = tk.Frame(self, bg="#ffffff")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # --- Section Informations de l'événement ---
        self.event_info_frame = tk.LabelFrame(self.main_frame, text=self.controller.get_text("event_info"), padx=15, pady=15, bg="#ffffff")
        self.event_info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.event_info_frame.text_key = "event_info"

        # Champs pour les informations de l'événement avec espacement amélioré
        labels = []
        entries = []
        
        # Nom de l'événement
        label1 = tk.Label(self.event_info_frame, text=self.controller.get_text("event_name") + " :", bg="#ffffff")
        label1.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        label1.text_key = "event_name"
        labels.append(label1)
        
        self.entry_event_name = tk.Entry(self.event_info_frame, width=40, font=("Arial", 10))
        self.entry_event_name.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        entries.append(self.entry_event_name)

        # Type d'événement
        label2 = tk.Label(self.event_info_frame, text=self.controller.get_text("event_type") + " :", bg="#ffffff")
        label2.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        label2.text_key = "event_type"
        labels.append(label2)
        
        self.entry_event_type = tk.Entry(self.event_info_frame, width=40, font=("Arial", 10))
        self.entry_event_type.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        entries.append(self.entry_event_type)

        # Lieu de l'événement
        label3 = tk.Label(self.event_info_frame, text=self.controller.get_text("event_location") + " :", bg="#ffffff")
        label3.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        label3.text_key = "event_location"
        labels.append(label3)
        
        self.entry_event_location = tk.Entry(self.event_info_frame, width=40, font=("Arial", 10))
        self.entry_event_location.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        entries.append(self.entry_event_location)

        # Date et heure
        label4 = tk.Label(self.event_info_frame, text=self.controller.get_text("event_date_time") + " :", bg="#ffffff")
        label4.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        label4.text_key = "event_date_time"
        labels.append(label4)
        
        self.entry_event_datetime = tk.Entry(self.event_info_frame, width=40, font=("Arial", 10))
        self.entry_event_datetime.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        entries.append(self.entry_event_datetime)

        # Prix
        label5 = tk.Label(self.event_info_frame, text=self.controller.get_text("event_price") + " :", bg="#ffffff")
        label5.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        label5.text_key = "event_price"
        labels.append(label5)
        
        self.entry_event_price = tk.Entry(self.event_info_frame, width=40, font=("Arial", 10))
        self.entry_event_price.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        entries.append(self.entry_event_price)

        # Capacité
        label6 = tk.Label(self.event_info_frame, text=self.controller.get_text("event_capacity") + " :", bg="#ffffff")
        label6.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        label6.text_key = "event_capacity"
        labels.append(label6)
        
        self.entry_event_capacity = tk.Entry(self.event_info_frame, width=40, font=("Arial", 10))
        self.entry_event_capacity.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        entries.append(self.entry_event_capacity)

        # Image
        label7 = tk.Label(self.event_info_frame, text=self.controller.get_text("event_image") + " :", bg="#ffffff")
        label7.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        label7.text_key = "event_image"
        labels.append(label7)
        
        self.entry_event_image_path = tk.Entry(self.event_info_frame, width=40, font=("Arial", 10))
        self.entry_event_image_path.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        entries.append(self.entry_event_image_path)

        # Stocker les références pour la mise à jour
        self.event_labels = labels
        self.event_entries = entries

        # Bouton pour passer à la section staff avec style amélioré
        btn_next = tk.Button(self.event_info_frame, text=self.controller.get_text("next"), command=self.show_staff_section, 
                           font=("Arial", 12, "bold"), bg="#4285F4", fg="white", width=15, relief=tk.FLAT)
        btn_next.grid(row=7, column=0, columnspan=2, pady=20)
        btn_next.text_key = "next"
        self.btn_next = btn_next

        # --- Section Informations du staff ---
        self.staff_info_frame = tk.LabelFrame(self.main_frame, text=self.controller.get_text("member_info"), padx=15, pady=15, bg="#ffffff")
        self.staff_info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.staff_info_frame.pack_forget()  # Cacher initialement
        self.staff_info_frame.text_key = "member_info"

        # Liste pour afficher les membres du staff avec style amélioré
        self.staff_listbox = tk.Listbox(self.staff_info_frame, width=50, height=5, font=("Arial", 10))
        self.staff_listbox.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Champs pour ajouter un membre du staff avec espacement amélioré
        staff_labels = []
        staff_entries = []
        
        # Nom du membre
        staff_label1 = tk.Label(self.staff_info_frame, text=self.controller.get_text("staff_member_name") + " :", bg="#ffffff")
        staff_label1.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        staff_label1.text_key = "staff_member_name"
        staff_labels.append(staff_label1)
        
        self.entry_staff_name = tk.Entry(self.staff_info_frame, width=40, font=("Arial", 10))
        self.entry_staff_name.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        staff_entries.append(self.entry_staff_name)

        # Rôle du membre
        staff_label2 = tk.Label(self.staff_info_frame, text=self.controller.get_text("staff_member_role") + " :", bg="#ffffff")
        staff_label2.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        staff_label2.text_key = "staff_member_role"
        staff_labels.append(staff_label2)
        
        self.entry_staff_role = tk.Entry(self.staff_info_frame, width=40, font=("Arial", 10))
        self.entry_staff_role.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        staff_entries.append(self.entry_staff_role)

        # Email du membre
        staff_label3 = tk.Label(self.staff_info_frame, text=self.controller.get_text("staff_member_email") + " :", bg="#ffffff")
        staff_label3.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        staff_label3.text_key = "staff_member_email"
        staff_labels.append(staff_label3)
        
        self.entry_staff_contact = tk.Entry(self.staff_info_frame, width=40, font=("Arial", 10))
        self.entry_staff_contact.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        staff_entries.append(self.entry_staff_contact)

        # Stocker les références pour la mise à jour
        self.staff_labels = staff_labels
        self.staff_entries = staff_entries

        # Boutons pour la gestion du staff avec style amélioré
        staff_buttons_frame = tk.Frame(self.staff_info_frame, bg="#ffffff")
        staff_buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)

        btn_add_staff = tk.Button(staff_buttons_frame, text=self.controller.get_text("add_member"), command=self.add_staff_member,
                                font=("Arial", 12, "bold"), bg="#4285F4", fg="white", width=15, relief=tk.FLAT)
        btn_add_staff.pack(side=tk.LEFT, padx=5)
        btn_add_staff.text_key = "add_member"
        self.btn_add_staff = btn_add_staff

        btn_save = tk.Button(staff_buttons_frame, text=self.controller.get_text("save_event"), command=self.create_event,
                           font=("Arial", 12, "bold"), bg="#4285F4", fg="white", width=15, relief=tk.FLAT)
        btn_save.pack(side=tk.LEFT, padx=5)
        btn_save.text_key = "save_event"
        self.btn_save = btn_save

        btn_back_staff = tk.Button(staff_buttons_frame, text=self.controller.get_text("back"), command=self.show_event_section,
                           font=("Arial", 12, "bold"), bg="#4285F4", fg="white", width=15, relief=tk.FLAT)
        btn_back_staff.pack(side=tk.LEFT, padx=5)
        btn_back_staff.text_key = "back"
        self.btn_back_staff = btn_back_staff

    def show_staff_section(self):
        """Affiche la section des informations du staff."""
        self.event_info_frame.pack_forget()
        self.staff_info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.update_staff_list()

    def show_event_section(self):
        """Affiche la section des informations de l'événement."""
        self.staff_info_frame.pack_forget()
        self.event_info_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def update_staff_list(self):
        """Met à jour la liste des membres du staff."""
        self.staff_listbox.delete(0, tk.END)
        for staff in self.staff_members:
            self.staff_listbox.insert(tk.END, f"{staff['nom']} - {staff['rôle']}")

    def add_staff_member(self):
        """Ajoute un membre du staff à la liste."""
        try:
            # Messages selon la langue
            messages = {
                "fr": {
                    "incomplete": "Veuillez remplir tous les champs pour ajouter un membre.",
                    "invalid_contact": "Le contact doit être un email valide.",
                    "success": "Le membre {} ({}) a été ajouté avec succès.",
                    "error": "Une erreur est survenue lors de l'ajout du membre:\n{}"
                },
                "en": {
                    "incomplete": "Please fill in all fields to add a member.",
                    "invalid_contact": "Contact must be a valid email.",
                    "success": "Member {} ({}) has been added successfully.",
                    "error": "An error occurred while adding the member:\n{}"
                }
            }

            # Récupérer et nettoyer les valeurs
            name = self.entry_staff_name.get().strip()
            role = self.entry_staff_role.get().strip()
            contact = self.entry_staff_contact.get().strip()

            # Vérifier que tous les champs sont remplis
            if not all([name, role, contact]):
                messagebox.showwarning(
                    "Champs incomplets",
                    messages[self.controller.lang]["incomplete"],
                    parent=self
                )
                return

            # Vérifier si le contact est un email valide
            is_valid_contact = '@' in contact and '.' in contact

            if not is_valid_contact:
                messagebox.showwarning(
                    "Contact invalide",
                    messages[self.controller.lang]["invalid_contact"],
                    parent=self
                )
                return

            # Créer le nouveau membre du staff
            staff_member = {
                "nom": name,
                "rôle": role,
                "contact": contact
            }

            # Ajouter à la liste
            self.staff_members.append(staff_member)
            
            # Mettre à jour l'affichage
            self.update_staff_list()
            
            # Afficher un message de succès
            messagebox.showinfo(
                "Membre ajouté",
                messages[self.controller.lang]["success"].format(name, role),
                parent=self
            )

            # Effacer les champs après l'ajout
            self.clear_staff_form()

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                messages[self.controller.lang]["error"].format(str(e)),
                parent=self
            )

    def create_event(self):
        """Crée l'événement avec validation complète et sauvegarde JSON."""
        try:
            # Récupérer et nettoyer les valeurs
            event_name = self.entry_event_name.get().strip()
            event_type = self.entry_event_type.get().strip()
            event_location = self.entry_event_location.get().strip()
            event_datetime = self.entry_event_datetime.get().strip()
            event_price = self.entry_event_price.get().strip()
            event_capacity = self.entry_event_capacity.get().strip()
            event_image_path = self.entry_event_image_path.get().strip()

            # Validation des champs obligatoires
            if not event_name:
                messagebox.showwarning("Champ requis", "Le nom de l'événement est obligatoire")
                self.entry_event_name.focus()
                return
            
            if not event_type:
                messagebox.showwarning("Champ requis", "Le type d'événement est obligatoire")
                self.entry_event_type.focus()
                return
            
            if not event_location:
                messagebox.showwarning("Champ requis", "Le lieu de l'événement est obligatoire")
                self.entry_event_location.focus()
                return
            
            if not event_datetime:
                messagebox.showwarning("Champ requis", "La date et heure de l'événement sont obligatoires")
                self.entry_event_datetime.focus()
                return

            # Validation du format de date
            try:
                datetime.strptime(event_datetime, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showwarning("Format de date invalide", 
                                     "La date doit être au format AAAA-MM-JJ HH:MM\nExemple: 2024-03-20 14:30")
                self.entry_event_datetime.focus()
                return

            # Validation du prix
            try:
                price_value = float(event_price) if event_price else 0
                if price_value < 0:
                    messagebox.showwarning("Prix invalide", "Le prix ne peut pas être négatif")
                    self.entry_event_price.focus()
                    return
                if price_value > 10000:
                    messagebox.showwarning("Prix invalide", "Le prix ne peut pas dépasser 10 000 €")
                    self.entry_event_price.focus()
                    return
            except ValueError:
                messagebox.showwarning("Prix invalide", "Le prix doit être un nombre valide")
                self.entry_event_price.focus()
                return

            # Validation de la capacité
            try:
                capacity_value = int(event_capacity) if event_capacity else 0
                if capacity_value <= 0:
                    messagebox.showwarning("Capacité invalide", "La capacité doit être supérieure à 0")
                    self.entry_event_capacity.focus()
                    return
                if capacity_value > 10000:
                    messagebox.showwarning("Capacité invalide", "La capacité ne peut pas dépasser 10 000 personnes")
                    self.entry_event_capacity.focus()
                    return
            except ValueError:
                messagebox.showwarning("Capacité invalide", "La capacité doit être un nombre entier valide")
                self.entry_event_capacity.focus()
                return

            # Validation du staff
            if not self.staff_members:
                messagebox.showwarning("Staff requis", "Au moins un membre du staff doit être ajouté")
                return

            # Créer le nouvel événement avec la structure correcte
            new_event = {
                "title": event_name,  # Utiliser 'title' au lieu de 'nom' pour la cohérence
                "type": event_type,
                "location": event_location,  # Utiliser 'location' au lieu de 'lieu'
                "date": event_datetime.split()[0],  # Extraire juste la date
                "time": event_datetime.split()[1],  # Extraire juste l'heure
                "price": price_value,
                "capacity": capacity_value,
                "description": f"Événement {event_type} - {event_name}",  # Description par défaut
                "inscrits": [],
                "staff": self.staff_members.copy(),
                "image_path": event_image_path if event_image_path else None,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Générer un ID unique pour l'événement
            new_event['id'] = generer_id_unique()

            # Valider l'événement avec la fonction de validation
            erreurs = valider_evenement(new_event)
            if erreurs:
                error_message = "Erreurs de validation:\n" + "\n".join(erreurs)
                messagebox.showerror("Erreurs de validation", error_message)
                return

            # Charger les événements existants
            events = self.controller.load_events()
            
            # Vérifier si un événement avec le même nom existe déjà
            for existing_event in events:
                if existing_event.get('title') == event_name:
                    if messagebox.askyesno("Événement existant", 
                                         f"Un événement avec le nom '{event_name}' existe déjà.\nVoulez-vous le remplacer ?"):
                        # Supprimer l'ancien événement
                        events = [e for e in events if e.get('title') != event_name]
                    else:
                        return

            # Ajouter le nouvel événement
            events.append(new_event)

            # Sauvegarder dans le fichier JSON
            if self.controller.save_events(events):
                messagebox.showinfo(
                    "Succès",
                    f"Événement '{event_name}' créé avec succès !\n\n"
                    f"ID: {new_event['id']}\n"
                    f"Type: {event_type}\n"
                    f"Lieu: {event_location}\n"
                    f"Date: {event_datetime}\n"
                    f"Prix: {price_value}€\n"
                    f"Capacité: {capacity_value} personnes\n"
                    f"Membres du staff: {len(self.staff_members)}",
                    parent=self
                )

                # Réinitialiser les formulaires
                self.clear_event_form()
                self.clear_staff_form()
                self.staff_members = []
                self.staff_listbox.delete(0, tk.END)
                
                # Revenir à l'écran d'accueil
                self.controller.show_frame("AccueilFrame")
            else:
                messagebox.showerror(
                    "Erreur",
                    "Erreur lors de la sauvegarde de l'événement.\nVérifiez les permissions du fichier.",
                    parent=self
                )

        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Une erreur inattendue est survenue lors de la création de l'événement:\n{str(e)}",
                parent=self
            )
            print(f"Erreur détaillée: {e}")

    def clear_event_form(self):
        """Efface les champs du formulaire d'événement."""
        self.entry_event_name.delete(0, tk.END)
        self.entry_event_type.delete(0, tk.END)
        self.entry_event_location.delete(0, tk.END)
        self.entry_event_datetime.delete(0, tk.END)
        self.entry_event_price.delete(0, tk.END)
        self.entry_event_capacity.delete(0, tk.END)
        self.entry_event_image_path.delete(0, tk.END)

    def clear_staff_form(self):
        """Efface les champs du formulaire d'ajout de staff."""
        self.entry_staff_name.delete(0, tk.END)
        self.entry_staff_role.delete(0, tk.END)
        self.entry_staff_contact.delete(0, tk.END)
        self.staff_listbox.delete(0, tk.END)

    def update_texts(self):
        """Met à jour les textes selon la langue sélectionnée."""
        print("Updating CreateEventFrame texts")  # Debug log
        
        # Mettre à jour le titre principal
        if hasattr(self, 'label'):
            self.label.config(text=self.controller.get_text("create_event"))
        
        # Mettre à jour les labels de la section événement
        for label in self.event_labels:
            if hasattr(label, 'text_key'):
                label.config(text=self.controller.get_text(label.text_key) + " :")
        
        # Mettre à jour les boutons de la section événement
        if hasattr(self, 'btn_next'):
            self.btn_next.config(text=self.controller.get_text("next"))
        
        # Mettre à jour les labels de la section staff
        for label in self.staff_labels:
            if hasattr(label, 'text_key'):
                label.config(text=self.controller.get_text(label.text_key) + " :")
        
        # Mettre à jour les boutons de la section staff
        if hasattr(self, 'btn_add_staff'):
            self.btn_add_staff.config(text=self.controller.get_text("add_member"))
        if hasattr(self, 'btn_save'):
            self.btn_save.config(text=self.controller.get_text("save_event"))
        if hasattr(self, 'btn_back_staff'):
            self.btn_back_staff.config(text=self.controller.get_text("back"))
        
        # Mettre à jour les titres des frames
        if hasattr(self, 'event_info_frame'):
            self.event_info_frame.config(text=self.controller.get_text("event_info"))
        if hasattr(self, 'staff_info_frame'):
            self.staff_info_frame.config(text=self.controller.get_text("member_info"))

if __name__ == "__main__":
    app = Application()
    app.mainloop() 