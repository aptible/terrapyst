from pathlib import Path

import pytest

from terrapyst.apply_log import TerraformApplyLog

APPLY_LOG_FILE = Path(__file__).parent.absolute() / "terraform" / "applies" / "vpc.jsonl"
with open(APPLY_LOG_FILE) as f:
    APPLY_LOG_CONTENTS = f.read()


def test_read_log():
    apply_log = TerraformApplyLog()
    apply_log.add_lines(APPLY_LOG_CONTENTS)

    assert "module.vpc.module.nat_gateway[0].aws_route.route_to_nat[2]" in apply_log.resources
    assert apply_log.changes["operation"] == "apply"
    assert apply_log.changes["add"] == 32
    assert apply_log.changes["change"] == 0
    assert apply_log.changes["remove"] == 0
    assert "vpc" in apply_log.outputs


def test_read_log_unreadable(caplog):
    apply_log = TerraformApplyLog()
    apply_log.add_lines("THIS WILL BE EMPTY\n")
    assert apply_log.outputs == {}
    assert "Apply log includes line of invalid json" in caplog.text


def test_warning(caplog):
    apply_log = TerraformApplyLog()
    apply_log.add_lines(APPLY_LOG_CONTENTS)
    apply_log.add_line('{"type":"fake"}')
    assert "Apply log includes unknown type:" in caplog.text
