Ooooo. Website.
===============

What Works
----------

All the main views - home page, subject list, subject index, section
including displaying comments.

What Doesn't
------------

Templates are incomplete / non-existent.

Comments cannot be added. Comments jQuery code is incomplete.

The timestamp format used for comments needs to be changed.

Paragraphs reference their sections by ForeignKey on id column of sections
table. It's inconvenient to add paragraphs this way - the section ids are
less transparent than, say, a composite key on the section's subject name
and short (url) name. Don't know whether it's better to change the key, or
add paragraphs using some new interface..

No tests have been written.

Routing URLs with trailing slashes is not working -
/subjects goes to the subjects page, while
/subjects/ gives 404.

Probably other stuff.
