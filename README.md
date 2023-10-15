# noble-tools
Contains various small programs for finding noble polyhedra. Depends on numpy and matplotlib.

## Tools
The following programs are meant to be used as tools; all others help support these.
* **plot1D.py** : Meant for making 1D graphs to find critical points.
* **plot2D.py** : Meant for creating 2D graphs to find critical curves.
* For solving nobles in 1D, run these programs in order:
  * **export1D.py**
  * **intersect1D.py**
  * **solve1D.py**
    * **solvepyritohedral.py** when working with truncated cube or small rhombicuboctahedral armies, as these armies have special pyritohedral subsymmetries.
  * ## Always make sure to configure the two python files with the correct armies and symmetries before running!

## Todo
* Finish 2D search