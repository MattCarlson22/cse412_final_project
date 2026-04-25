"""Mock data for the music library frontend.

Shapes mirror the Phase 2 schema columns so swapping these in for real
psycopg2 cursor results later is a near-drop-in change.
"""

USERS = [
    {"username": "jdoe", "password": "pass123", "email": "jdoe@email.com"},
    {"username": "asmith", "password": "music4life", "email": "asmith@gmail.com"},
    {"username": "mjohnson", "password": "vinyl99", "email": "mj@yahoo.com"},
    {"username": "kwilliams", "password": "beats2024", "email": "kwill@email.com"},
    {"username": "lbrown", "password": "sound_wave", "email": "lbrown@outlook.com"},
]

RELEASES = [
    {
        "id": 1,
        "title": "Abbey Road",
        "contributors": "The Beatles",
        "r_type": "Album",
        "format": "Vinyl",
        "r_date": "1969-09-26",
        "r_label": "Apple Records",
        "cover": "/static/img/placeholder.svg",
        "genre": "Rock",
        "details": "Often considered The Beatles' finest studio work, Abbey Road "
                   "was the last album the band recorded together. The second side "
                   "features a celebrated medley of songs that flow seamlessly into "
                   "one another.",
        "tracks": [
            {"t_num": 1, "title": "Come Together", "duration": 259, "genre": "Rock", "features": ""},
            {"t_num": 2, "title": "Something",     "duration": 182, "genre": "Rock", "features": ""},
            {"t_num": 3, "title": "Here Comes the Sun", "duration": 185, "genre": "Rock", "features": ""},
            {"t_num": 4, "title": "Oh! Darling",   "duration": 208, "genre": "Rock", "features": ""},
            {"t_num": 5, "title": "Golden Slumbers","duration": 91,  "genre": "Rock", "features": ""},
        ],
    },
    {
        "id": 2,
        "title": "OK Computer",
        "contributors": "Radiohead",
        "r_type": "Album",
        "format": "CD",
        "r_date": "1997-06-16",
        "r_label": "Parlophone",
        "cover": "/static/img/placeholder.svg",
        "genre": "Alternative Rock",
        "details": "Radiohead's third studio album, widely acclaimed as one of the "
                   "greatest albums ever made. Its themes of alienation, consumerism, "
                   "and political corruption proved remarkably prescient.",
        "tracks": [
            {"t_num": 1, "title": "Airbag",          "duration": 284, "genre": "Alternative Rock", "features": ""},
            {"t_num": 2, "title": "Paranoid Android", "duration": 386, "genre": "Alternative Rock", "features": ""},
            {"t_num": 3, "title": "Karma Police",     "duration": 263, "genre": "Alternative Rock", "features": ""},
            {"t_num": 4, "title": "No Surprises",     "duration": 228, "genre": "Alternative Rock", "features": ""},
            {"t_num": 5, "title": "Exit Music (For a Film)", "duration": 244, "genre": "Alternative Rock", "features": ""},
        ],
    },
    {
        "id": 3,
        "title": "Rumours",
        "contributors": "Fleetwood Mac",
        "r_type": "Album",
        "format": "Vinyl",
        "r_date": "1977-02-04",
        "r_label": "Warner Bros",
        "cover": "/static/img/placeholder.svg",
        "genre": "Soft Rock",
        "details": "Recorded during a period of intense personal turmoil within the "
                   "band, Rumours became one of the best-selling albums of all time, "
                   "with multiple chart-topping singles.",
        "tracks": [
            {"t_num": 1, "title": "Dreams",        "duration": 257, "genre": "Soft Rock", "features": ""},
            {"t_num": 2, "title": "Go Your Own Way","duration": 222, "genre": "Rock",      "features": ""},
            {"t_num": 3, "title": "The Chain",      "duration": 270, "genre": "Rock",      "features": ""},
            {"t_num": 4, "title": "Gold Dust Woman","duration": 289, "genre": "Soft Rock", "features": ""},
            {"t_num": 5, "title": "Never Going Back Again", "duration": 134, "genre": "Soft Rock", "features": ""},
        ],
    },
    {
        "id": 4,
        "title": "AM",
        "contributors": "Arctic Monkeys",
        "r_type": "Album",
        "format": "CD",
        "r_date": "2013-09-09",
        "r_label": "Domino Recording",
        "cover": "/static/img/placeholder.svg",
        "genre": "Indie Rock",
        "details": "The Arctic Monkeys' fifth studio album, a sleek and confident "
                   "record that blends heavy riffs with slinky, late-night grooves. "
                   "Features collaborations with Josh Homme and Richard Hawley.",
        "tracks": [
            {"t_num": 1, "title": "Do I Wanna Know?",                       "duration": 272, "genre": "Indie Rock", "features": ""},
            {"t_num": 2, "title": "R U Mine?",                              "duration": 200, "genre": "Indie Rock", "features": ""},
            {"t_num": 3, "title": "Why'd You Only Call Me When You're High?","duration": 164, "genre": "Indie Rock", "features": ""},
            {"t_num": 4, "title": "One for the Road",                       "duration": 215, "genre": "Indie Rock", "features": ""},
            {"t_num": 5, "title": "Snap Out of It",                         "duration": 191, "genre": "Indie Rock", "features": ""},
        ],
    },
    {
        "id": 5,
        "title": "Currents",
        "contributors": "Tame Impala",
        "r_type": "Album",
        "format": "Digital",
        "r_date": "2015-07-17",
        "r_label": "Modular Recordings",
        "cover": "/static/img/placeholder.svg",
        "genre": "Psychedelic Pop",
        "details": "Kevin Parker's third album as Tame Impala marked a sharp turn "
                   "toward electronic and disco-influenced sounds, written and produced "
                   "entirely by Parker during a personal upheaval.",
        "tracks": [
            {"t_num": 1, "title": "Let It Happen",            "duration": 467, "genre": "Psychedelic Pop", "features": ""},
            {"t_num": 2, "title": "The Less I Know the Better","duration": 218, "genre": "Psychedelic Pop", "features": ""},
            {"t_num": 3, "title": "'Cause I'm a Man",         "duration": 236, "genre": "Psychedelic Pop", "features": ""},
            {"t_num": 4, "title": "Eventually",               "duration": 317, "genre": "Psychedelic Pop", "features": ""},
            {"t_num": 5, "title": "New Person, Same Old Mistakes","duration": 348, "genre": "Psychedelic Pop", "features": ""},
        ],
    },
    {
        "id": 6,
        "title": "The Dark Side of the Moon",
        "contributors": "Pink Floyd",
        "r_type": "Album",
        "format": "Vinyl",
        "r_date": "1973-03-01",
        "r_label": "Harvest Records",
        "cover": "/static/img/placeholder.svg",
        "genre": "Progressive Rock",
        "details": "One of the best-selling albums of all time, The Dark Side of "
                   "the Moon spent 741 weeks on the Billboard 200. Its themes of "
                   "time, death, greed, and mental illness remain resonant.",
        "tracks": [
            {"t_num": 1, "title": "Speak to Me / Breathe", "duration": 234, "genre": "Progressive Rock", "features": ""},
            {"t_num": 2, "title": "Time",                  "duration": 421, "genre": "Progressive Rock", "features": ""},
            {"t_num": 3, "title": "Money",                 "duration": 382, "genre": "Progressive Rock", "features": ""},
            {"t_num": 4, "title": "Us and Them",           "duration": 469, "genre": "Progressive Rock", "features": ""},
            {"t_num": 5, "title": "Brain Damage",          "duration": 228, "genre": "Progressive Rock", "features": ""},
        ],
    },
    {
        "id": 7,
        "title": "Let It Bleed",
        "contributors": "The Rolling Stones",
        "r_type": "Album",
        "format": "Vinyl",
        "r_date": "1969-12-05",
        "r_label": "Decca Records",
        "cover": "/static/img/placeholder.svg",
        "genre": "Blues Rock",
        "details": "Released the same week as the Altamont Free Concert, "
                   "Let It Bleed captures the Rolling Stones at their rawest, "
                   "featuring guest appearances from Leon Russell and Ry Cooder.",
        "tracks": [
            {"t_num": 1, "title": "Gimme Shelter",      "duration": 271, "genre": "Blues Rock", "features": "Merry Clayton"},
            {"t_num": 2, "title": "Love in Vain",       "duration": 242, "genre": "Blues Rock", "features": ""},
            {"t_num": 3, "title": "Midnight Rambler",   "duration": 412, "genre": "Blues Rock", "features": ""},
            {"t_num": 4, "title": "Let It Bleed",       "duration": 327, "genre": "Blues Rock", "features": ""},
            {"t_num": 5, "title": "You Can't Always Get What You Want", "duration": 447, "genre": "Blues Rock", "features": "London Bach Choir"},
        ],
    },
    {
        "id": 8,
        "title": "Led Zeppelin IV",
        "contributors": "Led Zeppelin",
        "r_type": "Album",
        "format": "Vinyl",
        "r_date": "1971-11-08",
        "r_label": "Atlantic Records",
        "cover": "/static/img/placeholder.svg",
        "genre": "Hard Rock",
        "details": "Officially untitled but known by many names, Led Zeppelin IV "
                   "contains some of the band's most iconic work, including Stairway "
                   "to Heaven, which is one of the most requested songs in FM radio history.",
        "tracks": [
            {"t_num": 1, "title": "Black Dog",          "duration": 295, "genre": "Hard Rock", "features": ""},
            {"t_num": 2, "title": "Rock and Roll",      "duration": 220, "genre": "Hard Rock", "features": ""},
            {"t_num": 3, "title": "The Battle of Evermore", "duration": 350, "genre": "Folk Rock", "features": "Sandy Denny"},
            {"t_num": 4, "title": "Stairway to Heaven", "duration": 482, "genre": "Hard Rock", "features": ""},
            {"t_num": 5, "title": "When the Levee Breaks","duration": 427, "genre": "Blues Rock", "features": ""},
        ],
    },
    {
        "id": 9,
        "title": "Nevermind",
        "contributors": "Nirvana",
        "r_type": "Album",
        "format": "CD",
        "r_date": "1991-09-24",
        "r_label": "DGC Records",
        "cover": "/static/img/placeholder.svg",
        "genre": "Grunge",
        "details": "Nevermind displaced Michael Jackson from the number one spot "
                   "and is widely credited with bringing alternative rock to mainstream "
                   "audiences. Produced by Butch Vig.",
        "tracks": [
            {"t_num": 1, "title": "Smells Like Teen Spirit", "duration": 301, "genre": "Grunge", "features": ""},
            {"t_num": 2, "title": "In Bloom",               "duration": 255, "genre": "Grunge", "features": ""},
            {"t_num": 3, "title": "Come as You Are",        "duration": 219, "genre": "Grunge", "features": ""},
            {"t_num": 4, "title": "Lithium",                "duration": 257, "genre": "Grunge", "features": ""},
            {"t_num": 5, "title": "Polly",                  "duration": 178, "genre": "Grunge", "features": ""},
        ],
    },
    {
        "id": 10,
        "title": "Discovery",
        "contributors": "Daft Punk",
        "r_type": "Album",
        "format": "CD",
        "r_date": "2001-03-12",
        "r_label": "Virgin Records",
        "cover": "/static/img/placeholder.svg",
        "genre": "Electronic",
        "details": "Daft Punk's second studio album draws heavily on 70s and 80s "
                   "pop, funk, and disco. Served as the soundtrack for the anime film "
                   "Interstella 5555.",
        "tracks": [
            {"t_num": 1, "title": "One More Time",   "duration": 320, "genre": "Electronic", "features": ""},
            {"t_num": 2, "title": "Aerodynamic",     "duration": 213, "genre": "Electronic", "features": ""},
            {"t_num": 3, "title": "Digital Love",    "duration": 301, "genre": "Electronic", "features": ""},
            {"t_num": 4, "title": "Harder, Better, Faster, Stronger", "duration": 224, "genre": "Electronic", "features": ""},
            {"t_num": 5, "title": "Something About Us", "duration": 231, "genre": "Electronic", "features": ""},
        ],
    },
    {
        "id": 11,
        "title": "Random Access Memories",
        "contributors": "Daft Punk",
        "r_type": "Album",
        "format": "Vinyl",
        "r_date": "2013-05-17",
        "r_label": "Columbia Records",
        "cover": "/static/img/placeholder.svg",
        "genre": "Electronic",
        "details": "Recorded largely with live musicians, Random Access Memories "
                   "is a love letter to the analog sounds of 1970s pop and disco. "
                   "Won Album of the Year at the 2014 Grammy Awards.",
        "tracks": [
            {"t_num": 1, "title": "Give Life Back to Music", "duration": 274, "genre": "Electronic", "features": "Nile Rodgers"},
            {"t_num": 2, "title": "The Game of Love",       "duration": 261, "genre": "Electronic", "features": ""},
            {"t_num": 3, "title": "Giorgio by Moroder",     "duration": 544, "genre": "Electronic", "features": "Giorgio Moroder"},
            {"t_num": 4, "title": "Instant Crush",          "duration": 337, "genre": "Electronic", "features": "Julian Casablancas"},
            {"t_num": 5, "title": "Get Lucky",              "duration": 369, "genre": "Funk",       "features": "Pharrell Williams, Nile Rodgers"},
        ],
    },
    {
        "id": 12,
        "title": "In Rainbows",
        "contributors": "Radiohead",
        "r_type": "Album",
        "format": "Digital",
        "r_date": "2007-10-10",
        "r_label": "Self-released",
        "cover": "/static/img/placeholder.svg",
        "genre": "Alternative Rock",
        "details": "Released as a pay-what-you-want download, In Rainbows was a "
                   "landmark moment in digital music distribution. The album itself "
                   "is widely regarded as one of Radiohead's warmest and most intimate records.",
        "tracks": [
            {"t_num": 1, "title": "15 Step",       "duration": 237, "genre": "Alternative Rock", "features": ""},
            {"t_num": 2, "title": "Bodysnatchers",  "duration": 242, "genre": "Alternative Rock", "features": ""},
            {"t_num": 3, "title": "Nude",           "duration": 255, "genre": "Alternative Rock", "features": ""},
            {"t_num": 4, "title": "Weird Fishes/Arpeggi", "duration": 318, "genre": "Alternative Rock", "features": ""},
            {"t_num": 5, "title": "All I Need",     "duration": 234, "genre": "Alternative Rock", "features": ""},
        ],
    },
]

# Build a lookup dict by id for quick access in routes.
RELEASES_BY_ID = {r["id"]: r for r in RELEASES}

COLLECTIONS = [
    {
        "c_id": 101,
        "name": "My Vinyl Stash",
        "release_ids": [1, 3, 6, 7],
    },
    {
        "c_id": 102,
        "name": "Road Trip Faves",
        "release_ids": [2, 4, 9],
    },
    {
        "c_id": 103,
        "name": "Late Night Rotation",
        "release_ids": [5, 10, 11, 8, 12],
    },
]

COLLECTIONS_BY_ID = {c["c_id"]: c for c in COLLECTIONS}
