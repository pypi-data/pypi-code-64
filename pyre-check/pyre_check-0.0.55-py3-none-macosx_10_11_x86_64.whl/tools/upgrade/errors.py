# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import itertools
import json
import logging
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union, cast

import libcst
import libcst.matchers as libcst_matchers

from . import UserError, ast


LOG: logging.Logger = logging.getLogger(__name__)
MAX_LINES_PER_FIXME: int = 4


class LineBreakTransformer(libcst.CSTTransformer):
    def leave_SimpleWhitespace(
        self,
        original_node: libcst.SimpleWhitespace,
        updated_node: libcst.SimpleWhitespace,
    ) -> Union[libcst.SimpleWhitespace, libcst.ParenthesizedWhitespace]:
        whitespace = original_node.value.replace("\\", "")
        if "\n" in whitespace:
            first_line = libcst.TrailingWhitespace(
                whitespace=libcst.SimpleWhitespace(
                    value=whitespace.split("\n")[0].rstrip()
                ),
                comment=None,
                newline=libcst.Newline(),
            )
            last_line = libcst.SimpleWhitespace(value=whitespace.split("\n")[1])
            return libcst.ParenthesizedWhitespace(
                first_line=first_line, empty_lines=[], indent=True, last_line=last_line
            )
        return updated_node

    @staticmethod
    def basic_parenthesize(
        node: libcst.CSTNode,
        whitespace: Optional[libcst.BaseParenthesizableWhitespace] = None,
    ) -> libcst.CSTNode:
        if not hasattr(node, "lpar"):
            return node
        if whitespace:
            return node.with_changes(
                lpar=[libcst.LeftParen(whitespace_after=whitespace)],
                rpar=[libcst.RightParen()],
            )
        return node.with_changes(lpar=[libcst.LeftParen()], rpar=[libcst.RightParen()])

    def leave_Assert(
        self, original_node: libcst.Assert, updated_node: libcst.Assert
    ) -> libcst.Assert:
        test = updated_node.test
        if not test:
            return updated_node
        assert_whitespace = updated_node.whitespace_after_assert
        if isinstance(assert_whitespace, libcst.ParenthesizedWhitespace):
            return updated_node.with_changes(
                test=LineBreakTransformer.basic_parenthesize(test, assert_whitespace),
                whitespace_after_assert=libcst.SimpleWhitespace(value=" "),
            )
        return updated_node.with_changes(
            test=LineBreakTransformer.basic_parenthesize(test)
        )

    def leave_Assign(
        self, original_node: libcst.Assign, updated_node: libcst.Assign
    ) -> libcst.Assign:
        assign_value = updated_node.value
        assign_whitespace = updated_node.targets[-1].whitespace_after_equal
        if libcst_matchers.matches(
            assign_whitespace, libcst_matchers.ParenthesizedWhitespace()
        ):
            adjusted_target = updated_node.targets[-1].with_changes(
                whitespace_after_equal=libcst.SimpleWhitespace(value=" ")
            )
            updated_targets = list(updated_node.targets[:-1])
            updated_targets.append(adjusted_target)
            return updated_node.with_changes(
                targets=tuple(updated_targets),
                value=LineBreakTransformer.basic_parenthesize(
                    assign_value, assign_whitespace
                ),
            )
        return updated_node.with_changes(
            value=LineBreakTransformer.basic_parenthesize(assign_value)
        )

    def leave_Del(
        self, original_node: libcst.Del, updated_node: libcst.Del
    ) -> libcst.Del:
        delete_target = updated_node.target
        delete_whitespace = updated_node.whitespace_after_del
        if isinstance(delete_whitespace, libcst.ParenthesizedWhitespace):
            return updated_node.with_changes(
                target=LineBreakTransformer.basic_parenthesize(
                    delete_target, delete_whitespace
                ),
                whitespace_after_del=libcst.SimpleWhitespace(value=" "),
            )
        return updated_node.with_changes(
            target=LineBreakTransformer.basic_parenthesize(delete_target)
        )

    def leave_Raise(
        self, original_node: libcst.Raise, updated_node: libcst.Raise
    ) -> libcst.Raise:
        exception = updated_node.exc
        if not exception:
            return updated_node
        raise_whitespace = updated_node.whitespace_after_raise
        if isinstance(raise_whitespace, libcst.ParenthesizedWhitespace):
            return updated_node.with_changes(
                exc=LineBreakTransformer.basic_parenthesize(
                    exception, raise_whitespace
                ),
                whitespace_after_raise=libcst.SimpleWhitespace(value=" "),
            )
        return updated_node.with_changes(
            exc=LineBreakTransformer.basic_parenthesize(exception)
        )

    def leave_Return(
        self, original_node: libcst.Return, updated_node: libcst.Return
    ) -> libcst.Return:
        return_value = updated_node.value
        if not return_value:
            return updated_node
        return_whitespace = updated_node.whitespace_after_return
        if isinstance(return_whitespace, libcst.ParenthesizedWhitespace):
            return updated_node.with_changes(
                value=LineBreakTransformer.basic_parenthesize(
                    return_value, return_whitespace
                ),
                whitespace_after_return=libcst.SimpleWhitespace(value=" "),
            )
        return updated_node.with_changes(
            value=LineBreakTransformer.basic_parenthesize(return_value)
        )


