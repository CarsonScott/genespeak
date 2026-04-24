from .util import *
from .operation import Operation, convert
from .language import Language

_directory = os.path.dirname(os.path.abspath(__file__))
_lang_path = os.path.join(_directory, 'default.json')

LANGUAGE = Language.load(_lang_path)

def execute(*args, **kwargs):
  return LANGUAGE.execute(*args, **kwargs)

def validate(*args, **kwargs):
  return LANGUAGE.validate(*args, **kwargs)


'''
Low-Level Constructs:
  expression: (a > b);
  statement:  (a = b + 1);
  production: ((a > b) => (a = b + 1));

Blocks:
	1) Collection - An unordered set of statements that execute concurrently.
	2) Sequence - A set of statements that execute in order until one fails or all of them succeed.
	3) Selector - A set of statements that execute in order until one succeeds or all of them fail.

Collections are sets of objects with no logical structure, meaning they are largely independent of 
one another despite operating within a shared super-structure. The permanence of a given collection
is equivalent to the sum-permanences of its components.

Sequences are used to perform step-by-step tasks. They respond positively only if every step has 
succeeded, meaning they trigger a flux of energy that reinforces their structural wellbeing within
the system. Otherwise, like all genetic constructs, they decay out of existence through diffusion
of matter and energy.

Selectors are different in that they search for a singular valid task in response to a given state.
Whatever task responds first to a given state is selected for execution, effectively halting the 
search for alternatives. The selector thus reinforces itself when a single task becomes active
from its set of possibilities.

Selectors containing all production-rules function exactly like chains of if-then-else statements.
Blocks exists functionally outside the scope of formal language, with dynamics that do not translate
directly to expressions/statements.


* All genetic constructs have a "shelf life" which is dictated by the energy required to maintain 
  the physical structure along with the average rate of "returns" it generates.These are fluxes of 
  energy resulting from the successful execution of a construct to completion. This diffusion of
  energy strengthens active structures and thus reinforces those structures which brought it about.
  This keeps genetic constructs alive that "justify" their own existence by paying off their "debt"
  faster than they can be destroyed. 

  If a construct is unable to generate enough energy to sustain itself over a period of time (or if
  the context in which it is active does not provide enough support), it decays into "precursors", or 
  non-functional physical components, and any amount of energy that
  was used to maintain its structure.


'''
