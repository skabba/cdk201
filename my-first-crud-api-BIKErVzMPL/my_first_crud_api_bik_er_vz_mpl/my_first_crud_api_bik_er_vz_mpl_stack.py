from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class MyFirstCrudApiBikErVzMplStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        crud_api_table = dynamodb.Table(
            self,
            "CrudApiTable",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
        )

        crud_api_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.NODEJS_16_X,
            code=_lambda.Code.from_asset("lambda"),
            handler="crud.handler",
            environment={"DYNAMODB_TABLE_NAME": crud_api_table.table_name},
        )

        crud_api_table.grant_full_access(crud_api_lambda.grant_principal)

        crud_api_gw = apigw.LambdaRestApi(
            self,
            "CrudApi",
            handler=crud_api_lambda,
            proxy=False,
        )

        items = crud_api_gw.root.add_resource("items")
        items.add_method("GET")  # GET /items
        items.add_method("PUT")  # PUT /items

        item = items.add_resource("{id}")
        item.add_method("GET")  # GET /items/{id}
        item.add_method("DELETE")  # DELETE /items/{id}
