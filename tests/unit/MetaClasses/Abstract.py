# ==================================================================================================================== #
#             _____           _ _               __  __      _         ____ _                                           #
#  _ __  _   |_   _|__   ___ | (_)_ __   __ _  |  \/  | ___| |_ __ _ / ___| | __ _ ___ ___  ___  ___                   #
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` | | |\/| |/ _ \ __/ _` | |   | |/ _` / __/ __|/ _ \/ __|                  #
# | |_) | |_| || | (_) | (_) | | | | | | (_| |_| |  | |  __/ || (_| | |___| | (_| \__ \__ \  __/\__ \                  #
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, (_)_|  |_|\___|\__\__,_|\____|_|\__,_|___/___/\___||___/                  #
# |_|    |___/                          |___/                                                                          #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2022 Patrick Lehmann - Bötzingen, Germany                                                             #
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
"""
Unit tests for class :py:class:`pyTooling.MetaClasses.Abstract`.

:copyright: Copyright 2007-2022 Patrick Lehmann - Bötzingen, Germany
:license: Apache License, Version 2.0
"""
from unittest       import TestCase

from pyTooling.Exceptions import AbstractClassError
from pyTooling.MetaClasses import SuperType, abstractmethod, mustoverride

if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class NormalBase(metaclass=SuperType):
	def NormalMethod(self):
		pass


class NormalClass(NormalBase):
	pass


class AbstractBase(metaclass=SuperType):
	@abstractmethod
	def AbstractMethod(self):
		pass


class AbstractClass(AbstractBase):
	pass


class DerivedAbstractClass(AbstractBase):
	def AbstractMethod(self):
		super().AbstractMethod()


class MustOverrideBase(metaclass=SuperType):
	@mustoverride
	def MustOverrideMethod(self):
		pass


class MustOverrideClass(MustOverrideBase):
	pass


class DerivedMustOverrideClass(MustOverrideBase):
	def MustOverrideMethod(self):
		super().MustOverrideMethod()


class Abstract(TestCase):
	def test_NormalBase(self) -> None:
		cls = NormalBase()

	def test_NormalClass(self) -> None:
		cls = NormalClass()

	def test_AbstractBase(self) -> None:
		with self.assertRaises(AbstractClassError) as ExceptionCapture:
			base = AbstractBase()

		self.assertIn("AbstractBase", str(ExceptionCapture.exception))
		self.assertIn("AbstractMethod", str(ExceptionCapture.exception))

	def test_AbstractClass(self) -> None:
		with self.assertRaises(AbstractClassError) as ExceptionCapture:
			base = AbstractClass()

		self.assertIn("AbstractClass", str(ExceptionCapture.exception))
		self.assertIn("AbstractMethod", str(ExceptionCapture.exception))

	def test_DerivedAbstractClass(self) -> None:
		derived = DerivedAbstractClass()

		with self.assertRaises(NotImplementedError) as ExceptionCapture:
			derived.AbstractMethod()

		self.assertEqual("Method 'AbstractMethod' is abstract and needs to be overridden in a derived class.", str(ExceptionCapture.exception))

	def test_MustOverrideBase(self) -> None:
		with self.assertRaises(AbstractClassError) as ExceptionCapture:
			base = MustOverrideBase()

		self.assertIn("MustOverrideBase", str(ExceptionCapture.exception))
		self.assertIn("MustOverrideMethod", str(ExceptionCapture.exception))

	def test_MustOverrideClass(self) -> None:
		with self.assertRaises(AbstractClassError) as ExceptionCapture:
			base = MustOverrideClass()

		self.assertIn("MustOverrideClass", str(ExceptionCapture.exception))
		self.assertIn("MustOverrideMethod", str(ExceptionCapture.exception))

	def test_DerivedMustOverride(self) -> None:
		derived = DerivedMustOverrideClass()
