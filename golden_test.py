import contextlib
import io
import logging
import os
import tempfile

import pytest
from impl import Machine, Translator


@pytest.mark.golden_test("golden/*.yml")
def test_translator_and_machine(golden, caplog):
    caplog.set_level(logging.DEBUG)
    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source.txt")
        input_stream = os.path.join(tmpdirname, "input.txt")
        target = os.path.join(tmpdirname, "code.o")
        output = os.path.join(tmpdirname, "output.txt")

        with open(source, mode="w", encoding="utf-8") as f:
            f.write(golden["in_source"])
        with open(input_stream, mode="w", encoding="utf-8") as f:
            f.write(golden["in_stdin"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            Translator.main(source, target)
            print("============================================================")
            Machine.main(target, input_stream, output)

        with open(target) as f:
            code = f.read()

        assert code == golden.out["out_code"]
        assert stdout.getvalue() == golden.out["out_stdout"]
        assert "\n".join(caplog.text.split("\n")[-300:]) == golden.out["out_log"]
