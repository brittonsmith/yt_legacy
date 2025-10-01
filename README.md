# yt_legacy

This is a yt extension for loading various simulation data associated
with the legacy simulation project. This defines some subclasses of yt
datasets for

 * Gadget snapshots
 * Gadget halo catalogs
 * consistent-trees hlist halo catalogs

It is not recommended to use this unless you know you are working with
data from the "Legacy Simulations".

## Installation

The yt_legacy extension must be installed from source.

1. Clone the repository:

```
$ git clone https://github.com/brittonsmith/yt_legacy
```

2. Install using pip:

```
$ cd yt_legacy
$ pip install .
```

To install an editable install (for development), add the "-e" flag.
```
$ pip install -e .
```

## Using yt_legacy

To enable the special dataset types defined here, simply add "import
yt_legacy" below your yt import.

```
>>> import yt
>>> import yt_legacy
>>> ds = yt.load(...)
```
