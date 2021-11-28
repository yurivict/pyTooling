# =============================================================================
#             _____           _ _
#  _ __  _   |_   _|__   ___ | (_)_ __   __ _
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` |
# | |_) | |_| || | (_) | (_) | | | | | | (_| |
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, |
# |_|    |___/                          |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Package installer:  A collection of MetaClasses for Python.
#
# License:
# ============================================================================
# Copyright 2017-2021 Patrick Lehmann - Bötzingen, Germany
# Copyright 2007-2016 Technische Universität Dresden - Germany
#                     Chair of VLSI-Design, Diagnostics and Architecture
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
from pathlib             import Path
from pyTooling.Packaging import DescribePythonPackageHostedOnGitHub

gitHubNamespace =        "pyTooling"
packageName =            "pyTooling.*"
packageDirectory =       packageName[:-2]
packageInformationFile = Path(f"{packageDirectory}/Common/__init__.py")
#pythonVersions =         ["3.8", "3.9", "3.10"]

DescribePythonPackageHostedOnGitHub(
	packageName=packageName,
	description="pyTooling is a powerful collection of arbitrary useful classes, decorators, meta-classes and exceptions.",
	gitHubNamespace=gitHubNamespace,
	keywords="Python3 Exceptions Decorators MetaClasses Versioning Collection",
	sourceFileWithVersion=packageInformationFile,
#	developmentStatus="stable",
#	pythonVersions=pythonVersions
)
