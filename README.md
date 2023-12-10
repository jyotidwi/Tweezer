<p align="center">
    <img width=100% src="tweezer.png">
  </a>
</p>
<p align="center"> 🤖 Binary Analysis, Function Finding ⚙️ </b> </p>

<div align="center">

![GitHub contributors](https://img.shields.io/github/contributors/user1342/Tweezer)
![GitHub last commit](https://img.shields.io/github/last-commit/user1342/Tweezer)
<br>
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P7C2MM6)

</div>

# ⚙️ Setup
## Dependancies
Tweezer requires [Ghidra](https://ghidra-sre.org/) to be installed, and for ```analyzeHeadless``` to be on your path. If it is not on your path Tweezer will request on run where the binary is located. To install all other dependancies use the ```requirements.txt``` file, with:

```
pip install -r requirements.txt
python setup.py install
```

## Running
Depending on if you already have a trained model/ map of vectors you may decide to run Tweezer in one of two ways, either 1) to train a new model/ extend an existing model or 2) to run Tweezer against a decompiled function or binary. 

### Training/ Extending the Model
```bash
python tweezer --model-path <model-path> --binary-locations <binary-folder-1> <binary-folder-2>...
```

### Finding Closest Functions
```bash
python tweezer --model-path <model-path> --function <path-to-decompiled-function>
```

### Building Function Name Map
```bash
python tweezer --model-path <model-path> --binary <path-to-binary>
```

# 🙏 Contributions
Tweezer is an open-source project and welcomes contributions from the community. If you would like to contribute to Tweezer, please follow these guidelines:

- Fork the repository to your own GitHub account.
- Create a new branch with a descriptive name for your contribution.
- Make your changes and test them thoroughly.
- Submit a pull request to the main repository, including a detailed description of your changes and any relevant documentation.
- Wait for feedback from the maintainers and address any comments or suggestions (if any).
- Once your changes have been reviewed and approved, they will be merged into the main repository.

# ⚖️ Code of Conduct
Tweezer follows the Contributor Covenant Code of Conduct. Please make sure [to review](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md). and adhere to this code of conduct when contributing to Tweezer.

# 🐛 Bug Reports and Feature Requests
If you encounter a bug or have a suggestion for a new feature, please open an issue in the GitHub repository. Please provide as much detail as possible, including steps to reproduce the issue or a clear description of the proposed feature. Your feedback is valuable and will help improve Tweezer for everyone.

# 📜 License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
