#     Copyright 2020, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Nodes for comparisons.

"""

from nuitka import PythonOperators
from nuitka.Errors import NuitkaAssumptionError

from .ExpressionBases import ExpressionChildrenHavingBase
from .NodeMakingHelpers import (
    makeConstantReplacementNode,
    makeRaiseExceptionReplacementExpressionFromInstance,
    wrapExpressionWithSideEffects,
)
from .shapes.BuiltinTypeShapes import tshape_bool


class ExpressionComparisonBase(ExpressionChildrenHavingBase):
    named_children = ("left", "right")
    getLeft = ExpressionChildrenHavingBase.childGetter("left")
    getRight = ExpressionChildrenHavingBase.childGetter("right")

    def __init__(self, left, right, source_ref):
        assert left.isExpression()
        assert right.isExpression()

        ExpressionChildrenHavingBase.__init__(
            self, values={"left": left, "right": right}, source_ref=source_ref
        )

    def getOperands(self):
        return (self.getLeft(), self.getRight())

    def getComparator(self):
        return self.comparator

    def getDetails(self):
        return {"comparator": self.comparator}

    @staticmethod
    def isExpressionComparison():
        return True

    def getSimulator(self):
        return PythonOperators.all_comparison_functions[self.comparator]

    def _computeCompileTimeConstantComparision(self, trace_collection):
        left_value = self.subnode_left.getCompileTimeConstant()
        right_value = self.subnode_right.getCompileTimeConstant()

        return trace_collection.getCompileTimeComputationResult(
            node=self,
            computation=lambda: self.getSimulator()(left_value, right_value),
            description="Comparison of constant arguments.",
        )

    def computeExpression(self, trace_collection):
        left = self.subnode_left
        right = self.subnode_right

        if left.isCompileTimeConstant() and right.isCompileTimeConstant():
            return self._computeCompileTimeConstantComparision(trace_collection)

        # The value of these nodes escaped and could change its contents.
        trace_collection.removeKnowledge(left)
        trace_collection.removeKnowledge(right)

        # Any code could be run, note that.
        trace_collection.onControlFlowEscape(self)

        trace_collection.onExceptionRaiseExit(BaseException)

        return self, None, None

    def computeExpressionOperationNot(self, not_node, trace_collection):
        if self.getTypeShape() is tshape_bool:
            result = makeComparisonExpression(
                left=self.subnode_left,
                right=self.subnode_right,
                comparator=PythonOperators.comparison_inversions[self.comparator],
                source_ref=self.source_ref,
            )

            return (
                result,
                "new_expression",
                """Replaced negated comparison '%s' with inverse comparison '%s'."""
                % (self.comparator, result.comparator),
            )

        return not_node, None, None


class ExpressionComparisonRichBase(ExpressionComparisonBase):
    def __init__(self, left, right, source_ref):
        ExpressionComparisonBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

        self.type_shape = None
        self.escape_desc = None

    def getTypeShape(self):
        return self.type_shape

    def getDetails(self):
        return {}

    def canCreateUnsupportedException(self):
        return hasattr(self.subnode_left.getTypeShape(), "typical_value") and hasattr(
            self.subnode_right.getTypeShape(), "typical_value"
        )

    def createUnsupportedException(self):
        left = self.subnode_left.getTypeShape().typical_value
        right = self.subnode_right.getTypeShape().typical_value

        try:
            self.getSimulator()(left, right)
        except TypeError as e:
            return e
        else:
            raise NuitkaAssumptionError(
                "Unexpected no-exception doing comparison simulation",
                self.operator,
                self.simulator,
                self.subnode_left.getTypeShape(),
                self.subnode_right.getTypeShape(),
                repr(left),
                repr(right),
            )

    def computeExpression(self, trace_collection):
        left = self.subnode_left
        right = self.subnode_right

        if left.isCompileTimeConstant() and right.isCompileTimeConstant():
            return self._computeCompileTimeConstantComparision(trace_collection)

        left_shape = left.getTypeShape()
        right_shape = right.getTypeShape()

        self.type_shape, self.escape_desc = self.getComparisonShape(
            left_shape, right_shape
        )

        exception_raise_exit = self.escape_desc.getExceptionExit()
        if exception_raise_exit is not None:
            trace_collection.onExceptionRaiseExit(exception_raise_exit)

            if (
                self.escape_desc.isUnsupported()
                and self.canCreateUnsupportedException()
            ):
                result = wrapExpressionWithSideEffects(
                    new_node=makeRaiseExceptionReplacementExpressionFromInstance(
                        expression=self, exception=self.createUnsupportedException()
                    ),
                    old_node=self,
                    side_effects=(self.subnode_left, self.subnode_right),
                )

                return (
                    result,
                    "new_raise",
                    """Replaced comparator '%s' with %s %s arguments that cannot work."""
                    % (
                        self.comparator,
                        self.subnode_left.getTypeShape(),
                        self.subnode_right.getTypeShape(),
                    ),
                )

        if self.escape_desc.isValueEscaping():
            # The value of these nodes escaped and could change its contents.
            trace_collection.removeKnowledge(left)
            trace_collection.removeKnowledge(right)

        if self.escape_desc.isControlFlowEscape():
            # Any code could be run, note that.
            trace_collection.onControlFlowEscape(self)

        return self, None, None

    def mayRaiseException(self, exception_type):
        # TODO: Match more precisely
        return (
            self.escape_desc is None
            or self.escape_desc.getExceptionExit() is not None
            or self.subnode_left.mayRaiseException(exception_type)
            or self.subnode_right.mayRaiseException(exception_type)
        )

    def mayRaiseExceptionBool(self, exception_type):
        return self.type_shape.hasShapeSlotBool() is not True

    def mayRaiseExceptionComparison(self):
        return (
            self.escape_desc is None or self.escape_desc.getExceptionExit() is not None
        )


class ExpressionComparisonLt(ExpressionComparisonRichBase):
    kind = "EXPRESSION_COMPARISON_LT"

    comparator = "Lt"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonRichBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

    @staticmethod
    def getComparisonShape(left_shape, right_shape):
        return left_shape.getComparisonLtShape(right_shape)


class ExpressionComparisonLte(ExpressionComparisonRichBase):
    kind = "EXPRESSION_COMPARISON_LTE"

    comparator = "LtE"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonRichBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

    @staticmethod
    def getComparisonShape(left_shape, right_shape):
        return left_shape.getComparisonLteShape(right_shape)


class ExpressionComparisonGt(ExpressionComparisonRichBase):
    kind = "EXPRESSION_COMPARISON_GT"

    comparator = "Gt"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonRichBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

    @staticmethod
    def getComparisonShape(left_shape, right_shape):
        return left_shape.getComparisonGtShape(right_shape)


class ExpressionComparisonGte(ExpressionComparisonRichBase):
    kind = "EXPRESSION_COMPARISON_GTE"

    comparator = "GtE"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonRichBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

    @staticmethod
    def getComparisonShape(left_shape, right_shape):
        return left_shape.getComparisonGteShape(right_shape)


class ExpressionComparisonEq(ExpressionComparisonRichBase):
    kind = "EXPRESSION_COMPARISON_EQ"

    comparator = "Eq"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonRichBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

    @staticmethod
    def getComparisonShape(left_shape, right_shape):
        return left_shape.getComparisonEqShape(right_shape)


class ExpressionComparisonNeq(ExpressionComparisonRichBase):
    kind = "EXPRESSION_COMPARISON_NEQ"

    comparator = "NotEq"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonRichBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

    @staticmethod
    def getComparisonShape(left_shape, right_shape):
        return left_shape.getComparisonNeqShape(right_shape)


class ExpressionComparisonIsIsNotBase(ExpressionComparisonBase):
    def __init__(self, left, right, source_ref):
        ExpressionComparisonBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

        assert self.comparator in ("Is", "IsNot")

        # TODO: Forward propagate this one.
        self.match_value = self.comparator == "Is"

    def getDetails(self):
        return {}

    def getTypeShape(self):
        return tshape_bool

    def mayRaiseException(self, exception_type):
        return self.getLeft().mayRaiseException(
            exception_type
        ) or self.getRight().mayRaiseException(exception_type)

    def mayRaiseExceptionBool(self, exception_type):
        return False

    def computeExpression(self, trace_collection):
        left, right = self.getOperands()

        if trace_collection.mustAlias(left, right):
            result = makeConstantReplacementNode(constant=self.match_value, node=self)

            if left.mayHaveSideEffects() or right.mayHaveSideEffects():
                result = wrapExpressionWithSideEffects(
                    side_effects=self.extractSideEffects(),
                    old_node=self,
                    new_node=result,
                )

            return (
                result,
                "new_constant",
                """\
