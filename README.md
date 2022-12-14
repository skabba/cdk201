# CDK201
Build your first CRUD API in 60 minutes or less with AWS CDK!

## Welcome
In this workshop you will create a **CRUD API** that **C**reates, **R**eads, **U**pdates and **D**eletes items from a DynamoDB table. The API will run serverless, so there is no management of the underlying infrastructure and scaling is done automatically.

You will learn how easy it is to create an API on AWS with AWS CDK, all within 60 minutes.

The workshop features the creation of a DynamoDB table, HTTP API Gateway and a Lambda function.

This workshop is based on https://catalog.us-east-1.prod.workshops.aws/workshops/2c8321cb-812c-45a9-927d-206eea3a500f/en-US. But has been pimped so you can do the same but with AWS CDK code.

## Prep
This workshop will be executed from within an AWS Cloud9 (Online IDE) environment.

To open this online IDE you first need to login here: https://obsessedbyaws.signin.aws.amazon.com/console.

## Step 1
Start by opening your [Cloud9 environment](https://eu-west-1.console.aws.amazon.com/cloud9/home) and click on `Open IDE`. Once it has loaded you can close the `Welcome` tab.
EXPLAIN SOMETHING HERE

```shell
git config --global user.email "fake@example.com"
git config --global user.name "Fake Name"

```
```shell
export FIRST_NAME="YourFirstNameWithoutSpecialCharacters"
export LAST_NAME="YourLastNameWithoutSpecialCharacters"
```
```shell
export STACK_SUFFIX="${FIRST_NAME}_${LAST_NAME}"
mkdir my-first-crud-api-${STACK_SUFFIX} && cd $_
cdk init app --language=python
ls -al

```

### Explain files - TODO Sorry...
:-)

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
pip freeze > requirements.txt

```

## Step 2
Now run:
```shell
cdk synth
````
And check the output.

Also, did you notice that a folder named `cdk.out` appeared in the root of your CDK project?

The `cdk.out` folder contains a JSON CloudFormation template of your compiled CDK code.

## Step 3
Run:
```shell
cdk deploy
```
To deploy your (still empty) CDK app and check the output. In a new browser tab open: https://eu-west-1.console.aws.amazon.com/cloudformation and search/select/open your `MyFirstCrudApi${STACK_SUFFIX}Stack` stack. You can now review your stack configuration.

## Step 4
In the online IDE on the left side now open your `my_first_crud_api_${STACK_SUFFIX}/my_first_crud_api_${STACK_SUFFIX}` folder and then open the `my_first_crud_api_${STACK_SUFFIX}_stack.py` file.

Remove this piece of code:
```python
# example resource
# queue = sqs.Queue(
#     self, "MyFirstCrudApiRufZeyFmJkQueue",
#     visibility_timeout=Duration.seconds(300),
# )
```
> **_NOTE:_** From this moment on, don't forget to save (Windows: CTRL+S or MacOS: CMD+S) your files before running `cdk synth` or `cdk deploy`. Cloud9 has no built-in Auto-Save option.

### Step 4.1
Our CRUD API will need the following AWS services:

