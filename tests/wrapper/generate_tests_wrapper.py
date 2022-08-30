#  Copyright 2022 Ruiguo (Ray) Yang
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from test_data.person import Person
from test_data.product import ProductOwner, Product
from testscribe.gather_referenced_modules import get_module_names_from_value
from testscribe.transformer import transform_value


def add_module_names_from_class_tag_complex_class():
    """
    This wrapper makes it easier to construct the input with code.
    """
    v = transform_value(ProductOwner(owner=Person("a", 30), product=Product("p", 1)))
    return get_module_names_from_value(v)
