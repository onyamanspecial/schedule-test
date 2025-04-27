Quickstart
==========

Basic Usage
----------

Pathfinder provides two main modes of operation: pathfinder and optimizer.

Pathfinder Mode
~~~~~~~~~~~~~~

The pathfinder mode helps you find a sequence of ingredients to achieve desired effects:

.. code-block:: bash

    python main.py 1 -d "Calming" "Energizing"

This will find a path to achieve both the "Calming" and "Energizing" effects. You can also use effect numbers instead of names:

.. code-block:: bash

    python main.py 1 -d 5 10

To see a list of all available effects:

.. code-block:: bash

    python main.py 1 --list

Optimizer Mode
~~~~~~~~~~~~~

The optimizer mode helps you find the most profitable combination of ingredients for different drug types:

.. code-block:: bash

    python main.py 2 --type 1 --depth 3

This will find the most profitable combination for marijuana (type 1) with a maximum of 3 ingredients.

Options:

* ``--type``: Drug type (1=marijuana, 2=meth, 3=cocaine)
* ``--strain``: Marijuana strain (1-5)
* ``--depth``: Maximum number of ingredients
* ``--grow-tent``: Use a grow tent (marijuana/cocaine)
* ``--pgr``: Use plant growth regulators (marijuana/cocaine)
* ``--quality``: Meth quality (1=low, 2=medium, 3=high)