![CRUD API resources](https://miro.medium.com/max/1400/1*N1iRLifjnNcZo-W0oxoYSw.png)

We can import the respective CDK modules in our code. In `my_first_crud_api_${STACK_SUFFIX}_stack.py`.

**CHANGE THIS CODE**:
```python
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
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

Run `cdk synth` and check `cdk.out/YourStackName.template.json`.

Run `cdk deploy` and check the output:
```console
 ???  MyFirstCrudApiQFaxthUagmStack

???  Deployment time: 31.87s

Stack ARN:
arn:aws:cloudformation:eu-west-1:803120882800:stack/MyFirstCrudApiQFaxthUagmStack/725c2260-352b-11ed-86ac-06ac9ad3f395

???  Total time: 39.57s
```

Your DynamoDB table has now been deployed!

### Step 5.2 - Add CRUD Lambda Function
We first will create the Lambda function itself:
> **_NOTE:_** The lambda folder that you will now create, needs to be create inside the root of your CDK project! At the same level where the the `tests` folder is created.
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
            "CrudHandler",
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
            "CrudHandler",
            runtime=_lambda.Runtime.NODEJS_16_X,
            code=_lambda.Code.from_asset("lambda"),
            handler="crud.handler",
            environment={"DYNAMODB_TABLE_NAME": crud_ddb_table.table_name},
        )

        crud_ddb_table.grant_full_access(crud_api_lambda.grant_principal)
```

Run `cdk synth` and check cdk.out/YourStackName.template.json.

Run `cdk deploy` and check the output.

> **_CHALLENGE_**: Have a look around in your new [Lambda Function](https://eu-west-1.console.aws.amazon.com/lambda/home?region=eu-west-1#/functions?fo=and&o0=%3A&v0=MyFirstCrudApi).

### Step 5.3 - Add CRUD Rest API Gateway
Below the Lambda function resource code, add:
```python

        crud_api_gw = apigw.LambdaRestApi(
            self,
            f"CrudApi_{Stack.of(self).stack_name}",
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

        crud_lambda = _lambda.Function(
            self,
            "CrudHandler",
            runtime=_lambda.Runtime.NODEJS_16_X,
            code=_lambda.Code.from_asset("lambda"),
            handler="crud.handler",
            environment={"DYNAMODB_TABLE_NAME": crud_ddb_table.table_name},
        )

        crud_ddb_table.grant_full_access(crud_lambda.grant_principal)

        crud_rest_api = apigw.LambdaRestApi(
            self,
            f"CrudApi_{Stack.of(self).stack_name}",
            handler=crud_lambda,
            proxy=False,  # Because we manually add resources + methods
        )

        items = crud_rest_api.root.add_resource("items")
        items.add_method("GET")  # GET /items
        items.add_method("PUT")  # PUT /items

        item = items.add_resource("{id}")
        item.add_method("GET")  # GET /items/{id}
        item.add_method("DELETE")  # DELETE /items/{id}
```

Run `cdk synth` and check cdk.out/YourStackName.template.json.

Run `cdk deploy` and check the output.

> **_CHALLENGE_**: Have a look around in your new [REST API](https://eu-west-1.console.aws.amazon.com/apigateway).

## Step 6 - Test your CRUD API!
Check `cdk deploy` output. You should see something like:
```console
Outputs:
MyFirstCrudApiBGSoAiEbNxStack.CrudApiEndpoint4D383D02 = https://YourApiUri.execute-api.eu-west-1.amazonaws.com/prod/
```

Use this output in the following command:
```shell
#DO NOT COPY THIS!!!
#Replace URL with the Invoke URL above
export INVOKE_URL="https://YourApiUri.execute-api.eu-west-1.amazonaws.com/prod"
```

Now run:
```shell
curl -s ${INVOKE_URL}/items | js-beautify
```

You should get back the following output:
```json
{"Items":[],"Count":0,"ScannedCount":0}
```

Congratulations! You have just created you fully working CRUD API running on Amazon Web Services, using only Serverless. But there are no items :-(. That's correct because we still need to add them using our CRUD API.

### Step 6.1 - Create or update an item
Now it is time to add some items! The following command includes a request body with the item's ID, price, and name.
```shell
curl -X "PUT" -H "Content-Type: application/json" -d "{
    \"id\": \"abcdef234\",
    \"price\": 12345,
    \"name\": \"myitem\"
}" ${INVOKE_URL}/items
```

You should get back the following output:
```console
"Put item abcdef234"
```

> **_CHALLENGE_**: Can you find this entry in [DynamoDB](https://eu-west-1.console.aws.amazon.com/dynamodbv2/#tables)?

### Step 6.2 - Get all items
Use the following command to list all items:
```shell
curl -s ${INVOKE_URL}/items | js-beautify
```

You should get back the following output:
```json
{
    "Items": [{
        "price": 12345,
        "id": "abcdef234",
        "name": "myitem"
    }],
    "Count": 1,
    "ScannedCount": 1
}
```

### Step 6.3 - Get item by ID
Use the following command to get an item by its ID:
```shell
curl -s ${INVOKE_URL}/items/abcdef234 | js-beautify
```

You should get back the following output:
```json
{
    "Item": {
        "price": 12345,
        "id": "abcdef234",
        "name": "myitem"
    }
}
```

### Step 6.4 - Delete item by ID
Use the following command to delete an item:
```shell
curl -X "DELETE" ${INVOKE_URL}/items/abcdef234
```

You should get back the following output:
```console
"Deleted item abcdef234"
```

> **_CHALLENGE_**: Get all items to verify that the item was deleted or check in the AWS console.

## Step 7 - Bonus Challenge
If your still have time left then try to add an API Gateway method to delete all items at once.

## Step 8 - Clean UP!
To prevent unnecessary costs, delete the resources that you created as part of this getting started exercise. The following steps delete your REST API, your Lambda function, and associated resources.

Run and watch output:
```shell
cdk destroy
```

Now go to [DynamoDB](https://eu-west-1.console.aws.amazon.com/dynamodbv2/#tables) and see if your table has been deleted.

> **_CHALLENGE_**: Have a look at the [DynamoDB Table Construct](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html) documentation and try to think about why the table has not been deleted.

Leave the table alone, it will be deleted for you.

### Step 7.1
Please also delete your Cloud9 environment.

## Thanks a lot!
If your are done, you can sign out.
Thank you very much for doing this CDK201 workshop. I hope you enjoyed it and learned something new.