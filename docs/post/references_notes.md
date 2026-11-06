# Citation check

Each source cited in `README.md` was checked on 6 November 2026 by Claude agents: the DOI and metadata against Crossref, arXiv or the proceedings page, whether the source supports the sentence that cites it (with the supporting passage quoted), and whether that was judged from the full text, the abstract only, or a secondary description. The post was then corrected to match; in particular, the opening no longer says dropout had never been tested (McGrath et al 2023 had found repair without it), and the dropout prediction is now presented as an extension of the insurance hypothesis, not part of it. Sentences quoted under "Post" are from the draft before correction.

## Results A: ecology references R1 to R9 (items 1 to 20)

Checked 6 November 2026. Metadata for all nine DOIs checked against Crossref (api.crossref.org/works/<doi>). All nine resolve to the cited work, and authors, year, title, journal, volume, issue and pages match the post's reference list.

## Summary table

| Item | Ref | Metadata OK | Support | Evidence level | Action needed |
|---|---|---|---|---|---|
| 1 | paine1966 | Yes | Yes | Full text (JSTOR scan, pp. 65–75, read page images) | None |
| 2 | paine1966 | Yes | Partly | Full text | Reword: Paine counted all species "inhabiting this area", including mobile animals, not only species "holding space"; barnacles spread first, then mussels |
| 3 | paine1966 | Yes | Partly | Full text | Reword: the starfish does eat some of the lost species (chitons, limpets); "keystone" is not in Paine 1966 |
| 4 | estes1974 | Yes | Partly (abstract level) | Abstract only (PubMed / Europe PMC); publisher blocked | Abstract says "herbivorous invertebrates" and "macrophyte associations", not urchins and kelp; check the full text, or use the abstract-safe wording |
| 5 | crooks1999 | Yes | Yes | Full text (4-page PDF) | None (optional precision edit offered) |
| 6 | crooks1999 | Yes | Yes | Full text | None |
| 7 | paine1992 | Yes | Partly | Abstract (nature.com) + Paine's formula as given in Power et al 1996 (full text) | Reword: Paine's measure is per individual of A (change divided by A's density) |
| 8 | hedges1999 | Yes | No | Abstract (OSTI) + secondary; full text blocked by publisher | Reword: the ratio is treatment over control, not after over before |
| 9 | hedges1999 | Yes | Yes (via secondary) | Abstract + secondary citing the paper | None; the exact wording in Hedges et al was not seen |
| 10 | shurin2002 | Yes | Partly | Full text (author-hosted PDF) | Reword: "field experiments that manipulated predators" (6 were natural experiments), the pattern held in every system except streams, and the paper says cascades "often" weaken |
| 11 | shurin2002 | Yes | Partly | Full text | Add "often" |
| 12 | power1996 | Yes | Yes | Full text (Mills lab PDF, read page image for formula) | None; quotation exact |
| 13 | power1996 | Yes | Yes | Full text | None |
| 14 | power1996 | Yes | Partly | Full text | Reword: the paper gives 1 or −1, and a keystone has an absolute value much greater than 1 |
| 15 | power1996 | Yes | Yes | Full text | None; quotation exact apart from capital "N", and the omitted text does not change the meaning |
| 16 | power1996 | Yes | Yes | Full text | None; formula matches |
| 17 | power1996 | Yes | Yes | Full text | None |
| 18 | yachi1999 | Yes | Yes | Full text (PMC15485) | None |
| 19 | yachi1999 | Yes | No | Full text | Reword: the paper does not say that variable conditions produce redundancy |
| 20 | odum1969 | Yes | Partly | Full text of a published Spanish translation + English reproduction of Odum's Table 1 (Corman et al 2019); English original not read | Reword: Odum's terms are "homeostasis" and "stability (resistance to external perturbations)"; say "predicted" |

**The 15-to-8 count (flagged in the claims file):** Paine 1966 alone confirms it. Page 70: "The removal of *Pisaster* has resulted in a pronounced *decrease* in diversity, as measured simply by counting species inhabiting this area, whether consumed by *Pisaster* or not, from a 15 to an eight-species system." The 1963 start is also in Paine 1966: "Since June, 1963, a 'typical' piece of shoreline at Mukkaw Bay ... has been kept free of *Pisaster*." The 15 are the species Paine lists for the lower shore on the same page. They include chitons, limpets and a nudibranch, which move about and are not space holders, so the post's "species holding space" does not describe what was counted.

---

## R1. paine1966 (items 1 to 3)

**Metadata.** Crossref: Paine, "Food Web Complexity and Species Diversity", The American Naturalist 100(910):65–75, 1966. Matches.

**Evidence.** Full text. I read the JSTOR scan (https://userpages.umbc.edu/~rostamia/math481/1966-diversity-paine.pdf; a second copy is at faculty.fiu.edu) as page images, pp. 66–71.

**Item 1.** "In 1963 Robert Paine began removing the predatory starfish *Pisaster ochraceus* from a stretch of rocky shore at Mukkaw Bay, Washington." **Yes.**
- p. 70: "Since June, 1963, a "typical" piece of shoreline at Mukkaw Bay about eight meters long and two meters in vertical extent has been kept free of *Pisaster*."
- p. 66: "as observed at Mukkaw Bay, near Neah Bay, Washington (ca. 49° N latitude) ... *Pisaster ochraceus*, a starfish".

**Item 2.** "Mussels, which the starfish had been eating, spread over the rock, and the number of species holding space on it fell from fifteen to eight ([Paine 1966](#references))." **Partly.**
- The count is right: p. 70: "The removal of *Pisaster* has resulted in a pronounced *decrease* in diversity, as measured simply by counting species inhabiting this area, whether consumed by *Pisaster* or not, from a 15 to an eight-species system."
- The starfish does eat mussels: p. 67: "on a nutritional (calorie) basis, barnacles are only about one-third as important to *Pisaster* as either *Mytilus californianus*, a bivalve, or the browsing chiton *Katherina tunicata*."
- Two problems:
  1. **What was counted.** Paine counted "species inhabiting this area". These are the 15 species he lists on p. 70: three in the mid-shore band (*Mytilus*, *Balanus cariosus*, *Mitella*), plus "*B. glandula* as scattered clumps, a few anemones of one species, two chiton species (browsers), two abundant limpets (browsers); four macroscopic benthic algae ..., and the sponge *Haliclona*, often browsed upon by *Anisodoris*, a nudibranch". That makes 3 + 1 + 1 + 2 + 2 + 4 + 1 + 1 = 15. Chitons, limpets and the nudibranch move about. They are not "holding space".
  2. **The order of events.** Barnacles came first, then mussels and goose barnacles. p. 70: "Following the removal of *Pisaster*, *B. glandula* set successfully throughout much of the area and by September had occupied from 60 to 80% of the available space. By the following June the *Balanus* themselves were being crowded out by small, rapidly growing *Mytilus* and *Mitella*. ... eventually the experimental area will be dominated by *Mytilus*". This is a small simplification. Barnacles are also starfish prey (p. 67: "both major predators consuming them in quantity").
- **Proposed:** "Barnacles and then mussels, both of which the starfish had been eating, spread over the rock, and the number of species living there fell from fifteen to eight ([Paine 1966](#references))."

**Item 3.** "The starfish ate few of the species that disappeared; its effect on them went through the mussel, which is what makes it a keystone." **Partly.**
- Paine supports an indirect effect for some of the lost species. p. 70: "the sponge-nudibranch food chain has been displaced, and the anemone population reduced in density. Neither of these carnivores nor the sponge is eaten by *Pisaster*, indicating that the number of food chains initiated on this limited space is strongly influenced by *Pisaster*, but by an indirect process." On the algae, p. 70: "The benthic algae either have or are in the process of disappearing with the exception of the epiphyte, due to lack of appropriate space".
- But "ate few of the species that disappeared" is doubtful. Chitons and limpets also left (p. 70: "the chitons and larger limpets have also emigrated, due to the absence of space and lack of appropriate food"), and they are starfish prey. Fig. 1 (p. 67) shows *Pisaster* eating chitons (2 spp.) and limpets (2 spp.), and p. 67 says a chiton is one of its two most important foods by calories.
- The space was taken by barnacles and goose barnacles as well as mussels, not by "the mussel" alone.
- The word "keystone" does not appear in Paine 1966. Power et al 1996 (p. 609) date it to "the original usage of Paine (1969), in which keystone referred to a species that preferentially consumed and held in check another species that would otherwise dominate the system." Paine 1969 is not in the bibliography, but Power et al 1996 is, and it supports the term.
- **Proposed:** "Several of the species that disappeared, such as the seaweeds, the sponge and the sea slug that fed on it, are not eaten by the starfish; its effect on them was indirect, through the barnacles and mussels that took their space. Ecologists call a predator like this, one that holds in check a species that would otherwise take over, a keystone ([Power et al 1996](#references))."

## R2. estes1974 (item 4)

**Metadata.** Crossref: Estes & Palmisano, "Sea Otters: Their Role in Structuring Nearshore Communities", Science 185(4156):1058–1060, 1974. Matches.

**Evidence.** Abstract only, from Europe PMC (PMID 17738247). science.org returned 403 and the USGS page returned 403. The author's publication page (werc.ucsc.edu) refused connections, and I found no other open copy.

**Item 4.** "Sea otters, the sea urchins they eat, and the kelp the urchins eat form the same kind of chain ([Estes & Palmisano 1974](#references))." **Partly, at the abstract level.**
- Abstract, in full: "A comparison of western Aleutian Islands with and without sea otter populations shows that this species is important in determining littoral and sublittoral community structure. Sea otters control herbivorous invertebrate populations. Removal of sea otters causes increased herbivory and ultimately results in the destruction of macrophyte associations. The observations suggest that sea otter reestablishment indirectly affects island fauna associated with macrophyte primary productivity."
- The chain (otter, then plant-eating invertebrate, then large seaweed) is supported. The abstract does not name sea urchins or kelp. Search snippets of secondary sources (for example Watt et al 2000, citing this paper) describe the prey as "principally sea urchins, *Strongylocentrotus* spp." I did not read those sources, so I could not confirm urchins and kelp in the paper's own text.
- **Action:** have someone with Science access confirm "sea urchins" and "kelp" in the paper. If nobody can, use this sentence: "Sea otters, the plant-eating invertebrates they eat, and the kelp and other large seaweeds those invertebrates eat form the same kind of chain ([Estes & Palmisano 1974](#references))."

## R3. crooks1999 (items 5 and 6)

**Metadata.** Crossref: Crooks & Soulé, "Mesopredator release and avifaunal extinctions in a fragmented system", Nature 400(6744):563–566, 1999. Matches.

**Evidence.** Full text: a 4-page scan of the Nature article hosted at originalwisdom.com, with the text extracted.

**Item 5.** "An example of mesopredator release comes from fragmented scrub near San Diego, where canyons that had lost their coyotes held more domestic cats, raccoons and foxes, and fewer species of scrub-breeding birds ([Crooks & Soulé 1999](#references))." **Yes.**
- p. 563: "In coastal southern California, intensive urbanization over the past century has destroyed most of the native sage-scrub habitat, leaving undeveloped steep-sided canyons as habitat islands in an urban sea." p. 565: "residents bordering the San Diego fragments".
- p. 563: "Coyote populations have declined or disappeared from some fragments"; "Total mesopredator abundance ... was higher in fragments with fewer coyotes; coyote abundance had the strongest negative relationship with grey fox, cat and opossum abundance"; "Coyote presence had the strongest negative effect on domestic cat, opossum and raccoon abundance".
- p. 563: "As predicted, scrub bird diversity was higher in fragments where coyotes were either present or more abundant".
- Note: foxes track coyote *abundance*, and raccoons track coyote *presence* (the presence model for raccoons has P = 0.068 in Table 1c). The design compares fragments, so "canyons with few or no coyotes" is slightly more exact than "canyons that had lost their coyotes". This edit is optional: "...where canyons with few or no coyotes held more domestic cats, raccoons and foxes, and fewer species of scrub-breeding birds".

**Item 6.** "Ecologists call this *mesopredator release*: when a top predator is removed, smaller predators increase." (no link) **Yes.**
- p. 563: "Mammalian carnivores are particularly vulnerable to extinction in fragmented landscapes, and their disappearance may lead to increased numbers of smaller carnivores that are principle predators of birds and other small vertebrates. Such 'mesopredator release' has been implicated in the decline and extinction of prey species".

## R4. paine1992 (item 7)

**Metadata.** Crossref: Paine, "Food-web analysis through field measurement of per capita interaction strength", Nature 355(6355):73–75, 1992. Matches.

**Evidence.** Abstract from nature.com. The full text is paywalled and I found no open copy. The formula comes from Power et al 1996 (full text read), whose authors include Paine.

**Item 7.** "**Interaction strength.** The effect of species A on species B, measured by removing A and recording the change in B ([Paine 1992](#references))." **Partly.**
- Abstract: "I report here the first experimental study designed to estimate interaction strengths in a species-rich herbivore guild, documenting on a per capita basis mainly weak or positive interactions, and a few strong interactions". The abstract also says "empiricists have usually determined relative interaction strength from single-species removals".
- Power et al 1996, p. 610: "Paine's interaction strength (Paine 1992) was computed as [(t_N − t_D) / t_D] (1/n), where t_N is the abundance of the prey in the presence of the consumer, t_D is prey abundance in the absence of the consumer, and n is the number of consumer individuals stocked in experimental arenas." Also: "whereas Paine's measure is a per capita effect".
- The post's definition leaves out the per capita part (dividing by the number of A), which is the point of the paper's title.
- **Proposed:** "**Interaction strength.** The effect of species A on species B, measured by comparing B with and without A; [Paine 1992](#references) divided the change by the number of A present, giving an effect per individual."

## R5. hedges1999 (items 8 and 9)

**Metadata.** Crossref: Hedges, Gurevitch & Curtis, "The meta-analysis of response ratios in experimental ecology", Ecology 80(4):1150–1156, 1999. Matches.

**Evidence.** Abstract (OSTI record 355567). The Wiley/ESA full text returned 403, and I did not try to get around it. A secondary source cites the paper for item 9. Shurin et al 2002 (full text) uses the measure and cites this paper.

**Item 8.** "**The log response ratio.** The logarithm of a quantity, such as a population's density, after a treatment divided by before." **No.**
- OSTI abstract: the response ratio is "the ratio of mean outcome in the experimental group to that in the control group".
- Shurin et al 2002, p. 786, citing Hedges et al 1999: "The effect size of predator manipulations was measured as the log ratio of plant and herbivore density in the presence and absence of predators".
- The ratio is treatment over control, not after over before. (The post's own use, ablated over intact, is a treatment-over-control comparison, so the fix is only to the wording.)
- **Proposed:** "**The log response ratio.** The logarithm of a quantity, such as a population's density, under a treatment divided by the same quantity in an untreated control."

**Item 9.** "It treats an increase and a decrease of the same proportion equally ([Hedges et al 1999](#references))." **Yes, through a secondary source.**
- arXiv 2402.16375, footnote 22, citing Hedges et al 1999: "Logarithm transformation linearizes the RWTP metric so that deviations in the numerator and denominator have the same impact (Hedges et al., 1999)."
- I did not see the paper's own sentence. No change needed, but the evidence level is secondary.

## R6. shurin2002 (items 10 and 11)

**Metadata.** Crossref: Shurin et al (8 authors, as listed), "A cross-ecosystem comparison of the strength of trophic cascades", Ecology Letters 5(6):785–791, 2002. Matches.

**Evidence.** Full text: https://blanchet.grit.ucsb.edu/pdfs/Shurin-etal2002.pdf (co-author Blanchette's site).

**Item 10.** "**Attenuation.** Across 102 predator-removal experiments, a predator's effect on the animals it eats was larger than its effect on the plants those animals eat: cascades weaken with each step down the food chain ([Shurin et al 2002](#references))." **Partly.**
- Abstract: "We compared the responses of herbivore and plant communities to predator manipulations in 102 field experiments in six different ecosystems ... Predator effects on herbivores were generally larger and more variable than on plants, suggesting that cascades often become attenuated at the plant–herbivore interface."
- p. 786: "Five of the marine benthic studies, and one of the lentic benthic studies, were 'natural experiments' where the observers did not manipulate the predators directly." So not all 102 were removals.
- p. 789: "The smaller response by plants than herbivores in every system except streams indicates that the effects of predators often become attenuated as they are transmitted to lower trophic levels."
- The number 102 is right. But "predator-removal experiments" is not exact, the pattern did not hold in streams, and the paper says "often". The paper measures two levels (herbivores and plants), so "with each step" claims more than one step can show.
- **Proposed:** "**Attenuation.** Across 102 field experiments that compared communities with and without predators, a predator's effect on the animals it eats was usually larger than its effect on the plants those animals eat (in every type of ecosystem except streams): the effect of a predator often weakens as it passes down the food chain ([Shurin et al 2002](#references))."

**Item 11.** "**The effect of a removal shrinks with distance.** Removing one group of heads changed the heads that read its output more than the heads one step further on, in all three steps tested, as ecologists find along food chains." **Partly.** The source says "often" (quotes above).
- **Proposed:** "...in all three steps tested, as ecologists often find along food chains."

## R7. power1996 (items 12 to 17)

**Metadata.** Crossref: Power, Tilman, Estes, Menge, Bond, Mills, Daily, Castilla, Lubchenco, Paine, "Challenges in the Quest for Keystones", BioScience 46(8):609–620, 1996. Matches.

**Evidence.** Full text: https://umt.edu/mills-lab/files/2015/01/powerchallenges96.pdf (co-author Mills's lab). I read p. 610 as a page image to confirm the formula's subscripts.

**Item 12.** Quotation "whose impact on its community or ecosystem is large, and disproportionately large relative to its abundance". **Yes; exact.** p. 609: "To better reflect its current use, we define a keystone species as one whose impact on its community or ecosystem is large, and disproportionately large relative to its abundance."

**Item 13.** "Their measure is the proportional change in a property of the community when the species is removed, divided by the species' share of the community." **Yes.** p. 610: "CI_i = [(t_N − t_D)/t_N] (1/p_i) where t_N is a quantitative measure of the trait in the intact community or ecosystem, t_D is the trait when species i has been deleted, and p_i is the proportional abundance of species i before it was deleted." p. 609: "p is the proportional abundance (in most cases, proportional biomass relative to the total biomass of all other species in the community)".

**Item 14.** "A species whose effect matches its share scores 1; a keystone scores well above 1." **Partly.** p. 610: "If a species has an effect in direct proportion to its abundance, CI_i would be 1 (if, after the species deletion, the community or ecosystem characteristic decreased) or −1 (if the characteristic increased). If species i is a keystone, the absolute value of CI_i is much greater than 1." The post itself uses |CI| ≥ 2 and discusses negative CI, so the sentence should include the sign.
- **Proposed:** "A species whose effect matches its share scores 1, or −1 if the property rises when it is removed; a keystone scores well above 1 in absolute value."

**Item 15.** Quotation with ellipsis. **Yes.** Figure 1 caption, p. 610: "Negative values occur when a community characteristic increases after removal of a species, as would be the case if the characteristic were the abundance of another species and the first species were a consumer of that species." The ellipsis leaves out "the characteristic were the abundance of another species and" and "of that species". The post's own wording ("a species that consumes the measured property") covers this, so the meaning is kept. The source has a capital "N" because the quotation starts a sentence there; lower case is fine mid-sentence. This passage is in a figure caption.

**Item 16.** Formula "CI_i = [(t_N − t_D) / t_N] · (1 / p_i)". **Yes; matches** (p. 610, quoted under item 13). The post defines p_i as a head's share of the summed absolute direct effect, which corresponds to proportional abundance.

**Item 17.** "Ecologists call a species like this a *keystone*: its effect on its community is large compared with how common it is." (no link) **Yes.** Same p. 609 definition.

## R8. yachi1999 (items 18 and 19)

**Metadata.** Crossref: Yachi & Loreau, "Biodiversity and ecosystem productivity in a fluctuating environment: The insurance hypothesis", PNAS 96(4):1463–1468, 1999. Matches.

**Evidence.** Full text (PMC15485, HTML).

**Item 18.** "**The insurance hypothesis.** A community whose species respond differently to changing conditions keeps up its overall function better than one of identical species, because the loss of one is made up by the others ([Yachi & Loreau 1999](#references))." **Yes.**
- Abstract: "According to the insurance hypothesis, biodiversity insures ecosystems against declines in their functioning because many species provide greater guarantees that some will maintain functioning even if others fail."
- Introduction: "different species respond differently to environmental changes, hence the contribution of some species to ecosystem processes may decrease while that of others may increase when the environment changes. Thus greater species richness should lead to a decreased variability in ecosystem processes because of compensation among species."
- Results: "in the highly unlikely case when there is no asynchronicity at all in the species responses, the ecosystem behaves exactly as a single species."

**Item 19.** "It predicts that this redundancy is produced by variable conditions." **No.**
- The paper models how a community performs in a fluctuating environment. It does not predict that fluctuations produce redundancy. Its only statement about where the differences between species come from says the origin does not matter. Discussion: "The origin of asynchronicity of species responses does not matter; it can be generated in many ways, whether by competitive release, physiologically determined differences in the response to environmental fluctuations or purely stochastic effects."
- "Redundant" in the paper means a plateau in function as species are added: "we call an ecosystem redundant for some functional process if this process has attained a plateau for a lower value of species richness and is not enhanced by the addition of further species". What makes it redundant at lower richness is the variance of each species' response: "the greater the variance of the species responses, the lower the species richness at which the temporal mean of the ecosystem process saturates and the ecosystem becomes redundant." That variance is a property of the species, not something conditions produce.
- **Proposed:** "It describes the benefit of such a community when conditions vary; it does not say what produces the redundancy."
- **Knock-on effect, outside this item range:** two uncited sentences in the post depend on the unsupported reading and should be changed with it:
  - What I found: "and the insurance hypothesis made the one prediction about cause, which held."
  - Discussion: "That fits the insurance hypothesis: random loss of parts during training produces parts that can replace one another."
  - Neither is a claim Yachi & Loreau make. Suggested direction: present the dropout prediction as the author's extension of the insurance idea (for example, "I extended the insurance hypothesis to predict that random loss of parts during training would produce parts that can replace one another; that prediction held"). Do not attribute it to the hypothesis itself.

## R9. odum1969 (item 20)

**Metadata.** Crossref: Odum, "The Strategy of Ecosystem Development", Science 164(3877):262–270, 1969. Matches.

**Evidence.** I could not open the English original: Science and academia.edu blocked access and scispace was empty. I read:
- the full text of a published Spanish translation ("La estrategia de desarrollo de los ecosistemas", polired.upm.es, Boletín CFS);
- Corman et al 2019, *Ecosystems*, "Foundations and Frontiers of Ecosystem Science: Legacy of a Classic Paper (Odum 1969)" (par.nsf.gov/servlets/purl/10117615), whose Table 2 is "Recreated from Odum (1969)".

**Item 20.** "Ecologists expect communities to become more internally buffered as they mature ([Odum 1969](#references)), and that is the direction seen here." **Partly.**
- Corman et al 2019, Table 2, under "Overall homeostasis", developmental stage then mature stage: "20 Internal symbiosis Undeveloped Developed; 21 Nutrient conservation Poor Good; 22 Stability Poor Good".
- Spanish translation, Table 1: "22. Estabilidad (resistencia a las perturbaciones externas) Poca Mucha" ("Stability (resistance to external perturbations): little, much").
- Spanish translation, text: "la estrategia de sucesión como proceso a corto plazo es básicamente la misma estrategia de desarrollo evolutivo a largo plazo que se da en la biosfera —es decir, aumento de control sobre el entorno físico, o bien homeostasis con el mismo en el sentido de alcanzar un máximo de protección frente a posibles perturbaciones." Translation: "the strategy of succession as a short-term process is basically the same as the strategy of long-term evolutionary development in the biosphere, that is, increased control over the physical environment, or homeostasis with it, in the sense of achieving maximum protection against possible perturbations."
- The direction is supported. But "internally buffered" is the post's term: Odum's are homeostasis and resistance to *external* perturbations. Also, Corman et al report that the "overall homeostasis" predictions "were the least tested compared to total mentions", so "predicted" is more accurate than "expect".
- **Proposed:** "Ecologists have predicted that communities become more self-regulating and more resistant to disturbance as they mature ([Odum 1969](#references)), and that is the direction seen here."


## Citation check results B: machine-learning references R10 to R21 (items 21 to 60)

Post: /home/kevin/repos/trophic-cascade/docs/post/README.md (not edited).
Checked 6 November 2026. Sources were downloaded and converted to text; every quote below was copied from that text. Hyphenation and line breaks from the PDF extraction are joined.

Evidence levels:
- **Full text**: I had the whole paper and searched it for each claim, then read the passages around each hit and the sections the claim depends on. I did not read every page of every paper from start to finish.
- **README / code / model card**: the primary file itself.

## Summary table

| Item | Ref | Metadata OK | Support | Evidence level | Action needed |
|---|---|---|---|---|---|
| 21 | R10 wang2022 | Yes | Yes | Full text (arXiv v1) | None. "first described" is supported by McDougall et al (R15) |
| 22 | (R10, uncited) | – | **No** | Full text of McGrath et al and McDougall et al | **Reword.** McGrath et al say they "disprove" Wang et al's dropout hypothesis |
| 23 | R10 | Yes | Yes | Full text | None |
| 24 | R10 | Yes | Yes | Full text | None |
| 25 | R10 | Yes | Yes | Full text | Optional: add the word "heads" (clarity only) |
| 26 | R10 | Yes | Partly | Full text | **Reword.** The negative name movers also took part in the compensation (Wang et al Appendix F) |
| 27 | R10 | Yes | Yes (quote exact) | Full text | None |
| 28 | R10 | Yes | Yes | Full text | None |
| 29 | R10 | Yes | Yes | Full text | None |
| 30 | R10 | Yes | Yes | Full text | None |
| 31 | R10 | Yes | Yes (all 26 heads match Figure 2) | Full text | None |
| 32 | R10 | Yes | Yes | Full text | None |
| 33 | R10 | Yes | Yes | Full text | None |
| 34 | R10 | Yes | Yes | Full text | None |
| 35 | R11 radford2019 | Yes | Yes | Full text | None |
| 36 | R11 + uncited | Yes | Partly | Full text; HF config.json; OpenAI repo (cloned) | **Reword and add two links.** The facts are correct, but the sentence leaves out two things that matter |
| 37 | R12 elhage2021 | Yes | Partly | Full text (HTML) | **Reword.** The sum holds before the final LayerNorm rescaling |
| 38 | R12 | Yes | Yes | Full text (HTML) | None |
| 39 | R13 mcgrath2023 | Yes | Yes (quote exact) | Full text | None |
| 40 | R13 | Yes | Yes | Full text | None |
| 41 | R13 | Yes | Yes | Full text | None |
| 42 | R13 | Yes | Yes | Full text | None |
| 43 | R14 rushing2024 | Yes | Yes | Full text (arXiv v2) | None |
| 44 | R14 | Yes | Yes (quote exact) | Full text | None |
| 45 | R14 | Yes | Partly | Full text | **Reword.** The 30% is a rough figure measured in a different way, so "far below" claims too much |
| 46 | R14 | Yes | Yes | Full text | None |
| 47 | R14 | Yes | Yes | Full text | None |
| 48 | R14 | Yes | Yes | Full text | None |
| 49 | R15 mcdougall2024 | Partly | Yes | Full text (ACL version and arXiv v1) | **Fix the link.** The arXiv paper has a different title; link the ACL Anthology version |
| 50 | R15 | Partly (as above) | Yes | Full text | As item 49 |
| 51 | R16 tigges2024 | Yes | Partly | Full text (arXiv v2) | **Reword.** They say self-repair "seems plausible" as a cause; they do not attribute the stability to it |
| 52 | R16 | Yes | Yes | Full text | None |
| 53 | R16 | Yes | Yes | Full text | None |
| 54 | R17 rohweder2026 | Yes | Partly | Full text (arXiv v2) | **Reword (minor).** Their account also relies on representation geometry; they never mention dropout |
| 55 | R17 | Yes | The author's inference; the source does not contradict it | Full text | None |
| 56 | R18 heimersheim2024 | Yes | Yes | Full text | None |
| 57 | R19 zhou2020 | Yes | Yes | Full text (arXiv 2004.13342; text could not be extracted from the ACL PDF) + ACL abstract page | None |
| 58 | R20 eldan2023 | Yes | Yes | Full text | None |
| 59 | R20 | Yes | Partly | Full text + Hugging Face dataset page | **Reword or add a link.** The paper does not give "2.1 million"; the Hugging Face dataset does |
| 60 | R21 nanda2022 | Yes | Partly | README + HookedTransformer.py v3.9.0 source | **Reword.** The weight processing is not what makes the residual stream a sum |
| extra | GPT-2 dropout (uncited) | – | Correct | HF config.json; OpenAI src/model.py | Add links (see item 36) |

---

## R10. wang2022

**Metadata.** arXiv 2211.00593 resolves to "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small". Authors are Kevin Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris and Jacob Steinhardt (arXiv API); there is one arXiv version, v1, dated 1 Nov 2022. The paper was published at ICLR 2023 (iclr.cc/virtual/2023/poster/11341; mlanthology.org/iclr/2023/wang2023iclr-interpretability). The metadata is correct.
**Evidence:** full text of arXiv v1. The ICLR camera-ready may give slightly different numbers. One aggregator says it reports 28 heads where v1 reports 26. I did not open the camera-ready.

**Item 21** (dropout suggestion). Yes.
> "We hypothesize that this compensation phenomenon is caused by the use of dropout during training. Thus, the model was optimized for robustness to dysfunctional parts." (Sec. 3.4)

The description of dropout is fair. Wang et al do not describe dropout themselves; they cite nothing for it, and McGrath et al cite Srivastava et al 2014. Wang et al do not claim to be first, but McDougall et al (R15) support "first described": "we use the narrow Indirect Object Identification (IOI; Wang et al. (2023)) task to study self-repair, as this was studied in the GPT-2 Small model, and was the first known example of self-repair."

**Item 22** ("I could not find a test of that suggestion."). **No.** McGrath et al say they tested the suggestion, and they call the result a disproof:
> "The authors of (Wang et al., 2022) hypothesised that dropout (Srivastava et al., 2014) was responsible for self-repair behaviour, which we disprove as the model we study (Chinchilla 7B) was trained without any form of dropout or stochastic depth." (McGrath et al 2023, Sec. 6)

McDougall et al (ACL version) also say: "Appendix A provides evidence that copy suppression occurs in models trained without dropout."
The post itself says this in section 2 ("So dropout is not necessary for repair"), so the sentence also contradicts the post. My searches found no study that trains matched models with and without dropout and compares how much they repair. The only claim that is still open is whether dropout *increases* repair. A 2026 paper on backup heads (Gong et al, arXiv 2607.01940) does not mention dropout in its abstract.
Proposed: "[McGrath et al 2023](#references) found repair in a model trained without dropout, which shows that dropout is not needed for it, but I could not find a test of whether dropout makes the repair larger."
(If this is adopted, the McGrath sentence in section 2 partly repeats it. One of the two could be shortened.)

**Item 23.** Yes. "In IOI, sentences such as "When Mary and John went to the store, John gave a drink to" should be completed with "Mary"" (Sec. 1); "we aim to mechanistically understand how GPT-2 small (Radford et al., 2019) implements..."

**Item 24.** Yes (same passage; IO = Mary).

**Item 25.** Yes.
> "patching 9.6, 9.9, and 10.0 causes a large drop (they thus contribute positively to the logit difference)"; "Name Mover Heads output the remaining name. They are active at END, attend to previous names in the sentence, and copy the names they attend to."

Clarity only: the sentence "The three that contribute most directly" has no noun, and the previous sentence mentions no heads. Optional: "The three heads that contribute most directly, the *name movers*, ..."

**Item 26.** Partly. The numbers are supported:
> "we knocked out all the Name Mover Heads at once. To our surprise, the circuit still worked (only 5% drop in logit difference)... These new heads compensate for the loss of Name Movers Heads by replacing their role. We selected the eight heads with the highest direct influence on logit difference after knockout and call them Backup Name Mover Heads." (Sec. 3.4)

But Appendix F credits the negative name movers as well:
> "knocking-out the three main Name Mover Heads surprisingly changes the behavior of the other heads that write in the IO-S direction (both positively and negatively). These heads compensate for the loss of function from the Name Mover Heads such that the logit difference is only 5% lower. We observe that the Negative Name Mover Heads have a less negative effect on logit difference, and 10.7 even has a positive effect on the logit difference after the knockout."

The post's own section 5 finds that the negative name movers carried 37.5% of the replacement. As written, "because eight backup name movers increased their contribution" gives the backup heads all the credit.
Proposed: "When all three were switched off, the preference for the right name fell by only 5%, because other heads changed their contribution: eight *backup name movers* increased theirs, and the heads that normally push against the right name pushed less."

**Item 27.** Yes. The quote is word for word (Sec. 3.4, quoted under item 21).

**Item 28.** Yes. "Over 100,000 dataset examples, GPT-2 small has mean logit difference of 3.56 (IO predicted over S 99.3% of the time)" (Sec. 2).

**Item 29.** Yes ("only 5% drop in logit difference", Sec. 3.4; "only 5% lower", App. F).

**Item 30.** Yes. "We create dataset samples for IOI using 15 templates (see Appendix E)". Figure 14 lists 15 templates: "All templates in the table fit the 'BABA' pattern, but we use templates that fit the 'ABBA' pattern as well (i.e, by swapping the first instances of [B] and [A] in all of the above)." This also confirms "Wang et al's BABA set" in Details A.

**Item 31.** Yes. Figure 2 reads: "Previous Token Heads 2.2 4.11 / Duplicate Token Heads 0.1 3.0 (0.10) / Induction Heads 5.5 6.9 (5.8 5.9) / S-Inhibition Heads 7.3 7.9 8.6 8.10 / Backup Name Mover Heads 9.0 9.7 10.1 10.2 10.6 10.10 11.2 11.9 / Name Mover Heads 9.9 9.6 10.0 / Negative Name Mover Heads 10.7 11.10". Every head in the post's table matches. In the figure, 0.10, 5.8 and 5.9 are in parentheses, which marks them as weaker members (the "fuzzy" duplicate-token head and the minor induction heads). The post does not show this, and it does not need to.

**Item 32.** Yes. "After the knockout, we found the new heads directly affecting the logits using the same path patching experiment from Section 3.1" (Sec. 3.4). The path-patching experiment of Sec. 3.1 measures each head's direct path to the logits.

**Item 33.** Yes. "we instead knockout nodes through mean ablation: replacing them with their average activation value across some reference distribution" (Sec. 2.1). Wang et al also take the mean per template, as the post does: "we compute the mean of a node across samples of the same template."

**Item 34.** Yes. "all knockouts are performed in a modified pIOI distribution called pABC. It relies on the same generation procedure, but instead of using two names (IO and S) it used three unrelated random names (A, B and C)... We chose this distribution for mean-ablating because using pIOI would not remove enough information helpful for the task."

## R11. radford2019

**Metadata.** The URL resolves to the PDF "Language Models are Unsupervised Multitask Learners" by Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei and Ilya Sutskever. The PDF does not call itself a "technical report", but that label is the usual way to cite it. OK. **Evidence:** full text.

**Item 35.** Yes. Table 2 lists the smallest model ("117M 12 768"). The paper says: "The smallest model is equivalent to the original GPT". The gpt-2 README notes that small was later recounted as 124M: "our original parameter counts were wrong due to an error... you may have seen small referred to as 117M".

**Item 36.** Partly. Each fact is correct, but the sentence leaves out two things.
- "the paper does not say": correct. The words "dropout" and "regularization" do not appear in the PDF. **However**, the paper says the model follows GPT-1: "The model largely follows the details of the OpenAI GPT model (Radford et al., 2018) with a few modifications" (Sec. 2.3), and the GPT-1 paper says: "We used ... residual, embedding, and attention dropouts with a rate of 0.1 for regularization" (Radford et al 2018, https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf, Sec. 4.1). So the paper points to a design that used dropout.
- Hugging Face config: correct. https://huggingface.co/openai-community/gpt2/blob/main/config.json (https://huggingface.co/gpt2 redirects there; the file is identical). It contains `"attn_pdrop": 0.1`, `"embd_pdrop": 0.1`, `"resid_pdrop": 0.1` (and `"summary_first_dropout": 0.1`). Repo head is commit 607a30d (2024-02-19); config.json was last changed 2020-05-11.
- OpenAI's code: correct. https://github.com/openai/gpt-2/blob/master/src/model.py (permalink: https://github.com/openai/gpt-2/blob/9b63575ef42771a015060c964af2c3da4cf7c8ab/src/model.py). It has no dropout. `default_hparams()` has no dropout parameter, and a search of the whole cloned repository for "dropout" and "pdrop" finds nothing. **However**, the repository contains only code that loads and samples from the trained model (src/: encoder.py, generate_unconditional_samples.py, interactive_conditional_samples.py, model.py, sample.py). There is no training code, and dropout is switched off when a model is only run, so the absence of dropout in this code says nothing about how GPT-2 was trained.

Proposed: "Even GPT-2's use of dropout is uncertain: its [Hugging Face configuration](https://huggingface.co/openai-community/gpt2/blob/main/config.json) sets dropout to 0.1, but [the code OpenAI released](https://github.com/openai/gpt-2/blob/master/src/model.py), which only runs the trained model, contains none, and the paper ([Radford et al 2019](#references)) does not mention dropout, saying only that the model largely follows the earlier GPT model, which used it."

## R12. elhage2021

**Metadata.** The URL resolves to "A Mathematical Framework for Transformer Circuits", Transformer Circuits Thread, published 22 December 2021. The authors begin "Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, ...". OK. **Evidence:** full HTML text.

**Item 37.** Partly.
> "The residual stream is simply the sum of the output of all the previous layers and the original embedding."
> "we can fold everything but normalization into adjacent parameters, and then think of the normalization scaling as a variable reweighting of the set of path terms going through that layer normalization."

The paper also says it simplifies its own models: "We also ignore layer normalization." So the answer is a sum only up to the final LayerNorm's rescaling, which the post's Details divide out.
Proposed: "**Direct effect.** Apart from one rescaling at the end, the model's answer is a sum of the outputs of all its parts, so each head's own contribution to the logit difference can be computed ([Elhage et al 2021](#references))."

**Item 38.** Yes. The citation supports the method: decompose the output into components and treat the LayerNorm scale as a reweighting (quotes above). Measuring relative to the ABC mean is the author's own choice, and the sentence does not attribute it to Elhage et al.

## R13. mcgrath2023

**Metadata.** arXiv 2307.15771 resolves to "The Hydra Effect: Emergent Self-repair in Language Model Computations" by Thomas McGrath, Matthew Rahtz, János Kramár, Vladimir Mikulik and Shane Legg (2023). OK. **Evidence:** full text.

**Item 39.** Yes. "In this work we use a 7 billion parameter model from the Chinchilla family"; "ablations of one attention layer of a language model cause another layer to compensate (which we term the Hydra effect)"; "The Chinchilla-like language model we study here was trained entirely without dropout, stochastic depth, or layer dropout." The quote is word for word.

**Item 40.** Yes. The authors draw the same conclusion (Sec. 6, quoted under item 22).

**Item 41.** Yes (same).

**Item 42.** Yes. "late layer MLPs often act to reduce the probability of the maximum-likelihood token, and this reduction is attenuated when attention layers promoting that token are knocked out"; "at middle layers ... the Hydra effect and reduction in MLP effects collectively act to restore approximately 70% of the reduction in token logits." The paper says "probability" in one place and "downregulate the maximum-likelihood token" in the abstract, and it measures these effects in logits, so "logit" is fair.

## R14. rushing2024

**Metadata.** arXiv 2402.15390 resolves to "Explorations of Self-Repair in Language Models" by Cody Rushing and Neel Nanda. arXiv journal_ref: "Proceedings of the 41st International Conference on Machine Learning, PMLR 235:42836-42855, 2024". OK. **Evidence:** full text (v2).

**Item 43.** Yes. "self-repair exists on a variety of models families and sizes when ablating individual attention heads on the full training distribution. We further show that on the full training distribution self-repair is imperfect, as the original direct effect of the head is not fully restored, and noisy".

**Item 44.** Yes. The quote is exact: "A nontrivial fraction - possibly 30% - of the self-repairing of direct effects can be attributed to just the effect of ablations on the LayerNorm normalization factor."

**Item 45.** Partly. The figure is theirs, measured on ordinary text (The Pile and the like) for single heads, but they call it rough and measure it differently from the post's 5.8%:
> "when measuring the self-repair due to LayerNorm on a token as a fraction of the clean direct effect of the head on that token, and capping the percentage between 0 and 100%, we learn that LayerNorm can explain around 30% of the direct effect of a head on average across many layers. This is best treated more as a directional metric highlighting the existence of this motif, rather than a concrete, precise one"

Appendix A adds: "our figure for "30% of direct effect is self-repaired by LayerNorm" can potentially be interpreted as "in 30% of cases, the self-repair due to LayerNorm is larger in..."".
Proposed: "The replacement comes almost entirely from what the heads write: the final normalisation step accounts for only 5.8% of it, below the "possibly 30%" that [Rushing & Nanda 2024](#references) give as a rough figure, measured differently, for single heads on ordinary text."

**Item 46.** Yes. "if the original direct effect is positive and the self-repair is negative, we believe this should not be thought of as self-repair, but rather downstream breakage where later components perform worse as a result of the ablation."

**Item 47.** Yes. Their Appendix B splits Δlogit into a LayerNorm term using the clean and ablated scales S and S′: "∆logit = (S/S′ − 1)logit + (S/S′)(⟨Hnew/S, L⟩ − ⟨Hold/S, L⟩)". In Sec. 3 they take the LayerNorm share as what is left of the self-repair after the head and MLP changes. Computing each component with both scales and taking the difference gives the same split, applied to each component.

**Item 48.** Yes. "self-repair = ∆logit − ∆DEhead (1)". Their direct effect after ablation uses the clean scale: "define the new direct effect of the resample ablated head as DE′Head = ⟨Hnew/S, L⟩" (App. B). With that definition, LayerNorm changes count as self-repair, as the post says. The next sentence of the post (the top 2% of positions) is also supported: "we measure the average self-repair each attention head experiences across the top 2% of tokens filtered by each head's direct effect". Their ablation is also resample ablation, as in the post.

## R15. mcdougall2024

**Metadata.** Partly. ACL Anthology 2024.blackboxnlp-1.22 (doi:10.18653/v1/2024.blackboxnlp-1.22): "Copy Suppression: Comprehensively Understanding a Motif in Language Model Attention Heads", Callum Stuart McDougall, Arthur Conmy, Cody Rushing, Thomas McGrath, Neel Nanda. Proceedings of the 7th BlackboxNLP Workshop, pp. 337–363, November 2024. The title, venue and pages in the post match this. **But** the post links arxiv.org/abs/2310.04625, whose title is different: "Copy Suppression: Comprehensively Understanding an Attention Head" (v1, Oct 2023, "Preprint. Under review.").
Fix: change the link to [doi:10.18653/v1/2024.blackboxnlp-1.22](https://doi.org/10.18653/v1/2024.blackboxnlp-1.22) (or https://aclanthology.org/2024.blackboxnlp-1.22/).
**Evidence:** full text of both the ACL PDF and arXiv v1.

**Item 49.** Yes. "If i) language model components in earlier layers predict a certain token, ii) this token appears earlier in the context and iii) later attention heads in the model suppress prediction of the token, then this is copy suppression. ... we focus on reverse-engineering attention head 10.7 (L10H7) in GPT-2 Small"; "Copy suppression leads to self-repair: if an initial overconfident copier is ablated, then there is nothing to suppress." They also identify it with Wang et al's negative heads: "we explain how "Negative Heads" (which include 'negative name mover heads' from [Wang et al])...".

**Item 50.** Yes (same passage). For context, in their measurement the two negative heads explain 39% of the self-repair after the name movers are ablated: "The sum of the proportions of self-repair explained by Negative Heads L10H7 and L11H10 is 39%". This is close to the post's 37.5%.

## R16. tigges2024

**Metadata.** arXiv 2407.10827 resolves to "LLM Circuit Analyses Are Consistent Across Training and Scale" by Curt Tigges, Michael Hanna, Qinan Yu and Stella Biderman. arXiv comment: "NeurIPS 2024", which is Advances in Neural Information Processing Systems 37. OK. **Evidence:** full text (v2).

**Item 51.** Partly. Heads gaining and losing roles while the method stays the same is supported: "although such components may be implemented by different attention heads over time, the overarching algorithm that they implement remains"; "Heads often lose their current function; as this occurs, other heads take their place." The IOI circuit is the one they test for whether the method stays the same: "we examined the IOI circuit". **But** they do not attribute the stability to self-repair. They only say it may contribute:
> "It seems plausible that self-repair [46, 58] contributes to this behavioral stability, but we leave the question of the exact "load-balancing" mechanism to future work."

Proposed: "...and found that individual heads gain and lose their roles while the circuit's method stays the same; they suggest that self-repair may contribute to this stability and leave its mechanism to future work."

**Item 52.** Yes (the last clause only): "the identity of components in each circuit is not constant."

**Item 53.** Yes (the last clause only): "the name-mover head (4,6) suddenly stops exhibiting this behavior at 3×10^10 tokens, having acquired it after 4×10^9 tokens." This was in Pythia-160m; the post's wording does not say which model, which is fine.

## R17. rohweder2026

**Metadata.** arXiv 2603.06592 resolves to "Hierarchical Latent Structures in Data Generation Process Unify Mechanistic Phenomena across Scale" by Jonas Rohweder, Subhabrata Dutta and Iryna Gurevych (UKP Lab, TU Darmstadt). The current version is v2, 14 Jul 2026. OK. **Evidence:** full text (v2).

**Item 54.** Partly.
> "we answer this question by unifying these three phenomena as consequences of hierarchical latent structures in the data generation process, coupled with decorrelated gradients across additive model components and directional concavity in the representation geometry."

The word "dropout" does not appear anywhere in the paper. "With no role for dropout" is therefore a fair reading but not something they state, and the account also depends on representation geometry, which the post's sentence leaves out.
Proposed: "[Rohweder et al 2026](#references) explain the Hydra effect from the structure of the training data, together with properties of gradient descent and of the model's internal representations; their account does not mention dropout."

**Item 55.** This is the author's inference, and the source does not contradict it. The paper says its gradient and geometry conditions "though necessary for Hydra effect to emerge, are not sufficient", and it makes no prediction about how much repair models trained on the same data should differ by.

## R18. heimersheim2024

**Metadata.** arXiv 2404.15255 resolves to "How to use and interpret activation patching" by Stefan Heimersheim and Neel Nanda (2024). OK. **Evidence:** full text.

**Item 56.** Yes. "Mean ablation: Same as above but overwrite targeted activations with their dataset mean value rather than zero"; "Activation patching (also referred to as Interchange Intervention, Causal Tracing, Resample Ablation, or Causal Mediation Analysis) is the technique of replacing internal activations of a neural net." Their table lists "Corrupted→clean (Noising, Resample Ablation)" as patching in activations from the corrupt run.

## R19. zhou2020

**Metadata.** ACL Anthology 2020.findings-emnlp.178 (doi:10.18653/v1/2020.findings-emnlp.178): "Scheduled DropHead: A Regularization Method for Transformer Models". The anthology lists the authors in the order Wangchunshu Zhou, Tao Ge, Furu Wei, Ming Zhou, Ke Xu, which matches the post (the arXiv version lists Xu third). Findings of EMNLP 2020, pp. 1971–1980. OK.
**Evidence:** no text could be extracted from the ACL PDF (pypdf returned almost nothing), so I read the full text of the arXiv version (2004.13342) and checked the abstract on the ACL page.

**Item 57.** Yes. "In contrast to the conventional dropout mechanism which randomly drops units or connections, DropHead drops entire attention heads during training to prevent the multi-head attention model from being dominated by a small portion of attention heads."

## R20. eldan2023

**Metadata.** arXiv 2305.07759 resolves to "TinyStories: How Small Can Language Models Be and Still Speak Coherent English?" by Ronen Eldan and Yuanzhi Li (2023). OK. **Evidence:** full text; Hugging Face dataset card and the size API.

**Item 58.** Yes. "we introduce TinyStories, a synthetic dataset of short stories that only contain words that a typical 3 to 4-year-olds usually understand".

**Item 59.** Partly. "GPT-3.5 and GPT-4" and "young child" are supported (same sentence: "...generated by GPT-3.5 and GPT-4"). **The paper does not give a number of stories.** A search of the full text for "million" finds only parameter counts. The figure comes from the Hugging Face dataset roneneldan/TinyStories, which the project loads (trophic/data.py: `DATASET = "roneneldan/TinyStories"`). Its splits are 2,119,719 training rows and 21,990 validation rows (datasets-server size API).
Proposed: "**TinyStories:** about 2.1 million short stories ([Hugging Face release](https://huggingface.co/datasets/roneneldan/TinyStories)) written by GPT-3.5 and GPT-4 in the vocabulary of a young child ([Eldan & Li 2023](#references)), tokenized with the GPT-2 tokenizer, joined with an end-of-text token between stories, and cut into sequences of 256 tokens."

## R21. nanda2022

**Metadata.** The repository's README asks to be cited as `@misc{nanda2022transformerlens, title = {TransformerLens}, author = {Neel Nanda and Joseph Bloom}, year = {2022}, howpublished = {\url{https://github.com/TransformerLensOrg/TransformerLens}}}`. This matches the post. Version 3.9.0 exists on PyPI (the latest is 4.3.0). OK.
**Evidence:** README and the v3.9.0 source of `transformer_lens/HookedTransformer.py` (`from_pretrained` docstring).

**Item 60.** Partly. The defaults are `fold_ln=True`, `center_writing_weights=True`, `center_unembed=True` and `fold_value_biases=True`. The docstrings say these "do not change the computation":
> fold_ln: "LayerNorm ... followed by a linear layer ... is optimized to LayerNormPre (just centering & normalizing) followed by a new linear layer"
> center_writing_weights: "every component reading an input from the residual stream is preceded by a LayerNorm, which means that the mean of a residual stream vector ... never matters. This means we can remove the all ones component of weights and biases whose output writes to the residual stream."

The residual stream is the sum of per-component outputs whether or not the weights are processed; that is how the architecture works (Elhage et al: "The residual stream is simply the sum of the output of all the previous layers and the original embedding"). What the default processing does is make the final LayerNorm a pure rescaling, so that per-component direct effects add up exactly to the logit.
Proposed: "**Measurement in the pretrained models.** TransformerLens 3.9 ([Nanda & Bloom 2022](#references)) with its default weight processing, under which the final LayerNorm only rescales the residual stream, so that the per-component outputs, divided by that scale, sum exactly to the logits; a unit test checks that direct effects add up to the logit difference to 0.01."

## Extra: the uncited GPT-2 dropout claim

Both parts are correct (details under item 36):
- Hugging Face gpt2 config sets `attn_pdrop`, `embd_pdrop` and `resid_pdrop` to 0.1: https://huggingface.co/openai-community/gpt2/blob/main/config.json
- OpenAI's released src/model.py has no dropout: https://github.com/openai/gpt-2/blob/master/src/model.py (permalink at commit 9b63575: https://github.com/openai/gpt-2/blob/9b63575ef42771a015060c964af2c3da4cf7c8ab/src/model.py)

These two facts alone do not settle the question. The repository has no training code, and the GPT-2 paper defers to GPT-1, which used dropout of 0.1. That is why item 36 needs rewording.
