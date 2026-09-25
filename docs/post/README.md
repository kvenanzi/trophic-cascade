# Trophic Cascades in a Transformer: Mesopredator Release, Keystone Heads, and Whether Dropout Produces Them

| created | modified | status | confidence | importance |
|---|---|---|---|---|
| 2026-09-24 | 2026-09-25 | finished | likely[^conf] | 4 |

> **Abstract.** Ecologists measure the structure of a community by removing a species and recording what the others do, and have published measures for the result: interaction strength, the log response ratio, community importance, mesopredator release, and the hydra effect. Interpretability researchers perform the same experiment on transformers, ablating a component and recording what the others do, and have found that later components restore part of what was removed. I apply the ecological measures, as published, to attention heads, under six hypotheses committed before the experiments. In the indirect-object-identification circuit of GPT-2 small, removing the three name-mover heads removes 4.76 units of direct effect and *raises* the logit difference from 3.65 to 3.85 (compensation 1.042, 95% CI 1.023–1.061); eight backup and two negative name movers carry 94.5% of the offset, the pattern ecologists call mesopredator release, and the final LayerNorm 5.8%. Community importance ([Power et al 1996](#references)) identifies all four S-inhibition heads and three induction heads as keystones, heads with almost no direct effect whose removal costs 10–37% of the logit difference, and gives negative values to the heads that consume the quantity measured, including the copy-suppression head 10.7. The response of head activity to a removal attenuates with distance in the circuit in all three steps tested. Across five pretrained models, compensation for the top three heads ranges from 0.009 in Pythia-1.4B (interval including zero, which refutes the registered claim that every competent model compensates) to 1.04; across the training of Pythia-410M it rises (Spearman ρ 0.92) from −0.87 at step 4,000, where a removal costs the model more than the removed heads contributed, to 0.41. To test the conjecture of [Wang et al 2022](#references) that such compensation is caused by dropout, eighteen 30-million-parameter models were trained from scratch on 200 million tokens of TinyStories with no dropout, standard dropout, or head dropout, six seeds each, paired by seed. The pooled self-repair fraction is 0.359, 0.615, and 0.670; standard − none is +0.256 (95% CI 0.231–0.281) and head dropout − standard +0.055 (0.045–0.065), both positive for six of six seeds, and the differences remain (+0.251 and +0.309) when each dropout model is compared with the no-dropout checkpoint of equal validation loss. Dropout is not necessary for self-repair, which reaches 0.36 without it, but it increases it by a factor of 1.7, and head dropout, which removes the same unit the experiment removes, increases it most while costing less validation loss than standard dropout. Limitations: one circuit for the keystone and attenuation results, and one model size, dataset, and dropout rate for the training experiment.

## Summary without the terminology

A language model is built from many small components. When one of them is removed, other components often take over part of its function. Ecologists study the same kind of event when they remove a predator from a stretch of coast or a lake and record how the other species respond, and they have developed measurements for it. This report uses their measurements to ask two questions: how does this replacement work inside a model, and what produces it?

**Part A** removes components from trained models on one well-studied task. The model reads "When Mary and John went to the store, John gave a drink to" and must answer "Mary"; earlier work identified which components of GPT-2 carry out this task.

1. **When the main components are removed, other components take over all of their function.** GPT-2 relies mostly on three components to produce the answer. With all three removed, it prefers the correct name slightly more strongly than before. Backup components that contributed little begin to produce the answer, and a component whose normal role is to reduce the model's confidence in that answer stops doing so, because the signal it acts on is gone. Ecologists call the first pattern *mesopredator release*: when a top predator is removed, smaller predators increase.
2. **The components that matter most are not the ones that contribute most directly.** Several components have almost no direct effect on the answer, yet removing any one of them reduces the model's preference for the correct name by as much as a third, because they direct the components that do produce it. Ecologists call a species of this kind a *keystone*: its effect is large relative to its numbers. The components predicted to be keystones were keystones; one main component was predicted not to be one in this sense and was, by a small margin.
3. **The effect of a removal decreases with distance.** Removing a component changes the components that receive its output directly more than it changes the components one step further on, as removing a predator changes the animals it eats more than the plants those animals eat.
4. **Not every model does this.** Four of five models tested take over the function of removed components; the fifth, Pythia-1.4B, performs the task equally well but does not: when its main components are removed, no other component replaces them. The prediction that every capable model would do it was therefore wrong, and the amount varies between models from none to more than all of what was removed.
5. **The replacement develops during training, after a stage in which the opposite happens.** Measured at eleven points during the training of one model, removing the main components early in training caused *more* damage than those components contributed: the rest of the model reduced its preference for the correct name further, instead of restoring it. Later in training this reversed, and the model came to restore about 40% of what a removed component contributed, which is the pattern ecologists describe for a community that becomes more stable as it matures.

**Part B** tests where the replacement comes from. The researchers who first described the backup components suggested that they exist because of *dropout*, a training method that switches random components off during training so that the model cannot depend on any one of them. The suggestion had not been tested. Eighteen small models were trained from scratch on the same data, identical except for the training method (no dropout, standard dropout, or a form of dropout that switches off whole components), six of each, and each was measured for how much of a removed component's function the rest of it restores. A second comparison checks that any difference is due to dropout itself rather than to dropout models being less fully trained after the same amount of data.

Dropout increased the replacement. Models trained without dropout restored about 36% of a removed component's function; with standard dropout, 62%; with the form that switches off whole components, 67%. The order was the same for every one of the six sets of models, and it was the same when each dropout model was compared with a no-dropout model at the same stage of learning. Dropout is therefore not the only source of the replacement, since models trained without it still restore about a third, but it makes the replacement much larger, as the researchers suggested, and as the ecological idea that variable conditions produce redundancy predicts. The form that switches off whole components, which is the kind of removal the experiment itself performs, produced the most replacement, and its models also fit the data better than those trained with standard dropout.

## 1. Background

### 1.1 Removal experiments in ecology

In 1963 Robert Paine began prying the predatory starfish *Pisaster ochraceus* off an 8-metre stretch of rocky shore at Mukkaw Bay, Washington, and keeping it clear of them. Barnacles settled on the bare rock, then mussels, which the starfish had been eating, overgrew the barnacles, algae, and other attached species; the plot went from fifteen species of primary space holders to eight ([Paine 1966](#references); [Lafferty & Suchanek 2016](#references)). The starfish ate few of the species that disappeared; its effect on them ran through the mussel. The same removal *increased* diversity by another measure, since a mussel bed is habitat for more than 300 associated species ([Lafferty & Suchanek 2016](#references)): what a removal experiment shows depends on which property of the community is measured, a point that applies equally to the measurements below. [Paine 1969](#references) called a species of this kind a *keystone*. The same pattern, a predator whose removal changes the abundance of species two or more feeding levels below it, was found for sea otters, sea urchins, and kelp ([Estes & Palmisano 1974](#references)), for piscivorous fish, zooplankton, and algae in lakes ([Carpenter et al 1985](#references)), and for wolves, elk, and riparian willow and aspen in Yellowstone after 1995 ([Ripple & Beschta 2004](#references); [Ripple & Beschta 2012](#references)). The general term is a *trophic cascade*; the earliest general argument for it is [Hairston et al 1960](#references).

The field turned these observations into measurements, and four of its measures are used below.

- **Interaction strength.** The effect of species *i* on species *j* is measured by removing *i* and recording the change in *j* ([Paine 1992](#references)). [Berlow et al 1999](#references) compare the indices in use and recommend reporting the raw difference alongside ratio measures, because ratios are unstable when the baseline is small.
- **The log response ratio.** For a quantity that is always positive, such as a density, the response to a treatment is ln(treated / control); it is symmetric in increases and decreases and has a known sampling distribution ([Hedges et al 1999](#references)). [Shurin et al 2002](#references) used it to compare 102 predator-removal experiments across six ecosystem types, and found that predator effects on herbivores were larger than predator effects on plants: cascades *attenuate* with each step down the food web. [Borer et al 2005](#references) extended the comparison to 114 studies and found that traits of the predators and herbivores explain about a third of the variation in cascade strength.
- **Community importance.** [Power et al 1996](#references) define a keystone as a species "whose impact on its community or ecosystem is large, and disproportionately large relative to its abundance", and make it operational as community importance, CI_i = [(t_N − t_D) / t_N] · (1 / p_i), where t_N is a community trait in the intact community, t_D the same trait after species *i* has been deleted, and p_i the proportional abundance of *i* before deletion. A species whose effect is in proportion to its abundance has CI = 1; a keystone has CI well above 1. The authors note that the full effect, "all the direct and indirect effects of the species", is what a removal measures.
- **Press and pulse.** [Bender et al 1984](#references) distinguish a *pulse* perturbation, a one-time change in abundance after which the system is allowed to return, from a *press* perturbation, a sustained change held until the system settles into a new state. Species removal is a press.

Two outcomes of removal experiments have their own names. In *mesopredator release*, removing a top predator allows a smaller predator to increase: in fragmented scrub habitat near San Diego, canyons from which coyotes had disappeared held more domestic cats, raccoons, and foxes, and fewer species of scrub-breeding birds ([Crooks & Soulé 1999](#references)). In the *hydra effect* of population ecology, an increase in a population's mortality rate increases its equilibrium size, a result first seen in discrete density-dependent models in 1954 and reviewed by [Abrams 2009](#references). A third idea concerns where compensation comes from. The *insurance hypothesis* ([Yachi & Loreau 1999](#references)) holds that a community of species which respond differently to environmental fluctuation maintains its aggregate function better than a community of identical species, because the loss of one is offset by the others. The hypothesis predicts that redundancy is a product of variable conditions.

### 1.2 Removal experiments in transformers

The standard experiment in mechanistic interpretability is the same one. A component, most often an attention head, is *ablated*: its output is replaced by its mean over a reference distribution (mean ablation), by its output on a different input (resample ablation), or by zero, and the model's output is compared with the unablated model's ([Heimersheim & Nanda 2024](#references); [Zhang & Nanda 2024](#references)). The quantity that plays the role of a population's abundance is the component's *direct effect*: in a transformer the final residual stream is a sum of the outputs of every head and every MLP layer, so each component's contribution to a given logit can be computed by projecting its output through the final normalisation and the unembedding ([Elhage et al 2021](#references)).

[Wang et al 2022](#references) reverse-engineered the circuit GPT-2 small ([Radford et al 2019](#references)) uses to complete sentences such as "When Mary and John went to the store, John gave a drink to", in which the correct continuation is the name that is not repeated, the *indirect object* (IO). They identified 26 heads in seven classes (§4.2). The three heads with the largest direct effect, which they called *name movers* (9.9, 9.6, 10.0 in layer.head notation), attend from the last position to the IO and copy it to the output. When all three were knocked out, the logit difference between the IO and the repeated subject fell by only 5%, because eight other heads, which they named *backup name movers*, increased their direct effect to replace them. They wrote: "We hypothesize that this compensation phenomenon is caused by the use of dropout during training. Thus, the model was optimized for robustness to dysfunctional parts. More work is needed to determine the origin of this phenomenon." That hypothesis has not, to my knowledge, been tested.

[McGrath et al 2023](#references) found the same behaviour at the level of whole layers in a 7-billion-parameter Chinchilla-architecture model and named it the *Hydra effect*, after the mythological animal rather than the ecological term.[^hydra] Ablating one attention layer caused later attention layers to increase their direct effects, and certain late MLP layers, which normally reduce the logit of the most likely token, reduced it less ("erasure"). Their model was "trained entirely without dropout, stochastic depth, or layer dropout", which establishes that dropout is not *necessary* for compensation. Whether it *increases* compensation is a separate question. [Rushing & Nanda 2024](#references) measured compensation across the Pythia suite, GPT-2 small and medium, and Llama-7B on a million tokens of each model's pretraining distribution, defined *self-repair* as the change in the logit minus the change in the ablated head's direct effect, and found it widespread but imperfect and noisy. In their words "possibly 30%" of it runs through the final LayerNorm: removing a head changes the norm of the residual stream, and the normalisation rescales every surviving component accordingly. [McDougall et al 2024](#references) explained one head in detail: GPT-2's 10.7, one of Wang et al's two *negative* name movers, suppresses the logit of tokens that appear earlier in the context and that earlier layers are already predicting, so when the name movers are removed it has less to suppress; it accounts for about 39% of self-repair in the IOI task. [Tigges et al 2024](#references) followed the IOI circuit through the training checkpoints of the Pythia models and found that individual name-mover heads gain and lose the behaviour over training while the circuit's algorithm stays the same; they attribute the stability in part to self-repair and leave the mechanism to future work.

Three 2026 preprints bear on the present design. [Gong et al 2026](#references) rank candidate backup heads by the growth of their ablation effect after a primary set has been removed, which is, in ecological terms, a removal-based interaction strength; on GPT-2's IOI circuit it recovers Wang et al's backup heads at 0.94 ROC-AUC. [Patrawala et al 2026](#references) find that adjacent layers systematically counteract parts of each other's output on nearly all tokens in five of seven model families. [Rohweder et al 2026](#references) derive the Hydra effect, together with induction heads and function vectors, from hierarchical structure in the training data and decorrelated gradients across additive components, an account in which dropout plays no part.

### 1.3 The correspondence, and where it fails

| Ecology | Transformer, as measured here |
|---|---|
| species | attention head |
| abundance; proportional abundance p_i | direct effect of the head on the logit difference, relative to its mean-ablated value; p_i is its share of the summed absolute direct effect of all heads |
| removal (a press perturbation) | mean ablation of the head's output for the whole forward pass |
| community trait t | mean logit difference, logit(IO) − logit(S) |
| interaction strength of *i* on *j* | change in *j*'s direct effect when *i* is removed |
| density, and its log response ratio | a head's *activity*, the norm of its output relative to its mean, and ln(activity with *i* removed / activity intact) |
| mesopredator release | an increase in the direct effect of backup heads when the name movers are removed |
| hydra effect | compensation greater than 100%: the trait rises when a component that supports it is removed |
| trophic level | position in the IOI circuit's chain of dependence (§4.2) |
| a disturbance regime during community assembly | dropout during training |

The correspondence has limits that bear on how the results should be read. A transformer's forward pass is a directed acyclic graph: a head can affect only heads in later layers, and nothing downstream feeds back. Ecological cascades run through feedback over many generations and settle at a new equilibrium; the "response" here is computed in a single pass, with no dynamics and no equilibrium. Mean ablation fixes a head at its average output rather than deleting it, so it removes the head's input-dependent information and leaves its average contribution in place; it is closer to holding a population at a constant density than to extinction. And a head's direct effect on one logit difference is a narrow measure of its "abundance", as biomass is of a species'. The report uses the ecological measures because they come with precise definitions and a record of what they reveal in the systems they were built for, not because a transformer is an ecosystem; §6 assesses which of them measured something the standard interpretability quantities do not.

## 2. Hypotheses

Recorded before any of the registered experiments was run. One observation preceded them. On 2026-09-24, while checking that the measurement code reproduced Wang et al's baseline (§4.2), I mean-ablated the three name movers of GPT-2 small on the 600 prompts of §3.1 and found that the logit difference *rose*, from 3.65 to 3.85, where Wang et al report a 5% fall. H1 is therefore a replication with a known point estimate, and is stated so that it can still fail on its interval and its attribution. Every other hypothesis concerns a quantity that had not been computed when it was written.

**Part A: pretrained models, the IOI task.**

- **H1 (mesopredator release).** In GPT-2 small, mean-ablating the name movers {9.9, 9.6, 10.0} as a set gives compensation c = 1 − TE/DE whose 95% bootstrap interval lies above 0 (TE: fall in mean logit difference; DE: the three heads' summed mean direct effect). At least half of the offset, the summed change in direct effect over every component not ablated, is carried by Wang et al's eight backup name movers and two negative name movers together.
- **H2 (keystones).** A head is a *keystone* if its single-head removal changes the mean logit difference by at least 5% and its community importance satisfies |CI| ≥ 2. At least three of the four S-inhibition heads, and at least one of the previous-token, duplicate-token, or induction heads, are keystones. None of the three name movers is: the heads with the largest abundance have CI < 1, because of H1.
- **H3 (attenuation).** Take the circuit levels L1 previous-token, L2 duplicate-token and induction, L3 S-inhibition, L4 name mover, L5 negative name mover (§4.2). When all the heads of level *k* are removed together, the mean absolute log response ratio of activity is larger for the heads of level *k*+1 than for those of level *k*+2, for each of *k* = 1, 2, 3, with the bootstrap interval of the difference above 0 in at least two of the three.
- **H4 (generality).** In every pretrained model that passes a competence gate (IO preferred on at least 80% of prompts, mean logit difference at least 1.0), mean-ablating the three heads with the largest positive direct effect gives compensation whose 95% interval lies above 0. Models: GPT-2 small and medium, Pythia-160M, -410M, and -1.4B. No prediction is made about the size of c or its relation to model size.
- **H5 (development).** Over the Pythia-410M checkpoints of §4.5 that pass the competence gate, compensation of the top three heads rises with training: the Spearman correlation between training step and c is positive, with a bootstrap interval above 0. The ecological motivation is that mature communities are more internally buffered than early-successional ones ([Odum 1969](#references)); the interpretability motivation is the open question left by [Tigges et al 2024](#references).

**Part B: small models trained from scratch, three training regimes.**

- **H6 (dropout produces redundancy).** Small GPT-2-architecture models trained on TinyStories with standard dropout (p = 0.1 on embeddings, attention weights, and residual branches) show a larger pooled self-repair fraction on held-out text (§4.6) than the same models trained without dropout, paired by seed: the mean difference over six seeds is positive with a 95% interval above 0, and positive for at least five of the six seeds. Models trained with head-level dropout (DropHead, [Zhou et al 2020](#references); p = 0.1 on each head's output, no other dropout) show a larger self-repair fraction than standard dropout, by the same criterion. The predicted order is none < standard < DropHead. This is the insurance hypothesis in the form Wang et al stated it: training under random loss of components produces components that can replace one another's function. It concerns magnitude, not existence; McGrath et al and Rushing & Nanda have already shown compensation without dropout.
- **H6c (not an artefact of undertraining).** Dropout slows the fall of the training loss, and a less-trained model might differ in self-repair for that reason alone. The ordering of H6 also holds when each dropout run is compared with the checkpoint of its paired no-dropout run whose validation loss is closest to its own.

Each hypothesis receives a verdict in §6.1, and the document's confidence tag is set in the `[^conf]` footnote after the results are in.

## 3. Data

### 3.1 IOI prompts

Fifteen sentence templates, those of Wang et al's BABA set, each filled 40 times with a random IO name, subject name, place, and object, half with the IO first in the opening clause (ABBA) and half with the subject first (BABA): 600 prompts, seed 0 (`trophic/ioi.py`). Names, places, and objects are restricted to words that are single tokens, with a leading space, under both the GPT-2 and the Pythia tokenizer, so that the same 600 prompts are given to every model, and every prompt of a template has the same length in tokens. 72 names, 17 places, and 18 objects qualify. Each prompt has an *ABC* twin: the same template, name order, place, and object, with three other distinct names, so that no name repeats. The ABC prompts preserve the sentence structure and remove the repetition the circuit depends on; their activations are the reference for mean ablation.

### 3.2 TinyStories

The TinyStories corpus of [Eldan & Li 2023](#references), about 2.1 million short stories written by GPT-3.5 and GPT-4 in the vocabulary of a young child, tokenized with the GPT-2 tokenizer, concatenated with an end-of-text token between stories, and cut into sequences of 256 tokens. The published validation split is held out for validation loss and for the self-repair measurement.

## 4. Method

### 4.1 Measurement

All pretrained models are loaded with TransformerLens 3.9 ([Nanda & Bloom 2022](#references)) with its default weight processing, under which the final residual stream is exactly the sum of per-component outputs, so that direct effects add up to the logit difference (a unit test checks this to 0.01). For a prompt with correct answer IO and repeated subject S:

- the **logit difference** is logit(IO) − logit(S) at the last position;
- a head's **direct effect** is its output at the last position, minus its ABC mean, divided by the final LayerNorm scale and projected on W_U[IO] − W_U[S]; a mean-ablated head has direct effect 0. It is computed both with the scale of the run in question and with the scale of the intact run, and the difference between the two is the share of any change that runs through normalisation ([Rushing & Nanda 2024](#references));
- a head's **activity** is the norm of its output, (z − z̄)W_O, at the position where its class acts in the IOI circuit: S1+1 for previous-token heads, S2 for duplicate-token and induction heads, the last position for all others.

Mean ablation replaces the head's pre-projection output z, at every position, by its mean over the 40 ABC prompts of the same template at that position. Resample ablation, which substitutes the z of the paired ABC prompt, is run once on GPT-2 small as a check that no conclusion depends on the choice (§5). Intervals are percentile bootstraps over the 600 prompts, 2,000 resamples.

### 4.2 The GPT-2 small circuit

The head classes of Wang et al, Figure 2, used as the trophic levels of H3 and the named sets of H1 and H2:

| Level | Class | Heads (layer.head) |
|---|---|---|
| L1 | previous-token | 2.2, 4.11 |
| L2 | duplicate-token | 0.1, 3.0, 0.10 |
| L2 | induction | 5.5, 6.9, 5.8, 5.9 |
| L3 | S-inhibition | 7.3, 7.9, 8.6, 8.10 |
| L4 | name mover | 9.9, 9.6, 10.0 |
| – | backup name mover | 9.0, 9.7, 10.1, 10.2, 10.6, 10.10, 11.2, 11.9 |
| L5 | negative name mover | 10.7, 11.10 |

Backup name movers are not assigned a level: they operate beside the name movers rather than downstream of them.

### 4.3 Part A experiments

1. **Single-head removals** in GPT-2 small: each of the 144 heads mean-ablated alone, giving the 144 × 144 interaction-strength matrix, every head's community importance, and every head's compensation (H2).
2. **Set removals**: the name movers (H1); each circuit level (H3); every class.
3. **Other models** (H4): GPT-2 medium, Pythia-160M, -410M, -1.4B, with the three heads of largest positive mean direct effect chosen automatically in each.
4. **Checkpoints** (H5): Pythia-410M at steps 1,000, 2,000, 4,000, 8,000, 16,000, 32,000, 48,000, 64,000, 96,000, 128,000, and 143,000 (the final model), with the top three heads re-selected at each checkpoint, since [Tigges et al 2024](#references) show they change.

### 4.4 Part B: models and training

GPT-2 architecture (Hugging Face `GPT2LMHeadModel`), 6 layers, 8 heads of dimension 48 (d_model 384), MLP width 1,536, context 256, tied embeddings, GPT-2 tokenizer. AdamW, peak learning rate 1e-3 with 2% linear warm-up and cosine decay to 10%, weight decay 0.1, batch 128 sequences (32,768 tokens). The token budget is fixed, identical in every run, before the sweep, from a single timing run, at the largest multiple of ten million tokens that trains in 20 minutes or less on a Colab A100; it is chosen on throughput and is not revised after any result is seen.

Three arms:

| Arm | Embedding, attention, residual dropout | Head dropout |
|---|---|---|
| none | 0 | 0 |
| standard | 0.1 | 0 |
| drophead | 0 | 0.1 |

Head dropout zeroes each head's output independently, per sequence, with probability 0.1 during training, and scales the surviving heads' outputs by 1/0.9. Six seeds (0–5) per arm, 18 runs, run as one W&B sweep. The seed fixes both the initialisation and the order of the training sequences, so that the three arms of one seed see the same data in the same order and differ only in the regime.

### 4.5 Part B: measurement

Every model is measured in evaluation mode, with all dropout off, so that the arms differ only in how they were trained. Measurement runs inside the training job at eight evenly spaced points (after each eighth of the token budget), which gives the development of self-repair over training and the checkpoints needed for H6c without storing them.

At each point, 256 held-out sequences (65,536 token positions) are run intact and then once with each of the 48 heads resample-ablated, taking the head's output from the next sequence in the batch at the same position. For each head and position, following [Rushing & Nanda 2024](#references), Δlogit is the change in the logit of the correct next token, and ΔDE the change in the head's own direct effect on that logit, computed with the intact run's final-LayerNorm scale, so that compensation through normalisation counts as self-repair. Self-repair is Δlogit − ΔDE. For each head the positions are restricted to the 2% on which its intact direct effect is largest, as Rushing & Nanda do, so that the measure concerns the head's function rather than noise. The primary quantity is the **pooled self-repair fraction**, the sum of self-repair over all heads and their selected positions divided by the sum of −ΔDE, which is the share of removed direct effect that the rest of the model restores. The unweighted mean over heads of each head's fraction is reported as a secondary measure.

### 4.6 Statistics for Part B

The unit is the seed. For each contrast (standard − none, drophead − standard, drophead − none) the six within-seed differences give a mean, a 95% t interval, and a sign count; with six units, six of six positive is the only sign count with two-sided p < 0.05 under a sign test, and five of six is recorded as consistent but not significant on its own. Validation loss is reported for every arm, because dropout changes it.

## 5. Results

Part A was run twice: on a local GTX 1070 (W&B runs tagged `local-gtx1070`) and on a Colab A100 (the reference set, `notebooks/01_part_a.ipynb`). The two agree to the fifth decimal place on every quantity reported below (baseline logit difference 3.645846 against 3.645847; name-mover compensation 1.041904 against 1.041904; identical keystone lists), and the prompt file was byte-identical, so the numbers are properties of the models and prompts rather than of the hardware. Pythia-1.4B and the checkpoints were run on the A100 only.[^oom]

### 5.1 Baseline

GPT-2 small prefers the IO to the subject on 99.0% of the 600 prompts, with mean logit difference 3.65; Wang et al report 3.56 and 99.3% on their distribution. The twelve heads with the largest absolute direct effect are, in order, 9.9 (+2.86), 10.7 (−2.06), 9.6 (+1.22), 11.10 (−1.02), 10.0 (+0.68), 10.10 (+0.54), 10.6 (+0.36), 11.2 (−0.31), 8.10 (+0.28), 10.1 (+0.23), 7.9 (+0.20), and 7.3 (+0.10): the three name movers, both negative name movers, four of the backup name movers, and three S-inhibition heads. The three heads of largest positive direct effect, which H4 selects automatically in every other model, are exactly Wang et al's name movers.

### 5.2 Mesopredator release (H1)

Mean-ablating the three name movers removes a summed direct effect of 4.76 and *raises* the mean logit difference from 3.65 to 3.85. Compensation is 1.042 (95% CI 1.023–1.061): the remaining heads restore 104% of what was removed. Resample ablation, which substitutes the paired ABC prompt's output rather than the mean, gives 0.997 (0.978–1.016). The two methods disagree about whether the model over- or exactly compensates; both put compensation at approximately 100%.

![Direct effect of the ten most-changed heads, before and after the name movers are removed](figures/name_mover_removal.png)

*Figure 1. GPT-2 small: direct effect on the logit difference of the ten heads whose direct effect changed most when the name movers 9.9, 9.6, and 10.0 were mean-ablated together, intact (grey) and after the removal (blue). n = 600 prompts. Data: `figures/data.json`.*

The offset, the 4.96 logit-difference units by which the logit difference exceeds what the removal alone would leave, is carried by the components H1 named:

| Component | Change in direct effect | Share of offset (95% CI) |
|---|---|---|
| eight backup name movers | +2.82 | 0.569 (0.558–0.580) |
| two negative name movers | +1.86 | 0.375 (0.366–0.384) |
| all other heads | +0.31 | 0.063 (0.057–0.070) |
| MLP layers | −0.04 | −0.008 (−0.013 to −0.003) |
| backup and negative together | +4.69 | **0.945 (0.937–0.952)** |

The largest single response is 10.7, which goes from −2.06 to +0.07: with the name movers gone, the head that suppresses what the name movers predict has nothing to suppress, which is the copy-suppression account of [McDougall et al 2024](#references). The backup name movers 10.10, 10.2, 10.6, 11.2, and 10.1 each increase by 0.26 to 0.81 (Figure 1). The response runs almost entirely through the heads' outputs rather than through normalisation: the final LayerNorm scale falls by 7.4%, and that change accounts for 5.8% of the offset (5.6–6.1%), well below the "possibly 30%" [Rushing & Nanda 2024](#references) estimate for single heads on the pretraining distribution. The MLP layers act slightly against the compensation, the opposite direction to the erasure layers of McGrath et al, whose reduced suppression added to it. H1 is confirmed on both clauses.

### 5.3 Keystones (H2)

Removing each of the 144 heads alone gives each head's total effect on the logit difference, and with its abundance, its community importance (Figure 2).

![Abundance against share of the logit difference lost when each head is removed](figures/keystones.png)

*Figure 2. Every head of GPT-2 small: abundance (share of the summed absolute direct effect, log scale) against the share of the mean logit difference lost when the head alone is mean-ablated. The dashed curves are CI = ±1, an effect in proportion to abundance. Keystones and the heads with abundance above 0.05 are labelled. n = 600 prompts. Data: `figures/data.json`.*

Fourteen heads meet the registered criteria (removal changes the logit difference by at least 5% and |CI| ≥ 2):

| Head | Class | Abundance | Share of trait lost | CI |
|---|---|---|---|---|
| 8.6 | S-inhibition | 0.0049 | 0.366 | 74.9 |
| 8.10 | S-inhibition | 0.0256 | 0.291 | 11.4 |
| 5.5 | induction | 0.0001 | 0.279 | 2,973 |
| 7.9 | S-inhibition | 0.0189 | 0.275 | 14.6 |
| 6.9 | induction | 0.0001 | 0.152 | 1,160 |
| 3.0 | duplicate-token | < 0.0001 | 0.144 | 145,070 |
| 7.3 | S-inhibition | 0.0092 | 0.128 | 13.9 |
| 5.9 | induction | 0.0001 | 0.102 | 1,380 |
| 9.7 | backup name mover | 0.0070 | 0.094 | 13.5 |
| 6.0 | – | 0.0017 | 0.052 | 29.7 |
| 5.10 | – | 0.0004 | −0.061 | −149 |
| 11.2 | backup name mover | 0.0291 | −0.091 | −3.1 |
| 11.10 | negative name mover | 0.0947 | −0.287 | −3.0 |
| 10.7 | negative name mover | 0.1913 | −0.461 | −2.4 |

All four S-inhibition heads are keystones, as are three of the four induction heads and one of the three duplicate-token heads; the first clause of H2 is confirmed. None of the name movers is a keystone. But the clause that the most abundant heads have CI below 1 holds for 9.9 (CI 0.34) and 9.6 (−1.33), not for 10.0 (1.51), whose removal costs 9.5% of the trait against an abundance of 6.3%. H2 is confirmed except for that clause. The CI values of heads with near-zero direct effect, such as 145,070 for 3.0, are large because the denominator is small and carry no information beyond "large"; the ranking by share of the trait lost is the informative quantity for those heads.

Two results were not predicted. First, four heads have *negative* keystone values: removing 10.7 raises the logit difference by 46%, 11.10 by 29%, 11.2 by 9%, and 5.10 by 6%. [Power et al 1996](#references) anticipated this sign ("negative values occur when a community characteristic increases after removal of a species, as would be the case if … the first species were a consumer"): these heads consume the quantity being measured, and are the closest analogue in the model to a predator in the literal sense. Second, 6.0 and 5.10 are keystones and belong to none of Wang et al's classes; both sit upstream of the S-inhibition heads, and neither was examined further.

### 5.4 The interaction matrix

The 144 single-head removals give the change in every head's direct effect when every other head is removed. Of the 20,736 ordered pairs, 115 have an interaction strength above 0.05 in absolute value. Every responding head is in layers 9–11 (36 in layer 9, 53 in layer 10, 26 in layer 11), while the removed heads that produce those responses are in every layer from 0 to 10 except 1 and 2 (Figure 3). Only two of the 115 have the responding head at or before the removed head's layer, which can happen only through the final LayerNorm scale.

![Interaction-strength matrix: every removed head against the responding heads of layers 9 to 11](figures/interaction_matrix.png)

*Figure 3. GPT-2 small: the change in the direct effect of each head in layers 9–11 (columns) when each of the 144 heads is removed alone (rows). Red is an increase, blue a decrease. Heads in layers 0–8 are omitted as columns because none of them responds by more than 0.05. n = 600 prompts. Data: `figures/data.json` (the fifteen largest entries).*

The largest entries are the chain the circuit predicts: removing 9.9 raises 10.7 by 1.23; removing S-inhibition head 8.6 lowers 9.9 by 1.21 and raises 10.7 by 0.70; removing induction head 5.5 lowers 9.9 by 0.63; removing 10.7 lowers 11.10 by 0.59. Rows for the S-inhibition and induction heads have the same pattern of blue and red cells (lower the name movers, raise the negative name movers), which is what a two-step cascade looks like: the effect on the negative name movers passes through the name movers. With the final LayerNorm scale held at its intact value, 98.8% of the summed absolute interaction strength remains, so these are changes in what the heads write, not in how their output is normalised.

### 5.5 Attenuation (H3)

![Mean absolute log response ratio of activity for the next level and the level after it](figures/attenuation.png)

*Figure 4. GPT-2 small: mean absolute log response ratio of head activity at the next circuit level (blue) and the level after it (orange) when each level is removed as a set. n = 600 prompts. Data: `figures/data.json`.*

| Level removed | Next level | \|LRR\| | Level after next | \|LRR\| | Difference (95% CI) | Logit difference after removal |
|---|---|---|---|---|---|---|
| L1 previous-token | L2 duplicate + induction | 0.103 | L3 S-inhibition | 0.026 | +0.077 (0.073–0.081) | 3.39 |
| L2 duplicate + induction | L3 S-inhibition | 0.487 | L4 name mover | 0.343 | +0.144 (0.127–0.161) | 0.31 |
| L3 S-inhibition | L4 name mover | 0.237 | L5 negative name mover | 0.211 | +0.026 (0.016–0.040) | 0.40 |

The response is larger one level down than two levels down in all three cases, and the bootstrap interval excludes zero in all three; H3 is confirmed. The size of the attenuation differs. Removing the previous-token heads changes the induction heads (LRR −0.31 for 5.8 and −0.17 for 6.9) and leaves the S-inhibition heads within 5%, and it costs only 7% of the logit difference. The third comparison is close: removing the S-inhibition heads lowers the activity of 9.9 and 9.6 by 30% (LRR −0.36 and −0.35) and leaves 10.0 unchanged, while 10.7 and 11.10 fall by 21% and 17%. Nearly every activity response is a decrease: removing a level lowers the output of the heads downstream of it. The exceptions are small and all follow the removal of the previous-token heads (induction head 5.9 +8%, S-inhibition heads 7.9 and 8.10 +2% and +1%). No level shows release in the sense of H1; in this circuit, release is a property of the heads that read the name movers' output, not of the heads that feed them.

### 5.6 Other models (H4)

![Compensation of the top three heads in five models](figures/compensation_by_model.png)

*Figure 5. Compensation (1 − TE/DE) when the three heads with the largest positive direct effect are mean-ablated together, with 95% bootstrap intervals. 0 is no compensation; 1 is full compensation. n = 600 prompts per model. Data: `figures/data.json`.*

| Model | IO preferred | Mean logit difference | Top three heads | DE removed | TE | Compensation (95% CI) | Share through LayerNorm |
|---|---|---|---|---|---|---|---|
| GPT-2 small | 0.990 | 3.65 | 9.9, 9.6, 10.0 | 4.76 | −0.20 | 1.042 (1.023–1.061) | 0.058 |
| GPT-2 medium | 1.000 | 3.87 | 19.1, 15.14, 20.6 | 1.68 | 1.58 | 0.058 (0.041–0.076) | 0.23 |
| Pythia-160M | 0.978 | 3.99 | 8.9, 8.10, 8.2 | 3.11 | 2.27 | 0.269 (0.241–0.295) | 0.15 |
| Pythia-410M | 1.000 | 3.38 | 11.4, 18.8, 17.10 | 2.09 | 1.23 | 0.411 (0.391–0.432) | 0.03 |
| Pythia-1.4B | 0.998 | 3.89 | 10.7, 15.15, 13.1 | 1.81 | 1.80 | **0.009 (−0.023 to 0.037)** | – |

All five models pass the competence gate. Four show compensation with an interval above zero; Pythia-1.4B does not. Removing its three largest heads costs 1.80 of their 1.81 units of direct effect: the rest of the model restores 1%, and the interval includes zero. H4 is refuted.[^h4] The magnitude varies by a factor of more than a hundred among competent models, from none (Pythia-1.4B) through 6% (GPT-2 medium) and 27–41% (the two smaller Pythias) to 104% (GPT-2 small), with no order by model size within either family: the smallest GPT-2 compensates most and the smallest Pythia less than the next size up. The share that runs through the final LayerNorm scale ranges from 3% to 23% where it is defined (it is not defined for Pythia-1.4B, whose offset is approximately zero).

### 5.7 Development (H5)

![Compensation and competence across Pythia-410M training checkpoints](figures/checkpoints.png)

*Figure 6. Pythia-410M at eleven training checkpoints. Top: compensation of the top three heads, re-selected at each checkpoint, with 95% intervals (shaded, narrower than the line at most points), for the nine checkpoints that pass the competence gate. Bottom: mean logit difference; hollow red points fail the gate. n = 600 prompts per checkpoint. Data: `figures/data.json`.*

| Step | IO preferred | Mean logit difference | Top three heads | Compensation (95% CI) |
|---|---|---|---|---|
| 1,000 | 0.407 | −0.23 | – | fails gate |
| 2,000 | 0.473 | −0.17 | – | fails gate |
| 4,000 | 0.828 | 1.55 | 11.4, 13.5, 12.0 | −0.870 (−0.900 to −0.839) |
| 8,000 | 0.988 | 3.90 | 11.4, 13.5, 17.6 | −0.417 (−0.444 to −0.394) |
| 16,000 | 0.982 | 3.27 | 11.4, 13.5, 17.6 | 0.057 (0.035–0.079) |
| 32,000 | 0.993 | 3.13 | 11.4, 13.5, 17.6 | 0.367 (0.347–0.386) |
| 48,000 | 0.998 | 3.44 | 11.4, 17.6, 13.5 | 0.281 (0.258–0.301) |
| 64,000 | 0.998 | 3.27 | 11.4, 18.8, 17.10 | 0.379 (0.359–0.399) |
| 96,000 | 1.000 | 3.40 | 11.4, 18.8, 17.10 | 0.433 (0.414–0.451) |
| 128,000 | 1.000 | 3.36 | 11.4, 18.8, 17.10 | 0.429 (0.409–0.448) |
| 143,000 | 1.000 | 3.38 | 11.4, 18.8, 17.10 | 0.411 (0.391–0.432) |

Over the nine checkpoints that pass the gate, the Spearman correlation between training step and compensation is 0.92 (95% CI 0.88–0.93); H5 is confirmed.[^spearman] The development has a feature H5 did not anticipate. At the first two competent checkpoints compensation is strongly *negative*: at step 4,000, removing the top three heads costs 1.87 times their direct effect, and at step 8,000, 1.42 times. The rest of the model at that stage does not compensate for the loss; it amplifies it, the pattern [Rushing & Nanda 2024](#references) call downstream breakage. Compensation crosses zero between steps 8,000 and 16,000 and reaches about 0.4 by step 32,000, after which it changes little. The IOI behaviour itself is complete by step 8,000 (99% of prompts), so at that checkpoint the model solves the task with a circuit that fails more than proportionally when its top heads are removed. The identities of the top heads change as [Tigges et al 2024](#references) observed: 11.4 is among them from step 2,000 on, while 18.8 and 17.10 replace 13.5 and 17.6 between steps 48,000 and 64,000. The final checkpoint reproduces the independent Pythia-410M measurement of §5.6 exactly (0.411), as it should, since it is the same model.

### 5.8 Part B: dropout and self-repair (H6, H6c)

The timing run (§4.4) measured 173,971, 172,450, and 173,219 training tokens per second for the no-dropout, standard, and DropHead arms on a Colab A100; the slowest arm trains 207 million tokens in 20 minutes, which fixed the budget at 200 million tokens (6,103 steps, 42% of one pass over the 474 million training tokens) before the sweep was registered. All eighteen runs of sweep `fhuassaa` finished on one A100 in 21 minutes each (1,226–1,238 s of training); none crashed and none was repeated.[^points] Each model has 30.0 million parameters, 19.3 million of them in the tied embedding.

![Pooled self-repair fraction during training, by regime](figures/partb_development.png)

*Figure 7. Pooled self-repair fraction (the share of a resample-ablated head's direct effect that the rest of the model restores) at initialisation and after each eighth of training, mean of six seeds per regime. n = 65,536 held-out token positions per measurement. Data: `figures/data.json`; runs in sweep `fhuassaa`.*

![Final pooled self-repair fraction for each run, joined by seed](figures/partb_final.png)

*Figure 8. Final pooled self-repair fraction of each of the eighteen models. Grey lines join the three models of one seed, which share initialisation and data order; black bars are the means. Data: `figures/data.json`.*

| Regime | Pooled self-repair, mean (sd, range) | Validation loss, mean (sd) |
|---|---|---|
| no dropout | 0.359 (0.032, 0.298–0.388) | 1.6117 (0.0015) |
| standard dropout 0.1 | 0.615 (0.016, 0.592–0.632) | 1.6592 (0.0019) |
| DropHead 0.1 | 0.670 (0.019, 0.642–0.691) | 1.6256 (0.0015) |

| Contrast (paired by seed, n = 6) | Pooled self-repair, mean difference | 95% CI | Seeds positive | Validation loss, mean difference |
|---|---|---|---|---|
| standard − none | **+0.256** | +0.231 to +0.281 | 6 / 6 | +0.048 |
| DropHead − standard | **+0.055** | +0.045 to +0.065 | 6 / 6 | −0.034 |
| DropHead − none | +0.311 | +0.289 to +0.333 | 6 / 6 | +0.014 |
| standard − none, at matched validation loss (H6c) | **+0.251** | +0.226 to +0.276 | 6 / 6 | – |
| DropHead − none, at matched validation loss (H6c) | **+0.309** | +0.284 to +0.333 | 6 / 6 | – |

Both registered contrasts of H6 are positive for all six seeds, with intervals that exclude zero, and the order is the predicted one: none < standard < DropHead. Standard dropout raises the share of a removed head's function that the rest of the model restores from 36% to 62%, a factor of 1.7; head dropout raises it to 67%. The seed-to-seed standard deviation of the no-dropout arm (0.032) is an eighth of the standard-dropout effect, and six of six is the most extreme sign count possible with six units (two-sided sign-test p = 0.031). H6 is confirmed.

H6c is confirmed as well, and the matching is close. Every standard-dropout model's final validation loss (1.656–1.661) is nearest to the no-dropout run of the same seed at step 4,577, three-quarters of the way through training, where that run's loss is 1.655–1.659; every DropHead model's (1.623–1.627) is nearest to step 5,340, where it is 1.625–1.630. At those matched points the differences are +0.251 and +0.309, within 0.005 of the unmatched ones: the no-dropout models had long since stopped gaining self-repair (Figure 7; their mean moves from 0.356 to 0.359 over the last half of training), so comparing them earlier changes nothing. Head dropout supplies a second argument against the undertraining explanation from the other direction: it has *lower* validation loss than standard dropout on every seed (by 0.034 on average) and *higher* self-repair.

The development curves show where the difference arises. At initialisation all three regimes measure 0.008, the value expected of a network whose heads have not specialised. After the first 25 million tokens they have separated (0.27, 0.37, 0.44), and from there the no-dropout models level off near 0.36 by 100 million tokens while the two dropout regimes continue to rise through the end of training. Dropout does not create the compensation, which reaches 0.27 without it; it continues to build it after the no-dropout models have stopped.

The secondary, unweighted measure (the mean over heads of each head's own fraction) gives the same order and the same six-of-six sign counts, but its values are smaller and less stable (0.11, 0.48, 0.56 for the three regimes; standard − none +0.37, 95% CI +0.26 to +0.47). It weights a head whose removal changes almost nothing the same as one that changes much, and heads of the first kind have fractions dominated by noise, often negative; the pooled measure was registered as primary for that reason.

## 6. Discussion

### 6.1 Verdicts

| | Prediction | Outcome | Verdict |
|---|---|---|---|
| H1 | Removing the name movers is compensated (c > 0); backup and negative name movers carry at least half of the offset | c = 1.042 (1.023–1.061); 94.5% of the offset | confirmed |
| H2 | S-inhibition and at least one induction/duplicate head are keystones; the name movers are not, and have CI < 1 | all four S-inhibition, three induction, one duplicate head are keystones; no name mover is; 10.0 has CI 1.51 | confirmed except the CI < 1 clause (1 of 3 heads) |
| H3 | The activity response is larger one level down than two, for three removals | larger in all three, intervals exclude zero | confirmed |
| H4 | Every competent model compensates | four of five; Pythia-1.4B 0.009 (−0.023 to 0.037) | refuted |
| H5 | Compensation rises with training in Pythia-410M | Spearman ρ 0.92 (0.88–0.93), p = 0.0013; negative until step 8,000 | confirmed |
| H6 | Self-repair: none < standard dropout < DropHead | 0.359 < 0.615 < 0.670; both contrasts 6 / 6 seeds | confirmed |
| H6c | The order holds at matched validation loss | +0.251 and +0.309, 6 / 6 seeds | confirmed |

### 6.2 What the ecological measures contributed

The ecological vocabulary would be decoration if every quantity it named were already a standard interpretability quantity under another name. Four comparisons bear on that.

*Community importance* is total effect divided by abundance, and total effect is what an ablation already measures. The division is what changes the reading. Ranked by the share of the logit difference lost on removal, the most important heads in GPT-2 small are S-inhibition head 8.6, S-inhibition head 8.10, induction head 5.5, and S-inhibition head 7.9; ranked by direct effect, they are 9.9, 10.7, 9.6, and 11.10. CI names the relation between the two lists: the heads at the top of the first are those whose effect is out of proportion to what they write to the output, and a ranking by either quantity alone does not identify them as a class. The measure has a defect in this setting that it also has in ecology: when abundance approaches zero, CI grows without bound (145,070 for 3.0), and the registered criterion had to require a minimum effect as well as a minimum CI. Its sign convention was more useful than expected. Power et al anticipated negative values for "a consumer" of the measured trait, and the four heads with negative values, 10.7, 11.10, 11.2, and 5.10, are the heads that reduce the logit difference, including 10.7, which [McDougall et al 2024](#references) identified by other means as a copy-suppression head.

*Mesopredator release* and *interaction strength* correspond to quantities interpretability already uses: the change in a head's effect after a removal is the quantity [Gong et al 2026](#references) use to find backup heads, and [Wang et al 2022](#references) found the backup name movers by the same measurement. The ecological framing adds a prediction about direction rather than a new measurement: a release is an increase in a population held down by the removed species, and the heads that increased (Figure 1) are those the name movers held down, the backups whose output they duplicate and the negative name movers whose input they supply. The layers that feed the name movers showed no release at all (§5.5), which is also what the ecological definition requires.

The *log response ratio* made H3 testable. Activity has no common scale across heads in different positions and layers; the log ratio of activity after and before a removal is unit-free, symmetric in increase and decrease, and comparable across levels, which is the reason [Hedges et al 1999](#references) recommend it. With it, the attenuation that [Shurin et al 2002](#references) found across 102 ecological experiments appears in all three steps of the IOI circuit. Two of the three differences are large and one, from the S-inhibition heads to the name movers and then to the negative name movers, is small (0.237 against 0.211), and the comparison uses only one circuit, so this is a demonstration that the measure applies rather than a finding about transformers in general.

The *insurance hypothesis* supplied the one causal prediction, and the prediction held. [Yachi & Loreau 1999](#references) argue that variable conditions during the assembly of a community select for species that can replace one another. Dropout and head dropout are variable conditions of exactly that kind, the random absence of components during training, and they produce models whose remaining components restore more of what is removed, with the stronger form of variability (whole heads absent) producing more. Head dropout differs from standard dropout in the unit it removes, and it is the one that matches the unit of the removal experiment; that it has the larger effect is consistent with the redundancy being specific to what was removed during training.

### 6.3 On the dropout conjecture

[Wang et al 2022](#references) wrote that compensation "is caused by the use of dropout during training". The Part B results support a version of that statement and not the statement as written. Dropout is not necessary: models trained without it restore 36% of a removed head's direct effect, the Pythia models of Part A, trained without dropout, compensate by 27%, 41%, and 1%, and McGrath et al found the effect in a Chinchilla model trained without it. Dropout is a strong amplifier: under identical data, initialisation, and budget it raises the restored share by 26 percentage points, and does so at every seed. The Part A models cannot test this on their own, because they differ in everything, and GPT-2 small's overcompensation (1.04) beside GPT-2 medium's 0.06, from the same published training setup, shows how much varies between models trained the same way.[^gpt2dropout] The present result also bears on the explanation of [Rohweder et al 2026](#references), in which the Hydra effect follows from the structure of the training data and the geometry of gradient descent with no role for dropout: that account can explain the compensation present without dropout, and it does not predict the difference between the arms here, which share data and optimiser.

### 6.4 Threats to validity

- **One task for the removal experiments.** H1–H3 rest on the IOI circuit of one model, the best-studied circuit in the literature and therefore the one where head classes could be named in advance. The five-model and checkpoint studies use the same task. Whether keystones and attenuation appear with the same regularity on other tasks is unmeasured.
- **Three heads for H4 and H5.** Compensation was measured for the top three heads by direct effect. The refutation of H4 is a refutation for that selection; Pythia-1.4B might compensate for a different set.
- **Mean ablation.** Part A replaces a head's output with its mean over ABC prompts. Resample ablation gave the same answer for H1 (0.997 against 1.042), and was not run for the other hypotheses.
- **Part B is one model size, one dataset, one dropout rate.** The models are 30 million parameters, trained on 200 million tokens of simple stories at p = 0.1. The effect is large relative to its interval, but its size at other scales, rates, and data is unknown.
- **The self-repair measure includes normalisation.** Part B computes the removed head's change in direct effect with the intact run's LayerNorm scale, so compensation through the final LayerNorm counts as self-repair, as registered. How much of the dropout difference runs through normalisation rather than through other heads was not separated.
- **Matched validation loss is matched to within one-eighth of training.** H6c compares with the nearest of nine measurement points, and the nearest points differ from the dropout models' loss by at most 0.006. The no-dropout self-repair changes by less than 0.01 over the last half of training, so a finer match would not change the result; it was not run.
- **The ecological correspondence is a correspondence of measures, not of systems.** A forward pass has no feedback, no time, and no equilibrium (§1.3). Nothing here shows that transformers are ecosystems; it shows that four measures designed for ecosystems give interpretable, and in one case falsifiable, answers when applied to heads.

## 7. Further work

1. Separate the dropout effect into the part carried by other heads and the part carried by the final LayerNorm, by recomputing Part B's ΔDE with the ablated run's scale.
2. Repeat Part B at a second model size and a second dropout rate, to see whether the effect scales with the rate as the insurance hypothesis suggests.
3. Remove heads during training in a pattern other than random (always the same heads, or heads chosen by importance) to test whether the redundancy is specific to the components removed.
4. Apply community importance to the heads of Pythia-1.4B with other selections, to find where, if anywhere, its compensation is.
5. Measure keystones and attenuation on a second circuit with named components, such as the greater-than circuit of GPT-2 small, one of those [Conmy et al 2023](#references) recover automatically, to test whether the results of §5.3–5.5 are properties of IOI.

## 8. Reproduction

- **Code and data preparation:** [github.com/kvenanzi/trophic-cascade](https://github.com/kvenanzi/trophic-cascade). Numbered scripts take the prompts, models, and TinyStories to every table and figure; `notebooks/01_part_a.ipynb` and `notebooks/02_dropout_sweep.ipynb` run them on Colab. The hypotheses are in commit `cca53fc`, which precedes every registered run.
- **Every run:** the W&B project [within-noise/trophic-cascade](https://wandb.ai/within-noise/trophic-cascade) holds the Part A runs (reference set on the A100; the local replication tagged `local-gtx1070`), the eighteen Part B runs of sweep `fhuassaa` with their measurement tables and model weights, and the artifacts `gpt2-removals`, `models-*`, `checkpoints-pythia-410m`, and `measurements-*` from which every number here was computed. The [W&B Report](https://wandb.ai/within-noise/trophic-cascade/reports/Trophic-cascades-in-a-transformer--VmlldzoxODAwMjk2OA==) presents them with live panels.

<!-- qmd
::: {.column-page-right}
```{=html}
<iframe src="https://wandb.ai/within-noise/trophic-cascade/reports/Trophic-cascades-in-a-transformer--VmlldzoxODAwMjk2OA=="
        title="W&B Report: Trophic cascades in a transformer"
        loading="lazy" style="border:none;width:100%;height:900px"></iframe>
```
:::
-->

## Appendix A: Experiment log

All work was done on 2026-09-24 and 2026-09-25. Times are US Central; run identifiers are W&B run IDs in `within-noise/trophic-cascade`.

- **Scaffold** (commit `dd89807`, 17:13). Prompt generator, removal runner, ecological measures, and unit tests, including one that checks the per-component direct effects sum to the logit difference.
- **Reproduction check** (before 17:17). GPT-2 small's baseline on an earlier draft of the prompt set, whose ABC twins kept the first-clause names. Mean-ablating the name movers raised the logit difference from 3.65 to 3.85. This is the one observation that preceded the registration; the ABC prompts were then changed to replace all three names, as Wang et al do.
- **Pre-registration** (commit `cca53fc`, 17:17). §1–4 of this document. Three phrases in §1–2 were later reworded to remove figures of speech, without changing any prediction or criterion; the registered text is in that commit.
- **Local Part A** (17:19–17:26, GTX 1070). Runs `h1kfojqs` (GPT-2 small, H1–H3) and `hac0rg6h`, `avw4uanu`, `3q9faf3q`, `4uezvu5d` (four models, H4). The W&B key on the local machine had lost access, so these ran offline and were uploaded later. Pythia-1.4B could not be loaded (host memory); two attempts were stopped by the operating system and discarded.
- **Colab Part A** (18:30–18:43, A100). `iiltnel1` (GPT-2 small), `rjc6ndi6`, `ke9tk0qt`, `of54j7j7`, `dnxf74lk`, `esc71gqc` (five models), `3zy48ays` (H4 summary). Every quantity agreed with the local runs to the fifth decimal place.
- **Checkpoint loading fix** (commit `1f1ff71`, 18:37). The first checkpoint run failed: TransformerLens 3.9 sends an empty Hugging Face token for Pythia checkpoints when none is set, which the HTTP client rejects. Checkpoints are now downloaded with `transformers` and passed to TransformerLens. The failed run, which had logged nothing, was deleted.
- **H5** (18:39–18:43). Eleven checkpoint runs, `0oekew7f` through `ci6uf154`, and the summary `bngnyxjp`.
- **Part B smoke and timing** (19:01, 19:12). `5gnva5ju` (DropHead, 40 steps on the real data, every stage of the pipeline); `fmdm39r6` (timing; budget 200 million tokens).
- **Sweep** `fhuassaa` (registered after the timing run; runs 20:15 to 02:32). The first Colab session ended for inactivity before the agent had started, and no cell had been issued; the agent was started in a new session. Runs in order: `ryqgyaml`, `b08p7lt5`, `r9l9uae6`, `3tfis5fz`, `evackiyh`, `7j3yqh5d` (none, seeds 0–5); `zsyblp32`, `z3jlfpko`, `z7oqo7od`, `7b5nmdi5`, `aoja09w6`, `wgxi6q2o` (standard); `jlnsa7xj`, `5o6hsruz`, `6j67iu7u`, `k6zpon6c`, `dpxouw3m`, `d59he38q` (DropHead). 18 of 18 finished.

## Appendix B: Decisions

| Decision | Reason |
|---|---|
| Hypotheses committed before the registered runs, with the one prior observation stated | A result cannot confirm a hypothesis written after it |
| One prompt set for every model, with names, places, and objects that are single tokens under both tokenizers | Differences between models cannot come from differences in prompts |
| ABC twins replace all three names | Wang et al's reference distribution; keeping the first-clause names would leave part of the information the circuit uses |
| Mean ablation as the primary removal, resample ablation as a check | Mean ablation is Wang et al's; the check shows the H1 conclusion does not depend on it |
| Direct effect relative to the mean-ablated value | A removed head's direct effect is then exactly zero, so "what was removed" is well defined |
| Direct effect reported with both the run's own and the intact LayerNorm scale | Separates changes in what heads write from changes in normalisation |
| Keystone criterion requires a 5% effect as well as \|CI\| ≥ 2 | CI grows without bound as abundance approaches zero |
| Activity, and its log response ratio, for H3 | Direct effect is near zero for heads upstream of the output; activity is defined for every head |
| Top three heads chosen by direct effect for H4 and H5 | No hand-labelled circuit exists for the other models, and the selection must not depend on the result |
| Competence gate (80% of prompts, mean logit difference 1.0) | Compensation is undefined for a model that does not perform the task |
| Part B trains Hugging Face GPT-2 and measures in TransformerLens | TransformerLens has no dropout; its GPT-2 conversion makes the measurement identical to Part A's |
| Head dropout as a pre-hook on the output projection | The projection's input is the concatenation of the heads' outputs, so a per-head mask is exact |
| Seed fixes initialisation and data order | The three arms of a seed differ only in the regime, so the analysis can be paired |
| Measurement inside the training job, at nine points | Gives the development curves and the H6c checkpoints without storing 162 models |
| Token budget from a timing run under a rule fixed in advance | The budget cannot be chosen after seeing results |
| Pooled self-repair fraction as primary | The unweighted mean over heads is dominated by heads whose removal changes little |
| Every experiment on Colab, the local machine for code and small checks | Loading Pythia-1.4B exceeded the local memory and ended the session |
| Part A repeated on two machines | Agreement to the fifth decimal place shows the numbers do not depend on the hardware |

## References

- Abrams PA (2009). "When does greater mortality increase population size? The long history and diverse mechanisms underlying the hydra effect". *Ecology Letters* 12(5):462–474. [doi:10.1111/j.1461-0248.2009.01282.x](https://doi.org/10.1111/j.1461-0248.2009.01282.x)
- Bender EA, Case TJ, Gilpin ME (1984). "Perturbation Experiments in Community Ecology: Theory and Practice". *Ecology* 65(1):1–13. [doi:10.2307/1939452](https://doi.org/10.2307/1939452)
- Berlow EL, Navarrete SA, Briggs CJ, Power ME, Menge BA (1999). "Quantifying variation in the strengths of species interactions". *Ecology* 80(7):2206–2224. [doi:10.1890/0012-9658(1999)080[2206:QVITSO]2.0.CO;2](https://doi.org/10.1890/0012-9658(1999)080[2206:QVITSO]2.0.CO;2)
- Borer ET, Seabloom EW, Shurin JB, Anderson KE, Blanchette CA, Broitman B, Cooper SD, Halpern BS (2005). "What determines the strength of a trophic cascade?" *Ecology* 86(2):528–537. [doi:10.1890/03-0816](https://doi.org/10.1890/03-0816)
- Carpenter SR, Kitchell JF, Hodgson JR (1985). "Cascading Trophic Interactions and Lake Productivity". *BioScience* 35(10):634–639. [doi:10.2307/1309989](https://doi.org/10.2307/1309989)
- Conmy A, Mavor-Parker AN, Lynch A, Heimersheim S, Garriga-Alonso A (2023). "Towards Automated Circuit Discovery for Mechanistic Interpretability". *Advances in Neural Information Processing Systems 36*. [arxiv.org/abs/2304.14997](https://arxiv.org/abs/2304.14997)
- Crooks KR, Soulé ME (1999). "Mesopredator release and avifaunal extinctions in a fragmented system". *Nature* 400:563–566. [doi:10.1038/23028](https://doi.org/10.1038/23028)
- Eldan R, Li Y (2023). "TinyStories: How Small Can Language Models Be and Still Speak Coherent English?" *arXiv preprint arXiv:2305.07759*. [arxiv.org/abs/2305.07759](https://arxiv.org/abs/2305.07759)
- Elhage N, Nanda N, Olsson C, Henighan T, Joseph N, Mann B, Askell A, Bai Y, Chen A, Conerly T, DasSarma N, Drain D, Ganguli D, Hatfield-Dodds Z, Hernandez D, Jones A, Kernion J, Lovitt L, Ndousse K, Amodei D, Brown T, Clark J, Kaplan J, McCandlish S, Olah C (2021). "A Mathematical Framework for Transformer Circuits". *Transformer Circuits Thread*. [transformer-circuits.pub/2021/framework/index.html](https://transformer-circuits.pub/2021/framework/index.html)
- Estes JA, Palmisano JF (1974). "Sea Otters: Their Role in Structuring Nearshore Communities". *Science* 185(4156):1058–1060. [doi:10.1126/science.185.4156.1058](https://doi.org/10.1126/science.185.4156.1058)
- Gong Z, Lu H, Wang T, Zhang Y, Wang Y, Zeng Z, Xiao M, Yuen C, Lim WYB (2026). "Conditional Co-Ablation: Recovering Self-Repair Backups in Transformer Circuits". *arXiv preprint arXiv:2607.01940*. [arxiv.org/abs/2607.01940](https://arxiv.org/abs/2607.01940)
- Hairston NG, Smith FE, Slobodkin LB (1960). "Community Structure, Population Control, and Competition". *The American Naturalist* 94(879):421–425. [doi:10.1086/282146](https://doi.org/10.1086/282146)
- Hedges LV, Gurevitch J, Curtis PS (1999). "The meta-analysis of response ratios in experimental ecology". *Ecology* 80(4):1150–1156. [doi:10.1890/0012-9658(1999)080[1150:TMAORR]2.0.CO;2](https://doi.org/10.1890/0012-9658(1999)080[1150:TMAORR]2.0.CO;2)
- Heimersheim S, Nanda N (2024). "How to use and interpret activation patching". *arXiv preprint arXiv:2404.15255*. [arxiv.org/abs/2404.15255](https://arxiv.org/abs/2404.15255)
- Kesselman RF (2008). "Verbal Probability Expressions in National Intelligence Estimates: A Comprehensive Analysis of Trends from the Fifties through Post 9/11". *Master's thesis, Mercyhurst College*. [files.ethz.ch/isn/55739/kesselman_thesis_final.pdf](https://www.files.ethz.ch/isn/55739/kesselman_thesis_final.pdf)
- Lafferty KD, Suchanek TH (2016). "Revisiting Paine's 1966 Sea Star Removal Experiment, the Most-Cited Empirical Article in the American Naturalist". *The American Naturalist* 188(4):365–378. [doi:10.1086/688045](https://doi.org/10.1086/688045)
- McDougall C, Conmy A, Rushing C, McGrath T, Nanda N (2024). "Copy Suppression: Comprehensively Understanding a Motif in Language Model Attention Heads". *Proceedings of the 7th BlackboxNLP Workshop*:337–363. [arxiv.org/abs/2310.04625](https://arxiv.org/abs/2310.04625)
- McGrath T, Rahtz M, Kramár J, Mikulik V, Legg S (2023). "The Hydra Effect: Emergent Self-repair in Language Model Computations". *arXiv preprint arXiv:2307.15771*. [arxiv.org/abs/2307.15771](https://arxiv.org/abs/2307.15771)
- Nanda N, Bloom J (2022). "TransformerLens". [github.com/TransformerLensOrg/TransformerLens](https://github.com/TransformerLensOrg/TransformerLens)
- Odum EP (1969). "The Strategy of Ecosystem Development". *Science* 164(3877):262–270. [doi:10.1126/science.164.3877.262](https://doi.org/10.1126/science.164.3877.262)
- Paine RT (1966). "Food Web Complexity and Species Diversity". *The American Naturalist* 100(910):65–75. [doi:10.1086/282400](https://doi.org/10.1086/282400)
- Paine RT (1969). "A Note on Trophic Complexity and Community Stability". *The American Naturalist* 103(929):91–93. [doi:10.1086/282586](https://doi.org/10.1086/282586)
- Paine RT (1992). "Food-web analysis through field measurement of per capita interaction strength". *Nature* 355:73–75. [doi:10.1038/355073a0](https://doi.org/10.1038/355073a0)
- Patrawala A, Feng J, Jones E, Steinhardt J (2026). "LLM Layers Immediately Correct Each Other". *arXiv preprint arXiv:2609.07876*. [arxiv.org/abs/2609.07876](https://arxiv.org/abs/2609.07876)
- Power ME, Tilman D, Estes JA, Menge BA, Bond WJ, Mills LS, Daily G, Castilla JC, Lubchenco J, Paine RT (1996). "Challenges in the Quest for Keystones". *BioScience* 46(8):609–620. [doi:10.2307/1312990](https://doi.org/10.2307/1312990)
- Radford A, Wu J, Child R, Luan D, Amodei D, Sutskever I (2019). "Language Models are Unsupervised Multitask Learners". *OpenAI technical report*. [cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)
- Ripple WJ, Beschta RL (2004). "Wolves and the Ecology of Fear: Can Predation Risk Structure Ecosystems?" *BioScience* 54(8):755–766. [doi:10.1641/0006-3568(2004)054[0755:WATEOF]2.0.CO;2](https://doi.org/10.1641/0006-3568(2004)054[0755:WATEOF]2.0.CO;2)
- Ripple WJ, Beschta RL (2012). "Trophic cascades in Yellowstone: The first 15 years after wolf reintroduction". *Biological Conservation* 145(1):205–213. [doi:10.1016/j.biocon.2011.11.005](https://doi.org/10.1016/j.biocon.2011.11.005)
- Rohweder J, Dutta S, Gurevych I (2026). "Hierarchical Latent Structures in Data Generation Process Unify Mechanistic Phenomena across Scale". *arXiv preprint arXiv:2603.06592*. [arxiv.org/abs/2603.06592](https://arxiv.org/abs/2603.06592)
- Rushing C, Nanda N (2024). "Explorations of Self-Repair in Language Models". *Proceedings of the 41st International Conference on Machine Learning (PMLR 235)*:42836–42855. [arxiv.org/abs/2402.15390](https://arxiv.org/abs/2402.15390)
- Shurin JB, Borer ET, Seabloom EW, Anderson K, Blanchette CA, Broitman B, Cooper SD, Halpern BS (2002). "A cross-ecosystem comparison of the strength of trophic cascades". *Ecology Letters* 5(6):785–791. [doi:10.1046/j.1461-0248.2002.00381.x](https://doi.org/10.1046/j.1461-0248.2002.00381.x)
- Tigges C, Hanna M, Yu Q, Biderman S (2024). "LLM Circuit Analyses Are Consistent Across Training and Scale". *Advances in Neural Information Processing Systems 37*. [arxiv.org/abs/2407.10827](https://arxiv.org/abs/2407.10827)
- Wang K, Variengien A, Conmy A, Shlegeris B, Steinhardt J (2022). "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small". *arXiv preprint arXiv:2211.00593 (ICLR 2023)*. [arxiv.org/abs/2211.00593](https://arxiv.org/abs/2211.00593)
- Yachi S, Loreau M (1999). "Biodiversity and ecosystem productivity in a fluctuating environment: the insurance hypothesis". *Proceedings of the National Academy of Sciences* 96(4):1463–1468. [doi:10.1073/pnas.96.4.1463](https://doi.org/10.1073/pnas.96.4.1463)
- Zhang F, Nanda N (2024). "Towards Best Practices of Activation Patching in Language Models: Metrics and Methods". *International Conference on Learning Representations (ICLR 2024)*. [arxiv.org/abs/2309.16042](https://arxiv.org/abs/2309.16042)
- Zhou W, Ge T, Wei F, Zhou M, Xu K (2020). "Scheduled DropHead: A Regularization Method for Transformer Models". *Findings of the Association for Computational Linguistics: EMNLP 2020*:1971–1980. [aclanthology.org/2020.findings-emnlp.178](https://aclanthology.org/2020.findings-emnlp.178/)

## Footnotes

[^conf]: Status and confidence tags follow the gwern.net convention, with the confidence word taken from the [Kesselman 2008](#references) scale. The document is tagged "likely" as a whole. The Part B result rests on six paired seeds and an effect eight times the seed-to-seed standard deviation, and is "highly likely" for this model size, data, and dropout rate; that the same holds at other scales is "possible". The GPT-2 small results (H1, H2) are "highly likely" for this circuit and prompt distribution: they were reproduced on two machines to the fifth decimal place, and H1 with two ablation methods. H3 rests on one circuit, and its third step is small (0.026). The refutation of H4 applies to the top-three selection that was registered.

[^points]: §4.5 registered measurement after each eighth of the budget; the implementation also measures at step 0, before any training, which gives nine points per run. The step-0 value is reported in Figure 7 and is not used by any test.

[^gpt2dropout]: GPT-2's use of dropout in pretraining is itself uncertain: the Hugging Face configuration sets dropout to 0.1, but the model code OpenAI released contains no dropout operations and the paper ([Radford et al 2019](#references)) does not say. The Part A contrast between GPT-2 and Pythia is therefore not a contrast between dropout and no dropout.

[^oom]: Pythia-1.4B could not be loaded on the local machine: TransformerLens's weight processing holds two copies of the weights in host memory, which exceeded the 15 GB available.

[^h4]: H4 was stated as a universal claim over the models that pass the gate, and one competent model without compensation refutes it. It is possible that compensation in Pythia-1.4B is carried by heads outside the top three, or appears for a different selection of heads; the registered test was the top three by direct effect, and the result is reported for that test.

[^spearman]: The interval resamples prompts, holding the eleven checkpoints fixed; it describes the uncertainty in each checkpoint's compensation, not the uncertainty that would come from a different choice of checkpoints. With nine points, a Spearman correlation of 0.92 has an exact permutation p-value of 0.0013 (two-sided, all 362,880 orderings).

[^hydra]: McGrath et al write that "the use of the name 'Hydra' is not completely mythologically accurate". The ecological hydra effect, an increase in a population following an increase in its mortality ([Abrams 2009](#references)), is closer to the overcompensation observed in §2 than the mythological one, in which two heads replace each one removed. The correspondence between ecological cascades and transformer components has been drawn informally before, for example in an undated essay on the Emberverse site ([emberverse.ai](https://emberverse.ai/stage3/the_trophic_cascade.html)), which reports no measurements.
