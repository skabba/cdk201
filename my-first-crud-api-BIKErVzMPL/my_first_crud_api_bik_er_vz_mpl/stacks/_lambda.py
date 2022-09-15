"""Module for the Lambda Stack, containing Lambda functions."""

from aws_cdk import (
    Stack,
    NestedStack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_apigateway as apigw,
)


class ApiLambdaStack(NestedStack):
    """The Lambda Stack for functions"""

    def __init__(
        self,
        scope: Stack,
        construct_id: str,
        **kwargs,
    ) -> None:
        """Construct a new LambdaStack."""
        super().__init__(scope, construct_id, **kwargs)

        self.crud_api_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="hello.handler",
        )

        self.crud_api_lambda