class PartialErrorSuppression(Exception):
    def __init__(self, message: str, unsuppressed_paths: List[str]) -> None:
        super().__init__(message)
        self.unsuppressed_paths: List[str] = unsuppressed_paths


def error_path(error: Dict[str, Any]) -> str:
    return error["path"]


class Errors:
    @classmethod
    def empty(cls) -> "Errors":
        return cls([])

    @staticmethod
    def from_json(
        json_string: str,
        only_fix_error_code: Optional[int] = None,
        from_stdin: bool = False,
    ) -> "Errors":
        try:
            errors = json.loads(json_string)
            return Errors(_filter_errors(errors, only_fix_error_code))
        except json.decoder.JSONDecodeError:
            if from_stdin:
                raise UserError(
                    "Received invalid JSON as input. "
                    "If piping from `pyre check` be sure to use `--output=json`."
                )
            else:
                raise UserError(
                    f"Encountered invalid output when checking for pyre errors: `{json_string}`."
                )

    @staticmethod
    def from_stdin(only_fix_error_code: Optional[int] = None) -> "Errors":
        input = sys.stdin.read()
        return Errors.from_json(input, only_fix_error_code, from_stdin=True)

    def __init__(self, errors: List[Dict[str, Any]]) -> None:
        self.errors: List[Dict[str, Any]] = errors
        self.error_iterator: Iterator[
            Tuple[str, Iterator[Dict[str, Any]]]
        ] = itertools.groupby(sorted(errors, key=error_path), error_path)
        self.length: int = len(errors)

    def __iter__(self) -> Iterator[Tuple[str, Iterator[Dict[str, Any]]]]:
        return self.error_iterator.__iter__()

    def __next__(self) -> Tuple[str, Iterator[Dict[str, Any]]]:
        return self.error_iterator.__next__()

    def __len__(self) -> int:
        return self.length

    def __eq__(self, other: "Errors") -> bool:
        return self.errors == other.errors

    def suppress(
        self,
        comment: Optional[str] = None,
        max_line_length: Optional[int] = None,
        truncate: bool = False,
        unsafe: bool = False,
    ) -> None:
        unsuppressed_paths = []

        for path_to_suppress, errors in self:
            LOG.info("Processing `%s`", path_to_suppress)
            try:
                path = Path(path_to_suppress)
                input = path.read_text()
                output = _suppress_errors(
                    input,
                    _build_error_map(errors),
                    comment,
                    max_line_length
                    if max_line_length and max_line_length > 0
                    else None,
                    truncate,
                    unsafe,
                )
                path.write_text(output)
            except SkippingGeneratedFileException:
                LOG.warning(f"Skipping generated file at {path_to_suppress}")
            except (ast.UnstableAST, SyntaxError):
                unsuppressed_paths.append(path_to_suppress)

        if unsuppressed_paths:
            paths_string = ", ".join(unsuppressed_paths)
            raise PartialErrorSuppression(
                f"Could not fully suppress errors in: {paths_string}",
                unsuppressed_paths,
            )


