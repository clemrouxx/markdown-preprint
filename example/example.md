---
title: Example file for easy creation of a LaTeX file from Markdown
date: Today's date !!!
packages:
  - braket
author: clemrouxx (ETH Zürich)
---

> [!abstract]
> This paper show a fairly minimal example of file that can be transcompiled from Markdown to LaTeX and eventually to PDF, in the general style of a preprint. Although the style can be personalized using imported or custom LaTeX packages, this project has the advantage of implementing ways to label, reference and cite inside of the markdown file, in addition to other features, such as writing the abstract just as a modified quote (a "callout" in Obsidian terms).

# Goals
We try to provide a markdown to LaTeX program oriented towards scientific articles or preprints. We give ourselves the following guidelines :
- The user should have as little LaTeX code to write as possible
- But : it should still be feasible to customize the output style to a certain extent
- The Markdown file should still be readable
- The user shouldn't have to memorize some too specific syntax
- Ideally, it should look nice in Obsidian, and be consistant with its parsing

# Examples
## Modification of basic features

In our program, all inserted images will be transformed into Figures. As such, the program expects a label (just after the image, preceded with a "^"), and a caption (A paragraph of text just after the label and a line break). The usual prefix "fig:" for the label will be added automatically.

![](ducks.png)
^ducks
Enjoy this public-domain picture of ducks I found, as an example.

A similar modification happens for tables.

## New features

Here is a list of new features allowed by this syntax :
- References ! For this, just surround your label with \*\* ! For example, see Figure **fig:ducks**. (NB : For this to work, your label must include ":". If it doesn't, add one in front of the label in your reference).
- Labeled equations ! See for example equation **eq:coffee**.$$\hat{H}_{\text{int}}=\chi\int _{V}\ket{e} \bra{g} \otimes \hat{a}(\vec{r})d^{3}\vec{r}+\text{h.c.}$$^coffee
- Citations ! They work with an external .bib file that has to be named "bibliography.bib". You can cite any paper present in this file by preceding the reference key with an "@". Just like this : @Einstein.
- Additionnal information in a YAML header, which allows you to precise things like title, author(s), date, additionnal LaTeX packages... and more maybe in the future
$$\sum_{k}=b_{k}$$