# genespeak 
## A genetic language for modeling real-time cellular dynamics

## Formal Language

A genome is a collection of rules represented by statements in a formal language. Each rule contains a condition-expression and an action-statement, and ensures that the action is carried out whenever the condition holds true. 

Each rule in a genome has an associated energy cost that is required in order to activate it. A system is thus limited to a finite number of active rules at any given time which influences it selects rules to become active. Selection is a probabilistic process determined by the entropy of the system. Whenever a rule becomes active, energy diffuses outward to adjacent rules in the genome, making them more likely to become active. This creates local stability wherein collections of nearby rules promote the activity of one another, leading the distinct operational "states" of the system.

## Genetic Constructs

A construct is a set of rules that are (in some way) functionally dependent on one another. The activation of rules within a given construct depends on the exact construct type. Each type has a unique method of selecting and inhibiting rules. The basic types of constructs are as follows: 

1) __Block__: executes rules concurrently until they all fail

2) __Sequence__: executes rules sequentially until one fails or they all succeed

3) __Selector__: executes rules sequentially until one succeeds or they all fail


Blocks are the simplest type of construct, representing spatial relations that cause rules to promote one another as a function of "nearness" in the genome. Unlike other constructs the order of rules in a block does not matter.

A sequence represents a multi-step task in which rules are triggered one-by-one until one of them fails or all of them succeed. Conversely a selector is a search process in which rules activate one-by-one until one of them succeeds or they all fail. 

Every construct has a "shelf life" dictated by the total energy required to maintain it (cost) along with its overall success rate (reward). Each time a construct is deemed successful, it releases a flux of energy that causes all currently-loaded constructs to "refresh". 

This creates stability through self-reinforcement where constructs deemed successful generate feedback signals that increase their ability to remain active.
