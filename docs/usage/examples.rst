Examples
========

Pathfinder Examples
-----------------

Finding a Path to Multiple Effects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python main.py 1 -d "Calming" "Energizing" "Glowing"

Output::

    Path: Mega Bean → Paracetamol → Addy → Mega Bean

    Achieved effects:
    * Calming
    * Energizing
    * Foggy
    * Glowing

    Total ingredients: 4
    Total effects: 4
    Desired effects achieved: 3 / 3

Starting with Initial Effects
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python main.py 1 -d "Calming" "Energizing" -s "Foggy"

Output::

    Path: Paracetamol → Addy

    Achieved effects:
    * Calming
    * Energizing
    * Sneaky
    * Thought-Provoking

    Total ingredients: 2
    Total effects: 4
    Desired effects achieved: 2 / 2

Optimizer Examples
----------------

Finding the Most Profitable Marijuana Combination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python main.py 2 --type 1 --strain 1 --depth 3

Output::

    Best Combination for marijuana:
    Production Cost: $12.50
    Ingredients: Cuke, Mega Bean, Viagra
    Ingredient Cost: $14.67
    Total Cost: $27.17
    Total Value: $110.00
    Profit: $82.83
    Effects: Foggy, Tropic Thunder, Glowing, Cyclopean
    Recipe: Cuke → Mega Bean → Viagra

Finding the Most Profitable Meth Combination
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python main.py 2 --type 2 --quality 3 --depth 4

Output::

    Best Combination for meth:
    Production Cost: $24.00
    Ingredients: Banana, Cuke, Horse Semen, Mega Bean
    Ingredient Cost: $20.00
    Total Cost: $44.00
    Total Value: $210.00
    Profit: $166.00
    Effects: Foggy, Electrifying, Long faced, Cyclopean
    Recipe: Banana → Cuke → Horse Semen → Mega Bean
