# FUTURE FEATURES

- Add support for verbs as independent entities
- Update Word transformer and check anki integration
- Batching?

- Support verb-form cards:

User wants to study specific verb forms, however the current card model is not suitable for this task

word -> verb form
language
definition
category
usage
frequency_rank
sentence
partial_sentence

The verb form cards will be available for Italian, French

The easiest solution would be to add some "flag" to our csv structure, and check that so we proceed to a regular card or jumpt to
the verb-form one

Example

parlo,it,verb,context,thense,person

Parlo
it
....
verb
informal
...
Io parlo con lei
Io ... con lei

---

Card:

Present - firts person - parlare
Emetere sonido per comunicarsi

Io ... con lei

Io parlo con lei

---

I could use the same endpoint or build a new one

- Changes: Response_Interface, Language_Service, Row_Model
