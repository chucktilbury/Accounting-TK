# Accounting
Simple accounting software for Chuck's musical instrument manufacturing business.

This software is a first try at a very simple accounting system. It does
double entry and keeps track of customers and vendors. It tries to save typing
as much as possible by directly importing transactions directly from PayPal using 
the CSV download capability.

The idea of this software is for the system to be as simple as possible so
that it takes as little time to use as possible. There are no fancy special
purpose features to complicate matters. Just the basic things needed to
track the contacts and money.

The software is implemented using Python3 and Tkinter for the GUI. The
database is implemented with Sqlite3. No internet connection is required.
Only a single simultaneous user is supported.

This document covers the design of the software, not the database or the
business structure. The design of the business, including the database, 
is covered in 'business.md'.

