"""Tokenisation de tweets.

Découpe un texte en une liste de tokens en gardant les éléments utiles à
l'analyse de sentiment : URLs, mentions (@user), hashtags (#mot), émoticônes
(:) :( ;D ...), emojis, mots (accents et apostrophes inclus) et nombres.

La ponctuation simple est ignorée et la casse n'est pas modifiée : mise en
minuscules, décodage des entités HTML et suppression des URLs relèvent du
nettoyage (src/text_cleaning.py). Ce module ne dépend d'aucune autre fonctionnalité.
"""

import re

# L'ordre des alternatives compte : à une position donnée, la première qui
# correspond gagne (une URL est donc lue en entier avant d'être coupée en mots).
TOKEN_PATTERN = re.compile(
    r"""
    (?:https?://|www\.)\S*[^\s.,;:!?)\]}'"’]       # URL, sans ponctuation finale
    | @\w+                                          # mention
    | \#\w+                                         # hashtag
    | [:;=][-o*']?[()\[\]](?!\w)                    # émoticône :) :-( ;) , peut être collée à un mot (great:))
    | (?<!\w)[:;=][-o*']?[dDpP/\\|](?!\w)           # émoticône :D :P :/ , seule (évite 3:30 et note:data)
    | [\U0001F000-\U0001FAFF☀-➿]          # emoji (un token par emoji)
    | \d+(?:[.,]\d+)+%?                             # nombre avec séparateur : 3.5, 3,5, 1,000,000, 4.5%
    | \w+(?:['’-]\w+)*%?                            # mot ou nombre : can't, C'est, 100%
    """,
    re.VERBOSE,
)


def tokenize(text):
    """Découpe un tweet en liste de tokens.

    Exemple : "RT @john: Love it :) #Apple" donne
    ["RT", "@john", "Love", "it", ":)", "#Apple"].

    Une valeur vide ou non textuelle (None, NaN, nombre) retourne [].

    Choix et limites connus :
    - Un nombre avec séparateur reste un seul token : "3.5", "3,5", "4.5%",
      "1,000,000". Conséquence : "1,2,3" (sans espaces) donne aussi un seul token.
    - Les émoticônes à bouche symbole ( ) [ ] peuvent être collées à un mot
      ("great:)" donne "great" et ":)"). Celles à bouche lettre (:D :P) ou
      barre (:/ :|) doivent être seules, sinon "3:30" ou "note:data" seraient coupés à tort.
    - Les emojis composés (drapeaux, familles, teintes de peau) sont séparés
      en emojis simples ; le sélecteur de variation (U+FE0F) est ignoré.
    """
    if not isinstance(text, str):
        return []
    return TOKEN_PATTERN.findall(text)
