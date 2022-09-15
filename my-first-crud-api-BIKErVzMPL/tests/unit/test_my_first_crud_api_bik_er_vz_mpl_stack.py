import aws_cdk as core
import aws_cdk.assertions as assertions

from my_first_crud_api_bik_er_vz_mpl.my_first_crud_api_bik_er_vz_mpl_stack import (
    MyFirstCrudApiBikErVzMplStack,
)

# example tests. To run these tests, uncomment this file along with the example
# resource in my_first_crud_api_bik_er_vz_mpl/my_first_crud_api_bik_er_vz_mpl_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MyFirstCrudApiBikErVzMplStack(app, "my-first-crud-api-bik-er-vz-mpl")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
