# Methods followed in this study

All the code in this application is meant to obtain information from [PokéAPI](https://pokeapi.co/), and then organize it so it can be graphically displayed on a webpage. The nature of said analysis must be known in order to understand how the app is made and why. This document serves that purpose.

## 1. What counts and what doesn't

The goal of this program is to show the availability of different Pokémon a trainer can choose for their team on a normal game of the main series. For that matter, the **diversity** of each type is considered the most important factor, since well-balanced teams should have Pokémon of different types so they can face rivals of any type with at least one of their members.

It is also assumed that a player will aim to evolve their Pokémon as much as possible, to make them the strongest they can be. For that reason, Pokémon that are not fully evolved are considered an *"unfinished"* version of themselves and their types are not counted. In other words, only last evolutions are counted.

Most evolution lines keep the same types through all their members, or they just add a secondary type to what previously was a *mono-type* Pokémon, which is also considered to be the ultimate form that must be counted. Only a few Pokémon loose one of their types upon evolving (for example, Nincada is Bug/Ground and evolves to Ninjask and Shedinja, none of which keep the Ground type). This small error is accepted and ignored.

### Pokémon with differently-typed forms

Pokémon that have different forms also have different entries in the PokéAPI for each of them, and these entries specify which one is considered the *"default"* form. Only these default forms are counted, which excludes regional forms, Mega Evolution, Dynamax, Gigantamax and other battle-only forms, as well as varieties other than the default one.

I agree with the API's choice on which is the default form in most cases, based on what form they take in the wild or when initially obtained by the player through capture or evolution, without the use of any special method to change it. In the select cases where there's ambiguity enough to not consider any form more *default* than the others, the Pokémon is manually tagged **"without default form"** and it's not counted at all.

### Region-only Pokémon

Although I'm not counting regional forms, I am counting those that are unique but can only evolve from regional forms, such as Perrserker or Obstagoon. In those cases, they are manually tagged **"region-only"**, meaning they are only counted for the generation that corresponds to their region.

### Pre-evolutions from region-only Pokémon

In generations where regional forms exist, those that evolve in the previously mentioned *region-only* Pokémon also have their usual, default form that can be obtained in every generation. These forms are considered fully-evolved, and are counted for every generation (even where their regional form exists, since the default form can usually be obtained there too). For that purpose, they are manually tagged **"special"**.

### Pre-evolutions existing prior to their evolutions being introduced

Many Pokémon used to be fully-evolved until the coming of later generations, when new evolutions were created for them. For example, Magneton used to be a last evolution until the introduction of Magnezon at the 4th generation. In order for them to be properly counted, they are manually tagged *temporary*, and are counted in those generations prior to the ultimate evolution being added.

## 2. Collecting and processing data

When the app starts, it requests a list of all Pokémon and searches for last evolutions, listing them in a "source" file including their typings at each generation, among some other data. Then, it proceeds to the counting of selected species according to two different criteria: **generations** and **types**.

### a) Generations

In **generations**, the purpose is to obtain the types diversity among a single game generation. Species are counted only if they existed by that generation, and *region-onlies* are excluded unless they are from the generation's region.

The counting is made with two binary conditions: partial/strict and accumulated/not accumulated. Their combination results in 4 different files per generation.

"Partial" means that, for a given type, species are counted if they have the type, regardless of them being dual-typed or not. For example, Venusaur is counted for grass type, even if it's also poison type (and vice-versa). On the other hand, in "strict", species are counted only if their typing exactly matches the one that is being studied, so Venusaur would only be counted for grass/poison typing.

"Accumulated" means that Pokémon from previous generations are considered and counted, since (most of the time) they are still available. Non-accumulated files only consider Pokémon belonging to the generation of study.

### b) Types

In **types**, the aim is to see how the abundance of each type changes with time, so files are created with a count of species of the given type at each generation. Existence by the given generation and *region-only* condition are still considered. Since the different type combinations are too high, and because the counts of dual types barely add up until multiple generations pass, only single types are considered in this case. This means only the "partial" counting mode is used. However, the "accumulated or not" condition is still applied, resulting in 2 different files for each type.

---

To sum up and clarify, let's consider the next examples: generation 2 and steel type.

There will be 4 files for generation 2: `gen_2_partial.json`, `gen_2_strict.json`, `gen_2_partial_accumulated.json` and `gen_2_strict_accumulated.json`. In gen_2_partial_accumulated, Magneton adds a point for electric and steel types, while in gen_2_strict_accumulated it only adds a point for electric/steel typing (types order is indifferent). In the non-accumulated versions, it doesn't add anything at all, since it belongs to the previous gen.

Steel type will have 2 files: `steel.json` and `steel_accumulated.json`. In the first one, the count for generation 1 will be 0, since such type didn't exist yet, while the count for generation 2 will include Forretress, Steelix, Scizor and Skarmory, adding up to 4. In the accumulated version, Magneton will also be included in the generation 2 count, increasing it to 5.

###

## 3. Statistic calculations