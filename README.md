# treqs ng

This is the consolidated version of treqs. We focus on a new UI and then integrate features from various treqs variants. [Read more about previous/related versions and contributors](CONTRIBUTING.md).

# TReqs: Tool Support for Managing Requirements in Large-Scale Agile System Development

Requirements engineering is crucial to support agile development of large systems with long lifetimes. Agile cross-functional teams must be aware of requirements at system level and able to efficiently propose updates to those requirements.

- **Objective:** T-Reqs' objective is to offer lightweight tooling to manage requirements in large-scale agile system development.
- **Philosophy:** Bring requirements close to teams. T-Reqs aims to put requirements into the hands of teams and allows managing them together with changes of code and test.

Where many tools require an organization to adjust their process, T-Reqs aims to integrate into a particular organization's large-scale agile way of working.
It supports proven solutions for requirements challenges in large-scale agile, for example supporting agile teams in updating system requirements by relying on typical git based infrastructure to peer-review pull or merge requests.

T-Reqs is currently in industrial use and based on its success, we are exploring whether providing its key concepts and infrastructure as open source is valuable. Regardless, we hope our experience helps to trigger a dialogue on how the changing landscape of requirements engineering in relation to agile system and software development affects needs for tooling support.

### Requirements

  Python 3.x


## Getting started

### Installation

Clone this repo, then from the root of repo directory, run

    pip install -e .

### Running scripts on example requirements

    treqs 

That's it, treqs will produce help text and then execute its list, process, and check commands on its own requirements. Just switch to your other awesome gitlab projects and start using treqs there as well.

### Further reading

- [Read demonstrator](documentation/treqs-pitch/treqs-demonstrator.md)
- [Read tutorial](documentation/treqs-pitch/treqs-usage.md)
- [Requirements Challenges in Large-Scale Agile](https://oerich.wordpress.com/2017/06/28/re-for-large-scale-agile-system-development/)
- [T-Reqs: Key idea and User Stories](https://arxiv.org/abs/1805.02769)

## Versioning

TReqs follows semantic versioning from version 1.0.0 onwards. Before 1.0.0, the versioning was unstructured.
In summary, semantic versioning uses version numbers consisting of three numbers separated by dots: **(X.Y.Z)**. The different numbers have the following meaning.
    X: Describes the MAJOR version. Changes to this version make incompatible API changes,
    Y: Describes the MINOR version. Changes to this version means functionality has been added, but in a backwards compatible manner, and
    Z: Descrtibes PATCH versions, where changes relate to bug fixes, made in a backwards compatible fashion.

More details can be found [here](https://semver.org/).
