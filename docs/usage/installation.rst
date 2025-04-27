Installation
============

Requirements
-----------

Pathfinder requires Python 3.7 or higher. It also depends on the following packages:

* pyyaml>=6.0
* click>=8.0.0 (for CLI interface)

Installing from Source
--------------------

To install Pathfinder from source, clone the repository and install using pip:

.. code-block:: bash

    git clone https://github.com/yourusername/pathfinder.git
    cd pathfinder
    pip install -e .

This will install Pathfinder in development mode, allowing you to make changes to the code and have them immediately reflected in the installed package.

Using Requirements File
---------------------

Alternatively, you can install the required dependencies using the provided requirements.txt file:

.. code-block:: bash

    pip install -r requirements.txt
