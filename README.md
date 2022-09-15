# CDK201
Build your first CRUD API in 45 minutes or less with AWS CDK!

## Welcome
Foo bar

## Step 1
```
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

```
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
```
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install black
pip freeze > requirements.txt
```

## Step 2
<!-- Uncomment the following line in app.py:
`#env=cdk.Environment(account='123456789012', region='us-east-1'),`
TODO: don't put the account number here but show on slides
And change `123456789012` into `803120882800`, and change the region into `eu-west-1`. -->

## Step 3
Run `cdk synth` and check the output. Also, did you notice that a folder named `cdk.out` appeared in the root of your CDK project?

The `cdk.out` folder contains a JSON CloudFormation template of your compiled CDK code.

### Step 3.1
Run `cdk deploy` to deploy your CDK app and check the output. In a new browser tab open: https://eu-west-1.console.aws.amazon.com/cloudformation.

## Step 4
Open your my_first_crud_api_${STACK_SUFFIX} folder and module (open the my_first_crud_api_${STACK_SUFFIX}_stack.py file).

Remove this piece of code:
```
# The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "MyFirstCrudApiRufZeyFmJkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
```

### Step 4.1
Now add a few imports we are going to need. Our CRUD API will need the following AWS services:
![CRUD API resources](https://static.us-east-1.prod.workshops.aws/public/67bee81b-1d79-49a0-96ec-6aea8f9357d2/static/images/ddb-crud.png)
