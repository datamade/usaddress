import os
import subprocess
from distutils.cmd import Command

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class TrainModel(Command):
    description = "Training the model before building the package"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        PYTHONPATH = os.environ.get("PYTHONPATH", "")
        subprocess.run(
            ["parserator", "train", "training/labeled.xml", "usaddress"],
            env=dict(os.environ, PYTHONPATH=f".{os.pathsep}{PYTHONPATH}"),
        )


class build_py(_build_py):
    def run(self):
        self.run_command("train_model")  # Run the custom command
        super().run()


# Standard setup configuration
setup(
    cmdclass={
        "build_py": build_py,  # Override build_py
        "train_model": TrainModel,  # Register custom command
    },
)