def _filter_errors(
    errors: List[Dict[str, Any]], only_fix_error_code: Optional[int] = None
) -> List[Dict[str, Any]]:
    if only_fix_error_code is not None:
        errors = [error for error in errors if error["code"] == only_fix_error_code]
    return errors


def errors_from_targets(
    project_directory: Path,
    path: str,
    targets: List[str],
    check_alternate_names: bool = True,
) -> Errors:
    buck_test_command = (
        ["buck", "test", "--show-full-json-output"] + targets + ["--", "--run-disabled"]
    )
    buck_test = subprocess.run(
        buck_test_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    errors = Errors.empty()
    if buck_test.returncode == 0:
        # Successful run with no type errors
        LOG.info("No errors in %s...", path)
    elif buck_test.returncode == 32:
        buck_test_output = buck_test.stdout.decode().split("\n")
        pyre_error_pattern = re.compile(r"\W*(.*\.pyi?):(\d*):(\d*) (.* \[(\d*)\]: .*)")
        errors = {}
        for output_line in buck_test_output:
            matched = pyre_error_pattern.match(output_line)
            if matched:
                path = matched.group(1)
                line = int(matched.group(2))
                column = int(matched.group(3))
                description = matched.group(4)
                code = matched.group(5)
                error = {
                    "line": line,
                    "column": column,
                    "path": project_directory / path,
                    "code": code,
                    "description": description,
                    "concise_description": description,
                }
                errors[(line, column, path, code)] = error
        errors = Errors(list(errors.values()))
    elif check_alternate_names and buck_test.returncode == 5:
        # Generated type check target was not named as expected.
        LOG.warning("Could not find buck test targets: %s", targets)
        LOG.info("Looking for similar targets...")
        targets_to_retry = []
        for target in targets:
            query_command = ["buck", "query", target]
            similar_targets = subprocess.run(
                query_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output = similar_targets.stdout.decode()
            error_output = similar_targets.stderr.decode()
            if output:
                targets_to_retry.append(output.strip())
            elif error_output:
                typecheck_targets = [
                    target.strip()
                    for target in error_output.split("\n")
                    if target.strip().endswith("-pyre-typecheck")
                ]
                targets_to_retry += typecheck_targets
        if targets_to_retry:
            LOG.info("Retrying similar targets: %s", targets_to_retry)
            errors = errors_from_targets(
                project_directory, path, targets_to_retry, check_alternate_names=False
            )
        else:
            LOG.error("No similar targets to retry.")
    else:
        LOG.error(
            "Failed to run buck test command:\n\t%s\n\n%s",
            " ".join(buck_test_command),
            buck_test.stderr.decode(),
        )
    return errors


def _remove_comment_preamble(lines: List[str]) -> None:
    # Deprecated: leaving remove logic until live old-style comments are cleaned up.
    while lines:
        old_line = lines.pop()
        new_line = re.sub(r"# pyre: .*$", "", old_line).rstrip()
        if old_line == "" or new_line != "":
            # The preamble has ended.
            lines.append(new_line)
            return


def _add_error_to_line_break_block(lines: List[str], errors: List[List[str]]) -> None:
    # Gather unbroken lines.
    line_break_block = [lines.pop() for _ in range(0, len(errors))]
    line_break_block.reverse()

    # Transform line break block to use parenthesis.
    indent = len(line_break_block[0]) - len(line_break_block[0].lstrip())
    line_break_block = [line[indent:] for line in line_break_block]
    statement = "\n".join(line_break_block)
    transformed_statement = libcst.Module([]).code_for_node(
        cast(
            libcst.CSTNode,
            libcst.parse_statement(statement).visit(LineBreakTransformer()),
        )
    )
    transformed_lines = transformed_statement.split("\n")
    transformed_lines = [" " * indent + line for line in transformed_lines]

    # Add to lines.
    for line, comment in zip(transformed_lines, errors):
        lines.extend(comment)
        lines.append(line)


def _split_across_lines(
    comment: str, indent: int, max_line_length: Optional[int]
) -> List[str]:
    if not max_line_length or len(comment) <= max_line_length:
        return [comment]

    comment = comment.lstrip()
    available_columns = max_line_length - indent - len("#  ")

    buffered_line = ""
    result = []
    prefix = " " * indent
    for token in comment.split():
        if buffered_line and (
            len(buffered_line) + len(token) + len(" ") > available_columns
        ):
            # This new token would make the line exceed the limit,
            # hence terminate what we have accumulated.
            result.append(("{}{}".format(prefix, buffered_line)).rstrip())
            # The first line already has a comment token on it, so don't prefix #. For
            # the rest, we need to add the comment symbol manually.
            prefix = "{}#  ".format(" " * indent)
            buffered_line = ""

        buffered_line = buffered_line + token + " "

    result.append(("{}{}".format(prefix, buffered_line)).rstrip())
    return result


class SkippingGeneratedFileException(Exception):
    pass


def _suppress_errors(
    input: str,
    errors: Dict[int, List[Dict[str, str]]],
    custom_comment: Optional[str] = None,
    max_line_length: Optional[int] = None,
    truncate: bool = False,
    unsafe: bool = False,
) -> str:
    if "@" "generated" in input:
        raise SkippingGeneratedFileException()

    lines = input.split("\n")  # type: List[str]

    # Replace lines in file.
    new_lines = []
    removing_pyre_comments = False
    line_break_block_errors: List[List[str]] = []
    for index, line in enumerate(lines):
        if removing_pyre_comments:
            stripped = line.lstrip()
            if stripped.startswith("#") and not re.match(
                r"# *pyre-(ignore|fixme).*$", stripped
            ):
                continue
            else:
                removing_pyre_comments = False
        number = index + 1
        relevant_errors = errors[number] if number in errors else []
        if any(error["code"] == "0" for error in relevant_errors):
            # Handle unused ignores.
            replacement = re.sub(r"# pyre-(ignore|fixme).*$", "", line).rstrip()
            if replacement == "":
                removing_pyre_comments = True
                _remove_comment_preamble(new_lines)
                continue
            else:
                line = replacement

        comments = []
        for error in relevant_errors:
            if error["code"] == "0":
                continue
            indent = len(line) - len(line.lstrip(" "))
            description = custom_comment if custom_comment else error["description"]
            comment = "{}# pyre-fixme[{}]: {}".format(
                " " * indent, error["code"], description
            )
            if not max_line_length or len(comment) <= max_line_length:
                comments.append(comment)
            else:
                truncated_comment = comment[: (max_line_length - 3)] + "..."
                split_comment_lines = _split_across_lines(
                    comment, indent, max_line_length
                )
                if truncate or len(split_comment_lines) > MAX_LINES_PER_FIXME:
                    comments.append(truncated_comment)
                else:
                    comments.extend(split_comment_lines)

        if len(line_break_block_errors) > 0 and not line.endswith("\\"):
            # Handle error suppressions in line break block
            line_break_block_errors.append(comments)
            new_lines.append(line)
            _add_error_to_line_break_block(new_lines, line_break_block_errors)
            line_break_block_errors = []
            continue

        if line.endswith("\\"):
            line_break_block_errors.append(comments)
            comments = []

        LOG.info(
            "Adding comment%s on line %d: %s",
            "s" if len(comments) > 1 else "",
            number,
            " \n".join(comments),
        )
        new_lines.extend(comments)
        new_lines.append(line)
    output = "\n".join(new_lines)
    if not unsafe:
        ast.check_stable(input, output)
    return output


def _build_error_map(
    errors: Iterator[Dict[str, Any]]
) -> Dict[int, List[Dict[str, str]]]:
    error_map = defaultdict(lambda: [])
    for error in errors:
        if error["concise_description"]:
            description = error["concise_description"]
        else:
            description = error["description"]
        match = re.search(r"\[(\d+)\]: (.*)", description)
        if match:
            error_map[error["line"]].append(
                {"code": match.group(1), "description": match.group(2)}
            )
    return error_map
