# ==================================================================================================================== #
#             _____           _ _           __     __            _             _                                       #
#  _ __  _   |_   _|__   ___ | (_)_ __   __ \ \   / /__ _ __ ___(_) ___  _ __ (_)_ __   __ _                           #
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` \ \ / / _ \ '__/ __| |/ _ \| '_ \| | '_ \ / _` |                          #
# | |_) | |_| || | (_) | (_) | | | | | | (_| |\ V /  __/ |  \__ \ | (_) | | | | | | | | (_| |                          #
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, (_)_/ \___|_|  |___/_|\___/|_| |_|_|_| |_|\__, |                          #
# |_|    |___/                          |___/                                          |___/                           #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2020-2022 Patrick Lehmann - Bötzingen, Germany                                                             #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""Implementation of semantic and date versioning version-numbers.

.. hint:: See :ref:`high-level help <VERSIONING>` for explanations and usage examples.
"""
from enum          import IntEnum
from typing import Optional as Nullable, Any

from ..Decorators  import export
from ..MetaClasses import Overloading


@export
class SemVersion(metaclass=Overloading):
	"""Representation of a semantic version number like ``3.7.12``."""

	class Parts(IntEnum):
		Major = 1
		Minor = 2
		Patch = 4
		Build = 8
		Pre   = 16
		Post  = 32
		Prefix = 64
		Postfix = 128
		AHead   = 256

	class Flags(IntEnum):
		Clean = 1
		Dirty = 2

	parts   : Parts
	flags   : int = Flags.Clean
	major   : int = 0
	minor   : int = 0
	patch   : int = 0
	build   : int = 0
	pre     : int = 0
	post    : int = 0
	prefix  : str = ""
	postfix : str = ""
	ahead   : int = 0

	def __init__(self, versionString : str):
		if versionString == "":
			raise ValueError("Parameter 'versionString' is empty.")
		elif versionString is None:
			raise ValueError("Parameter 'versionString' is None.")
		elif versionString.startswith(("V", "v", "I", "i", "R", "r")):
			versionString = versionString[1:]
		elif versionString.startswith(("rev", "REV")):
			versionString = versionString[3:]

		split = versionString.split(".")
		length = len(split)
		self.major = int(split[0])
		if length >= 2:
			self.minor = int(split[1])
		if length >= 3:
			self.patch = int(split[2])
		if length >= 4:
			self.build = int(split[3])
		self.flags = self.Flags.Clean

	def __init__(self, major: int, minor: int, patch: int = 0, build: int = 0):  # type: ignore[no-redef]
		self.major = major
		self.minor = minor
		self.patch = patch
		self.build = build
		self.flags = self.Flags.Clean

	def __eq__(self, other: Any) -> bool:
		"""Compare two Version instances (version numbers) for equality.

		:returns: True, if both version numbers are equal.
		raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")
		"""
		if not isinstance(other, SemVersion):
			raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")

		return (
			(self.major == other.major) and
			(self.minor == other.minor) and
			(self.patch == other.patch) and
			(self.build == other.build)
		)

	def __ne__(self, other: Any) -> bool:
		"""Compare two Version instances (version numbers) for inequality.

		:returns: True, if both version numbers are not equal.
		raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")
		"""
		if not isinstance(other, SemVersion):
			raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")

		return not self.__eq__(other)

	@staticmethod
	def __compare(left: 'SemVersion', right: 'SemVersion') -> Nullable[bool]:
		if (left.major < right.major):
			return True
		if (left.major > right.major):
			return False

		if (left.minor < right.minor):
			return True
		if (left.minor > right.minor):
			return False

		if (left.patch < right.patch):
			return True
		if (left.patch > right.patch):
			return False

		if (left.build < right.build):
			return True
		if (left.build > right.build):
			return False

		return None

	def __lt__(self, other: Any) -> bool:
		"""Compare two Version instances (version numbers) if the version is less than the second operand.

		:returns: True if version is less than the second operand.
		:raises TypeError: If parameter ``other`` is not of type :py:class:`SemVersion`.
		"""
		if not isinstance(other, SemVersion):
			raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")

		result = self.__compare(self, other)
		return result if result is not None else False

	def __le__(self, other: Any) -> bool:
		"""Compare two Version instances (version numbers) if the version is less than or equal to the second operand.

		:returns: True if version is less than or equal to the second operand.
		:raises TypeError: If parameter ``other`` is not of type :py:class:`SemVersion`.
		"""
		if not isinstance(other, SemVersion):
			raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")

		result = self.__compare(self, other)
		return result if result is not None else True

	def __gt__(self, other: Any) -> bool:
		"""Compare two Version instances (version numbers) if the version is greater than the second operand.

		:returns: True if version is greater than the second operand.
		:raises TypeError: If parameter ``other`` is not of type :py:class:`SemVersion`.
		"""
		if not isinstance(other, SemVersion):
			raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")

		return not self.__le__(other)

	def __ge__(self, other: Any) -> bool:
		"""Compare two Version instances (version numbers) if the version is greater than or equal to the second operand.

		:returns: True if version is greater than or equal to the second operand.
		:raises TypeError: If parameter ``other`` is not of type :py:class:`SemVersion`.
		"""
		if not isinstance(other, SemVersion):
			raise TypeError(f"Parameter 'other' is not of type 'SemVersion'.")

		return not self.__lt__(other)

	def __repr__(self) -> str:
		"""Return a string representation of this version number without prefix ``v``.

		:returns: Raw version number representation without a prefix.
		"""
		return f"{self.major}.{self.minor}.{self.patch}"

	def __str__(self) -> str:
		"""Return a string representation of this version number with prefix ``v``.

		:returns: Version number representation including a prefix.
		"""
		return f"v{self.major}.{self.minor}.{self.patch}"


@export
class CalVersion(metaclass=Overloading):
	"""Representation of a calendar version number like ``2021.10``."""
