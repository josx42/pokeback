# Methods followed in this study

All the code in this application is meant to obtain information from [PokéAPI](https://pokeapi.co/), and then organize it so it can be graphically displayed on a webpage. The nature of said analysis must be known in order to understand how the app is made and why. This document serves that purpose.

## What counts and what doesn't

The goal of this program is to show the availability of different Pokémon a trainer can choose for their team on a normal game of the main series. For that matter, the **diversity** of each type is considered the most important factor, since well-balanced teams should have Pokémon of different types so they can face rivals of any type with at least one of their members.

It is also assumed that a player will aim to evolve their Pokémon as much as possible, to make them the strongest they can be. For that reason, Pokémon that are not fully evolved are considered an *"unfinished"* version of themselves and their types are not counted. In other words, only last evolutions are counted.

Most evolution lines keep the same types through all their members, or they just add a secondary type to what previously was a *mono-type* Pokémon, which is also considered to be the ultimate form that must be counted. Only a few Pokémon loose one of their types upon evolving (for example, Nincada is Bug/Ground and evolves to Ninjask and Shedinja, none of which keep the Ground type). This small error is accepted and ignored.

## Pokémon with differently-typed forms

Pokémon that have different forms also have different entries in the PokéAPI for each of them, and these entries specify which one is considered the *"default"* form. Only these default forms are counted, which excludes regional forms, Mega Evolution, Dynamax, Gigantamax and other battle-only forms, as well as varieties other than the default one.

I agree with the API's choice on which is the default form in most cases, based on what form they take in the wild or when initially obtained by the player through capture or evolution, without the use of any special method to change it. In the select cases where there's ambiguity enough to not consider any form more *default* than the others, the Pokémon is manually tagged **"without default form"** and it's not counted at all.

## Region-only Pokémon

Although I'm not counting regional forms, I am counting those that are unique but can only evolve from regional forms, such as Perrserker or Obstagoon. In those cases, they are manually tagged **"region-only"**, meaning they are only counted for the generation that corresponds to their region.

## Pre-evolutions from region-only Pokémon

In generations where regional forms exist, those that evolve in the previously mentioned *region-only* Pokémon also have their usual, default form that can be obtained in every generation. These forms are considered fully-evolved, and are counted for every generation (even where their regional form exists, since the default form can usually be obtained there too). For that purpose, they are manually tagged **"special"**.