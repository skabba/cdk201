"""Module for the Storage Stack, containing persistent storages."""

from aws_cdk import (
    Stack,
    NestedStack,
    aws_dynamodb as dynamodb,
)


class StorageStack(NestedStack):
    """The Storage Stack for persistant storage (DDB)"""

    def __init__(
        self,
        scope: Stack,
        construct_id: str,
        **kwargs,
    ) -> None:
        """Construct a new StorageStack."""
        super().__init__(scope, construct_id, **kwargs)

        self.crud_api_table = dynamodb.Table(
            scope=self,
            id="CrudApiTable",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
        )
