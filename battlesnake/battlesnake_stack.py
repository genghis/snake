from aws_cdk import (
    aws_apigatewayv2,
    aws_lambda,
    CfnOutput,
    Stack,   
)
from constructs import Construct
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from os import path

class BattlesnakeStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        snakey = aws_lambda.Function(self, "battlesnake-function",
                runtime=aws_lambda.Runtime.PYTHON_3_12,
                code=aws_lambda.Code.from_asset("battlesnake"),
                handler="snakelambda.main")
        snakey_integration = HttpLambdaIntegration("SnakeIntegration", snakey)
        api = aws_apigatewayv2.HttpApi(self, "battlesnake-api",default_integration=snakey_integration)
    
        CfnOutput(self, "Endpoint URL", value=api.url)