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

from typer.testing import CliRunner

from test_data.dummy_app import app


def run_dummy_app_that_raise_exception():
    runner = CliRunner()
    result = runner.invoke(app)
    out = result.stdout
    print(f"output:\n{out}")
    assert "Aborted due to an exception" in out
    return result.exit_code
