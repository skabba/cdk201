# CDK201
Build your first CRUD API in 45 minutes or less with AWS CDK!

## Welcome
Foo bar

## Prep
This workshop will be executed from within an AWS Cloud9 (Online IDE) environment.

To open this online IDE you first need to login here: https://obsessedbyaws.signin.aws.amazon.com/console.

## Step 1
```shell
export STACK_SUFFIX=$(cat /dev/urandom | \
                    tr -dc '[:alpha:]' | \
                    fold -w ${1:-10} | \
                    head -n 1)
mkdir my-first-crud-api-${STACK_SUFFIX} && cd $_
cdk init app --language=python
ls -al
```

### Explain files
abc

```console
total 28
drwxrwxr-x 5 ec2-user ec2-user  206 Sep 14 08:34 .
drwxrwxr-x 4 ec2-user ec2-user   86 Sep 14 08:34 ..
-rw-rw-r-- 1 ec2-user ec2-user 1027 Sep 14 08:34 app.py
-rw-rw-r-- 1 ec2-user ec2-user 1356 Sep 14 08:34 cdk.json
-rw-rw-r-- 1 ec2-user ec2-user  119 Sep 14 08:34 .gitignore
drwxrwxr-x 2 ec2-user ec2-user   73 Sep 14 08:34 my_first_crud_api_ua_vddf_bi_hp
-rw-rw-r-- 1 ec2-user ec2-user 1658 Sep 14 08:34 README.md
-rw-rw-r-- 1 ec2-user ec2-user   14 Sep 14 08:34 requirements-dev.txt
-rw-rw-r-- 1 ec2-user ec2-user   47 Sep 14 08:34 requirements.txt
-rw-rw-r-- 1 ec2-user ec2-user  437 Sep 14 08:34 source.bat
drwxrwxr-x 3 ec2-user ec2-user   37 Sep 14 08:34 tests
drwxrwxr-x 5 ec2-user ec2-user   74 Sep 14 08:34 .venv
```

### Step 1.1
```shell
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install black
pip freeze > requirements.txt
```

## Step 2
Run `cdk synth` and check the output. Also, did you notice that a folder named `cdk.out` appeared in the root of your CDK project?

The `cdk.out` folder contains a JSON CloudFormation template of your compiled CDK code.

## Step 3
Run `cdk deploy` to deploy your (still empty) CDK app and check the output. In a new browser tab open: https://eu-west-1.console.aws.amazon.com/cloudformation and search/select/open your "MyFirstCrudApi${STACK_SUFFIX}Stack" stack. You can now review your stack configuration.

## Step 4
Open your `my_first_crud_api_${STACK_SUFFIX}` folder and then open the `my_first_crud_api_${STACK_SUFFIX}_stack.py` file.

Remove this piece of code:
```python
        # example resource
        # queue = sqs.Queue(
        #     self, "MyFirstCrudApiRufZeyFmJkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
```

### Step 4.1
Our CRUD API will need the following AWS services:

![CRUD API resources](https://miro.medium.com/max/1400/1*N1iRLifjnNcZo-W0oxoYSw.png)

We can import the respective CDK modules in our code. In `my_first_crud_api_${STACK_SUFFIX}_stack.py`.

**CHANGE THIS CODE**:
```python
from aws_cdk import (
    Duration,
    Stack,
    aws_sqs as sqs,
)
```
**INTO THIS CODE**:
```python
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
)
```

> **_NOTE:_** we import aws_lambda specifically as _lambda (note the underscore), because in Python, lambda is a keyword which cannot be used.

## Step 5
We are now going to add the code to define our CRUD API resources.

### Step 5.1 - Add DynamoDB Table
Below `# The code that defines your stack goes here` add:
```python
        crud_ddb_table = dynamodb.Table(
            self,
            "CrudApiTable",
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
        )
```

Run `cdk synth` and check cdk.out/YourStackName.template.json.
Run `cdk deploy` and check the output.

### Step 5.2 - Add CRUD Lambda Function
We first will create the Lambda function itself:
```shell
mkdir lambda
touch lambda/crud.js
```
Open this file (`lambda/crud.js`) and add the following Node.js code:
```javascript
const AWS = require("aws-sdk");

const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
  let body;
  let statusCode = 200;
  const tableName = process.env.DYNAMODB_TABLE_NAME;
  const method_and_resource = event["httpMethod"] + " " + event["resource"];
  const headers = {
    "Content-Type": "application/json"
  };

  try {
    switch (method_and_resource) {
      case "DELETE /items/{id}":
        await dynamo
          .delete({
            TableName: tableName,
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        body = `Deleted item ${event.pathParameters.id}`;
        break;
      case "GET /items/{id}":
        body = await dynamo
          .get({
            TableName: tableName,
            Key: {
              id: event.pathParameters.id
            }
          })
          .promise();
        break;
      case "GET /items":
        body = await dynamo.scan({ TableName: tableName }).promise();
        break;
      case "PUT /items":
        let requestJSON = JSON.parse(event.body);
        await dynamo
          .put({
            TableName: tableName,
            Item: {
              id: requestJSON.id,
              price: requestJSON.price,
              name: requestJSON.name
            }
          })
          .promise();
        body = `Put item ${requestJSON.id}`;
        break;
      default:
        throw new Error(`Unsupported route: "${event.routeKey}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }

  return {
    statusCode,
    body,
    headers
  };
};
```
Then go back to the file where we were defining our CRUD API Stack (the `my_first_crud_api_${STACK_SUFFIX}_stack.py` file). Then below the previously added DynamoDB resource code, add the following code:
```python
        crud_api_lambda = _lambda.Function(
            self,
            "HelloHandler",
            runtime=_lambda.Runtime.NODEJS_16_X,
            code=_lambda.Code.from_asset("lambda"),
            handler="crud.handler",
            environment={"DYNAMODB_TABLE_NAME": crud_ddb_table.table_name},
        )

        crud_ddb_table.grant_full_access(crud_api_lambda.grant_principal)
```

The entire file (`my_first_crud_api_${STACK_SUFFIX}_stack.py`) should now look like:
```python
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

        # The code that defines your stack goes here

        crud_ddb_table = dynamodb.Table(
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
            environment={"DYNAMODB_TABLE_NAME": crud_ddb_table.table_name},
        )

        crud_ddb_table.grant_full_access(crud_api_lambda.grant_principal)
```

Run `cdk synth` and check cdk.out/YourStackName.template.json.
Run `cdk deploy` and check the output.

### Step 5.3 - Add CRUD Rest API Gateway
Below the Lambda function resource code, add:
```python
        crud_api_gw = apigw.LambdaRestApi(
            self,
            "CrudApi",
            handler=crud_api_lambda,
            proxy=False, # Because we manually add resources + methods
        )

        items = crud_api_gw.root.add_resource("items")
        items.add_method("GET")  # GET /items
        items.add_method("PUT")  # PUT /items

        item = items.add_resource("{id}")
        item.add_method("GET")  # GET /items/{id}
        item.add_method("DELETE")  # DELETE /items/{id}
```

Run `cdk synth` and check cdk.out/YourStackName.template.json.
Run `cdk deploy` and check the output.

## Step 6 - Test your CRUD API!
Check `cdk deploy` output. You should see something like:
```console
Outputs:
MyFirstCrudApiBGSoAiEbNxStack.CrudApiEndpoint4D383D02 = https://YourApiUri.execute-api.eu-west-1.amazonaws.com/prod/
```
Now run `curl -X GET https://YourApiUri.execute-api.eu-west-1.amazonaws.com/prod/items`.