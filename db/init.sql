/**
* Create configuration for czech and install necessary dictionaries.
**/

-- CREATE USER vyrobenounas WITH PASSWORD 'vyrobenounas';

CREATE EXTENSION unaccent;

-- ALTER TEXT SEARCH DICTIONARY unaccent OWNER TO vyrobenounas;

CREATE TEXT SEARCH CONFIGURATION czech ( COPY = pg_catalog.simple );

-- ALTER TEXT SEARCH CONFIGURATION czech OWNER TO vyrobenounas;

CREATE TEXT SEARCH DICTIONARY czech_ispell (
    TEMPLATE = ispell,
    DictFile = czech,
    AffFile = czech,
    StopWords = czech
);

-- ALTER TEXT SEARCH DICTIONARY czech_ispell OWNER TO vyrobenounas;

ALTER TEXT SEARCH CONFIGURATION czech
    ALTER MAPPING FOR hword, hword_part, word,
                      asciihword, asciiword, hword_asciipart
    WITH czech_ispell, unaccent;

CREATE DATABASE vyrobenounas WITH
    -- OWNER vyrobenounas
    ENCODING 'utf8' LC_COLLATE 'cs_CZ.utf8'
    TEMPLATE template0;

/**
* # \dF+ czech
* Text search configuration "public.czech"
* Parser: "pg_catalog.default"
*       Token      |     Dictionaries
* -----------------+-----------------------
*  asciihword      | czech_ispell,unaccent
*  asciiword       | czech_ispell,unaccent
*  email           | simple
*  file            | simple
*  float           | simple
*  host            | simple
*  hword           | czech_ispell,unaccent
*  hword_asciipart | czech_ispell,unaccent
*  hword_numpart   | simple
*  hword_part      | czech_ispell,unaccent
*  int             | simple
*  numhword        | simple
*  numword         | simple
*  sfloat          | simple
*  uint            | simple
*  url             | simple
*  url_path        | simple
*  version         | simple
*  word            | czech_ispell,unaccent
**/
