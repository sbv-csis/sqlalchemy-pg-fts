import pytest

from sqlalchemy_pg_fts.websearch import _filter, websearch_to_tsquery


@pytest.mark.parametrize(
    "query,filtered",
    [
        ('""', ""),
        ("!", " "),
        ("|", " "),
        ("&", " "),
        ("(", " "),
        (")", " "),
        ("[", " "),
        ("]", " "),
        ("{", " "),
        ("}", " "),
        ("<", " "),
        (">", " "),
        ("+", " "),
        ("=", " "),
        ("%", " "),
        ("$", " "),
        ("#", " "),
        (",", " "),
        (".", " "),
        ("?", " "),
        (";", " "),
        ("`", " "),
        ("/", " "),
        ("\\", " "),
        ('"word"', "word"),
        ('" "', ""),
        ('" word "', "word"),
        # unchanged
        ("", ""),
        (" ", " "),
        ("word", "word"),
        ('"word word"', '"word word"'),
    ],
)
def test_filter(query, filtered):
    assert _filter(query) == filtered


@pytest.mark.parametrize(
    "query,tsquery",
    [
        ("dinosaurs meteor paleontology", "dinosaurs & meteor & paleontology"),
        ("dino*", "dino:*"),
        ("", ""),
        ('dinosaur -"bird chicken"', "dinosaur & !( bird <-> chicken )"),
        ("dinosaur -bird -chicken", "dinosaur & ! bird & ! chicken"),
        ('dino* "long ago"', "dino:* & ( long <-> ago )"),
        ('dino "long ago" -extinct', "dino & ( long <-> ago ) & ! extinct"),
        ('(dino -extinct) or "quite alive"', "dino & ! extinct | ( quite <-> alive )"),
        (
            'dinosaur metor or -paleontology "party bus"',
            "dinosaur & metor | ! paleontology & ( party <-> bus )",
        ),
        # Additional test cases inspired by PostgreSQL websearch_to_tsquery tests
        ("abc def", "abc & def"),
        ("cat or rat", "cat | rat"),
        ("cat OR rat", "cat | rat"),
        ("fat or rat", "fat | rat"),
        ('"fat cat"', "( fat <-> cat )"),
        ('abc "fat cat"', "abc & ( fat <-> cat )"),
        ('"fat cat" def', "( fat <-> cat ) & def"),
        ('abc "def ghi" jkl', "abc & ( def <-> ghi ) & jkl"),
        ("cat -rat", "cat & ! rat"),
        ('cat -"fat rat"', "cat & !( fat <-> rat )"),
        ('cat -"fat rat" cheese', "cat & !( fat <-> rat ) & cheese"),
        ("fat or -rat", "fat | ! rat"),
        ('"fat cat" eaten or rat', "( fat <-> cat ) & eaten | rat"),
        ('"fat cat" eaten or -rat', "( fat <-> cat ) & eaten | ! rat"),
        ("abc -def -ghi", "abc & ! def & ! ghi"),
        ("test*", "test:*"),
        ("fat* or rat*", "fat:* | rat:*"),
        ("abc -test*", "abc & ! test:*"),
        ('"fat cat" -test*', "( fat <-> cat ) & ! test:*"),
        ("word", "word"),
        ("-word", "! word"),
        ("word -negated", "word & ! negated"),

    ],
)
def test_websearch_to_tsquery(query, tsquery):
    assert websearch_to_tsquery(query) == tsquery
