#!/usr/bin/env python3
"""Regenerate data/catalog.js from data/catalog.json (run after editing the catalogue)."""
import os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data=open(os.path.join(root,'data/catalog.json')).read()
open(os.path.join(root,'data/catalog.js'),'w').write('/* Generated from data/catalog.json — regenerate with: python3 tools/build_catalog_js.py */\nwindow.NE_CATALOG = '+data+';\n')
print('data/catalog.js written')
