"""
Language detection utility for job postings.
"""

import re
from typing import Tuple


class LanguageDetector:
    """
    Detects the language of text using keyword analysis and pattern matching.
    Lightweight solution without external dependencies.
    """
    
    # Common words and patterns for each language
    LANGUAGE_PATTERNS = {
        'english': {
            'common_words': ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'with', 'as', 'on', 'at', 'by', 'from', 'that', 'this', 'are', 'be', 'have', 'has', 'will', 'would', 'could', 'should', 'may', 'can', 'our', 'your', 'their', 'we', 'you', 'they'],
            'job_keywords': ['experience', 'skills', 'requirements', 'responsibilities', 'qualifications', 'position', 'role', 'team', 'company', 'work', 'development', 'management', 'software', 'engineer', 'developer', 'analyst', 'manager', 'opportunity', 'candidate', 'apply', 'application'],
            'weight': 1.0
        },
        'french': {
            'common_words': ['le', 'de', 'et', 'la', 'les', 'des', 'un', 'une', 'dans', 'pour', 'avec', 'sur', 'par', 'plus', 'ce', 'ne', 'se', 'que', 'qui', 'nous', 'vous', 'ils', 'elle', 'leur', 'cette', 'être', 'avoir', 'faire', 'dire', 'aller', 'voir'],
            'job_keywords': ['expérience', 'compétences', 'exigences', 'responsabilités', 'qualifications', 'poste', 'rôle', 'équipe', 'entreprise', 'travail', 'développement', 'gestion', 'logiciel', 'ingénieur', 'développeur', 'analyste', 'gestionnaire', 'opportunité', 'candidat', 'postuler', 'candidature'],
            'weight': 1.1  # Slightly higher weight for French as it's common in Belgium
        },
        'dutch': {
            'common_words': ['de', 'het', 'en', 'van', 'een', 'in', 'is', 'op', 'aan', 'met', 'voor', 'zijn', 'die', 'er', 'als', 'bij', 'om', 'uit', 'naar', 'maar', 'ook', 'dan', 'wel', 'geen', 'nog', 'kunnen', 'hebben', 'worden', 'deze', 'door'],
            'job_keywords': ['ervaring', 'vaardigheden', 'vereisten', 'verantwoordelijkheden', 'kwalificaties', 'functie', 'rol', 'team', 'bedrijf', 'werk', 'ontwikkeling', 'beheer', 'software', 'ingenieur', 'ontwikkelaar', 'analist', 'manager', 'kans', 'kandidaat', 'solliciteren', 'sollicitatie'],
            'weight': 1.1  # Higher weight for Dutch/Flemish as it's common in Belgium
        },
        'spanish': {
            'common_words': ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'ser', 'se', 'no', 'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'poder', 'decir', 'este', 'ese', 'otro', 'después'],
            'job_keywords': ['experiencia', 'habilidades', 'requisitos', 'responsabilidades', 'calificaciones', 'posición', 'puesto', 'equipo', 'empresa', 'trabajo', 'desarrollo', 'gestión', 'software', 'ingeniero', 'desarrollador', 'analista', 'gerente', 'oportunidad', 'candidato', 'aplicar', 'aplicación'],
            'weight': 0.9
        },
    }
    
    # Language-specific characters and patterns
    SPECIAL_CHARACTERS = {
        'french': ['é', 'è', 'ê', 'ë', 'à', 'â', 'ç', 'ù', 'û', 'ô', 'î', 'ï', 'œ'],
        'dutch': ['ĳ', 'ë', 'ï'],
        'spanish': ['ñ', 'á', 'é', 'í', 'ó', 'ú', '¿', '¡'],
        'german': ['ä', 'ö', 'ü', 'ß'],
        'italian': ['à', 'è', 'é', 'ì', 'ò', 'ù']
    }
    
    @staticmethod
    def detect_language(text: str) -> Tuple[str, float]:
        """
        Detect the language of the given text.
        
        Args:
            text: The text to analyze
            
        Returns:
            Tuple of (language_name, confidence_score)
        """
        if not text:
            return 'english', 0.5  # Default to English
        
        text_lower = text.lower()
        words = re.findall(r'\b[a-zàâäçèéêëîïôùûüÿñáíóúß]+\b', text_lower)
        
        if not words:
            return 'english', 0.5
        
        scores = {}
        
        for lang, patterns in LanguageDetector.LANGUAGE_PATTERNS.items():
            score = 0
            word_count = 0
            
            # Count common words
            for word in patterns['common_words']:
                count = words.count(word)
                if count > 0:
                    score += count * 2  # Common words worth 2 points
                    word_count += count
            
            # Count job-specific keywords
            for keyword in patterns['job_keywords']:
                if keyword in text_lower:
                    score += 3  # Job keywords worth 3 points
                    word_count += 1
            
            # Check for special characters
            if lang in LanguageDetector.SPECIAL_CHARACTERS:
                for char in LanguageDetector.SPECIAL_CHARACTERS[lang]:
                    if char in text_lower:
                        score += 5  # Special characters are strong indicators
            
            # Apply language weight
            score *= patterns['weight']
            
            # Normalize by text length
            if word_count > 0:
                scores[lang] = score / max(1, len(words) / 100)
            else:
                scores[lang] = 0
        
        if not scores:
            return 'english', 0.5
        
        # Get the language with highest score
        best_lang = max(scores.items(), key=lambda x: x[1])
        
        # Calculate confidence (0-1 scale)
        total_score = sum(scores.values())
        confidence = best_lang[1] / total_score if total_score > 0 else 0.5
        
        # If confidence is too low, default to English
        if confidence < 0.3:
            return 'english', 0.5
        
        return best_lang[0], confidence
    
    @staticmethod
    def get_language_name(language_code: str) -> str:
        """
        Get the full language name from code.
        
        Args:
            language_code: The language code (e.g., 'en', 'fr')
            
        Returns:
            Full language name
        """
        language_names = {
            'english': 'English',
            'french': 'Français',
            'dutch': 'Nederlands',
            'spanish': 'Español',
            'german': 'Deutsch',
            'italian': 'Italiano'
        }
        return language_names.get(language_code, 'English')
    
    @staticmethod
    def get_salutation(language: str) -> str:
        """
        Get the appropriate salutation for the detected language.
        
        Args:
            language: The detected language
            
        Returns:
            Appropriate salutation
        """
        salutations = {
            'english': 'Dear Hiring Manager,',
            'french': 'Madame, Monsieur,',
            'dutch': 'Geachte heer/mevrouw,',
            'spanish': 'Estimado/a responsable de contratación,',
            'german': 'Sehr geehrte Damen und Herren,',
            'italian': 'Gentile responsabile delle assunzioni,'
        }
        return salutations.get(language, 'Dear Hiring Manager,')
    
    @staticmethod
    def get_closing(language: str) -> str:
        """
        Get the appropriate closing for the detected language.
        
        Args:
            language: The detected language
            
        Returns:
            Appropriate closing
        """
        closings = {
            'english': 'Sincerely,',
            'french': 'Cordialement,',
            'dutch': 'Met vriendelijke groet,',
            'spanish': 'Atentamente,',
            'german': 'Mit freundlichen Grüßen,',
            'italian': 'Cordiali saluti,'
        }
        return closings.get(language, 'Sincerely,')