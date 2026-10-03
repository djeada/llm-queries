# Formatowanie list (PL)

Szablony do tworzenia czytelnych, jednopoziomowych list punktowanych po polsku.

## Najlepiej sprawdza się przy

- notatkach i podsumowaniach
- porządkowaniu zaleceń lub wniosków
- przerabianiu akapitów na krótkie punkty
- ujednolicaniu stylu listy w dokumencie

## Oczekiwany wynik

- jedna lista bez zagnieżdżonych poziomów
- pełne, naturalnie brzmiące zdania
- spójny znak wypunktowania
- brak zbędnych wstępów i komentarzy
- wyróżnienia tylko wtedy, gdy użytkownik ich zażąda

## Wymagane dane wejściowe

- tekst lub temat do uporządkowania
- grupa docelowa
- preferowana długość punktów
- informacja, czy wolno używać pogrubienia lub kursywy

## Podstawowy prompt

```text
Przeredaguj poniższy tekst jako jednopoziomową listę punktowaną.

Zasady:
1. Każdy punkt ma być pełnym zdaniem.
2. Zachowaj znaczenie, fakty, liczby i stopień pewności z tekstu źródłowego.
3. Nie dodawaj nowych informacji.
4. Używaj jednego znaku wypunktowania: "-".
5. Nie twórz podpunktów.
6. Usuń powtórzenia i zbędne wprowadzenia.
7. Jeśli termin specjalistyczny jest potrzebny, zachowaj go.
8. Nie używaj pogrubienia ani kursywy, chyba że poproszę o wyróżnienie.

Tekst:
"""
[WKLEJ TEKST]
"""
```

## Wariant z wyróżnieniem pojęcia

```text
Przeredaguj poniższy tekst jako jednopoziomową listę punktowaną.

W każdym punkcie wyróżnij pogrubieniem najwyżej jedno ważne pojęcie, ale nie
zaczynaj punktu od wyróżnionego słowa. Wyróżnienie ma pomagać w skanowaniu
tekstu, a nie zastępować treść zdania.

Zachowaj wszystkie fakty i nie dodawaj nowych informacji.

Tekst:
"""
[WKLEJ TEKST]
"""
```

## Wariant skrócony

```text
Skróć poniższy materiał do [LICZBA] punktów.

Każdy punkt:
- ma zawierać jedną główną myśl,
- ma być zrozumiały bez dodatkowego komentarza,
- ma zachować ważne liczby, terminy i zastrzeżenia,
- nie może powtarzać informacji z innych punktów.

Materiał:
"""
[WKLEJ MATERIAŁ]
"""
```

## Lista kontrolna

- Liczba poziomów listy wynosi jeden.
- Każdy punkt jest pełnym zdaniem.
- Punkty mają równoległą strukturę tam, gdzie to naturalne.
- Wyróżnienia są zgodne z poleceniem.
- Żaden fakt nie został dopisany bez źródła.
- Lista nie zawiera pustych podsumowań typu „Podsumowując”.
