#!/usr/bin/env python3
"""Third drop — 52 files added alongside the others, named '... - N (1).jpeg'.
All 52 are new content (verified by perceptual hash), but two are re-photographs of works
already catalogued, caught by eye rather than by hash."""

EXCLUDE = {
 1:'composite — several prints laid out together',
 13:'re-photograph of b257 "Les Poissons sur Glace"',
 27:'re-photograph of b281 "Capelain à la Tienda Esclat"',
 42:'photo — worktable with glue, scissors and offcuts',
}
PRINTS   = {2}
DRAWINGS = {50}
# the rabbit series: linocut fragments cut up and collaged with gouache
RABBITS  = {3,4,5,6,7,8,9,10,35,36,37,38,39,40,43,44,45,46,47,48,49}

P_CUBA    = {16,17,18,19,20,21}
P_SPAIN   = {23,26,30,32}
P_FRANCE  = {22,24,25,28,29}
P_MARKET  = {11,12,31,33,34}
P_BOTANY  = {41,51,52}
# 14, 15 -> landscapes

TITLES = {
 5:"Rabbits by the Stream", 7:"Rustling Rabbits in a Field of Waves",
 10:"Distractions for Rabbits", 11:"Pescados en el Mercado", 12:"Rap Blanc",
 18:"San Antonio", 21:"Hotel El Castillo, Baracoa", 23:"La Playa, Empúries",
 24:"Collioure", 26:"L'Escala, Empúries", 28:"St Cyprien", 29:"Céret Backyard",
 30:"The Beach at Empúries", 32:"La Piscine, Casa Mas Sant Nicolau",
 33:"L'Aubergine", 34:"Aubergine, Tomate et Ail", 38:"What's for Dinner, Rabbit?",
 39:"One Small Step", 40:"Run, Rabbit, Run!",
}
PLACES = {
 5:("","May 2019"), 7:("","June 2017"), 10:("","April 2019"),
 11:("Spain","July 2017"), 12:("","August 2017"),
 18:("San Antonio, Cuba",""), 21:("Baracoa, Cuba",""),
 23:("Empúries, Spain","July 2018"), 24:("Collioure, France","July 2018"),
 26:("L'Escala, Spain","August 2018"), 28:("St Cyprien, France","July 2018"),
 29:("Céret, France",""), 30:("Empúries, Spain","August 2018"),
 32:("Spain","August 2018"), 33:("","August 2018"),
}
