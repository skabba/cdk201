from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
)
from constructs import Construct

# import nested stacks
from my_first_crud_api_bik_er_vz_mpl.stacks.storage import StorageStack
from my_first_crud_api_bik_er_vz_mpl.stacks._lambda import ApiLambdaStack


class MyFirstCrudApiBikErVzMplStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define nested stacks
        self.storage_stack = StorageStack(
            scope=self,
            construct_id="StorageStack",
        )

        self.api_lambda_stack = ApiLambdaStack(
            scope=self,
            construct_id="ApiLambdaStack",
        )