Determined values to alias and therefore result of %s comparison."""
                % (self.comparator),
            )

        if trace_collection.mustNotAlias(left, right):
            result = makeConstantReplacementNode(
                constant=not self.match_value, node=self
            )

            if left.mayHaveSideEffects() or right.mayHaveSideEffects():
                result = wrapExpressionWithSideEffects(
                    side_effects=self.extractSideEffects(),
                    old_node=self,
                    new_node=result,
                )

            return (
                result,
                "new_constant",
                """\
Determined values to not alias and therefore result of '%s' comparison."""
                % (self.comparator),
            )

        return ExpressionComparisonBase.computeExpression(
            self, trace_collection=trace_collection
        )

    def extractSideEffects(self):
        left, right = self.getOperands()

        return left.extractSideEffects() + right.extractSideEffects()

    def computeExpressionDrop(self, statement, trace_collection):
        from .NodeMakingHelpers import makeStatementOnlyNodesFromExpressions

        result = makeStatementOnlyNodesFromExpressions(expressions=self.getOperands())

        del self.parent

        return (
            result,
            "new_statements",
            """\
Removed %s comparison for unused result."""
            % self.comparator,
        )


class ExpressionComparisonIs(ExpressionComparisonIsIsNotBase):
    kind = "EXPRESSION_COMPARISON_IS"

    comparator = "Is"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonIsIsNotBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )


class ExpressionComparisonIsNot(ExpressionComparisonIsIsNotBase):
    kind = "EXPRESSION_COMPARISON_IS_NOT"

    comparator = "IsNot"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonIsIsNotBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )


class ExpressionComparisonExceptionMatchBase(ExpressionComparisonBase):
    def __init__(self, left, right, source_ref):
        ExpressionComparisonBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

    def getDetails(self):
        return {}

    def getTypeShape(self):
        return tshape_bool

    def getSimulator(self):
        # TODO: Doesn't happen yet, but will once we trace exceptions.
        assert False

        return PythonOperators.all_comparison_functions[self.comparator]


class ExpressionComparisonExceptionMatch(ExpressionComparisonExceptionMatchBase):
    kind = "EXPRESSION_COMPARISON_EXCEPTION_MATCH"

    comparator = "exception_match"


class ExpressionComparisonExceptionMismatch(ExpressionComparisonExceptionMatchBase):
    kind = "EXPRESSION_COMPARISON_EXCEPTION_MISMATCH"

    comparator = "exception_mismatch"


class ExpressionComparisonInNotInBase(ExpressionComparisonBase):
    def __init__(self, left, right, source_ref):
        ExpressionComparisonBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )

        assert self.comparator in ("In", "NotIn")

    def getDetails(self):
        return {}

    def getTypeShape(self):
        return tshape_bool

    def mayRaiseException(self, exception_type):
        left = self.getLeft()

        if left.mayRaiseException(exception_type):
            return True

        right = self.getRight()

        if right.mayRaiseException(exception_type):
            return True

        return right.mayRaiseExceptionIn(exception_type, left)

    def mayRaiseExceptionBool(self, exception_type):
        return False

    def computeExpression(self, trace_collection):
        return self.getRight().computeExpressionComparisonIn(
            in_node=self, value_node=self.getLeft(), trace_collection=trace_collection
        )


class ExpressionComparisonIn(ExpressionComparisonInNotInBase):
    kind = "EXPRESSION_COMPARISON_IN"

    comparator = "In"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonInNotInBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )


class ExpressionComparisonNotIn(ExpressionComparisonInNotInBase):
    kind = "EXPRESSION_COMPARISON_NOT_IN"

    comparator = "NotIn"

    def __init__(self, left, right, source_ref):
        ExpressionComparisonInNotInBase.__init__(
            self, left=left, right=right, source_ref=source_ref
        )


_comparator_to_nodeclass = {
    "Is": ExpressionComparisonIs,
    "IsNot": ExpressionComparisonIsNot,
    "In": ExpressionComparisonIn,
    "NotIn": ExpressionComparisonNotIn,
    "Lt": ExpressionComparisonLt,
    "LtE": ExpressionComparisonLte,
    "Gt": ExpressionComparisonGt,
    "GtE": ExpressionComparisonGte,
    "Eq": ExpressionComparisonEq,
    "NotEq": ExpressionComparisonNeq,
    "exception_match": ExpressionComparisonExceptionMatch,
    "exception_mismatch": ExpressionComparisonExceptionMismatch,
}


def makeComparisonExpression(left, right, comparator, source_ref):
    return _comparator_to_nodeclass[comparator](
        left=left, right=right, source_ref=source_ref
    )
