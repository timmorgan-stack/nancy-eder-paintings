#!/usr/bin/env python3
"""Classification of the 'Art and Pottery' drop (170 images), done by eye from contact sheets.
EXCLUDE = photographs of places/food/products/studio, and one composite duplicate.
Everything else is catalogued. Titles in TITLES were read off the artist's own captions."""

EXCLUDE = {
  6:'photo — cheese counter', 15:'photo — sky', 27:'photo — arch and bench',
  46:'photo — studio desk (kept as a site asset, not a gallery work)',
  49:'composite photo — duplicates 85 and 108',
  76:'photo — rooftops', 91:'photo — gate', 98:'photo — building', 111:'photo — garden gate',
  119:'photo — cards on a market table', 120:'photo — packaged card sets',
  131:'photo — yellow building', 133:'photo — market fruit', 136:'photo — bench',
  137:'photo — street', 139:'photo — plate of food', 140:'photo — octopus',
  145:'photo — rooftop view', 149:'photo — garden', 150:'photo — roof tiles',
  157:'photo — palm tree', 167:'photo — carousel',
}

POTTERY  = {18,34,41,45,51,62,65,95,97,104,110,134}
PRINTS   = {107,118,121,122}
COLLAGE  = {158,159,160}

# Pen-and-ink line drawings (includes the bold brush-ink studies 161-163)
DRAWINGS = {2,4,5,7,9,11,13,16,17,19,20,21,22,23,25,30,35,37,38,48,50,54,56,57,59,60,61,63,64,
            66,67,68,69,70,71,72,74,75,78,79,80,87,89,93,94,96,101,102,105,106,115,116,123,125,
            129,130,132,141,142,143,144,146,147,148,151,152,153,154,155,156,161,162,163,168}

# Drawing sub-series
D_MARKET = {4,38,56,66,68,143,156}
D_TREES  = {5,7,22,30,61,67,75,78,79,102,105,106,115,123,151,153,161,162,163}

# Painting sub-series (everything not in the above sets is a painting)
P_FLORIDA   = {85,108}
P_BOTANICAL = {1,3,10,14,24,26,31,32,39,40,43,44,47,52,53,77,84,109,114,164,165,166,171}
P_MARKET    = {8,42,170}
P_STUDIES   = {12,28,29,55,83,92,112,113,117,138}

TITLES = {
 2:"The Garden Fence", 4:"Fromage at the Market", 5:"Imaginary Forest",
 7:"In the Still of the Woods", 11:"Morning Walk", 13:"Flamingo Gardens, Davie",
 16:"Mayfair, Florida", 20:"Chez Mioche", 21:"Recyclables", 22:"Up in the Branches",
 30:"Striped Grass", 35:"Oak Bluffs, Martha's Vineyard", 37:"Brandon Street, Seattle",
 38:"Sardines for Dinner", 48:"Bedroom View", 50:"Snack Bar, Plantation Gardens",
 52:"Happy New Year", 54:"Barn Beyond the Garden", 56:"Sardines",
 57:"Road from Figueres", 59:"View from the Lido Parking Lot", 60:"Backyard Tomatoes",
 61:"Trees at the Dump", 63:"One Way Up", 64:"The Cypress in Céret",
 66:"Sardines from Auchan", 67:"Aubergine Tulips", 68:"Bar Fish at Auchan",
 69:"View from the Bedroom", 70:"The Dentist's Jardin", 71:"Avenue of Les Cigales",
 74:"Path to the Recyclables", 75:"Home in the Trees", 78:"Into the Woods",
 82:"Rooftop View", 85:"Lakeland, Florida", 94:"Goat and Pig House",
 96:"The Dentist's House", 99:"La Playa en L'Escala", 101:"View from the Rooftop Terrace",
 102:"Oakleaf Hydrangea", 105:"Goat House in the Trees", 106:"Street Plane Trees",
 107:"Run, Rabbit, Run", 108:"Hollis Garden Cabbage", 115:"Chestnut Tree Leaves",
 118:"It's Only a Paper Moon", 121:"Rabbits in the Reeds", 122:"Rabbits and Fishes",
 124:"Recyclables", 125:"The Little House", 126:"Céret Hotel", 128:"Road to Banyuls",
 129:"Backyard View", 130:"View from the Bedroom", 141:"A Day in Céret",
 142:"Road to Perpignan", 143:"Merlu on Sale", 144:"Rooftop Terrace View of Fields",
 146:"Roof Terrace View", 147:"View from the Rooftop", 148:"The Town Wall",
 151:"Chestnut Tree Leaves", 152:"The Dentist's Garden Wall", 153:"Town Trees in Summer",
 154:"Town Street, Céret", 155:"Francis & Helen's Pool House",
}

# place / date read from captions where the artist wrote one
PLACES = {
 13:("Davie, Florida",""), 16:("Florida",""), 35:("Oak Bluffs, Martha's Vineyard",""),
 37:("Seattle","May 2011"), 50:("Plantation Gardens, Florida",""), 57:("Figueres, Spain",""),
 64:("Céret, France",""), 67:("","May 2021"), 85:("Lakeland, Florida",""),
 99:("L'Escala, Spain",""), 102:("","May 2021"), 125:("","May 2021"),
 126:("Céret, France",""), 128:("Banyuls, France","July 2023"), 141:("Céret, France",""),
 142:("Perpignan, France",""), 154:("Céret, France",""),
 155:("Espagne","2022"),
}
