## Active developers

- Eric Knauss @oerich (Owner, Maintainer)
- @grischal (Maintainer)
- @rashidahk (Maintainer)
- @piotr20a (Developer)
- @halldor95 (Developer)
- @egillsmari (Developer)
- @andri95 (Developer)
- @latiif (Developer)

## Past contributions

TReqs has been developed over a period of time and many have contributed directly or indirectly.

- [T-Reqs v1](https://github.com/regot-chalmers/treqs)
- [T-Reqs: Key idea and User Stories](https://arxiv.org/abs/1805.02769)

### Thesis work

- [Gebremichael, Mebrahtom Guesh: Master's thesis](https://odr.chalmers.se/handle/20.500.12380/300667), [gitlab](https://gitlab.com/mebrahtom/treqs)
- [Kasauli, Rashidah: PhD thesis](https://research.chalmers.se/en/publication/517099)
- [Alsahhar, Yazan and Bulai, Gabriel-Marian: Bachelor's thesis](https://gupea.ub.gu.se/handle/2077/62550)
- Chen, Yu-Jhen: Project work

### Running Tests Locally

To ensure the stability and correctness of our codebase, we have a suite of tests that cover various aspects of the
project. Before you submit any changes, it's important to run these tests locally to catch any potential issues.
We use the built-in unittest framework in Python to manage and run our tests. To run the tests locally, follow these
steps:

- __Clone the Repository__: Begin by cloning the repository to your local machine using the following command:

```bash
git clone https://gitlab.com/treqs-on-git/treqs-ng.git
```

- __Navigate to the Project Directory__: Change your current working directory to the project's root
  folder:

```bash
cd treqs-ng
```

- __Run Tests__: Use the following command to run all the tests in the directory and its subdirectories:

```bash
python3 -m unittest discover -s tests
```

If `python` on your system already is set to version 3.*, you can run the tests using:

```bash
python -m unittest discover -s tests
```




