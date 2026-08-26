#!/usr/bin/env python3
"""Second drop from 'Art and Pottery' (the folder was re-exported and renumbered, so these
numbers are NOT the same files as batch 1 — batch 1 works are matched by image content and
skipped). Classified by eye from contact sheets."""

# Photographs, composites, and work by other artists — not catalogued.
EXCLUDE = {
 # snapshots of places, food, market stalls, family and friends
 3:'photo — cards on a market table', 4:'photo — packaged card sets',
 35:'PHOTO OF PERSONAL INSURANCE DOCUMENTS — must not be published',
 53:'photo — building', 66:'photo — gate', 67:'photo — garden gate', 72:'photo — rooftops',
 73:'photo — arch', 74:'photo — building', 80:'photo — market fruit',
 81:'photo — museum wall label for a Chaïm Soutine painting',
 84:'photo — bench', 85:'photo — people by a tree', 86:'photo — two people',
 87:'photo — street', 89:'photo — plate of food', 90:'photo — octopus',
 91:'photo — dining room', 92:'photo — people at a table', 94:'photo — cheese counter',
 102:'photo — street', 108:'photo — garden', 109:'photo — roof tiles', 117:'photo — palm tree',
 118:'photo — cooking', 119:'photo — sky', 122:'photo — two people', 143:'photo — two people',
 150:'photo — beach', 171:'photo — carousel', 183:'photo — handwritten recipe page',
 193:'photo — tea table', 194:'photo — table', 223:'photo — agaves', 271:'photo — two people',
 301:'photo — hay bales', 306:'photo — kitchen', 333:'photo — many works on a counter',
 # other artists' paintings, photographed in their frames at a museum
 235:"another artist's painting (museum, gilt frame)",
 236:"another artist's painting (museum, gilt frame)",
 237:"another artist's painting (museum, gilt frame)",
 # several works in one photograph — can't be sold or shown as a single piece
 147:'composite — two works already catalogued', 300:'composite — five ink drawings',
 321:'composite — small paintings on a table', 322:'composite — small paintings on a table',
}

PRINTS   = {184,185,186,187,188,189,190,191}
DRAWINGS = {287}
COLLAGE  = {192,231,232,238,239,240,241,245,249,250,251,252,258,259,260,261,266,268,270,
            272,273,274,275,277,279,280,283,289}

# Painting sub-series
P_MARKET     = {195,196,197,198,199,206,209,211,220,255,256,257,281}
P_BOTANICAL  = {203,222,225,226,227,228,229,230,242,246,247,253,254,263,267,278,282,302,303,
                304,305,309,310,311,317,318,320,323,325,326,327,328,329,330,331,332}
P_TREES      = {202,205,214,218,221,233,234,248,262,264,276,296,298,312,313,314,315}
P_MAINE      = {284,285,286,288,290,291,292,293,294,295,297}
P_FLORIDA    = {265}
P_STUDIES    = {215,219,224,244,319}
# everything else painted -> "landscapes" (place not recorded, so we don't claim one)

TITLES = {
 265:"Burlington Avenue North Corner", 281:"Capelain à la Tienda «Esclat»",
 282:"Spring Fronds", 285:"25 White Spruce Road", 286:"Breezy Hillside",
 289:"Acadia", 291:"Southwest Harbor", 292:"Mount Desert Island",
 293:"Schoodic Peninsula", 294:"Bar Harbor", 295:"Trees in the Breeze, Acadia",
 255:"Sardines et Rougets", 256:"Les Poissons", 257:"Les Poissons sur Glace",
}
PLACES = {
 265:("St Petersburg, Florida","February 2019"), 281:("Spain","July 2018"),
 282:("","2024"), 289:("Acadia, Maine",""), 291:("Southwest Harbor, Maine",""),
 292:("Mount Desert Island, Maine",""), 293:("Schoodic Peninsula, Maine","2024"),
 294:("Bar Harbor, Maine",""), 295:("Acadia, Maine","2024"),
}
